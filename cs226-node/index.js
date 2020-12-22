const express = require('express')
const path = require('path');
const bodyParser = require("body-parser")
const cors = require("cors")
const cities = require("./api/cities.route")
const mongoUtil = require("./utils/mongoUtil")

const app = express()
const port = process.env.PORT || 8000

app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

// Register api routes
app.use("/", express.static(path.join(__dirname,'cs226-web','dist')))
app.use("/api/cities", cities)


mongoUtil.connectToServer(function (err, client) {
    if (err) console.log(err);
    app.listen(port, () => {
        console.log(`listening on port ${port}`)
    })
});



