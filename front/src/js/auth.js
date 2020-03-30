function Auth() {
    var self = this

}

Auth.prototype.run = function () {
    var self = this;
    self.listenSiginEvent();
    self.listenSigupEvent();
};

Auth.prototype.listenSiginEvent = function (event) {
    var SigninGroup = $('.card-signin');
    var telephoneInput = SigninGroup.find("input[name='telephone']");
    var usernameInput = SigninGroup.find("input[name='username']");
    var passwordInput = SigninGroup.find("input[name='password']");
    var rememberInput = SigninGroup.find("input[name='remember']");
    var SiginBtn = SigninGroup.find('.btn');
    SiginBtn.click(function () {
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var username = usernameInput.val();
        var remember = rememberInput.val();
        console.log(username);
        blogajax.post({
            'url':'/account/login/',
            'data':{
                'telephone':telephone,
                'username':username,
                'password':password,
                'remember':remember,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    blogalert.alertSuccess('登录成功', function () {
                        window.location.href = "/";
                    })
                }
            }
        })
    })
};


Auth.prototype.listenSigupEvent = function (event) {
    var SignupGroup = $('.card-signup');
    var usernameInput = SignupGroup.find("input[name='username']");
    var passwordInput = SignupGroup.find("input[name='password']");
    var emailInput = SignupGroup.find("input[name='email']");
    var repeat_passwordInput = SignupGroup.find("input[name='repeat_password']");
    var telephoneInput = SignupGroup.find("input[name='telephone']");
    var SiginBtn = SignupGroup.find('.btn');
    SiginBtn.click(function () {
        var username = usernameInput.val();
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var repeat_password = repeat_passwordInput.val();
        var email = emailInput.val();
        blogajax.post({
            'url': '/account/signup/',
            'data': {
                'username': username,
                'telephone': telephone,
                'password': password,
                'repeat_password': repeat_password,
                'email': email,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    blogalert.alertSuccess('注册成功', function () {
                        window.location.href = "/";
                    })
                }
            }
        })
    });
};
$(function () {
    //创建 auth对象
    var auth = new Auth();
    auth.run();
});
