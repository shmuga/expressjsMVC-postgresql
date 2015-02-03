var express = require('express');
var app = express();

var index = require('./api/index');
app.use("/", index);

module.exports = app;