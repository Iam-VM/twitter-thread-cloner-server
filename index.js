const path = require('path');
const express = require('express');
const convertRoute = require('./convertRoutes/index');
const bodyParser = require('body-parser');
const socketIO = require('socket.io');


const app = express();
const httpServer = require('http').createServer(app);
const io = socketIO(httpServer);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

io.on("connection", socket => {
    console.log("Connected");

    socket.on("disconnect", () => {
        console.log("disconnected");
    });
});


const PORT = process.env.PORT || 4000

app.use(express.static(path.join(__dirname, "build")));
app.use("*", (req, res, next) => {
    req.io = io;
    next();
});
app.use('/convert', convertRoute);

app.get("/download/:file", (req, res) => {
    res.download(`./fileSystem/${req.params.file}`);
});


app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "build/index.html"));
});

httpServer.listen(PORT, () => {
    console.log(`Listening to PORT [ ${PORT} ]`)
})
