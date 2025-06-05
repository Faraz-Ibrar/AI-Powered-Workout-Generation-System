import json
import random
from enum import Enum
from typing import List, Optional, Tuple
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

# =============================================================================
# ENUMS AND DATA STRUCTURES
# =============================================================================

class FitnessGoal(str, Enum):
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"
    ENDURANCE = "endurance"

class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    ARMS = "arms"
    CORE = "core"
    LEGS = "legs"
    SHOULDERS = "shoulders"
    CARDIO = "cardio"

class UserProfile:
    def __init__(self, fitness_level: FitnessLevel, goal: FitnessGoal, 
                 available_days: int, equipment: List[str], 
                 session_duration: Optional[int] = None):
        self.fitness_level = fitness_level
        self.goal = goal
        self.available_days = available_days
        self.equipment = equipment
        self.session_duration = session_duration

class Exercise:
    def __init__(self, name: str, equipment: List[str], primary_muscle: MuscleGroup, 
                 secondary_muscles: List[MuscleGroup] = None, calorie_burn_rate: float = 5.0):
        self.name = name
        self.equipment = equipment
        self.primary_muscle = primary_muscle
        self.secondary_muscles = secondary_muscles if secondary_muscles else []
        self.calorie_burn_rate = calorie_burn_rate  # Base MET value

class ExerciseSession:
    def __init__(self, exercise: Exercise, goal: FitnessGoal):
        self.exercise = exercise
        self.goal = goal
        self.reps, self.sets, self.duration = self._assign_work_parameters()
        self.calories = self._calculate_calories()

    def _assign_work_parameters(self) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        if self.exercise.primary_muscle == MuscleGroup.CARDIO:
            reps, sets = None, None
            if self.goal == FitnessGoal.STRENGTH:
                duration = 20  # HIIT style
            elif self.goal == FitnessGoal.HYPERTROPHY:
                duration = 30  # Moderate
            else:  # ENDURANCE
                duration = 45  # Long steady
            return reps, sets, duration
        else:
            duration = None
            if self.goal == FitnessGoal.STRENGTH:
                reps = random.randint(4, 6)
                sets = random.randint(2, 4)  # Limit sets to a maximum of 4
            elif self.goal == FitnessGoal.HYPERTROPHY:
                reps = random.randint(8, 12)
                sets = random.randint(2, 3)  # Limit sets to a maximum of 3
            else:  # ENDURANCE
                reps = random.randint(15, 20)
                sets = 2  # Fixed sets for endurance
            return reps, sets, duration

    def _calculate_calories(self) -> float:
        if self.exercise.primary_muscle == MuscleGroup.CARDIO:
            return self.duration * self.exercise.calorie_burn_rate
        else:
            # Calculate time-based calories for strength training
            if self.goal == FitnessGoal.STRENGTH:
                rest = 150  # 2.5 mins
            elif self.goal == FitnessGoal.HYPERTROPHY:
                rest = 90   # 1.5 mins
            else:           # ENDURANCE
                rest = 45   # 0.75 mins
            total_time = (self.reps * 5 + rest) * self.sets / 60.0
            return total_time * self.exercise.calorie_burn_rate

class WorkoutDay:
    def __init__(self, day_number: int):
        self.day_number = day_number
        self.sessions: List[ExerciseSession] = []

    def add_session(self, session: ExerciseSession):
        self.sessions.append(session)

    def total_calories(self) -> float:
        return sum(session.calories for session in self.sessions)

    def get_muscle_groups(self) -> List[MuscleGroup]:
        return list({session.exercise.primary_muscle for session in self.sessions})

class WorkoutPlan:
    def __init__(self, days: List[WorkoutDay]):
        self.days = days

    def total_calories(self) -> float:
        return sum(day.total_calories() for day in self.days)

    def get_occurrences_by_muscle(self) -> dict:
        occurrences = {mg: [] for mg in MuscleGroup if mg != MuscleGroup.CARDIO}
        for i, day in enumerate(self.days):
            for session in day.sessions:
                mg = session.exercise.primary_muscle
                if mg in occurrences:
                    occurrences[mg].append(i)
        return occurrences

# =============================================================================
# EXERCISE DATABASE
# =============================================================================

