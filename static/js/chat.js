$(function() {
    function submitMessage() {
        var text = $("#message").val();
        text = text.replace(/^\n*/, "").replace(/\n*$/, "").replace(/\n/g, "<br>");
        $("#message").val("").focus();
        $.post("post", {text : text}, function (data, textStatus, jqXHR) {
            reloadHistory();
        });
    }

    function reloadHistory() {
        // FIXME: use HTTP HEAD to check if we need to change history
        $.ajax("history", {success: function (data, textStatus, jqXHR) {
            var fromBottom = $(document).height() -  $(window).scrollTop() - $(window).height();
            $("#history").empty();
            $.each(data.messages, function (index, message) {
                $("#history").append(formatMessage(message.author, message.text));
            });
            if (fromBottom < 50) {
                $(document).scrollTop($(document).height());
            }
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
