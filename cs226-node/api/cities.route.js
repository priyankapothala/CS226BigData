const express = require('express')
const router = express.Router()
let citiesDAO = require('../dao/citiesDAO')

router.get('/',async function (req, res, next) {
    let sortType = {}
    if (req.query.criteria) {
      sortType = [req.query.criteria, -1]
    }
    else {
      sortType = ['quality_of_life', -1]
    }
    let data = await citiesDAO.getCities(sortType)
    res.send(data)
});

module.exports = router
