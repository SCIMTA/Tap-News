const mongoose = require('mongoose');

mongoose.set('useCreateIndex', true);
module.exports.connect = (uri) => {
  // mongoose.connect(uri, { useNewUrlParser: true });
  mongoose.connect(
    uri,
    {
        useUnifiedTopology: true,
        useNewUrlParser: true,
        writeConcern: {
            j: true,
        }
    },
    () => console.log('Connected to DB!')
);

  mongoose.connection.on('error', (err) => {
    console.error(`Mongoose connection error: ${err}`);
    process.exit(1);
  });

  // load modules.
  require('./user');
}
