var gulp = require('gulp');
var cssnano = require('gulp-cssnano');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var cache = require('gulp-cache');
var imagemin = require('gulp-imagemin');
var bs = require('browser-sync').create();
var sass = require('gulp-sass');
//gulp-util:这个插件有一个方法log,可以打印出当前js的错误信息
var util = require('gulp-util');
// var sourcemaps = require('gulp-sourcemaps');
//定义路径
var path = {
    'html' : './templates/**/',
    'css' : './src/css/**/',
    'js' : './src/js/',
    'images' : './src/images/',
    'css_dist' : './dist/css',
    'js_dist' : './dist/js',
    'images_dist' : './dist/images',
};

//定义一个css任务
gulp.task('css', function () {
    gulp.src(path.css + '*.scss')
        .pipe(sass().on('error',sass.logError))
        .pipe(cssnano())
        .pipe(rename({suffix : '.min'}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});

//定义一个js任务
gulp.task('js', function () {
    gulp.src(path.js + '*.js')
        // .pipe(sourcemaps().init())
        .pipe(uglify().on('error',util.log))
        .pipe(rename({suffix: '.min'}))
        // .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});

//定义一个image任务
gulp.task('images', function () {
    gulp.src(path.images +'*.*')
        .pipe(cache(imagemin()))
        // .pipe(cache())
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
});

//定义一个处理html文件的任务
gulp.task('html', function () {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())
});

//定义一个watch任务
gulp.task('watch', function () {
    gulp.watch(path.html+'*.html' , ['html']);
    gulp.watch(path.css+'*.scss' , ['css']);
    gulp.watch(path.js+'*.js' , ['js']);
    gulp.watch(path.images+'*.*' , ['image'])
});


//初始化browser-sync的任务
gulp.task('bs', function () {
    bs.init({
        'server' :{
            'baseDir' : './'
        }
    });
});
//创建一个默认任务
//监听文件的修改,如果有修改自动刷新浏览器
gulp.task('server', ['bs','watch']);
gulp.task('default', ['watch']);