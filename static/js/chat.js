$(function() {
    var lastMessageId = 0;

    // add a message to history and submit it to the server
    function submitMessage() {
        var text = $("#message").val();
        $("#message").val("");
        $("#history").append(formatMessage(chat_user, chat_userMessageType, text, true));
        $(document).scrollTop($(document).height());
        $.post("post", {text : text});
    }

    // long poll - continuosly query the server for new messages
    function longPoll() {
        $.ajax("poll", {
            data: { last_message_id: chat_lastMessageId },
            timeout: 30 * 1000,
            success: function (data, textStatus, jqXHR) {
                // when poll returns successfully, update the messages
                updateHistory();
            },
            complete: function () {
                longPoll();
            }
        });
    }

    // get message updates from the server
    var reloading = false; // prevent multiple ajax calls from going out at the same time
    function updateHistory() {
        if (reloading) {
            return;
        }
        reloading = true;
        $.ajax("updates", {
            data: { last_message_id: chat_lastMessageId },
            success: function (data, textStatus, jqXHR) {
                chat_lastMessageId = data.last_message_id;
                var doScroll = isCloseToBottom();
                $.each(data.messages, function (index, message) {
                    $("#history").append(formatMessage(message.author, message.type, message.text, false));
                });
                if (doScroll) {
                    scrollToBottom();
                }
                updateStatus(data.conversation.status);
            },
            complete: function () {
                reloading = false;
            }
        });
    }

    // format a single message
    // FIXME: this is a duplication of the server-side message formatting code
    function formatMessage(author, type, text, escape) {
        if (escape) {
            text = $("<div/>").text(text).html();
        }
        text = text.replace(/(\r?\n)+/g,"<br>");
        msg = $("<div>").addClass("message").addClass(type);
        msg.append($("<div>").addClass("author").addClass().append(author + ":"));
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
            $("#status").hide();
        }
    }

    function isCloseToBottom() {
        fromBottom = $(document).height() -  $(window).scrollTop() - $(window).height();
        return (fromBottom < 50);
    }

    function scrollToBottom() {
        $(document).scrollTop($(document).height());
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

    // start long polling
    if (globalConfig.ENABLE_LONG_POLL) {
        longPoll();
    }

    // start periodic updates
    setInterval(updateHistory, globalConfig.UPDATE_INTERVAL);

    // update status
    updateStatus(chat_status);

    // when page is reloaded scroll to the bottom if already there
    if (isCloseToBottom()) {
        scrollToBottom();
    }
});
