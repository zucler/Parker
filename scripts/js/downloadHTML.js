var page = new WebPage()
var fs = require('fs');
var system = require('system');
var args = system.args;

if (!args[1]) {
    console.log("No URL provided, quitting...")
    phantom.exit();
}

var url = args[1];

if (args[2]) {
    var savePath = args[2];
}
else {
    var savePath = "temp.html";
}
page.onLoadFinished = function () {
    console.log("page load finished");
    fs.write(savePath, page.content, 'w');
    phantom.exit();
};

page.open(url, function () {
    page.evaluate(function () {
    });
});
