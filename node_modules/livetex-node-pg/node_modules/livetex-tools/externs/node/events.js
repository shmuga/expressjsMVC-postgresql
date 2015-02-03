


/**
 * @namespace
 */
var events = {};


/**
 * @interface
 */
events.IEventEmitter = function() {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.IEventEmitter.prototype.addListener = function(type, listener) {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.IEventEmitter.prototype.once = function(type, listener) {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.IEventEmitter.prototype.removeListener = function(type, listener) {};


/**
 * @param {string=} opt_type
 */
events.IEventEmitter.prototype.removeAllListeners = function(opt_type) {};


/**
 * @param {string} type
 * @param {...} var_args
 */
events.IEventEmitter.prototype.emit = function(type, var_args) {};


/**
 * @param {string} type
 * @return {!Array.<function(...)>}
 */
events.IEventEmitter.prototype.listeners = function(type) {};


/**
 * @constructor
 * @implements {events.IEventEmitter}
 */
events.EventEmitter = function() {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.EventEmitter.prototype.addListener = function(type, listener) {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.EventEmitter.prototype.once = function(type, listener) {};


/**
 * @param {string} type
 * @param {function(...)} listener
 */
events.EventEmitter.prototype.removeListener = function(type, listener) {};


/**
 * @param {string=} opt_type
 */
events.EventEmitter.prototype.removeAllListeners = function(opt_type) {};


/**
 * @param {string} type
 * @param {...} var_args
 */
events.EventEmitter.prototype.emit = function(type, var_args) {};


/**
 * @param {string} type
 * @return {!Array.<function(...)>}
 */
events.EventEmitter.prototype.listeners = function(type) {};