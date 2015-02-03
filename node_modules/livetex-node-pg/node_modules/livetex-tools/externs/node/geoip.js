

/**
 * @namespace
 */
var geoip = {};


/**
 * @constructor
 * @param {string} path Путь к файлу данных.
 * @param {boolean=} opt_cached Флаг кэширования.
 */
geoip.City = function(path, opt_cached) {};


/**
 * @param {string} address
 * @param {function(Error,  {
   country_code: string,
   country_name: string,
   region: string,
   city: string
   })} callback
 */
geoip.City.prototype.lookup = function(address, callback) {};
