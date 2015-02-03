


/**
 * @interface
 */
var __IAbstractStream = function() {};


__IAbstractStream.prototype.destroy = function() {};



/**
 * @interface
 * @extends {events.IEventEmitter}
 * @extends {__IAbstractStream}
 *
 * @event data
 * @event error
 * @event end - EOF or FIN
 */
var IReadableStream = function() {};


IReadableStream.prototype.pause = function() {};


IReadableStream.prototype.resume = function() {};



/**
 * @interface
 * @extends {events.IEventEmitter}
 * @extends {__IAbstractStream}
 *
 * @event error
 * @event close
 */
var IWritableStream = function() {};


/**
 * @param {!Buffer|string} bufferOrString
 * @param {string=} opt_encoding
 * @param {!Function=} opt_callback
 */
IWritableStream.prototype.write = function(bufferOrString, opt_encoding, opt_callback) {};


/**
 * @param {(!Buffer|string)=} opt_bufferOrString
 * @param {string=} opt_encoding
 */
IWritableStream.prototype.end = function(opt_bufferOrString, opt_encoding) {};



/**
 * @interface
 * @extends {IWritableStream}
 * @extends {IReadableStream}
 */
var IStream = function() {};
