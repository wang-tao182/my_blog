function Comment() {

}

Comment.prototype.run = function () {
    var self = this;
    self.listenSubmitComment();

};

Comment.prototype.listenSubmitComment = function (event) {
    var submitBtn = $('.submit-btn');
    var contentInput = $("textarea[name='comment']");
    submitBtn.click(function () {
        var articleId = submitBtn.attr('data-comment');
        var content = contentInput.val();
        blogajax.post({
            'url': '/comment/',
            'data': {
                'pk': articleId,
                'content': content,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];
                    console.log(result)
                    var html = template('comment-item',{'comment':comment});
                    var ul = $('.comment-list');
                    ul.prepend(html);
                    window.messageBox.showSuccess('发布评论成功');
                    contentInput.val('')
                }
            }
        })
    })
};

$(function () {
    var comment = new Comment();
    comment.run();
});