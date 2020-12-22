const csvtojson = require("csvtojson");

const mongodb = require("mongodb").MongoClient;

let url = "mongodb://localhost:27017/";

function isNumeric(n) { 
	return !isNaN(parseFloat(n)) && isFinite(n);
}

csvtojson()
  .fromFile("cities.csv")
  .then(csvData => {
    var parsedData = csvData.map(function(obj) {
      return Object.keys(obj).reduce(function(memo, key) {
        var value = obj[key];
        memo[key] = isNumeric(value) ? parseFloat(value) : value;
        return memo;
      }, {})
    })
    console.log(parsedData[0])
    mongodb.connect(url,{ useNewUrlParser: true, useUnifiedTopology: true },(err, client) => {
        if (err) throw err;
          let db = client.db("cs266_db")
          db.collection('cities',function(err, collection){
            collection.deleteMany({},function(err, removed){
              if (err) throw err;
              collection.insertMany(parsedData, (err, res) => {
                if (err) throw err;
                console.log(`Inserted: ${res.insertedCount} rows`);
                client.close();
              });
            });
        });
      });
  });
