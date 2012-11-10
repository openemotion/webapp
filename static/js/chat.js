$(function() {
    function submitMessage() {
        text = $("#message").val();
        text = text.replace(/^\n*/, "").replace(/\n*$/, "").replace(/\n/g, "<br>");
        $("#message").val("").focus();
        $.post("post", {text : text}, function (data, textStatus, jqXHR) {
            reloadHistory();
        });
    }

    function reloadHistory() {
        $.ajax("history", {success: function (data, textStatus, jqXHR) {
            fromBottom = $(document).height() -  $(window).scrollTop() - $(window).height();
            $("#history").empty().append(data);
            console.log(fromBottom);
            if (fromBottom < 50) {
                $(document).scrollTop($(document).height());
            }
        }});
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
    })

    // $("#message").focus();

    setInterval(reloadHistory, 1000);
});
