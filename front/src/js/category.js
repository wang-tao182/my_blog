function Category() {

};

Category.prototype.run = function () {
    var self = this;
    self.listenAddCategory();
    self.listendelCategory();
    self.listeneditCategory();
};

Category.prototype.listenAddCategory = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        blogalert.alertOneInput({
            'text': '分类名称',
            'confirmCallback': function (inputValue) {
                blogajax.post({
                    'url': '/cms/add_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        }
                    }
                })
            }
        });


    })
};

Category.prototype.listendelCategory = function () {
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var categoryId = tr.attr('data-pk');
        blogalert.alertConfirm({
            'text': '确定要删除吗?',
            'confirmCallback': function () {
                blogajax.post({
                    'url': '/cms/del_category/',
                    'data': {
                        'categoryId': categoryId
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        }
                    }
                })
            }
        });
    })
};

Category.prototype.listeneditCategory = function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var categoryId = tr.attr('data-pk');
        var category_name = tr.attr('data-name');
        blogalert.alertOneInput({
            'text': '编辑分类名称',
            'value':category_name,
            'placeholder': '请输入分类名称',
            'confirmCallback': function (inputValue) {
                blogajax.post({
                    'url': '/cms/edit_category/',
                    'data': {
                        'name': inputValue,
                        'categoryId': categoryId,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        }
                    }
                })
            }
        });
    })
};


$(function () {
    var category = new Category();
    category.run()
});