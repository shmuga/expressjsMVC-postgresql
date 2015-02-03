


/**
 * @namespace
 */
var crypto = {};


/**
 * @param {string} name
 * @return {!crypto.Hash}
 */
crypto.createHash = function(name) {};


/**
 * @constructor
 */
crypto.Hash = function() {};


/**
 * @param {string} data
 * @param {string=} opt_encoding
 */
crypto.Hash.prototype.update = function(data, opt_encoding) {};


/**
 * @param {string=} opt_encoding
 * @return {string}
 */
crypto.Hash.prototype.digest = function(opt_encoding) {};
