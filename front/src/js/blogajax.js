/**
 * Created by hynev on 2018/5/15.
 */

//ajax进行从csrftoken验证有两种方式
//1 在ajax中的form中手动添加csrfmiddlea=waretoken
//2 在请求头中添加x-CSRFToken.
//首先我们可以在返回的cookie中提取csrf token,再设置进去
//获取浏览器中的cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//判断不同的请求方法,执行相应的函数
var blogajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        // args 代表通过请求传上来的所有参数
        // success为auth.js里的函数
        var success = args['success'];
        args['success'] = function (result) {
            if(result['code'] === 200){
                if(success){
                    success(result);
                }
            }else{
                var messageObject = result['message'];
                //typeof 检查一个变量是否存在,是否有值.
                if(typeof messageObject == 'string' || messageObject.constructor == String){
                    window.messageBox.showError(messageObject);
                }else{
                    // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                    for(var key in messageObject){
                        var messages = messageObject[key];
                        var message = messages[0];
                        window.messageBox.showError(message);
                    }
                }
                if(success){
                    success(result);
                }
            }
        };
        args['fail'] = function (error) {
            console.log(error);
            window.messageBox.showError('服务器内部错误！');
        };
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    //如果不是以上请求方法,执行以下代码
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
};
