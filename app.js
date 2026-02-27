const express = require('express');
const mainRoute = require('./routes/Main_route');


const app = express();
//using pug as the view engine
app.set('view engine', 'pug');
app.set('views', './views');
//public refference to css and js files
app.use(express.static('public'));

app.use(mainRoute);

app.use((req, res, next) => {
    console.log("404 Not Found");
    res.status(404).send("404 Not Found");

});


app.listen(3000,() => {
    console.log('Server is running on port 3000');
});