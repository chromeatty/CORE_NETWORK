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
        $('.like-btn').click(function() {
            var btn = $(this);
            var form = btn.closest('form');
            var offerId = form.data('offer-id');
            // get the CSRF token from the form
            var csrfToken = $('[name="csrfmiddlewaretoken"]').val();  
    
            $.ajax({
                // URL to send the post request to
                url: '/toggle_like/',  
                type: 'POST',
                data: {
                    'offer_id': offerId,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    if (response.status === 'success') {
                        // Update the button and likes count
                        if (response.liked) {
                            btn.addClass('btn-success').removeClass('btn-outline-success').html('<i class="fas fa-heart"></i> Unlike');
                        } else {
                            btn.addClass('btn-outline-success').removeClass('btn-success').html('<i class="far fa-heart"></i> Like');
                        }
                        btn.closest('.item_offer').find('.likes-count').text(response.likes_count);
                        
                        // If it is on the liked offers page and an offer is unliked, remove the card
                        if (!response.liked && $('div[data-page-type="requester_view_liked_offers"]').length > 0) {
                            //btn.closest('.item_offer').fadeOut(1, function() { $(this).remove(); });
                            btn.closest('.item_offer').remove();
                            // If all cards are gone
                            if ($('.offer-container .item_offer').length === 0) {
                                $('.offer-container').append('<div class="col-12 no-offers"><div class="alert alert-info text-center">No liked offers.</div></div>');
                            }
                        }
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Could not toggle like. Error: ' + xhr.status + ': ' + xhr.responseText);
                }
            });
        });
    });    
});