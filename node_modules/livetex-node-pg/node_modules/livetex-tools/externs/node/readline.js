


/**
 * @namespace
 */
var readline = {};


/**
 * Создаёт экземпляр интерфейса readline.
 *
 * @param {!Object} options Опции интерфейса.
 * @see http://nodejs.org/api/readline.html#readline_readline_createinterface_options
 */
readline.createInterface = function(options) {};


/**
 * @constructor
 */
readline.Interface = function() {};


/**
 * Устанавливает маркер начала ввода данных в консоль.
 *
 * @param {string} prompt Маркер начала ввода данных в консоль.
 * @param {number} length Длина prompt.
 */
readline.Interface.prototype.setPrompt = function(prompt, length) {};


/**
 * Показывает маркер начала ввода данных в консоль и устанавливает курсор.
 *
 * @param {boolean} preserveCursor Флаг. Если установлено значение true, то
 * курсор показываться не будет. (опционально)
 */
readline.Interface.prototype.prompt = function(preserveCursor) {};


/**
 * Выводит в консоль сообщение и вызывает обработчик ответа.
 *
 * @param {string} query Вопрос или сообщение, показываемое в консоли.
 * @param {function(string, number)} callback Обработчик ответа.
 */
readline.Interface.prototype.question = function(query, callback) {};


/**
 * Приостанавливает ввод данных в консоль.
 */
readline.Interface.prototype.pause = function() {};


/**
 * Возобновляет ввод данных через консоль.
 */
readline.Interface.prototype.resume = function() {};


/**
 * Закрывает readline интерфейс. Выбрасывает событие 'close'.
 */
readline.Interface.prototype.close = function() {};


/**
 * Записывает data в потк вывода.
 *
 * @param {*} data Данные, которые будут записаны в output.
 * @param {!Object} key Объект, представляющий собой набор клавиш.
 */
readline.Interface.prototype.write = function(data, key) {};