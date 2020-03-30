function WriteArticle() {

}

WriteArticle.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listenwritearticle();
};

WriteArticle.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 300,
        'serverUrl': '/ueditor/upload/',
    });
};


WriteArticle.prototype.listenwritearticle = function () {
    var submitBtn = $('.btn-primary');

    submitBtn.click(function (event) {
        event.preventDefault();
        var article = submitBtn.attr('data-article-id');
        var Inputtitle = $("input[name='title']");
        // var Inputcontent = $("textarea[name='content']");
        var Inputdesc = $("input[name='desc']");
        var title = Inputtitle.val();
        //富文本编辑器
        var content = window.ue.getContent();
        // var content = Inputcontent.val()
        var desc = Inputdesc.val();
        var category = $("select[name='category']").val();
        var url = '';
        if (article) {
            url = "/cms/edit_article/"
        } else {
            url = "/cms/write_article/"
        }
        blogajax.post({
            'url': url,
            'data': {
                'title': title,
                'desc': desc,
                'content': content,
                'category': category,
                'pk': article
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    // window.messageBox.showSuccess('发布成功');
                    if (article) {
                        blogalert.alertSuccess('恭喜修改成功', function () {
                            window.location.reload()
                        })

                    } else {
                        blogalert.alertSuccess('恭喜发布成功', function () {
                            window.location.reload()
                        })
                    }
                }
            }
        })
    })
};


$(function () {
    var writeArticle = new WriteArticle();
    writeArticle.run();
});