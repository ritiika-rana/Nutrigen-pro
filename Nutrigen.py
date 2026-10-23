import streamlit as st
import plotly.graph_objects as go
import random

# ================= PAGE CONFIG & CSS =================
st.set_page_config(page_title="NutriGen Pro | AI Diet Planner", page_icon="🍏", layout="wide")

st.markdown("""
    <style>
    .legend-box { display: inline-block; padding: 2px 8px; border-radius: 4px; color: white; font-weight: bold; margin-right: 8px; margin-bottom: 5px; font-size: 13px;}
    .underweight { background-color: #3498db; }
    .normal { background-color: #2ecc71; }
    .overweight { background-color: #f1c40f; color: black; }
    .obese { background-color: #e74c3c; }
    </style>
""", unsafe_allow_html=True)

# Session States for Smart History
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False
if "plan_history" not in st.session_state:
    st.session_state.plan_history = []

# ================= SIDEBAR INPUTS =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966334.png", width=60)
    st.header("⚙️ Smart Profile Setup")
    
    user_name = st.text_input("Full Name", placeholder="e.g. Ritika")
    
    st.divider()
    st.subheader("📏 Body Metrics")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 10, 100, 18)
        weight = st.number_input("Weight (kg)", 20.0, 150.0, 39.0)
    with col2:
        gender = st.selectbox("Gender", ["Female", "Male"])
        height = st.number_input("Height (cm)", 100.0, 250.0, 162.0)
    
    st.divider()
    st.subheader("🎯 Goals & Lifestyle")
    goal = st.selectbox("Fitness Goal", ["Weight Gain", "Weight Loss", "Maintain Fitness"])
    diet_type = st.selectbox("Diet Preference", ["Pure Vegetarian", "Non-Vegetarian", "Vegan"])
    activity_level = st.selectbox("Daily Activity", [
        "Sedentary (Sitting/Studying)",
        "Lightly Active (Walking/Chores)",
        "Moderately Active (Daily Exercise)",
        "Very Active (Heavy Workout)"
    ])
    
    st.subheader("💰 Budget & Health Constraints")
    budget = st.slider("Daily Budget (₹)", 100, 2000, 250, 50)
    allergies = st.text_input("Any Food Allergies?", placeholder="e.g. Peanut, Milk, Soy")
    
    out_lang = st.selectbox("Explanation Language", ["Professional English", "Simple English", "Hinglish"])
    
    generate_btn = st.button("🚀 Generate Smart Plan", use_container_width=True)

# ================= MAIN SCREEN OUTPUT =================
st.title("🍏 NutriGen Pro: Advanced AI Engine")
st.markdown("Your scientifically calculated diet & workout plan tailored to your budget and body.")
st.divider()

if height > 0 and weight > 0:
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
    activity_multiplier = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    activity_key = activity_level.split(" (")[0]
    tdee = bmr * activity_multiplier.get(activity_key, 1.2)
    
    if goal == "Weight Gain":
        target_calories = tdee + 500
    elif goal == "Weight Loss":
        target_calories = tdee - 500
    else:
        target_calories = tdee

# Budget Tier Logic (1 = Low, 2 = Medium, 3 = High)
if budget <= 300:
    user_budget_tier = 1
elif budget <= 800:
    user_budget_tier = 2
else:
    user_budget_tier = 3

# ================= GENERATION & WARNING LOGIC =================
if generate_btn:
    if bmi >= 25.0 and goal == "Weight Gain":
        st.error("⚠️ **Medical Alert:** Your BMI indicates you are Overweight/Obese. Gaining more weight is NOT recommended. Please select 'Weight Loss' or consult a doctor.")
        st.session_state.show_dashboard = False
    elif bmi < 18.5 and goal == "Weight Loss":
        st.error("⚠️ **Medical Alert:** Your BMI indicates you are Underweight. Losing more weight is NOT recommended. Please select 'Weight Gain' or consult a doctor.")
        st.session_state.show_dashboard = False
    else:
        st.toast("Scientific Plan Generated Successfully!", icon="✅")
        st.session_state.show_dashboard = True
        st.session_state.plan_history = [0]

