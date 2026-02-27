// use to controle '/' route only --> default route
const express = require('express');
const router = express.Router();
const path = require('../Util/Path');

router.get('/', (req, res) => {
    res.render("main", { title: "Home" });
});


module.exports = router;