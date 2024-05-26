const express = require('express');
const crypto = require('crypto');
const db = require('./database');
const router = express.Router();

const hashPassword = (password, salt) => {
    return new Promise((resolve, reject) => {
        crypto.pbkdf2(password, salt, 100000, 64, 'sha256', (err, derivedKey) => {
            if (err) reject(err);
            else resolve(derivedKey.toString('hex'));
        });
    });
};

router.post('/login', (req, res) => {
  const { username, password } = req.body;
  db.get(`SELECT * FROM StudentLogins WHERE Username = ?`, [username], async (err, user) => {
    if (err) {
      res.status(500).json({ status: 'error', message: 'Database error' });
      return;
    }
    if (user) {
      try {
          const hashedPassword = await hashPassword(password, user.Salt); // Assume salt is stored or you have a method to retrieve it
          if (hashedPassword === user.Password) {
              res.json({ status: 'success', message: 'Login successful' });
          } else {
              res.status(401).json({ status: 'error', message: 'Invalid credentials' });
          }
      } catch (error) {
          res.status(500).json({ status: 'error', message: 'Error in password hashing' });
      }
    } else {
      res.status(404).json({ status: 'error', message: 'User not found' });
    }
  });
});

module.exports = router;
