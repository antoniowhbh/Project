const sqlite3 = require('sqlite3').verbose();

// Open the database
let db = new sqlite3.Database('./uniguide_student.db', (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the uniguide_student database.');
});

module.exports = db;
