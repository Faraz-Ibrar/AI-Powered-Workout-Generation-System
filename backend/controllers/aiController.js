const { exec } = require('child_process');
const path = require('path');
const util = require('util');
const UserProfile = require('../models/UserProfile');

// Promisify exec to use with async/await
const execPromise = util.promisify(exec);

exports.generateWorkoutPlan = async (req, res) => {
  console.log('=== generateWorkoutPlan called ===');
  console.log('Request body:', req.body);

  const userId = req.body.userId;

  // Check if userId is provided and valid
  if (!userId || typeof userId !== 'string' || userId.length !== 24) {
    console.log('ERROR: Invalid userId provided');
    return res.status(400).json({ error: 'User ID must be a 24-character string' });
  }

  console.log('Processing userId:', userId);

  // Absolute path to the Python script
  const scriptPath = path.join(__dirname, '../ai/workout_ai.py');
  console.log('Python script path:', scriptPath);

  // Wrap path in quotes to handle spaces
  const command = `python "${scriptPath}" ${userId}`;
  console.log('Executing command:', command);

  try {
    // Execute the Python script
    const { stdout, stderr } = await execPromise(command);
    console.log('=== Python script execution completed ===');

    if (stderr) {
      console.error('[Python Script STDERR]', stderr);
    }

    console.log('[Python Script STDOUT]', stdout);
    console.log('[STDOUT Length]', stdout.length);

    // Check if stdout is empty
    if (!stdout || stdout.trim() === '') {
      console.error('ERROR: Python script returned empty output');
      return res.status(500).json({ error: 'Python script returned no data' });
    }

    // Parse Python script output
    let result;
    try {
      result = JSON.parse(stdout.trim());
      console.log('[Parsed Result]', result);
    } catch (parseError) {
      console.error('[JSON Parse Error]', parseError.message);
      console.error('[Raw Output]', stdout);
      return res.status(500).json({ error: 'Failed to parse AI response' });
    }

    // Check for errors in Python script result
    if (result.status !== 'success') {
      console.log('Python script returned error:', result.error);
      return res.status(400).json({ error: result.error });
    }

    // Save the generated workout plan into MongoDB
    const updateResult = await UserProfile.updateOne(
      { _id: userId },
      { $set: { workoutPlan: result.data } }
    );

    if (updateResult.matchedCount === 0) {
      console.error('ERROR: User not found in MongoDB');
      return res.status(404).json({ error: 'User not found' });
    }

    console.log('=== Sending successful response ===');
    console.log('Response data:', result.data);

    // Success - send the workout plan back to frontend
    res.status(200).json({
      success: true,
      message: 'Workout plan generated successfully',
      workoutPlan: result.data
    });

  } catch (error) {
    console.error('[Server Error]', error.message);
    return res.status(500).json({ error: 'Internal server error' });
  }
};