EXERCISE_DB = [
    # Chest exercises
    Exercise("Barbell Bench Press", ["barbell", "bench"], MuscleGroup.CHEST, [], 6.0),
    Exercise("Push-ups", [], MuscleGroup.CHEST, [MuscleGroup.ARMS, MuscleGroup.SHOULDERS], 3.8),
    Exercise("Dumbbell Flyes", ["dumbbells", "bench"], MuscleGroup.CHEST, [], 5.0),
    Exercise("Incline Push-ups", [], MuscleGroup.CHEST, [MuscleGroup.ARMS], 4.0),
    Exercise("Dumbbell Bench Press", ["dumbbells", "bench"], MuscleGroup.CHEST, [], 5.5),
    Exercise("Chest Dips", ["parallel bars"], MuscleGroup.CHEST, [MuscleGroup.ARMS], 5.0),
    
    # Back exercises
    Exercise("Pull-ups", ["pull-up bar"], MuscleGroup.BACK, [MuscleGroup.ARMS], 5.0),
    Exercise("Bent-over Rows", ["barbell"], MuscleGroup.BACK, [MuscleGroup.ARMS], 5.5),
    Exercise("Lat Pulldowns", ["cable machine"], MuscleGroup.BACK, [MuscleGroup.ARMS], 4.5),
    Exercise("Dumbbell Rows", ["dumbbells"], MuscleGroup.BACK, [MuscleGroup.ARMS], 5.0),
    Exercise("T-Bar Rows", ["barbell"], MuscleGroup.BACK, [], 5.5),
    Exercise("Superman", [], MuscleGroup.BACK, [MuscleGroup.CORE], 3.0),
    
    # Arms exercises
    Exercise("Bicep Curls", ["dumbbells"], MuscleGroup.ARMS, [], 3.0),
    Exercise("Tricep Dips", ["parallel bars"], MuscleGroup.ARMS, [], 4.0),
    Exercise("Hammer Curls", ["dumbbells"], MuscleGroup.ARMS, [], 3.5),
    Exercise("Barbell Curls", ["barbell"], MuscleGroup.ARMS, [], 3.5),
    Exercise("Tricep Extensions", ["dumbbells"], MuscleGroup.ARMS, [], 3.0),
    Exercise("Close-Grip Push-ups", [], MuscleGroup.ARMS, [MuscleGroup.CHEST], 4.0),
    
    # Core exercises
    Exercise("Plank", [], MuscleGroup.CORE, [], 3.0),
    Exercise("Russian Twists", [], MuscleGroup.CORE, [], 4.0),
    Exercise("Hanging Leg Raises", ["pull-up bar"], MuscleGroup.CORE, [], 5.0),
    Exercise("Crunches", [], MuscleGroup.CORE, [], 3.5),
    Exercise("Mountain Climbers", [], MuscleGroup.CORE, [], 6.0),
    Exercise("Dead Bug", [], MuscleGroup.CORE, [], 3.0),
    
    # Legs exercises
    Exercise("Squats", ["barbell"], MuscleGroup.LEGS, [MuscleGroup.CORE], 7.0),
    Exercise("Lunges", ["dumbbells"], MuscleGroup.LEGS, [], 5.5),
    Exercise("Deadlifts", ["barbell"], MuscleGroup.LEGS, [MuscleGroup.BACK], 8.0),
    Exercise("Bodyweight Squats", [], MuscleGroup.LEGS, [MuscleGroup.CORE], 5.0),
    Exercise("Bulgarian Split Squats", [], MuscleGroup.LEGS, [], 6.0),
    Exercise("Calf Raises", [], MuscleGroup.LEGS, [], 3.0),
    
    # Shoulders exercises
    Exercise("Overhead Press", ["barbell"], MuscleGroup.SHOULDERS, [MuscleGroup.ARMS], 5.0),
    Exercise("Lateral Raises", ["dumbbells"], MuscleGroup.SHOULDERS, [], 4.0),
    Exercise("Front Raises", ["dumbbells"], MuscleGroup.SHOULDERS, [], 4.0),
    Exercise("Pike Push-ups", [], MuscleGroup.SHOULDERS, [MuscleGroup.ARMS], 4.5),
    Exercise("Rear Delt Flyes", ["dumbbells"], MuscleGroup.SHOULDERS, [], 3.5),
    Exercise("Arnold Press", ["dumbbells"], MuscleGroup.SHOULDERS, [], 5.0),
    
    # Cardio exercises
    Exercise("Running", [], MuscleGroup.CARDIO, [], 10.0),
    Exercise("Cycling", ["stationary bike"], MuscleGroup.CARDIO, [], 8.0),
    Exercise("Jumping Rope", [], MuscleGroup.CARDIO, [], 12.0),
    Exercise("Burpees", [], MuscleGroup.CARDIO, [], 15.0),
    Exercise("High Knees", [], MuscleGroup.CARDIO, [], 8.0),
    Exercise("Jumping Jacks", [], MuscleGroup.CARDIO, [], 7.0)
]

