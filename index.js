const express = require('express'); // Import Express
const bodyParser = require('body-parser'); // Import body-parser
const cors = require('cors'); // Import cors
const path = require('path'); // Import path for serving static files

const app = express(); // Initialize Express app
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json()); // Parse JSON requests
app.use(cors()); // Enable CORS for all origins
app.use('/static', express.static(path.join(__dirname, 'static'))); // Serve the static folder

// Serve the frontend HTML (index.html in the root folder)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// POST /predict route
app.post('/predict', (req, res) => {
    const { location, risk_factor } = req.body;
    let prediction = "No significant risk detected.";

    if (risk_factor > 8) {
        prediction = `High risk of disaster in ${location}. Take immediate precautions.`;
    } else if (risk_factor > 5) {
        prediction = `Moderate risk of disaster in ${location}. Stay alert.`;
    } else if (risk_factor > 3) {
        prediction = `Low risk of disaster in ${location}. Monitor the situation.`;
    }

    res.json({ prediction, data: { location, risk_factor } });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
