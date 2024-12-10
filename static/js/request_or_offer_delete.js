$(document).ready(function() {
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
        $('.delete-btn').click(function() {
            var ID_type, django_link, action;
    
            console.log('Delete button clicked');
            var btn = $(this);
            var form = btn.closest('form');
            var pageType = $('div[data-page-type]').data('page-type');
            if (pageType === 'user_offer_list_page' || pageType === 'user_offer_details_page') {
                ID_type = form.data('offer-id');
                django_link = '/delete_offer/';
            }
            else if (pageType === 'user_requst_list_page'|| pageType === 'user_request_details_page') {
                ID_type = form.data('request-id');
                django_link = '/delete_request/';
            }
            //var requestId = form.data('request-id');// change for offer!!!!!!
            var csrfToken = form.find('[name="csrfmiddlewaretoken"]').val();
            var action = btn.attr('data-action');
            //console.log('ID_type:', ID_type);
            
    
            if (confirm('Are you sure you want to delete this ' + action + ' ?')) {
                $.ajax({
                    url: django_link + ID_type + '/',  
                    type: "POST",
                    data: {
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            if (pageType === 'user_offer_list_page'){
                                $('#offer-' + ID_type).remove();
                                if ($('.offer-container .item_offer').length === 0) {
                                    $('.offer-container').append('<div class="col-12 no-offers-message"><div class="alert alert-info text-center">No offers found.</div></div>');
                                }
                            } else if (pageType === 'user_offer_details_page') {
                                //$('#offer-' + ID_type).remove(); // this is not needed as we are redirecting to the list page
                                window.location.href = '/user_offer_list/';
                            } else if (pageType === 'user_requst_list_page') {
                                $('#request_-' + ID_type).remove();
                                if ($('.request-container .item_request').length === 0) {
                                    $('.request-container').append('<div class="col-12 no-requests-message"><div class="alert alert-info text-center">No requests found.</div></div>');
                                }
                            }else if (pageType === 'user_request_details_page') {
                                window.location.href = '/user_request_list/';
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
});