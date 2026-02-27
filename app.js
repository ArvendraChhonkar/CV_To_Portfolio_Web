const express = require('express');



const app = express();


app.use((req, res, next) => {
    console.log("404 Not Found");
    res.status(404).send("404 Not Found");

});


app.listen(3000,() => {
    console.log('Server is running on port 3000');
});