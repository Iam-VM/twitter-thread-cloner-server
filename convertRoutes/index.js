const router = require('express').Router();
const childProcess = require('child_process');
const path = require("path");


router.post('/pdf', (req, res) => {
    const download_url_slice =  "http://localhost:4000/download/";
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'pdf']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        data = data.toString()
        switch (data.slice(0, 3)) {
            case "END":
                res.send(download_url_slice + data.slice(3))
                break;
            case "CRF":
                console.log("CRF");
                req.io.emit("statusCode", "creating file...");
                break;
            case "PTF":
                console.log("PTF");
                req.io.emit("statusCode", "proceeding to fetch tweets...");
                // TODO: send "proceeding to tweet fetch"
                break;
            case "FTW":
                console.log("FTW");
                const dataSplitted = data.split(":");
                req.io.emit("statusCode", `fetching tweet ${dataSplitted[1]}`);
                // TODO: send "Fetchning tweet N"
                break;
            case "PRO":
                console.log("PRO");
                req.io.emit("statusCode", "processing tweets...");
                // TODO: send "processing tweets"
                break;
            case "MRG":
                console.log("MRG");
                req.io.emit("statusCode", "merging tweets...");
                // TODO send "merging tweets"
                break;
            default:
                console.log("raise error");
            // TODO: do something
        }
    });
});

router.post('/txt', (req, res) => {
    const download_url_slice =  "http://localhost:4000/download/";
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'txt']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        data = data.toString()
        switch (data.slice(0, 3)) {
            case "END":
                res.send(download_url_slice + data.slice(3))
                break;
            case "CRF":
                console.log("CRF");
                req.io.emit("statusCode", "creating file...");
                // TODO: send "creating file"
                break;
            case "PTF":
                console.log("PTF");
                req.io.emit("statusCode", "proceeding to fetch tweets...");
                // TODO: send "proceeding to tweet fetch"
                break;
            case "FTW":
                console.log("FTW");
                const dataSplitted = data.split(":");
                req.io.emit("statusCode", `fetching tweet ${dataSplitted[1]}`);
                // TODO: send "Fetchning tweet N"
                break;
            case "PRO":
                console.log("PRO");
                req.io.emit("statusCode", "processing tweets...");
                // TODO: send "processing"
                break;
            default:
                console.log("raise error");
            // TODO: do something
        }
    });
});

router.post('/ppt', (req, res) => {
    const download_url_slice =  "http://localhost:4000/download/";
    const pyProcess = childProcess.spawn('python3', [path.join(__dirname + '/../twitterScript/main.py'), req.body.url.toString(), 'ppt']);
    pyProcess.stderr.pipe(process.stderr);
    pyProcess.stdout.on('data', (data) => {
        data = data.toString()
        switch (data.slice(0, 3)) {
            case "END":
                res.send(download_url_slice + data.slice(3))
                break;
            case "CRF":
                console.log("CRF");
                req.io.emit("statusCode", "creating file...");
                // TODO: send "creating file"
                break;
            case "PTF":
                console.log("PTF");
                req.io.emit("statusCode", "proceeding to fetch tweets...");
                // TODO: send "proceeding to tweet fetch"
                break;
            case "FTW":
                console.log("FTW");
                const dataSplitted = data.split(":");
                req.io.emit("statusCode", `fetching tweet ${dataSplitted[1]}`);
                // TODO: send "Fetchning tweet N"
                break;
            case "PRO":
                console.log("PRO");
                req.io.emit("statusCode", "processing tweets...");
                // TODO: send "processing"
                break;
            default:
                console.log("raise error");
            // TODO: do something
        }
    });
});


module.exports = router;
