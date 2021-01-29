const router = require('express').Router();
const childProcess = require('child_process');
const path = require("path");


router.post('/pdf', (req, res) => {
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname, 'main.py'), req.body.url.toString(), 'pdf']);
    pyProcess.stdout.on('data', (data) => {
        console.log(data.toString())
        res.send(data);
    });
});

router.post('/txt', (req, res) => {
    console.log("reached /txt")
    const pyProcess = childProcess.spawn('python3', [path.join('../twitterScript/main.py'), req.body.url.toString(), 'txt']);
    pyProcess.stdout.on('data', (data) => {
        console.log(data)
        res.send(`http://localhost:${process.env.PORT || 4000}/download/${data}`);
    });
});

router.post('/ppt', (req, res) => {
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname, 'script.py'), req.body.url.toString(), 'ppt']);
    pyProcess.stdout.on('data', (data) => {
        console.log(data.toString())
        res.send(data);
    });
});

module.exports = router;
