"use strict";
var Model = require('./model');

var m = function(pg){
    this.q = pg;
    this.name = "User";
    this.table = "users";
};
m.prototype = Object.create(Model.prototype);


m.prototype.findByEmail = function(email,res) {
    this.query("SELECT * FROM users WHERE email=$email",{
        'email': email
    },res);
};

module.exports = m;
