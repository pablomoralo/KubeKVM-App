const express = require('express');
const router = express.Router();
var os = require("os");

router.get('/', (req, res) => {
  res.render('index');
});

router.get('/test', (req, res) => {
  const name = os.hostname();
  res.render('test', {name});
});

module.exports = router;
