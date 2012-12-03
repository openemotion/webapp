$(function() {
    function reloadConversationList() {
        $.ajax("conversations", {
            ifModified: true,
            success: function (data, textStatus, jqXHR) {
                $("#conversation_list").empty().append(data);
            }
        });
    }

    setInterval(reloadConversationList, globalConfig.UPDATE_INTERVAL);
});