const router = require('express').Router();
const childProcess = require('child_process');
const path = require("path");


router.post('/pdf', (req, res) => {
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'pdf']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        res.send(`http://localhost:${process.env.PORT || 4000}/download/${data}`);
    });
});

router.post('/txt', (req, res) => {
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'txt']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        res.send(`http://localhost:${process.env.PORT || 4000}/download/${data}`);
    });
});

router.post('/ppt', (req, res) => {
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'ppt']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        res.send(`http://localhost:${process.env.PORT || 4000}/download/${data}`);
    });
});


module.exports = router;
