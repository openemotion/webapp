$(function() {
    var lastMessageId = 0;

    function submitMessage() {
        var text = $("#message").val();
        text = text.replace(/^\n*/, "").replace(/\n*$/, "").replace(/\n/g, "<br>");
        $("#message").val("");
        $.post("post", {text : text}, function (data, textStatus, jqXHR) {
            reloadHistory();
        });
    }

    var reloading = false; // prevent multiple ajax calls from going out at the same time
    function reloadHistory() {
        if (reloading) {
            return;
        }
        reloading = true;
        $.ajax("history?after_id=" + lastMessageId, {success: function (data, textStatus, jqXHR) {
            lastMessageId = data.last_id;
            var fromBottom = $(document).height() -  $(window).scrollTop() - $(window).height();
            $.each(data.messages, function (index, message) {
                $("#history").append(formatMessage(message.author, message.text));
            });
            if (fromBottom < 50) {
                $(document).scrollTop($(document).height());
            }
            reloading = false;
        }});
    }

    function formatMessage(author, text) {
        return "<p><strong>" + author + "</strong>" + ": " + text + "</p>";
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

    $("#submit").click(function(e) {
        submitMessage();
    });

    reloadHistory();
    setInterval(reloadHistory, 1000);
});
