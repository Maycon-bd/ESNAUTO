const {Config} = require('@remotion/cli/config');
const {existsSync} = require('node:fs');
const chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
if (existsSync(chromePath)) Config.setBrowserExecutable(chromePath);
Config.setConcurrency(1);