# ================= DASHBOARD RENDERING =================
if st.session_state.show_dashboard:
    st.header(f"📊 Dashboard for {user_name if user_name else 'User'}")
    
    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c1:
        fig_bmi = go.Figure(go.Indicator(
            mode="gauge+number", value=bmi,
            title={'text': "Body Mass Index (BMI)", 'font': {'size': 16}},
            gauge={'axis': {'range': [10, 40]}, 'bar': {'color': "rgba(0,0,0,0.3)"},
                   'steps': [{'range': [10, 18.5], 'color': "#3498db"}, {'range': [18.5, 24.9], 'color': "#2ecc71"}, 
                             {'range': [25, 29.9], 'color': "#f1c40f"}, {'range': [30, 40], 'color': "#e74c3c"}]}
        ))
        fig_bmi.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_bmi, use_container_width=True)
        
    with c2:
        st.markdown(f"<div style='text-align: center; margin-top: 10px;'><b>Target Calories:</b> <span style='color:#2ecc71; font-size:18px;'>{int(target_calories)} kcal</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'><b>Daily Budget:</b> ₹{budget}</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='margin-top: 15px; text-align: center;'>
            <span class='legend-box underweight'>🟦 < 18.5</span> <span style='font-size:12px;'>Underweight</span><br>
            <span class='legend-box normal'>🟩 18.5-24.9</span> <span style='font-size:12px;'>Normal</span><br>
            <span class='legend-box overweight'>🟨 25.0-29.9</span> <span style='font-size:12px;'>Overweight</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        macros = ['Carbs', 'Protein', 'Fats']
        values = [target_calories*0.5, target_calories*0.3, target_calories*0.2]
        fig_macros = go.Figure(data=[go.Pie(labels=macros, values=values, hole=.6, marker_colors=['#ff9999','#66b3ff','#99ff99'], textinfo='label+percent', textposition='outside')])
        fig_macros.update_layout(height=260, margin=dict(l=30, r=30, t=40, b=10), showlegend=False, title={'text': "Macronutrients", 'y':0.95, 'x':0.5, 'xanchor': 'center'})
        st.plotly_chart(fig_macros, use_container_width=True)
    
    st.divider()
    
    # 🥗 Dynamic Food Database with Budget Tiers (Food, Reason, Budget_Level 1-3)
    veg_meals_detailed = {
        "Early Morning": [
            ("Warm Water with Lemon & Honey", "Detoxifies body cheaply.", 1),
            ("Jeera Water + 2 Dates", "Improves digestion; Dates give an instant energy boost.", 1),
            ("Warm Water + 5 Soaked Almonds & Walnuts", "Premium healthy fats for brain function.", 2),
            ("Matcha Green Tea + Pumpkin Seeds", "Rich antioxidants and premium metabolism boost.", 3),
            ("Aloe Vera Juice + 1 Fig (Anjeer)", "Boosts immunity and clears digestive tract.", 2)
        ],
        "Breakfast": [
            ("Poha with Peanuts & Green Peas", "Complex carbs for sustained energy in low budget.", 1),
            ("2 Moong Dal Chillas + Green Chutney", "Moong dal is a cheap and easily digestible protein.", 1),
            ("2 Paneer Parathas + Curd + 1 Apple", "High protein from Paneer builds muscle.", 2),
            ("Avocado Toast on Sourdough + Greek Yogurt", "Premium healthy fats and probiotics.", 3),
            ("Big bowl of Oats with Almond Milk, Chia Seeds & Berries", "High-fiber premium breakfast.", 3)
        ],
        "Mid-Morning": [
            ("1 Fresh Banana or Watermelon", "Hydrates the body and gives instant energy.", 1),
            ("Roasted Chana (Handful)", "Chana gives a great protein punch.", 1),
            ("1 Glass Buttermilk (Chaas) + Flax seeds", "Cools the stomach; Flax seeds provide Omega-3.", 2),
            ("Fresh Pressed Pomegranate Juice", "High Vitamin C for immunity and blood flow.", 3)
        ],
        "Lunch": [
            ("1 Bowl Dal, 2 Roti, 1 Cup Rice, Mix Veg Sabzi", "Complete amino acid profile (Dal+Rice).", 1),
            ("Kala Chana (Black Chickpeas) Curry + Rice", "High fiber and iron content.", 1),
            ("Soya Chunks Curry + 2 Multigrain Roti + Curd", "Soya is the highest vegetarian protein source.", 2),
            ("Palak Paneer + 2 Roti + Raita", "Spinach provides iron, Paneer provides premium protein.", 2),
            ("Quinoa Salad with Roasted Tofu & Olive Oil", "Superfood carbs and clean vegan protein.", 3)
        ],
        "Evening Snack": [
            ("Handful of Peanuts + Jaggery (Gur)", "Classic budget combo that boosts hemoglobin.", 1),
            ("Boiled Sweet Potato Chaat", "Excellent source of Vitamin A.", 1),
            ("Makhana (Fox nuts) roasted in Ghee + Green Tea", "Makhana is rich in calcium.", 2),
            ("Protein Smoothie (Whey/Plant Protein) with Almonds", "Fast-absorbing premium muscle recovery.", 3)
        ],
        "Dinner": [
            ("Light Vegetable Khichdi + 1 Spoon Ghee", "Ultimate comfort food, very easy to digest.", 1),
            ("Bottle Gourd (Lauki) Sabzi + 2 Jowar Roti", "Extremely low calorie and hydrating.", 1),
            ("Tofu Bhurji + 2 Roti + Tomato Soup", "Light on the stomach; Tofu provides clean protein.", 2),
            ("Paneer Tikka (Home made) + Sautéed Broccoli", "Slow-digesting casein protein repairs muscles.", 3),
            ("Zucchini Noodles with Pesto & Roasted Tempeh", "Gourmet premium dinner for low-carb diets.", 3)
        ]
    }

    # 🏋️‍♂️ Exercise Database
    workouts = {
        "Weight Gain": [
            "1. **Warmup:** 5 mins dynamic stretching.",
            "2. **Strength Training:** Push-ups, Squats, and Lunges (4 sets of 12 reps).",
            "3. **Heavy Lifts:** Dumbbell rows or Pull-ups (Focus on muscle hypertrophy).",
            "4. **Rest:** Sleep 8 hours for muscle recovery."
        ],
        "Weight Loss": [
            "1. **Cardio:** 15 mins Brisk Walking or Jogging.",
            "2. **HIIT:** Jumping Jacks, Burpees, and High Knees (30 secs work, 15 secs rest).",
            "3. **Core:** Planks (3 sets of 45 secs) & Crunches.",
            "4. **Consistency:** Aim for 10,000 steps daily."
        ],
        "Maintain Fitness": [
            "1. **Flexibility:** 15 mins Yoga (Surya Namaskar).",
            "2. **Balance:** Bodyweight Squats & Light Push-ups.",
            "3. **Cardio:** Cycling or Swimming for 20 mins.",
            "4. **Active Lifestyle:** Take stairs instead of elevators."
        ]
    }

    # Format user allergy input
    allergy_list = [a.strip().lower() for a in allergies.split(",")] if allergies else []

    if allergy_list:
        st.warning(f"⚠️ Filtering out items containing: {', '.join(allergy_list)}")

    # ================= HISTORY RENDERING =================
    st.markdown("---")
    
    for index, variant in enumerate(st.session_state.plan_history):
        st.markdown(f"### 📋 {goal} Plan - Option {index + 1} (₹{budget} Budget)")
        
        table_data = []
        for meal_time in ["Early Morning", "Breakfast", "Mid-Morning", "Lunch", "Evening Snack", "Dinner"]:
            
            # Filter meals based on Budget and Allergies
            valid_options = []
            for food, reason, cost in veg_meals_detailed[meal_time]:
                if cost <= user_budget_tier:
                    # Check allergy
                    is_safe = True
                    for al in allergy_list:
                        if al in food.lower() or al in reason.lower():
                            is_safe = False
                            break
                    if is_safe:
                        valid_options.append((food, reason))
            
            # Fallback if allergies remove all options
            if not valid_options:
                valid_options = [("Custom Safe Meal", "Filtered due to strict budget/allergies. Consult doctor.")]
            
            # Smart Selection
            selected_index = variant % len(valid_options)
            food, reason = valid_options[selected_index]
            
            if out_lang == "Hinglish":
                reason = reason.replace("muscle", "maspeshiyon").replace("digestion", "pachan").replace("energy", "taqat")
            elif out_lang == "Simple English":
                reason = reason.replace("Antioxidant-rich", "Good for health").replace("Complex carbs", "Good carbs").replace("amino acid profile", "protein mix")
                
            table_data.append({"Meal Time": meal_time, "Recommended Food": food, "🔬 [WHY?] Explanation": reason})
        
        st.table(table_data)

    st.markdown("### 🔄 Not Satisfied?")
    if st.button("➕ Generate Another Option to Compare", type="primary"):
        st.session_state.plan_history.append(st.session_state.plan_history[-1] + 1)
        st.rerun()

    # ================= EXERCISE SECTION =================
    st.markdown("---")
    st.header("🏋️‍♂️ Recommended Daily Workout")
    st.info(f"Based on your goal: **{goal}** and **{activity_key}** lifestyle, here is your customized routine:")
    
    col_ex1, col_ex2 = st.columns([2, 1])
    with col_ex1:
        for step in workouts[goal]:
            st.markdown(step)
    with col_ex2:
        st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=120)