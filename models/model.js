"use strict";
var Model = function(pg,name,table){
    this.q = pg;
    this.name = name;
    this.table = table;
};

Model.prototype.query = function(query,prepared,res) {
    this.q.execPrepared(query,prepared,res,console.error);
};
Model.prototype.getName = function(){return this.name};

Model.prototype.getAll = function(res) {
    this.query("SELECT * FROM " + table,res);
};

module.exports = Model;