const express = require('express');
const router = express.Router();
const UserProfile = require('../models/UserProfile');
const aiController = require('../controllers/aiController');

// Create a new user profile
router.post('/', async (req, res) => {
    const { fitnessLevel, goal, availableDays, equipment, calorieGoal } = req.body;

    // Basic validation
    if (!fitnessLevel || !goal || availableDays <= 0 || !calorieGoal || !equipment) {
        return res.status(400).json({ message: 'Invalid input data' });
    }

    const userProfile = new UserProfile(req.body);
    try {
        const savedProfile = await userProfile.save();
        res.status(201).json(savedProfile);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
});


// Get all user profiles
router.get('/', async (req, res) => {
    try {
        const profiles = await UserProfile.find();
        res.json(profiles);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Generate workout plan
router.post('/generate-workout', aiController.generateWorkoutPlan);



module.exports = router;
