'use strict'

let express = require('express');
let http = require('http');

let app = express();
app.use(express.static('.'));

const json = require('./assets/courses.json'); // json object of scraped courses from web advisor

app.get('/get_json', function(req, res) {
    res.send(json);
});

let server = http.createServer(app);
server.listen(9000);
console.log('WAIO running @ localhost:9000');