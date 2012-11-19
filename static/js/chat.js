$(function() {
    var lastMessageId = 0;

    function submitMessage() {
        var text = $("#message").val();
        text = text.replace(/^\n*/, "").replace(/\n*$/, "").replace(/\n/g, "<br>");
        $("#message").val("");
        $("#history").append(formatMessage(chat_user, chat_userMessageType, text, true));
        $(document).scrollTop($(document).height());
        $.post("post", {text : text});
    }

    var reloading = false; // prevent multiple ajax calls from going out at the same time
    function updateHistory() {
        if (reloading) {
            return;
        }
        reloading = true;
        $.ajax("updates", {
            data: { after_id: chat_lastMessageId },
            timeout: 15000, // long polling
            success: function (data, textStatus, jqXHR) {
                if (data.last_message_id != -1) {
                    chat_lastMessageId = data.last_message_id;
                }
                var fromBottom = $(document).height() -  $(window).scrollTop() - $(window).height();
                $.each(data.messages, function (index, message) {
                    $("#history").append(formatMessage(message.author, message.type, message.text, true));
                });
                if (fromBottom < 50) {
                    $(document).scrollTop($(document).height());
                }
                updateStatus(data.status);
                reloading = false;
            },
            complete: function () {
                updateHistory();
            }
        });
    }

    function formatMessage(author, type, text) {
        msg = $("<div>").addClass("message").addClass(type);
        msg.append($("<div>").addClass("author").addClass().append(author).append(":"));
        msg.append($("<div>").addClass("text").append(text));
        return msg;
    }

    function updateStatus(status) {
        if (status === "pending") {
            $("#facilitate").show();
            $("#converse").hide();
        }
        else {
            $("#facilitate").hide();
            $("#converse").show();
        }
    }

    $("#message").keypress(function(e) {
        var text = $("#message").val();
        if (e.keyCode === 13 && text.match(/\n$/)) {
            if (text.replace(/\n/g, "") !== "") {
                submitMessage();
            }
            e.preventDefault();
        }
    });

    $("#submit_message").click(function(e) {
        submitMessage();
    });

    // FIXME: use long polling to reduce number of requests and speed things up
    // setInterval(function () { updateHistory(true); }, 1000);
    updateHistory();

    updateStatus(chat_status);

    // FIXME: code duplication!
    if (($(document).height() -  $(window).scrollTop() - $(window).height()) < 50) {
        $(document).scrollTop($(document).height());
    }

});
