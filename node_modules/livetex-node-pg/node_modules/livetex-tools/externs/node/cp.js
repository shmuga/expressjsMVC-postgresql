


/**
 * @namespace
 */
var cp = {};


/**
 * @constructor
 * @extends {events.EventEmitter}
 *
 * @event exit
 * @event close
 * @event disconnect
 * @event message
 */
cp.ChildProcess = function() {};


/**
 * @type {string}
 */
cp.ChildProcess.prototype.pid = '';


/**
 * @param {string} message
 */
cp.ChildProcess.prototype.send = function(message) {};


/**
 *
 * @param {string} script
 * @param {!Array.<string>=} opt_options
 * @return {!cp.ChildProcess}
 */
cp.fork = function(script, opt_options) {};


/**
 * @param {string} command Команда для запуска.
 * @param {Array.<string>=} opt_args Список аргументов.
 * @param {Object=} opt_options Свойства.
 * @return {cp.ChildProcess} Дочерний процесс.
 */
cp.spawn = function(command, opt_args, opt_options) {};


/**
 * @param {string} file Файл программы для запуска.
 * @param {Array.<string>} args Список аргументов.
 * @param {Object} options Свойства.
 * @param {function(Error, Buffer, Buffer)} callback Обработчик завершения.
 */
cp.execFile = function(file, args, options, callback) {};
