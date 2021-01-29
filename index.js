const path = require('path');
const express = require('express');
const convertRoute = require('./convertRoutes/index');
const bodyParser = require('body-parser');
const childProcess = require('child_process');


const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

childProcess.exec(`source ${path.join(__dirname,'twitterScript/venv/bin/activate')}`);



const PORT = process.env.PORT || 4000

app.use(express.static(path.join(__dirname, "build")));
app.use('/convert', convertRoute);

app.get("/download/:file", (req, res) => {
    res.download(`./fileSystem/${req.params.file}`);
});


app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "build/index.html"));
});

app.listen(PORT, () => {
    console.log(`Listening to PORT [ ${PORT} ]`)
})
