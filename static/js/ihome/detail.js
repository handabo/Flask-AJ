function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){


    var url = location.search

    $.get('/house/house_detail/'+url.split('=')[1]+'/', function (data) {

        var house_detail = template('house_detail_script', {ohouse:data.house})
        $('.container').append(house_detail)

        var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
        })
        $(".book-house").show();

    });

})