# =============================================================================
# WORKOUT GENERATION SYSTEM (GENETIC ALGORITHM)
# =============================================================================

class WorkoutGenerationSystem:
    def __init__(self):
        self.population_size = 50
        self.generations = 100
        self.mutation_rate = 0.1
        self.hill_climb_iterations = 50  # Number of hill climbing iterations

    def generate_workout_plan(self, user_profile: UserProfile) -> WorkoutPlan:
        population = [self._create_random_plan(user_profile) for _ in range(self.population_size)]
        best_plan = population[0]
        best_fitness = self._fitness_function(best_plan, user_profile)

        for _ in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self._fitness_function(plan, user_profile) for plan in population]
            
            # Track best plan
            max_fitness = max(fitness_scores)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_plan = population[fitness_scores.index(max_fitness)]
            
            # Create new generation
            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self._tournament_select(population, fitness_scores)
                parent2 = self._tournament_select(population, fitness_scores)
                child1, child2 = self._crossover(parent1, parent2)
                new_population.append(self._mutate(child1, user_profile))
                new_population.append(self._mutate(child2, user_profile))
            
            population = new_population
        
        # Apply hill climbing to refine best plan found by GA
        refined_plan = self._hill_climbing(best_plan, user_profile)
        return refined_plan

    def _hill_climbing(self, plan: WorkoutPlan, user_profile: UserProfile) -> WorkoutPlan:
        current_plan = plan
        current_score = self._fitness_function(current_plan, user_profile)

        for _ in range(self.hill_climb_iterations):
            # Make a small local modification
            neighbor_plan = self._local_modify(current_plan, user_profile)

            # Evaluate new plan's fitness
            neighbor_score = self._fitness_function(neighbor_plan, user_profile)

            # Accept new plan if it improves fitness
            if neighbor_score > current_score:
                current_plan = neighbor_plan
                current_score = neighbor_score

        return current_plan

    def _local_modify(self, plan: WorkoutPlan, user_profile: UserProfile) -> WorkoutPlan:
        # Make a copy of the plan to modify
        import copy
        new_days = []
        for day in plan.days:
            new_day = WorkoutDay(day.day_number)
            new_day.sessions = [ExerciseSession(s.exercise, user_profile.goal) for s in day.sessions]
            for s_old, s_new in zip(day.sessions, new_day.sessions):
                s_new.reps = s_old.reps
                s_new.sets = s_old.sets
                s_new.duration = s_old.duration
                s_new.calories = s_old.calories
            new_days.append(new_day)
        new_plan = WorkoutPlan(new_days)

        # Randomly select a day to modify
        if not new_plan.days:
            return new_plan
        day = random.choice(new_plan.days)
        if not day.sessions:
            return new_plan

        # Randomly choose modification type: swap exercise or change sets/reps (if possible)
        modification_type = random.choice(["swap", "adjust_sets"])

        if modification_type == "swap":
            # Swap an exercise in this day with another valid exercise not already in the day
            session_idx = random.randint(0, len(day.sessions) - 1)
            old_session = day.sessions[session_idx]
            mg = old_session.exercise.primary_muscle
            valid_exercises = self._get_valid_exercises(mg, user_profile.equipment)
            existing_names = {s.exercise.name for s in day.sessions}
            unused_exercises = [e for e in valid_exercises if e.name not in existing_names]
            if unused_exercises:
                new_exercise = random.choice(unused_exercises)
                new_session = ExerciseSession(new_exercise, user_profile.goal)
                day.sessions[session_idx] = new_session

        elif modification_type == "adjust_sets":
            # Increase or decrease sets or duration for a random session if possible
            session = random.choice(day.sessions)
            if session.sets is not None:
                # Modify sets randomly +-1 with boundaries (min 1, max 10)
                change = random.choice([-1, 1])
                new_sets = max(1, min(10, session.sets + change))
                if new_sets != session.sets:
                    session.sets = new_sets
                    session.calories = session._calculate_calories()
            elif session.duration is not None:
                # Modify duration randomly +-5 minutes (min 5, max 90)
                change = random.choice([-5, 5])
                new_duration = max(5, min(90, session.duration + change))
                if new_duration != session.duration:
                    session.duration = new_duration
                    session.calories = session._calculate_calories()

        return new_plan

    def _create_random_plan(self, user_profile: UserProfile) -> WorkoutPlan:
        num_days = user_profile.available_days
        muscle_groups_per_day = self._get_muscle_group_split(num_days)
        days = []
        
        for i, muscle_groups in enumerate(muscle_groups_per_day):
            day = WorkoutDay(i + 1)
            
            # Add 4 exercises per muscle group (minimum)
            for mg in muscle_groups:
                valid_exercises = self._get_valid_exercises(mg, user_profile.equipment)
                if valid_exercises:
                    # Select 4 unique exercises for this muscle group
                    exercises_count = min(4, len(valid_exercises))
                    selected_exercises = random.sample(valid_exercises, exercises_count)
                    
                    for exercise in selected_exercises:
                        session = ExerciseSession(exercise, user_profile.goal)
                        self._add_or_combine_session(day, session)
            
            # If we don't have at least 8 exercises, add more unique ones
            while len(day.sessions) < 8:
                added_exercise = False
                for mg in muscle_groups:
                    if len(day.sessions) >= 8:
                        break
                    valid_exercises = self._get_valid_exercises(mg, user_profile.equipment)
                    # Get exercises not already in the day
                    existing_exercise_names = {s.exercise.name for s in day.sessions}
                    unused_exercises = [e for e in valid_exercises if e.name not in existing_exercise_names]
                    
                    if unused_exercises:
                        exercise = random.choice(unused_exercises)
                        session = ExerciseSession(exercise, user_profile.goal)
                        self._add_or_combine_session(day, session)
                        added_exercise = True
                
                # If no new unique exercises can be added, break to avoid infinite loop
                if not added_exercise:
                    break
            
            # If we have a calorie goal, add more sets to existing exercises
            if user_profile.session_duration:
                target_daily_calories = user_profile.session_duration / num_days
                while day.total_calories() < target_daily_calories * 0.8:  # 80% of target
                    # Instead of adding new exercises, increase sets of existing ones
                    if day.sessions:
                        session_to_boost = random.choice(day.sessions)
                        if session_to_boost.sets:  # Only for non-cardio exercises
                            session_to_boost.sets += 1
                            session_to_boost.calories = session_to_boost._calculate_calories()
                    else:
                        break
            
            days.append(day)
        
        # Ensure cardio is included
        plan = WorkoutPlan(days)
        if not self._has_cardio(plan):
            self._add_cardio(plan, user_profile)
        
        return plan

    def _add_or_combine_session(self, day: WorkoutDay, new_session: ExerciseSession):
        """Add a session to the day, or combine with existing session if same exercise"""
        # Check if this exercise already exists in the day
        for existing_session in day.sessions:
            if existing_session.exercise.name == new_session.exercise.name:
                # Combine the sessions by adding sets
                if existing_session.sets and new_session.sets:
                    existing_session.sets += new_session.sets
                    existing_session.calories = existing_session._calculate_calories()
                elif existing_session.duration and new_session.duration:
                    existing_session.duration += new_session.duration
                    existing_session.calories = existing_session._calculate_calories()
                return
        
        # If exercise doesn't exist, add new session
        day.add_session(new_session)

    def _get_muscle_group_split(self, num_days: int) -> List[List[MuscleGroup]]:
        if num_days == 1:
            return [[MuscleGroup.CHEST, MuscleGroup.BACK, MuscleGroup.LEGS, MuscleGroup.CARDIO]]
        elif num_days == 2:
            return [
                [MuscleGroup.CHEST, MuscleGroup.BACK, MuscleGroup.SHOULDERS],
                [MuscleGroup.LEGS, MuscleGroup.ARMS, MuscleGroup.CORE, MuscleGroup.CARDIO]
            ]
        elif num_days == 3:
            return [
                [MuscleGroup.CHEST, MuscleGroup.BACK],
                [MuscleGroup.LEGS, MuscleGroup.SHOULDERS],
                [MuscleGroup.ARMS, MuscleGroup.CORE, MuscleGroup.CARDIO]
            ]
        elif num_days == 4:
            return [
                [MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
                [MuscleGroup.BACK, MuscleGroup.ARMS],
                [MuscleGroup.LEGS, MuscleGroup.CORE],
                [MuscleGroup.CARDIO]
            ]
        else:  # 5+ days
            base_pattern = [
                [MuscleGroup.CHEST],
                [MuscleGroup.BACK],
                [MuscleGroup.LEGS],
                [MuscleGroup.SHOULDERS, MuscleGroup.ARMS],
                [MuscleGroup.CORE, MuscleGroup.CARDIO]
            ]
            result = []
            for i in range(num_days):
                result.append(base_pattern[i % len(base_pattern)])
            return result

    def _get_valid_exercises(self, muscle_group: MuscleGroup, 
                             user_equipment: List[str]) -> List[Exercise]:
        valid_exercises = []
        for exercise in EXERCISE_DB:
            if exercise.primary_muscle != muscle_group:
                continue
            
            # Check if user has all required equipment for this exercise
            if all((eq == "" or eq in user_equipment) for eq in exercise.equipment):
                valid_exercises.append(exercise)
            # Also include exercises that require no equipment
            elif not exercise.equipment:
                valid_exercises.append(exercise)
        
        # If no valid exercises found, return bodyweight exercises for that muscle group
        if not valid_exercises:
            bodyweight_exercises = [e for e in EXERCISE_DB 
                                  if e.primary_muscle == muscle_group and not e.equipment]
            return bodyweight_exercises
        
        return valid_exercises

    def _has_cardio(self, plan: WorkoutPlan) -> bool:
        for day in plan.days:
            for session in day.sessions:
                if session.exercise.primary_muscle == MuscleGroup.CARDIO:
                    return True
        return False

    def _add_cardio(self, plan: WorkoutPlan, user_profile: UserProfile):
        cardio_exercises = self._get_valid_exercises(MuscleGroup.CARDIO, user_profile.equipment)
        if not cardio_exercises:
            return
        
        day_idx = random.randint(0, len(plan.days) - 1)
        for _ in range(2):  # Add 2 cardio exercises
            session = ExerciseSession(random.choice(cardio_exercises), user_profile.goal)
            plan.days[day_idx].add_session(session)

    def _fitness_function(self, plan: WorkoutPlan, user_profile: UserProfile) -> float:
        score = 0
        
        # 1. Equipment compatibility - heavily penalize incompatible equipment
        for day in plan.days:
            for session in day.sessions:
                for eq in session.exercise.equipment:
                    if eq and eq not in user_profile.equipment:
                        score -= 50
        
        # 2. Recovery spacing
        muscle_occurrences = plan.get_occurrences_by_muscle()
        for muscle, days in muscle_occurrences.items():
            days.sort()
            for i in range(1, len(days)):
                if days[i] - days[i-1] == 1:
                    score -= 15
        
        # 3. Cardio inclusion
        if self._has_cardio(plan):
            score += 30
        else:
            score -= 100
        
        # 4. Minimum exercises per day
        for day in plan.days:
            if len(day.sessions) < 8:
                score -= (8 - len(day.sessions)) * 10
            else:
                score += 20
        
        # 5. Calorie goal alignment
        if user_profile.session_duration:
            total_cals = plan.total_calories()
            deviation = abs(total_cals - user_profile.session_duration) / user_profile.session_duration
            if deviation > 0.2:
                score -= 100 * deviation
            elif deviation < 0.1:
                score += 50
        
        return score

    def _tournament_select(self, population: List[WorkoutPlan], 
                           fitness_scores: List[float], size: int = 3) -> WorkoutPlan:
        selected = random.sample(list(zip(population, fitness_scores)), size)
        return max(selected, key=lambda x: x[1])[0]

    def _crossover(self, parent1: WorkoutPlan, parent2: WorkoutPlan) -> Tuple[WorkoutPlan, WorkoutPlan]:
        if len(parent1.days) <= 1:
            return parent1, parent2
        
        crossover_point = random.randint(1, len(parent1.days) - 1)
        child1_days = parent1.days[:crossover_point] + parent2.days[crossover_point:]
        child2_days = parent2.days[:crossover_point] + parent1.days[crossover_point:]
        return WorkoutPlan(child1_days), WorkoutPlan(child2_days)

    def _mutate(self, plan: WorkoutPlan, user_profile: UserProfile) -> WorkoutPlan:
        if random.random() < self.mutation_rate and plan.days:
            day_idx = random.randint(0, len(plan.days) - 1)
            day = plan.days[day_idx]
            
            if day.sessions:
                session_idx = random.randint(0, len(day.sessions) - 1)
                old_session = day.sessions[session_idx]
                mg = old_session.exercise.primary_muscle
                
                valid_exercises = self._get_valid_exercises(mg, user_profile.equipment)
                existing_names = {s.exercise.name for s in day.sessions if s != old_session}
                unused_exercises = [e for e in valid_exercises if e.name not in existing_names]
                
                if unused_exercises:
                    new_exercise = random.choice(unused_exercises)
                    day.sessions[session_idx] = ExerciseSession(new_exercise, user_profile.goal)
        
        return plan

# =============================================================================
# SERIALIZATION AND UTILITIES
# =============================================================================

def serialize_workout_plan(plan: WorkoutPlan) -> dict:
    week_plan = []
    for day in plan.days:
        exercises = []
        for session in day.sessions:
            ex = {
                "name": session.exercise.name,
                "equipment": session.exercise.equipment,
                "primary_muscle": session.exercise.primary_muscle.value,
                "calories": round(session.calories, 2)
            }
            if session.reps and session.sets:
                ex.update({
                    "reps": session.reps,
                    "sets": session.sets
                })
            else:
                ex["duration_minutes"] = session.duration
            exercises.append(ex)
        
        week_plan.append({
            "day_number": day.day_number,
            "muscle_groups": [mg.value for mg in day.get_muscle_groups()],
            "exercises": exercises,
            "total_calories": round(day.total_calories(), 2)
        })
    
    return {
        "weekly_plan": week_plan,
        "total_weekly_calories": round(plan.total_calories(), 2),
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

# =============================================================================
# MAIN FUNCTION TO INTERACT WITH DATABASE
# =============================================================================

def main(user_id: str):
    import sys
    result = {"status": "success", "data": None, "error": None}
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['workoutdb']
        users_col = db['userprofiles']

        # Validate user_id
        if len(user_id) != 24:
            result["status"] = "error"
            result["error"] = "Invalid user ID format: must be 24 characters long."
            print(json.dumps(result, cls=CustomEncoder))
            sys.stdout.flush()
            return

        try:
            user_object_id = ObjectId(user_id)
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Invalid user ID format: {str(e)}"
            print(json.dumps(result, cls=CustomEncoder))
            sys.stdout.flush()
            return

        user_doc = users_col.find_one({"_id": user_object_id})
        if not user_doc:
            result["status"] = "error"
            result["error"] = "User not found"
            print(json.dumps(result, cls=CustomEncoder))
            sys.stdout.flush()
            return

        try:
            user_profile = UserProfile(
                fitness_level=FitnessLevel[user_doc['fitnessLevel'].upper().replace(' ', '_')],
                goal=FitnessGoal[user_doc['goal'].upper().replace(' ', '_')],
                available_days=user_doc['availableDays'],
                equipment=[eq.lower() for eq in user_doc.get('equipment', [])],
                session_duration=user_doc.get('sessionDuration')
            )
        except KeyError as e:
            result["status"] = "error"
            result["error"] = f"Missing field in user profile: {str(e)}"
            print(json.dumps(result, cls=CustomEncoder))
            sys.stdout.flush()
            return
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Error processing user profile: {str(e)}"
            print(json.dumps(result, cls=CustomEncoder))
            sys.stdout.flush()
            return

        system = WorkoutGenerationSystem()
        plan = system.generate_workout_plan(user_profile)

        serialized_plan = serialize_workout_plan(plan)

        # Save generated plan to the user document
        users_col.update_one({"_id": user_object_id}, {"$set": {"workoutPlan": serialized_plan}})

        result["data"] = serialized_plan
        print(json.dumps(result, cls=CustomEncoder))
        sys.stdout.flush()

    except Exception as e:
        result["status"] = "error"
        result["error"] = f"Unexpected error: {str(e)}"
        print(json.dumps(result, cls=CustomEncoder))
        sys.stdout.flush()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        result = {"status": "error", "data": None, "error": "Usage: python workout_ai.py <user_id>"}
        print(json.dumps(result, cls=CustomEncoder))
        sys.stdout.flush()
        sys.exit(1)
    main(sys.argv[1])
