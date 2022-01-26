const monk = require('monk');
const db = monk(process, env, 'mongodb+srv://dawid200713:Mpqcesb8*@cluster0.cndbo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority');
module.exports = db;