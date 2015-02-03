



/**
 * @namespace
 */
var assert = {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string} message
 * @param {string} operator
 */
assert.fail = function(actual, expected, message, operator) {};


/**
 *
 * @param {*} value
 * @param {string=} opt_message
 */
assert.ok = function(value, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.equal = function(actual, expected, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.notEqual = function(actual, expected, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.deepEqual = function(actual, expected, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.notDeepEqual = function(actual, expected, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.strictEqual = function(actual, expected, opt_message) {};


/**
 * @param {*} actual
 * @param {*} expected
 * @param {string=} opt_message
 */
assert.notStrictEqual = function(actual, expected, opt_message) {};


/**
 * @param {function(...)} block
 * @param {Error=} opt_error
 * @param {string=} opt_message
 */
assert.throws = function(block, opt_error, opt_message) {};


/**
 * @param {function(...)} block
 * @param {Error=} opt_error
 * @param {string=} opt_message
 */
assert.doesNotThrow = function(block, opt_error, opt_message) {};


/**
 * @param {*} value
 */
assert.ifError = function(value) {};