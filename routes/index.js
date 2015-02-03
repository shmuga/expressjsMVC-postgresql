var express = require('express');
var router = express.Router();
var crypto = require('crypto');
var models = require('../models');

var requireUserAuth = function(req,res,next){
   console.log(req.session);
   if (req.session && req.session.user !== undefined){
      next();
   }else{
      req.flash('info','Sorry you have no permission to view this page. Please sign in first.');
      res.redirect("/login");
   }
};

router.get('/', requireUserAuth, function(req, res) {
   res.render("index");

});


//login page get method
router.get('/login', function(req, res) {
   if (req.session && req.session.user !== undefined){
      res.redirect("/");
   }
   res.render("login");
});

//login page post method
router.post('/login', function(req, res) {

   var loginAction = function(table){
      passEncrypted = crypto.createHash('sha256').update(req.body.password).digest("hex");
      if (table[0].password == passEncrypted){
         req.session.user = table;
         res.redirect("/");
      }else{
         res.redirect("/login")
      }
   };
   models.User.findByEmail(req.body.email,loginAction);
});

//logout get method
router.get('/logout', function(req, res) {
   req.session = null;
   res.redirect("/login");
});

module.exports = router;
