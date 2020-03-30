function CMSarticleList() {

}


CMSarticleList.prototype.run = function () {
    var self = this;
    self.initDatepicker();
    self.ListenDelete();
};

CMSarticleList.prototype.ListenDelete = function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        blogalert.alertConfirm({
            'text': '确定要删除吗?',
            'confirmCallback': function () {
                var pk = deleteBtn.attr('data-article-id');
                blogajax.post({
                    'url': '/cms/del_article/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.messageBox.showSuccess('删除成功');
                            window.location.reload()
                        }
                    }
                })
            }
        })
    })
};


//日历表
CMSarticleList.prototype.initDatepicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1)+ '/' + (todayDate.getDate()+1);
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2017/6/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);
};


$(function () {
    var articleList = new CMSarticleList();
    articleList.run()
});