$(function() {
    reload = function () {
        $.ajax(window.location.pathname, {
            success: function (data, textStatus, jqXHR) {
                $.each($(data), function(index, element) {
                    element = $(element);
                    if (element.attr('id') == 'main') {
                        $('#main').html(element.html());
                    }
                });
            }
        });
    }
    setInterval(reload, globalConfig.UPDATE_INTERVAL);
});