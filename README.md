 Rocket Landing Prediction Project
Capstone project for IBM Data Science Professional Certificate
Goal: Predict the successful landing of SpaceX Falcon 9’s First Stage using historical launch data.

 Problem Statement
Reusing rocket boosters greatly reduces the cost of space flight.
The objective of this project is to build a classification model that predicts whether the Falcon 9 first stage will land successfully, using launch and rocket performance parameters.

📊 Dataset
Data collected from the SpaceX API + Web scraping (Wikipedia launch data).
Key features:
Launch site
Payload mass (kg)
Flight orbit
Booster version
Number of flights
Block type
Success indicator (binary target: 1 = Landed Successfully, 0 = Failed).
 Workflow
 
Data Collection

Web scraping (Wikipedia) + SpaceX REST API.
Data Wrangling & Cleaning

Handling null values, feature engineering, categorical encoding.
Exploratory Data Analysis (EDA)

Visualized payload vs landing rates, orbit vs success probabilities, launch site performance.
Modeling (Classification)

Logistic Regression
Support Vector Machines (SVM)
Decision Tree Classifier
Random Forest / XGBoost
Evaluation

Metrics: Accuracy, Precision, Recall, F1-score.
Confusion matrices for all models.
Hyperparameter tuning (GridSearchCV).

 Results
Best Model: [Logistic Regression/SVM].
Accuracy: 83%
Precision/Recall/F1: Reported and compared across models.
Insights: Payload and Orbit were major predictors of landing success.

 Visualization / Dashboard
Developed an interactive dashboard with Plotly Dash to visualize launch site performance and orbit trends.

 Key Learnings
Built an end-to-end binary classification pipeline.
Applied multiple ML models and compared results.
Gained understanding of how feature engineering and tuning improve prediction accuracy.

 Repository Structure
├── dataset_part_1.csv              # Raw dataset
├── edadataviz.ipynb                # Exploratory Data Analysis
├── SpaceX_Machine_Learning_Prediction_Part_5.ipynb  # Modeling
├── jupyter-labs-spacex-data-collection-api.ipynb    # Data collection
├── jupyter-labs-webscraping.ipynb  # Web scraping
├── spacex-dash-app.py              # Visualization dashboard
└── README.md                       # Project documentation
