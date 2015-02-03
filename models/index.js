"use strict";

var fs        = require("fs");
var path      = require("path");
var env       = process.env.NODE_ENV || "development";
var config    = require(__dirname + '/../config/config.json')[env];
var db        = {};
var pg        = require('livetex-node-pg');
pg.init(100,config);


fs
  .readdirSync(__dirname)
  .filter(function(file) {
    return (file.indexOf(".") !== 0 && file !== "index.js" && file !== "model.js");
  })
  .forEach(function(file) {
        var model = require('./' + file);
        var tmp = new model(pg);
        db[tmp.getName()] = tmp;
  });
module.exports = db;