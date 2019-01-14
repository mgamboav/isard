
// including plugins

//Adding dependencies
var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var minify = require('gulp-clean-css');
var prefix = require('gulp-autoprefixer');
var sourcemaps = require('gulp-sourcemaps');

var user_js = [ 'bower_components/gentelella/vendors/jquery/dist/jquery.min.js', 
				'bower_components/gentelella/vendors/bootstrap/dist/js/bootstrap.min.js',
				'bower_components/gentelella/vendors/validator/validator.js',
				'bower_components/gentelella/vendors/datatables.net/js/jquery.dataTables.min.js',
				'bower_components/gentelella/vendors/datatables.net-bs/js/dataTables.bootstrap.min.js',
				'bower_components/gentelella/vendors/ion.rangeSlider/js/ion.rangeSlider.min.js',
				'bower_components/gentelella/vendors/pnotify/dist/pnotify.js', 
				'bower_components/gentelella/vendors/pnotify/dist/pnotify.confirm.js', 
				'bower_components/gentelella/vendors/pnotify/dist/pnotify.buttons.js', 
				'bower_components/gentelella/vendors/parsleyjs/dist/parsley.min.js', 
				'bower_components/gentelella/vendors/select2/dist/js/select2.full.min.js',
				'bower_components/gentelella/vendors/iCheck/icheck.min.js', 
				'bower_components/gentelella/vendors/switchery/dist/switchery.min.js', 	
				'bower_components/gentelella/vendors/bootstrap-progressbar/bootstrap-progressbar.min.js', 	
				'static/vendor/socket.io.min.js', 	
				'static/isard.js',	
				'static/js/restful.js', 
				'static/js/sockets.js',
				'static/js/viewer.js', 
				//~ 'static/js/disposables.js', 
				'static/js/media.js', 
				//~ 'static/js/quota_socket.js', 
				'static/js/quota.js', 
				'static/js/desktops.js', 
				'static/js/templates.js', 
				'static/js/media.js',
				'static/js/snippets/domain_derivates.js', 
				'static/js/snippets/alloweds.js', 
				'static/js/snippets/media.js', 
				'static/js/snippets/domain_hardware.js', 
				'static/js/snippets/domain_hotplugged.js', 
				'static/js/snippets/domain_graphs.js', 
				'static/js/snippets/domain_genealogy.js']

//gulpfile.js file

user_css = ['bower_components/gentelella/vendors/bootstrap/dist/css/bootstrap.min.css', 
			'bower_components/gentelella/vendors/font-awesome/css/font-awesome.min.css', 
			'bower_components/gentelella/vendors/pnotify/dist/pnotify.css', 
			'bower_components/gentelella/vendors/pnotify/dist/pnotify.buttons.css', 
			'bower_components/gentelella/build/css/custom.min.css', 
			'bower_components/gentelella/vendors/animate.css/animate.min.css',
			'bower_components/gentelella/vendors/font-awesome/css/font-awesome.min.css']

//defining tasks
gulp.task('default', function() {  //default is a task name, we can give any name.
	gulp.src(user_js)
	.pipe(sourcemaps.init())
	.pipe(concat('isard-user.js'))
	.pipe(sourcemaps.write()) 
	.pipe(uglify())
	.pipe(gulp.dest('static/build'));
	gulp.src(user_css)
    .pipe(concat('isard-user.css'))
    .pipe(minify())
    .pipe(prefix('last 2 versions'))
    .pipe(gulp.dest('static/build'))
});
