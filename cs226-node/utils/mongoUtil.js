const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017";

var _db;
const dbName = 'cs266_db'
module.exports = {
    connectToServer: function (callback) {
        MongoClient.connect(url, {useNewUrlParser: true, useUnifiedTopology: true}, function (err, client) {
            _db = client.db(dbName);
            return callback(err);
        });
    },
    getDb: function () {
        return _db;
    }
};

