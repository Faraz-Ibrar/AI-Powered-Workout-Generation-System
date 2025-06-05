// backend/models/UserProfile.js
const mongoose = require('mongoose');


const UserProfileSchema = new mongoose.Schema({
  fitnessLevel: { type: String, required: true },
  goal: { type: String, required: true },
  availableDays: { type: Number, required: true },
  calorieGoal: { type: Number, required: true },
  equipment: {
    type: [String], // Assuming you want to store equipment as an array of strings
    required: true,
  }
});


module.exports = mongoose.model('UserProfile', UserProfileSchema);
