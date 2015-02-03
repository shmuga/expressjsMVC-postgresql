

/**
 *
 * @namespace
 */
var hbase = {};


/**
 * @constructor
 * @extends {Error}
 */
hbase.Error = function() {

  /**
   * @type {number}
   */
  this.code;

  /**
   * @type {string}
   */
  this.body;
};


/**
 * @constructor
 * @param {{
 *  host:string,
 *  port: number
 * }} options
 */
hbase.Client = function(options) {};


/**
 * @param {string} table
 * @param {string} row
 * @return {!hbase.Row}
 */
hbase.Client.prototype.getRow = function(table, row) {};


/**
 * @constructor
 * @param {!hbase.Client} client
 * @param {string} table
 * @param {string} row
 */
hbase.Row = function(client, table, row) {};


/**
 * @param {string} column
 * @param {string} value
 * @param {function(hbase.Error)} callback
 */
hbase.Row.prototype.put = function(column, value, callback) {};


/**
 * @param {string} column
 * @param {function(hbase.Error)} callback
 */
hbase.Row.prototype.delete = function(column, callback) {};


/**
 * @param {string} column
 * @param {!Object.<string>} options
 * @param {function(hbase.Error, Array.<{column:string, $:string}>)} callback
 */
hbase.Row.prototype.get = function(column, options, callback) {};
