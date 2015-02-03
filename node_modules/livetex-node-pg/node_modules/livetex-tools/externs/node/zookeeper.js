


/**
 * @namespace
 */
var zk = {};


/**
 * @typedef {{
 *   connect: string,
 *   timeout: number,
 *   debug_level: string,
 *   host_order_deterministic: boolean,
 *   data_as_buffer: boolean
 * }}
 */
zk.options;


/**
 * @typedef {{
 *   ephemeralOwner: string,
 *   version: number,
 *   numChildren: number
 * }}
 */
zk.stat;

/**
 * @typedef {function(number, string, string)}
 */
zk.patch_cb;

/**
 * @typedef {function(number, string, !Array.<string>)}
 */
zk.child_cb;

/**
 * @typedef {function(number, string)}}
 */
zk.void_cb;

/**
 * @typedef {function(number, string, zk.stat)}
 */
zk.stat_cb;

/**
 * @typedef {function(number, string, zk.stat, string)}
 */
zk.data_cb;

/**
 * @typedef {function(number, number, string)}
 */
zk.watch_cb;

/**
 * @constructor
 * @extends {events.EventEmitter}
 */
zk.ZooKeeper = function() {};

/**
 *
 * @type {string}
 */
zk.ZooKeeper.ZOO_LOG_LEVEL_WARNING = '';

zk.ZooKeeper.ZOK = 0;
zk.ZooKeeper.ZNODEEXISTS = -110;
zk.ZooKeeper.ZNONODE = -101;

zk.ZooKeeper.ZOO_EPHEMERAL = 1;
zk.ZooKeeper.ZOO_SEQUENCE = 2;

zk.ZooKeeper.ANY_NODE_VERSION = -1;
zk.ZooKeeper.ZOO_CREATE_TYPE = -1;
zk.ZooKeeper.ZOO_DELETE_TYPE = -2;


/**
 * @type {string}
 */
zk.ZooKeeper.prototype.client_id = '';

/**
 * @param {zk.options} options
 * @param {function(Error)} callback
 */
zk.ZooKeeper.prototype.connect = function(options, callback) {};

/**
 * @param {string} path
 * @param {string} data
 * @param {number} flags
 * @param {zk.patch_cb} path_cb
 */
zk.ZooKeeper.prototype.a_create = function(path, data, flags, path_cb) {};

/**
 * @param {string} path
 * @param {number} version
 * @param {zk.void_cb} void_cb
 */
zk.ZooKeeper.prototype.a_delete = function(path, version, void_cb) {};

/**
 * @param {string} path
 * @param {number} version
 * @param {zk.void_cb} void_cb
 */
zk.ZooKeeper.prototype.a_delete_ = function(path, version, void_cb) {};

/**
 * @param {string} path
 * @param {boolean} watch
 * @param {zk.child_cb} child_cb
 */
zk.ZooKeeper.prototype.a_get_children = function(path, watch, child_cb) {};

/**
 * @param {string} path
 * @param {string} data
 * @param {number} version
 * @param {zk.stat_cb} stat_cb
 */
zk.ZooKeeper.prototype.a_set = function(path, data, version, stat_cb) {};

/**
 * @param {string} path
 * @param {boolean} watch
 * @param {zk.data_cb} data_cb
 */
zk.ZooKeeper.prototype.a_get = function(path, watch, data_cb) {};

/**
 * @param {string} path
 * @param {zk.watch_cb} watch_cb
 * @param {zk.stat_cb} stat_cb
 */
zk.ZooKeeper.prototype.aw_exists = function(path, watch_cb, stat_cb) {};

/**
 * @param {string} path
 * @param {zk.watch_cb} watch_cb
 * @param {zk.child_cb} child_cb
 */
zk.ZooKeeper.prototype.aw_get_children = function(path, watch_cb, child_cb) {};

zk.ZooKeeper.prototype.close = function() {};


/**
 * @param {string} path
 * @param {string} data
 * @param {number} flags
 * @param {function(Error, string)} callback
 */
zk.ZooKeeper.prototype.mkdirp = function(path, data, flags, callback) {};


/**
 * @param {string} path
 * @param {boolean} watch
 * @param {zk.stat_cb} stat_cb
 */
zk.ZooKeeper.prototype.a_exists = function(path, watch, stat_cb) {};
