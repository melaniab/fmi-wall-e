var http = require("http");
var fs = require('fs');
const img_dir = './masked_imgs/';

function send_image(response) {
  var files = fs.readdirSync(img_dir);
  files.sort();
  var img = fs.readFileSync(img_dir + files[files.length - 1]);
  response.writeHead(200, {'Content-Type': 'image/gif' });
  response.end(img, 'binary');
}

http.createServer(function (request, response) {
  send_image(response);
}).listen(8081);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');
