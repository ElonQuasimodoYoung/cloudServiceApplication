// Group 11
// Ziqiang Li, 1173898
// Donghao Yang, 1514687
// Rui Mao, 1469805
// Xiaxuan Du, 1481272
// Ruoyu Lu, 1466195

// LOad the file income.json and parse it into a variable named income
const income = require ('../../data/income_sudo/GCCSA-income-working_hours.json');

// Sett the HTTPS module so that accepts self-signed certificates
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Iterate through the income array and load each item into ElasticSearch using a simple HTTP request
const https = require ('https');

const options = {
  hostname: 'localhost',
  port: 9200,
  path: '/income/_doc',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: 'elastic:elastic'
};

income.features.forEach((feature) => {
  if (feature.properties) {
    const data = JSON.stringify(feature.properties);

    const req = https.request(options, (res) => {
      console.log(`Status Code: ${res.statusCode}`);
      res.on('data', (d) => {
        process.stdout.write(d);
      });
    });

    req.on('error', (error) => {
      console.error(error);
    });

    req.write(data);  // send data
    req.end();  // request end
  } else {
    console.log("No properties found for feature:", feature);
  }
});


