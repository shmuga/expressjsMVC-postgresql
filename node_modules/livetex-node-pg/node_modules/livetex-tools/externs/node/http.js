



/**
 * @namespace
 */
var http = {};


/**
 * @param {function(!http.ServerRequest, !http.ServerResponse)=}
 *    opt_requestHandler
 * @return {!http.Server}
 */
http.createServer = function(opt_requestHandler) {};


/**
 * @constructor
 * @extends {events.EventEmitter}
 */
http.Server = function() {};


/**
 * @param {number|string} port
 * @param {string=} opt_host
 */
http.Server.prototype.listen = function(port, opt_host) {};


http.Server.prototype.close = function() {};


/**
 * @constructor
 * @extends {events.EventEmitter}
 */
http.ServerRequest = function() {};


/**
 * @type {!Object.<string, string>}
 */
http.ServerRequest.prototype.headers = {};



/**
 * @type {!net.Socket}
 */
http.ServerRequest.prototype.connection;


/**
 * @type {string}
 */
http.ServerRequest.prototype.method = '';


/**
 * @type {string}
 */
http.ServerRequest.prototype.url = '';


http.ServerRequest.prototype.resume = function() {};


http.ServerRequest.prototype.pause = function() {};


/**
 * @param {string} event Событие.
 * @param {function(!Object)} callback Обработчик результата.
 */
http.ServerRequest.prototype.on = function(event, callback) {};


/**
 * @constructor
 * @extends {events.EventEmitter}
 */
http.ServerResponse = function() {};


/**
 * @param {(string|!Buffer)=} opt_data
 */
http.ServerResponse.prototype.end = function(opt_data) {};


/**
 * @param {string} name
 * @param {string} value
 */
http.ServerResponse.prototype.setHeader = function(name, value) {};


/**
 * @param {number} code
 * @param {!Object=} opt_headers
 */
http.ServerResponse.prototype.writeHead = function(code, opt_headers) {};


/**
 * @param {string | Buffer} chunk Данные.
 * @param {string=} opt_encode Кодировка для строковых данных.
 */
http.ServerResponse.prototype.write = function(chunk, opt_encode) {};


/**
 * @type {number}
 */
http.ServerResponse.prototype.statusCode = 200;


/**
 * @type {!Object}
 */
http.ServerResponse.prototype.headers;


