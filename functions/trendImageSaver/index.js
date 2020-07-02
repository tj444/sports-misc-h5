const setup = require('./lib/setup');
const fs = require('fs');
const qiniu = require('qiniu');


module.exports.initializer = function(context, callback) {
  console.log('initializing');
  callback(null, ''); 
};

module.exports.handler = (req, resp, context) => {
  const url = 'http://api.tc.jiedaimarket.cn/trendImage';

  screenshot(url, context)
    .then(outputFile => {
      // Get screenshot successful return
      resp.setStatusCode(200);
      resp.setHeader('content-type', 'image/jpeg');
      resp.send(fs.readFileSync(outputFile));
    })
    .catch(err => {
      // Get screenshot failed return
      resp.setStatusCode(500);
      resp.setHeader('content-type', 'text/plain');

      resp.send(err.message);
    });
};

// Get screenshot method
async function screenshot(url, context) {
  // Open a new browser viewport
  let browser = await setup.getBrowser(context);

  const page = await browser.newPage();
  const outputFile = '/tmp/screenshot.jpg';

  let retry = 0;
  let success = false;
  
  // Try to read the screenshot less than 6 times
  do {
    try {
      await page.goto(url, {
        'waitUntil': 'networkidle0'
      });
      // await page.evaluateHandle('document.fonts.ready');
      success = true;
    } catch(e) {
      retry++;

      if (retry >= 6) {
        throw e;
      }
    }
  } while(!success && retry < 6);

  // Set the path of the screenshot, whether it is full page or not, and type
  await page.screenshot({
    path: outputFile,
    fullPage: true,
    type: 'jpeg'
  });

  return outputFile;
}