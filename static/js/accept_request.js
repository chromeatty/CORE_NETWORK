$(document).ready(function() {
    // CSRF token for AJAX requests
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

    
    $(document).ready(function() {
        $('.accept-btn').click(function() {
            var btn = $(this);
            var form = btn.closest('form');
            var requestId = form.data('request-id');
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            var action = btn.attr('data-action');
    
            if (confirm('Are you sure you want to ' + action + ' this request?')) {
                $.ajax({
                    url: '/toggle_accept/',  // URL to send the post request to
                    type: 'POST',
                    data: {
                        'request_id': requestId,
                        'csrfmiddlewaretoken': csrfToken,
                        'action': action
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            // for accepted requests, remove the card from the page
                            if (!response.accepted && $('div[data-page-type="offer_view_accepted_requests"]').length > 0) {
                                $('#request_-' + requestId).remove();
                                // validate if this is the last request and append message if true
                                if ($('.item_request').length === 0) { 
                                    $('.request-container').append('<div class="col-12 no-requests"><div class="alert alert-info text-center">No more accepted requests.</div></div>');
                                }
                            // for available view_accepted_requests, remove the card from the page
                            } else if (response.accepted && $('div[data-page-type="offer_view_all_requests"]').length > 0) {
                                $('#request_-' + requestId).remove();
                                if ($('.item_request').length === 0) { // Check if this is the last request
                                    $('.request-container').append('<div class="col-12 no-requests"><div class="alert alert-info text-center">No more available requests.</div></div>');
                                }
                            } else if ($('div[data-page-type="offer_view_detail_requester"]').length > 0){
                                if (response.accepted) {
                                    btn.addClass('btn-danger').removeClass('btn-success');
                                    btn.html('<i class="fas fa-user-minus"></i> Retract');
                                    btn.attr('data-action', 'retract');
                                    $('.card-body').find('.card-text' + '.accepted-by').remove();
                                    $('.card-body').append('<p class="card-text accepted-by"><i class="fas fa-user-check"></i> <strong>Accepted by:</strong> ' + response.accepted_by + '</p>');
                                    //<p class="card-text accepted-by"><i class="fas fa-user-check"></i> <strong>Accepted by:</strong> {{ request_.accepted_by.username }}</p>
                                } else {
                                    btn.addClass('btn-success').removeClass('btn-danger');
                                    btn.html('<i class="fas fa-user-plus"></i> Accept');
                                    btn.attr('data-action', 'accept');
                                    $('.card-body').find('.card-text' + '.accepted-by').remove();
                                }
                            }
                        } else {
                            alert('Failed to retract acceptance: ' + response.error);
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        alert('Error: ' + xhr.status + ': ' + xhr.responseText);
                    }
                });
            }
        });
    });
});