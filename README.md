# AI-Powered Workout Plan Generation System

## Project Summary

This project is an AI-powered workout plan generation system designed to create personalized fitness regimens tailored to individual user profiles. The system intelligently considers multiple factors including:

- User's current fitness level
- Fitness goals (strength, hypertrophy, endurance)
- Available workout days per week
- Available equipment
- Optional calorie burn targets

The system employs advanced AI optimization techniques to generate diverse, effective, and personalized workout plans that promote optimal training outcomes and sustained user engagement.

**Technology Stack:** Full MERN (MongoDB, Express.js, React, Node.js) application with Python-based AI backend integration.

## Project Structure

```
AI-Workout-System/
├── backend/
│   ├── ai/
│   │   └── workout_ai.py          # AI algorithms implementation
│   ├── config/
│   │   └── db.js                  # Database configuration
│   ├── controllers/
│   │   └── aiController.js        # AI service controllers
│   ├── models/
│   │   └── UserProfile.js         # User data models
│   ├── routes/
│   │   └── userRoutes.js          # API routes
│   ├── .env                       # Environment variables
│   ├── package.json
│   └── server.js                  # Express server
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── UserProfileForm.css
│       │   └── UserProfileForm.js # User input interface
│       ├── App.js                 # Main React application
│       ├── App.css
│       ├── index.js
│       └── ...
├── package.json
└── README.md
```

## Setup and Run Instructions

