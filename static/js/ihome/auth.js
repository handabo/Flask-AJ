function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $('#form-auth').submit(function(){
        read_name = $('#real-name').val()
        id_card = $('#id-card').val()
        $.ajax({
            url:'/user/auth/',
            data:{'read_name': read_name, 'id_card': id_card},
            dataType:'json',
            type:'PATCH',
            success:function(data){
                auth()
            },
            error:function(data){
                alert('请求失败')
            }
        });
    })
})

function auth(){
    $.get('/user/read_user_info/', function(data){
        if(data.code == '200'){
            $('#real-name').val(data.user.id_name)
            $('#id-card').val(data.user.id_card)
            if(data.user.id_name){
                $('.btn-success').hide()
            }
        }
    })
}

auth()


