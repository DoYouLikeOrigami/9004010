/* --------- plugins --------- */

var
	gulp        = require('gulp'),
	jade        = require('gulp-jade'),
	scss = require('gulp-sass'),
	plumber     = require('gulp-plumber'),
	autoprefixer = require('gulp-autoprefixer');

/* --------- paths --------- */

var
	paths = {
		jade : {
			location: 'app/markups/**/*.jade',
			compiled: 'app/markups/_pages/*.jade',
			destination: 'antipark/templates'
		},

		scss : {
			location    : 'app/scss/**/*.scss',
			entryPoint  : 'app/css/main.css',
			destination: 'app/css'
		},

		compile__css : {
			location : 'app/css/*.css',
			destination : 'antipark/static/css'
		}
	};

/* --------- jade --------- */

gulp.task('jade', function() {
	gulp.src(paths.jade.compiled)
		.pipe(plumber())
		.pipe(jade({
			pretty: '\t',
		}))
		.pipe(gulp.dest(paths.jade.destination));
});

/* --------- scss --------- */

gulp.task('scss', function () {
	gulp.src(paths.scss.location)
    	.pipe(scss().on('error', scss.logError))
    	.pipe(gulp.dest(paths.scss.destination));
});

/* --------- autoprefixer --------- */

gulp.task('autoprefixer', function () {
    gulp.src(paths.compile__css.location)
    	.pipe( autoprefixer({
    		browsers: ['last 15 versions'],
    		cascade: false
    	}))
    	.pipe( gulp.dest(paths.compile__css.destination));

});

/* --------- watch --------- */

gulp.task('watch', function(){
	gulp.watch(paths.jade.location, ['jade']);
	gulp.watch(paths.scss.location, ['scss']);
	gulp.watch(paths.compile__css.location, ['autoprefixer']);
});

/* --------- default --------- */

gulp.task('default', ['jade', 'scss', 'autoprefixer', 'watch']);
