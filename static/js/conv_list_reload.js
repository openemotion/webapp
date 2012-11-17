$(function() {
    function reloadConversationList() {
        $.ajax("conversations", {
            success: function (data, textStatus, jqXHR) {
                $("#conversation_list").empty().append(data);
                console.log("updating...");
            }
        });
    }

    setInterval(reloadConversationList, 1000);
});