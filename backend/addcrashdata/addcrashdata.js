// Group 11
// Ziqiang Li, 1173898
// Donghao Yang, 1514687
// Rui Mao, 1469805
// Xiaxuan Du, 1481272
// Ruoyu Lu, 1466195

const async = require('async');
const accidentData = require('../../data/TAS_DSG_-_Tasmania_Crash_Statistics__Point__2010-2020/dsg_tasmania_crash_stats_2010_2020-1558551482072282246.json');
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
const https = require('https');

const options = {
  hostname: 'localhost',
  port: 9200,
  path: '/crashdata/_doc',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: 'elastic:elastic'
};

async function sendDataToElasticsearch(feature) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      console.log(`statusCode: ${res.statusCode}`);
      res.on('data', (d) => {
        process.stdout.write(d);
      });
      resolve();
    });

    req.on('error', (error) => {
      console.error(error);
      reject(error);
    });

    req.write(JSON.stringify(feature.properties));
    req.end();
  });
}

async function processFeatures() {
  try {
    await async.mapLimit(accidentData.features, 500, async (feature) => {
      await sendDataToElasticsearch(feature);
    });
    console.log('All features processed successfully.');
  } catch (error) {
    console.error('Error sending data to Elasticsearch:', error);
  }
}

processFeatures();
