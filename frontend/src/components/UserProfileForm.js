import React, { useState } from 'react';
import axios from 'axios';
import './UserProfileForm.css';

const UserProfileForm = () => {
    const [currentScreen, setCurrentScreen] = useState('form');
    const [profile, setProfile] = useState({
        fitnessLevel: '',
        goal: '',
        availableDays: '',
        equipment: [],
        calorieGoal: '',
    });

    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [workoutPlan, setWorkoutPlan] = useState(null);

    const handleChange = (e) => {
        const name = e.target.name;
        const value = e.target.value;

        setProfile((prev) => ({
            ...prev,
            [name]: value
        }));

        if (errors[name]) {
            setErrors((prev) => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const handleCheckboxChange = (e) => {
        const checked = e.target.checked;
        const value = e.target.value;

        setProfile((prev) => {
            if (checked) {
                return { ...prev, equipment: [...prev.equipment, value] };
            } else {
                return { ...prev, equipment: prev.equipment.filter((item) => item !== value) };
            }
        });

        if (checked && errors.equipment) {
            setErrors((prev) => ({
                ...prev,
                equipment: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        if (!profile.fitnessLevel) newErrors.fitnessLevel = 'Fitness level is required.';
        if (!profile.goal) newErrors.goal = 'Goal is required.';
        if (!profile.availableDays || profile.availableDays <= 0)
            newErrors.availableDays = 'Please enter a valid number of available days.';
        if (!profile.equipment.length) newErrors.equipment = 'Select at least one equipment.';
        if (!profile.calorieGoal) newErrors.calorieGoal = 'Calorie Goal is required.';
        return newErrors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const validationErrors = validateForm();
        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            return;
        }

        setLoading(true);
        setSuccessMessage('');
        setErrorMessage('');
        setWorkoutPlan(null);

        try {
            console.log('=== Submitting form ===');
            console.log('Profile data:', profile);

            const profileResponse = await axios.post('http://localhost:5000/api/users', profile);
            console.log('Profile created:', profileResponse.data);

            const userId = profileResponse.data._id;
            console.log('User  ID:', userId);

            console.log('Generating workout plan...');
            const workoutResponse = await axios.post('http://localhost:5000/api/users/generate-workout', {
                userId: userId
            });

            console.log('=== Workout response received ===');
            console.log('Full response:', workoutResponse);
            console.log('Response data:', workoutResponse.data);

            // Access the workout plan from the response
            const workoutPlan = workoutResponse.data.workoutPlan.weekly_plan; // Adjusted to match the response structure

            if (workoutPlan) {
                console.log('Workout plan generated successfully!');
                console.log('Workout plan:', workoutPlan);

                setWorkoutPlan(workoutPlan);
                setSuccessMessage('Profile saved and workout plan generated successfully!');
                setCurrentScreen('results');
                setErrors({});
            } else {
                console.error('Failed to generate workout plan - no data received');
                setErrorMessage('Failed to generate workout plan - no data received');
            }

        } catch (error) {
            console.error('=== Error occurred ===');
            console.error('Error details:', error);
            console.error('Error response:', error.response?.data);

            if (error.response?.status === 404) {
                setErrorMessage('API endpoint not found. Check if backend server is running.');
            } else {
                setErrorMessage('Failed to save profile or generate workout plan: ' +
                    (error.response?.data?.error || error.message));
            }
        } finally {
            setLoading(false);
        }
    };

    const handleCreateNewProfile = () => {
        setCurrentScreen('form');
        setProfile({
            fitnessLevel: '',
            goal: '',
            availableDays: '',
            equipment: [],
            calorieGoal: '',
        });
        setErrors({});
        setSuccessMessage('');
        setErrorMessage('');
        setWorkoutPlan(null);
        setLoading(false);
    };

    // Form Screen Component
    const FormScreen = () => (
        <form className="user-profile-form" onSubmit={handleSubmit} noValidate>
            <h2>Create Your Profile</h2>

            {/* Fitness Level */}
            <label>
                Fitness Level:
                <select name="fitnessLevel" value={profile.fitnessLevel} onChange={handleChange} required>
                    <option value="">Select your fitness level</option>
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
                {errors.fitnessLevel && <span className="error">{errors.fitnessLevel}</span>}
            </label>

            {/* Goal */}
            <label>
                Goal:
                <select name="goal" value={profile.goal} onChange={handleChange} required>
                    <option value="">Select your goal</option>
                    <option value="Strength">Strength</option>
                    <option value="Hypertrophy">Hypertrophy</option>
                    <option value="Endurance">Endurance</option>
                </select>
                {errors.goal && <span className="error">{errors.goal}</span>}
            </label>

            {/* Available Days */}
            <label>
                Available Days per Week:
                <input
                    type="number"
                    name="availableDays"
                    value={profile.availableDays}
                    onChange={handleChange}
                    min="1"
                    max="7"
                    placeholder="e.g., 3"
                    required
                />
                {errors.availableDays && <span className="error">{errors.availableDays}</span>}
            </label>

            {/* Equipment checkboxes */}
            <label>Equipment (select all that apply):</label>
            <div className="checkbox-group">
                {[
                    "Dumbbells",
                    "Barbell",
                    "Bench",
                    "Pull-up Bar",
                    "Parallel bars",
                    "Cable machine",
                    "Stationary bike",
                ].map((item) => (
                    <div key={item} className="checkbox-item">
                        <input
                            type="checkbox"
                            id={`equipment-${item}`}
                            name="equipment"
                            value={item}
                            checked={profile.equipment.includes(item)}
                            onChange={handleCheckboxChange}
                        />
                        <label htmlFor={`equipment-${item}`}>{item}</label>
                    </div>
                ))}
                {errors.equipment && <span className="error">{errors.equipment}</span>}
            </div>

            {/* Calorie Goal */}
            <label>
                Calorie Goal (1000-20000):
                <input
                    type="number"
                    name="calorieGoal"
                    value={profile.calorieGoal}
                    onChange={handleChange}
                    min="1000"
                    max="20000"
                    placeholder="e.g., 5000"
                    required
                />
                {errors.calorieGoal && <span className="error">{errors.calorieGoal}</span>}
            </label>

            <button type="submit" disabled={loading}>
                {loading ? 'Generating Workout Plan...' : 'Submit'}
            </button>

            {errorMessage && <div className="error">{errorMessage}</div>}
        </form>
    );

    // Collapsible section component
    const CollapsibleSection = ({ title, children, isOpen, onToggle, icon }) => (
        <div className="collapsible-section">
            <div className="collapsible-header" onClick={onToggle}>
                <div className="header-content">
                    {icon && <span className="section-icon">{icon}</span>}
                    <h4>{title}</h4>
                </div>
                <span className={`toggle-arrow ${isOpen ? 'open' : ''}`}>▼</span>
            </div>
            {isOpen && (
                <div className="collapsible-content">
                    {children}
                </div>
            )}
        </div>
    );

    // Exercise component
    const ExerciseItem = ({ exercise, index }) => (
        <div className="exercise-item">
            <div className="exercise-header">
                <span className="exercise-number">{index + 1}</span>
                <h5>{exercise.name || 'Exercise'}</h5>
            </div>
            <div className="exercise-details">
                {exercise.sets !== undefined && exercise.reps !== undefined && (
                    <>
                        <span className="detail-badge">Sets: {exercise.sets}</span>
                        <span className="detail-badge">Reps: {exercise.reps}</span>
                    </>
                )}
                <span className="detail-badge">Calories: {exercise.calories}</span>
            </div>
        </div>
    );

    // State for collapsible sections
    const [openSections, setOpenSections] = useState({});

    const toggleSection = (sectionKey) => {
        setOpenSections(prev => ({
            ...prev,
            [sectionKey]: !prev[sectionKey]
        }));
    };

    // Function to render workout plan hierarchically
    const renderWorkoutPlan = (plan) => {
        if (!plan) return null;

        const workoutData = plan; // Directly use the plan as it is already the weekly_plan

        return workoutData.map((day, dayIndex) => (
            <CollapsibleSection
                key={`day-${dayIndex}`}
                title={`Day ${day.day_number} - Muscle Groups: ${day.muscle_groups.join(', ')}`}
                isOpen={openSections[`day-${dayIndex}`]}
                onToggle={() => toggleSection(`day-${dayIndex}`)}
                icon="🗓️"
            >
                <div className="day-total-calories">
                    <strong>Total Calories:</strong> {day.total_calories}
                </div>
                {day.exercises.map((exercise, exerciseIndex) => (
                    <ExerciseItem
                        key={`exercise-${dayIndex}-${exerciseIndex}`}
                        exercise={exercise}
                        index={exerciseIndex}
                    />
                ))}
            </CollapsibleSection>
        ));
    };

    // Results Screen Component
    const ResultsScreen = () => (
        <div className="results-screen">
            <h2>Your Workout Plan</h2>

            {successMessage && (
                <div className="success-message">
                    {successMessage}
                </div>
            )}

            {workoutPlan && (
                <div className="workout-plan">
                    <div className="plan-header">
                        <h3>Generated Workout Plan</h3>
                        <button
                            className="expand-all-btn"
                            onClick={() => {
                                const allSections = {};
                                const toggleAll = Object.keys(openSections).length === 0 ||
                                    Object.values(openSections).some(v => !v);

                                workoutPlan.forEach((_, index) => {
                                    allSections[`day-${index}`] = toggleAll;
                                });

                                setOpenSections(allSections);
                            }}
                        >
                            {Object.values(openSections).some(v => v) ? 'Collapse All' : 'Expand All'}
                        </button>
                    </div>

                    <div className="hierarchical-plan">
                        {renderWorkoutPlan(workoutPlan)}
                    </div>
                </div>
            )}

            <div className="button-container">
                <button
                    onClick={handleCreateNewProfile}
                    className="btn btn-primary"
                >
                    Create New Profile
                </button>
            </div>
        </div>
    );

    // Render based on current screen
    return (
        <div className="user-profile-container">
            {currentScreen === 'form' ? <FormScreen /> : <ResultsScreen />}
        </div>
    );
};

export default UserProfileForm;
