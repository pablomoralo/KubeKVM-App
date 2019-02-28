const mongoose = require('mongoose');
const config = require('./config');

mongoose.set('useCreateIndex', true);
/*mongoose.connect(config.db, {
  useCreateIndex: true,
  useNewUrlParser: true,
  useFindAndModify: false
})
.then(db => console.log('DB is connected'))
.catch(err => console.error(err));
*/

mongoose.connect(config.db, { useNewUrlParser: true }, (err, res) => {
  if (err) {
    return console.log(`Error al conectar a la base de datos: ${err}`);
  }
  console.log('Conexión a la base de datos establecida...');
})
