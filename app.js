var flash = require('express-flash'),
    express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var session = require('cookie-session');
var index = require('./routes/index');
var api = require('./routes/api');
var users = require('./routes/users');
var app = express();

var requireUserAuth = function(req,res,next){
    if (req.session && req.session.user !== undefined){
        next();
    }else{
        req.flash('info','Sorry you have no permission to use this api. Please sign in first.');
        res.redirect("/login");
    }
};

// view engine setup
app.set('views', path.join(__dirname, 'views'));

app.set('view engine', 'jade');
// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    keys: ['adsdujhl12u3jhn2lj123bhk']
}));
app.use(flash());

//routes
app.use('/', index);
app.all("/api/*",requireUserAuth);
app.use('/api', api);
app.use('/users', users);


//auth for all api functions






// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
