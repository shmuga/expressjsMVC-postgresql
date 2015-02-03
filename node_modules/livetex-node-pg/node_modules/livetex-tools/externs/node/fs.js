

/**
 * @namespace
 */
var fs = {};


/**
 * @param {string} filename
 * @param {string} encoding
 * @return {string}
 */
fs.readFileSync = function(filename, encoding) {};


/**
 * @param {string} filename
 * @param {string} encoding
 * @param {function(Error, (string|!Buffer))} callback
 */
fs.readFile = function(filename, encoding, callback) {};


/**
 * @param {string} filename
 * @param {*} data
 * @param {function(?)} callback
 * @param {Object=} opt_options
 */
fs.writeFile  = function(filename, data, callback, opt_options) {};


/**
 * @param {string} filename
 * @param {string|!Buffer} data
 * @param {string=} opt_encoding
 */
fs.writeFileSync = function(filename, data, opt_encoding) {};


/**
 * @param {string} filename
 * @return {boolean}
 */
fs.existsSync = function(filename) {};


/**
 * @param {string} filename
 */
fs.unlinkSync = function(filename) {};