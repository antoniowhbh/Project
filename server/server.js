const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const authRouter = require('./authRouter');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

// Routes
app.use(authRouter);

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
