const setup = require('./lib/setup');
const fs = require('fs');
const qiniu = require('qiniu');


module.exports.initializer = function(context, callback) {
  console.log('initializing');
  callback(null, ''); 
};

module.exports.handler = (event, context, callback) => {
  const url = 'http://api.tc.jiedaimarket.cn/trendImage';

  screenshot(url, context)
    .then(outputFile => {
      uploadToQiniu(outputFile, callback);
    })
    .catch(err => {
      callback(err, 'fail');
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

function uploadToQiniu(localFile, callback) {
  const accessKey = process.env.QINIU_AK;
  const secretKey = process.env.QINIU_SK;
  const mac = new qiniu.auth.digest.Mac(accessKey, secretKey);
  // const key = 'sporttery/trends/image.jpg';
  // const bucket = 'elmercdn';
  const key = process.env.QINIU_FILEKEY;
  const bucket = process.env.QINIU_BUCKET;
  const options = {
    scope: bucket + ':' + key
  }
  const putPolicy = new qiniu.rs.PutPolicy(options);
  const uploadToken = putPolicy.uploadToken(mac);
  const config = new qiniu.conf.Config();
  config.zone = qiniu.zone[process.env.QINIU_UPZONE];

  const formUploader = new qiniu.form_up.FormUploader(config);
  const putExtra = new qiniu.form_up.PutExtra();
  // 文件上传
  formUploader.putFile(uploadToken, key, localFile, putExtra, function(respErr,
    respBody, respInfo) {
    if (respErr) {
      callback(respErr, 'fail');
    }
    if (respInfo.statusCode == 200) {
      const cdnManager = new qiniu.cdn.CdnManager(mac);

      console.log(respBody);
      const url = process.env.QINIU_URL + '/' + process.env.QINIU_FILEKEY;
      cdnManager.refreshUrls([url], function(err, respBody, respInfo) {
        if (respInfo.statusCode == 200) {
          console.log(respBody);
          callback(null, localFile);
        }
      });
    } else {
      console.log(respInfo.statusCode);
      console.log(respBody);
    }
  });
}