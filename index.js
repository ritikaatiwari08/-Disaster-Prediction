const express = require('express'); // Import Express
const bodyParser = require('body-parser'); // Import body-parser
const cors = require('cors'); // Import cors

const app = express(); // Initialize Express app
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json()); // Parse JSON requests
app.use(cors()); // Enable CORS for all origins

// Root route
app.get('/', (req, res) => {
    res.send('AI-Based Disaster Prediction and Response System is running!');
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
