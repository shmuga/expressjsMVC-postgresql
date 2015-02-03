


/**
 * @namespace
 */
var net = {};


/**
 * @return {!net.Server}
 */
net.createServer = function() {};


/**
 * @param {number} port
 * @param {string=} opt_host
 * @return {!net.Socket}
 */
net.createConnection  = function(port, opt_host) {};

/**
 * @constructor
 * @extends {events.EventEmitter}
 */
net.Server = function() {};


/**
 * @param {number|string} portOrPath
 * @param {string=} opt_host
 */
net.Server.prototype.listen = function(portOrPath, opt_host) {};


net.Server.prototype.close = function() {};


/**
 * @constructor
 * @implements {IStream}
 * @extends {events.EventEmitter}
 */
net.Socket = function() {};


/**
 * @type {string}
 */
net.Socket.prototype.remoteAddress = '';

/**
 * @type {number}
 */
net.Socket.prototype.remotePort = 0;

/**
 * @param {number|string} portOrPath
 * @param {string=} opt_host
 */
net.Socket.prototype.connect = function(portOrPath, opt_host) {};


/**
 * @param {!Buffer|string} bufferOrString
 * @param {string=} opt_encoding
 */
net.Socket.prototype.write = function(bufferOrString, opt_encoding) {};


/**
 * В отличие от destroy дожидается отправки всех данных в очереди для записи.
 *
 * @param {(!Buffer|string)=} opt_bufferOrString
 * @param {string=} opt_encoding
 */
net.Socket.prototype.end = function(opt_bufferOrString, opt_encoding) {};


net.Socket.prototype.destroy = function() {};


net.Socket.prototype.pause = function() {};


net.Socket.prototype.resume = function() {};