### Prerequisites
- **Node.js** (v14 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **MongoDB** (local installation or MongoDB Atlas) - [Download here](https://mongodb.com/)
- **npm** package manager (comes with Node.js)
- **Git** for version control

### Complete Installation Guide

#### Step 1: Clone the Repository
```bash
git clone <https://github.com/Faraz-Ibrar/AI-Powered-Workout-Generation-System.git>
cd AI-Workout-System
```

#### Step 2: Backend Setup

**Open Terminal 1 for Backend:**

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install express mongoose cors dotenv nodemon
   ```
   
   **Dependencies Explanation:**
   - `express` - Web framework for Node.js
   - `mongoose` - MongoDB object modeling for Node.js
   - `cors` - Enable Cross-Origin Resource Sharing
   - `dotenv` - Load environment variables from .env file
   - `nodemon` - Auto-restart server during development

3. **Install Python dependencies:**
   ```bash
   pip install numpy pandas scikit-learn pymongo bson datetime typing enum34
   ```
   
   **Python Libraries Explanation:**
   - `numpy` - Numerical computing library
   - `pandas` - Data manipulation and analysis
   - `scikit-learn` - Machine learning library
   - `pymongo` - MongoDB driver for Python
   - `bson` - BSON (Binary JSON) support
   - `datetime` - Date and time handling
   - `typing` - Type hints support
   - `enum34` - Enumeration support

4. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   MONGODB_URI=mongodb://127.0.0.1:27017/workoutdb
   ```

5. **Start the backend server:**
   ```bash
   node /server.js
   ```
   **Note:** Make sure your `package.json` has this script:
   ```json
   "scripts": {
     "start": "node server.js",
     "dev": "nodemon server.js"
   }
   ```
   
   The backend will run on `http://localhost:5000`
   **Keep this terminal open and running**

#### Step 3: Frontend Setup

**Open Terminal 2 for Frontend (New Terminal Window/Tab):**

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install React dependencies:**
   ```bash
   npm install react react-dom axios react-router-dom
   ```
   
   **Frontend Dependencies Explanation:**
   - `react` - React library for building user interfaces
   - `react-dom` - React DOM rendering
   - `axios` - HTTP client for making API requests
   - `react-router-dom` - Routing library for React applications

3. **Start the development server:**
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000`
   **Keep this terminal open and running**

#### Step 4: Database Setup

**Just make sure mongoDb is installed and running**

#### Step 5: Running the Complete System

**You should now have 3 terminals running:**

1. **Terminal 1 (Backend):** 
   ```bash
   cd backend && node /server.js
   ```
   Status: Backend server running on `http://localhost:5000`

2. **Terminal 2 (Frontend):**
   ```bash
   cd frontend && npm start
   ```
   Status: React app running on `http://localhost:3000`


#### Step 6: Testing the Application

1. **Open your browser** and go to `http://localhost:3000`
2. **Fill out the user profile form** with your fitness information
3. **Generate your AI-powered workout plan**
4. **Verify backend connectivity** by checking Terminal 1 for API request logs

### Package.json Files Reference

**Backend package.json:**
```json
{
  "name": "workout-ai-backend",
  "version": "1.0.0",
  "description": "AI-powered workout plan generation backend",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.5.0",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "body-parser": "^1.20.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

**Frontend package.json:**
```json
{
  "name": "workout-ai-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.5.0",
    "react-router-dom": "^6.15.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.17.0",
    "web-vitals": "^2.1.4"
  }
}
```

### Troubleshooting Common Issues

**Port Already in Use:**
```bash
# Kill process on port 3000 (frontend)
npx kill-port 3000

# Kill process on port 5000 (backend)
npx kill-port 5000
```

**MongoDB Connection Issues:**
- Ensure MongoDB service is running
- Check if port 27017 is available
- Verify connection string in `.env` file


### Development Workflow

1. **Make changes to backend code** → Server auto-restarts (thanks to nodemon)
2. **Make changes to frontend code** → Page auto-refreshes (thanks to React hot reload)
3. **Database changes** → Use MongoDB Compass or shell for direct database operations
4. **Python AI code changes** → Restart backend server to reload Python modules

## Complete Dependencies List

### Backend Dependencies (Node.js)
```json
{
  "dependencies": {
    "express": "^4.18.2",           // Web framework
    "mongoose": "^7.5.0",           // MongoDB ODM
    "cors": "^2.8.5",               // Cross-Origin Resource Sharing
    "dotenv": "^16.3.1",            // Environment variables
    "body-parser": "^1.20.2",       // Parse HTTP request bodies
    "bcryptjs": "^2.4.3",           // Password hashing (optional)
    "jsonwebtoken": "^9.0.2"        // JWT authentication (optional)
  },
  "devDependencies": {
    "nodemon": "^3.0.1"             // Auto-restart server during development
  }
}
```

### Frontend Dependencies (React)
```json
{
  "dependencies": {
    "react": "^18.2.0",             // React library
    "react-dom": "^18.2.0",         // React DOM rendering
    "axios": "^1.5.0",              // HTTP client for API calls
    "react-router-dom": "^6.15.0",  // Routing for React
    "react-scripts": "5.0.1",       // Create React App scripts
    "@mui/material": "^5.14.0",     // Material-UI components (optional)
    "@emotion/react": "^11.11.0",   // CSS-in-JS library
    "@emotion/styled": "^11.11.0"   // Styled components
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.17.0",
    "web-vitals": "^2.1.4"
  }
}
```

### Python Dependencies (AI Backend)
```txt
numpy==1.24.3              # Numerical computing
pandas==2.0.3              # Data manipulation
scikit-learn==1.3.0        # Machine learning algorithms
pymongo==4.5.0             # MongoDB driver
python-dotenv==1.0.0       # Environment variables in Python
flask==2.3.3               # Lightweight web framework (if using Flask endpoints)
requests==2.31.0           # HTTP library
datetime                   # Built-in datetime module
typing                     # Built-in typing module
enum34==1.1.10             # Enumeration support
bson==0.5.10               # BSON support
```

### Quick Start Commands (Copy & Paste Ready)

**Terminal 1 - Backend Setup:**
```bash
cd backend
npm install express mongoose cors dotenv body-parser nodemon
pip install numpy pandas scikit-learn pymongo python-dotenv flask requests enum34 bson
node /server.js
```

**Terminal 2 - Frontend Setup:**
```bash
cd frontend  
npm install react react-dom axios react-scripts
npm start
```


## AI Techniques Used and Justification

### 1. Genetic Algorithms

**Implementation:** Core optimization engine for workout plan generation

**Justification:**
- **Large Solution Space Exploration:** Fitness planning involves numerous variables (exercises, sets, reps, rest periods, workout frequency) creating a vast solution space that genetic algorithms can efficiently navigate
- **Multi-objective Optimization:** Simultaneously optimizes for multiple fitness goals (strength, hypertrophy, endurance) while respecting constraints (available time, equipment, fitness level)
- **Diversity Maintenance:** Generates diverse workout plans preventing monotony and promoting long-term adherence
- **Adaptive Evolution:** Plans can evolve over time as user fitness improves or goals change
- **Constraint Handling:** Naturally incorporates user constraints (equipment availability, time limitations) into the optimization process

**Technical Benefits:**
- Population-based approach ensures multiple viable solutions
- Crossover operations combine successful elements from different plans
- Mutation introduces beneficial variations and prevents local optima
- Fitness function can be customized for different user profiles

### 2. Hill Climbing Algorithm

**Implementation:** Local search optimization for plan refinement

**Justification:**
- **Fine-tuning Optimization:** After genetic algorithm produces the best candidate, hill climbing performs local improvements to maximize plan effectiveness
- **Computational Efficiency:** Faster convergence for local optimization compared to continuing genetic evolution
- **Parameter Adjustment:** Precisely adjusts workout parameters (volume, intensity, progression) for optimal results
- **Quality Enhancement:** Ensures the final workout plan achieves maximum fitness score within the local solution neighborhood

**Technical Benefits:**
- Deterministic improvement process
- Minimal computational overhead
- Guaranteed local optimum
- Complements genetic algorithm's global search capabilities

### Combined Approach Benefits

The hybrid genetic algorithm + hill climbing approach provides:

1. **Global + Local Optimization:** Genetic algorithms explore globally while hill climbing optimizes locally
2. **Balanced Performance:** Achieves both diversity (genetic) and precision (hill climbing)
3. **Scalable Solution:** Can handle increasing complexity as user base and requirements grow
4. **Personalization:** Generates truly individualized plans rather than template-based solutions
5. **Continuous Improvement:** Plans can be re-optimized as user data and preferences evolve

This AI-driven approach ensures users receive scientifically-optimized, personalized workout plans that adapt to their unique fitness journey while maintaining engagement through intelligent variation and progression.

## Features

- **Personalized Assessment:** Comprehensive user profiling system
- **AI-Driven Optimization:** Advanced algorithms for plan generation
- **Equipment Flexibility:** Adapts to available equipment
- **Goal-Oriented Planning:** Supports multiple fitness objectives
- **Progressive Planning:** Plans evolve with user progress
- **Responsive Design:** Mobile-friendly interface
- **Data Persistence:** Secure user data storage

## API Endpoints

- `POST /api/users/profile` - Create/update user profile
- `GET /api/users/profile/:id` - Retrieve user profile
- `POST /api/users/generate-workout` - Generate AI workout plan

---

**Note:** This system is designed for educational and research purposes. Users should consult with fitness professionals before beginning any new workout regimen.
