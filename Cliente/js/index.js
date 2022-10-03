const http = require('http');
const express = require('express');
const swig = require('swig');
const routing = require('./routing.js');
const bodyParser = require('body-parser');

const app = express();
const port = 8888;



app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.engine('html',swig.renderFile);
app.set('view engine','html');
app.set('views','html');
app.set('view cache', false);
swig.setDefaults({ cache: false });

app.use('/',routing);

app.listen(port,() => console.log('Example app listening on port '+port))
