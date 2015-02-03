var express = require('express');
var router = express.Router();

router.get('/functions', function(req, res) {
    res.send("ok");
});

module.exports = router;