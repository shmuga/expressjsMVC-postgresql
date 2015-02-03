

/**
 * @namespace
 */
var process = {};


/**
 * @param {function()} callback
 */
process.nextTick = function(callback) {};


/**
 * @param {!Array.<number>=} opt_prevTime
 * @return {!Array.<number>}
 */
process.hrtime = function(opt_prevTime) {};


/**
 * @param {number} opt_code Код завершения.
 */
process.exit = function(opt_code) {};


/**
 * @param {string} pid Process ID.
 * @param {string} opt_signal Сигнал завершения.
 */
process.kill = function(pid, opt_signal) {};


/**
 * @type {string}
 */
process.pid = '';


/**
 * @return {!process.MemoryUsageInfo}
 */
process.memoryUsage = function() {};


/**
 * @constructor
 */
process.MemoryUsageInfo = function() {

  /**
   * @type {number}
   */
  this.rss = 0;

  /**
   * @type {number}
   */
  this.heapTotal = 0;

  /**
   * @type {number}
   */
  this.heapUsed = 0;
};


/**
 * @type {!IStream}
 */
process.stdin;


/**
 * @type {!IStream}
 */
process.stdout;


/**
 * @type {!Array.<string>}
 */
process.argv;