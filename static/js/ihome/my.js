function logout() {
    $.get("/user/logout/", function(data){
        if (data.code == '200') {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){

    $.get('/user/user_info/', function(data){
        if(data.code == '200'){
            $('#user-name').text(data.user_info.name)
            $('#user-mobile').text(data.user_info.phone)
            $('#user-avatar').attr('src', '/static/media/' + data.user_info.avatar)
        }
    })
})