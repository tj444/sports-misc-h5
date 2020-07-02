const path = require('path');

const launchOptionForFC = [
    // error when launch(); No usable sandbox! Update your kernel
    '--no-sandbox',
    // error when launch(); Failed to load libosmesa.so
    '--disable-gpu',
    // freeze when newPage() 
    '--single-process',
    "--proxy-server='direct://'",
    '--proxy-bypass-list=*'
];

const localChromePath = path.join('/', 'code', 'headless_shell.tar.gz');

const setupChromePath = path.join(path.sep, 'tmp');
const executablePath = path.join(
    setupChromePath,
    'headless_shell'
);

const DEBUG = process.env.DEBUG;

module.exports = {
    launchOptionForFC,
    localChromePath,
    setupChromePath,
    executablePath,
    DEBUG
};