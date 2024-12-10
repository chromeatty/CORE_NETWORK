$(document).ready(function() {
    // CSRF token for AJAX load
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Delete button function
    $('.delete-btn').click(function() {
        var messageId = $(this).data('message-id');
        if (confirm('Are you sure you want to delete this message?')) {
            $.ajax({
                url: `/delete_message/${messageId}/`,
                type: 'POST',
                success: function(response) {
                    if (response.status === 'success') {
                        // check the type of page to determine the action
                        var pageType = $('div[data-page-type]').data('page-type');

                        if (pageType === 'inbox_page') {
                            // If on inbox.html
                            $('#message-' + messageId).remove();
                            if ($('.message-container .list-group-item').length === 0) {
                                $('.message-container').append('<div class="col-12 no-message"><div class="alert alert-info text-center">No messages.</div></div>');
                            }
                        } else if (pageType === 'view_message_page') {
                            // If on view_message.html
                            var inboxUrl = $('div[data-page-type]').data('inbox-url'); 
                            window.location.href = inboxUrl; // redirect to inbox page
                        }
                    } else {
                        alert(response.message);
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Could not delete. Error: ' + xhr.status + ': ' + xhr.responseText);
                }
            });
        }
    });
});