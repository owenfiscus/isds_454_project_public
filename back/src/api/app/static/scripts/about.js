var expanded_andres = 0;
var expanded_colt = 0;
var expanded_jesse = 0;
var expanded_jt = 0;
var expanded_owen = 0;

var last_id;

function expand_close_about_card(id, aid, sid, nid) {
    var iaid = aid;

    id = `#${String(id.id)}`;
    aid = `#${String(aid.id)}`;
    sid = `#${String(sid.id)}`;
    nid = `#${String(nid.id)}`;

    switch (id) {
        case '#about_more_andres':
            expanded_andres = expand_close(id, sid, nid, expanded_andres);
        break;
        case '#about_more_colt':
            expanded_colt = expand_close(id, sid, nid, expanded_colt);
        break;
        case '#about_more_jesse':
            expanded_jesse = expand_close(id, sid, nid, expanded_jesse);
        break;
        case '#about_more_jt':
            expanded_jt = expand_close(id, sid, nid, expanded_jt);
        break;
        case '#about_more_owen':
            expanded_owen = expand_close(id, sid, nid, expanded_owen);
        break;
    }

    function expand_close(id, sid, nid, expanded) {
        if (expanded == 0) {
            $(id).slideDown(300);
            $(sid).html("expand_less");
            $(nid).css({"border-radius":"0"})

            // adjust card & grid sizing
            if (iaid.classList.contains('about_cards_row_one')) {
                if ($(window).width() < 940) {
                    $('.about_cards').css({"grid-template-rows": "350px 250px auto"})
                    $('.about_card').css({"height": "350px"})
                } else {
                    $('.about_cards').css({"grid-template-rows": "450px 350px auto"})
                    $('.about_card').css({"height": "450px"})
                }

                $(iaid).removeClass('about_collapsed');
                $(iaid).addClass('about_expanded');

            } else if (iaid.classList.contains('about_cards_row_two')) {
                if ($('.about_cards_row_one').hasClass('about_expanded')) {
                    if ($(window).width() < 940) {
                        $('.about_cards').css({"grid-template-rows": "350px 350px auto"})
                    } else {
                        $('.about_cards').css({"grid-template-rows": "450px 450px auto"})
                    }
                } else {
                    if ($(window).width() < 940) {
                        $('.about_cards').css({"grid-template-rows": "250px 350px auto"})
                    } else {
                        $('.about_cards').css({"grid-template-rows": "350px 450px auto"})
                    }
                }
                $('.about_card').css({"height": "450px"})
            }
        
            expanded_state = 1;
        } else {
            $(id).slideUp(300);
            $(sid).html("expand_more");
            setTimeout(() => { $(nid).css({"border-radius":"0 0 1rem 1rem"}) }, 300);

            $(iaid).removeClass('about_expanded');
            $(iaid).addClass('about_collapsed');

            // count the number of expanded cards
            var expanded_count = $('.about_expanded').length;

            setTimeout(() => {
                // if all the cards on the top row are collapsed, reduce the row's height
                if (expanded_count == 0) {
                    if ($(window).width() < 940) {
                        $('.about_cards').css({"grid-template-rows": "250px 250px auto"})
                    } else {
                        $('.about_cards').css({"grid-template-rows": "350px 350px auto"})
                    }
                }
                
                if ($(window).width() < 940) {
                    $('.about_card').css({"height": "250px"})
                } else {
                    $('.about_card').css({"height": "350px"})
                }
            }, 300);

            expanded_state = 0;
        }

        return expanded_state;
    }
}
