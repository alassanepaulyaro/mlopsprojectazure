### MLOPS project with Azure and AWS

#### Overview
This application is a Student Exam Performance Indicator. It allows users to input various student information such as gender, ethnicity, parental education level, lunch type, test preparation course, and scores in reading and writing. Using this data, the application predicts the Math Score for the student.
The code consists of several components that together form a Machine Learning pipeline and a Flask web application interface.
________________________________________
#### Major Components
1.	Data Ingestion
- Classes:
    - DataIngestionConfig: Specifies file paths for training data, test data, and raw data.
    - DataIngestion: Reads CSV data (from stud.csv), splits it into training and testing sets, and saves the resultant files.
- Process:
    - Reads the dataset into a Pandas DataFrame.
    - Splits the dataset (80/20) into training and testing.
    - Saves the train/test CSV files into artifact directories.

2. Data Transformation

- Classes:
    - DataTransformationConfig: Holds the file path for the preprocessor object.
    - DataTransformation: Creates transformation pipelines for both numerical and categorical columns.

- Pipelines:
    - Numerical Pipeline:
        1.	Imputes missing values with the median strategy.
        2.	Scales the features using StandardScaler.

    - Categorical Pipeline:
        1.	Imputes missing values using the most frequent value strategy.
        2.	Applies one-hot encoding to categorical features.
        3.	Scales the resulting one-hot features with StandardScaler (with with_mean=False).

- Process:
    - Combines the numerical and categorical pipelines into a ColumnTransformer.
    - Fits the preprocessor on the training set and transforms both train and test sets.
    - Saves the final preprocessor object as preprocessor.pkl.

3.	Model Training
- Classes:
    - ModelTrainerConfig: Specifies the file path to save the trained model.
    - ModelTrainer: Manages the training and evaluation of multiple regression models.
    - Models Used:
    - Random Forest
    - Decision Tree
    - Gradient Boosting
    - Linear Regression
    - XGBRegressor
    - CatBoost Regressor
    - AdaBoost Regressor

- Hyperparameter Tuning:
    - A custom approach is used:
    - For most models, GridSearchCV is applied with specified parameter grids.
    - For XGBoost and CatBoost, a manual parameter search is performed.

- Evaluation:
    - r2_score is used to measure model performance on the test set.
    - The best-performing model (highest r2_score) is saved as model.pkl.

4.	Prediction Pipeline
- Classes:
    - PredictPipeline: Loads the trained model (model.pkl) and the saved preprocessor (preprocessor.pkl), then transforms new feature data and predicts the math score.
    - CustomData: A utility class to convert user input into a Pandas DataFrame for prediction.

5.	Exception Handling & Utilities
- Classes:
    - CustomException: A custom exception class that neatly formats and logs error messages.

- Functions:
    - error_message_detail(error, error_detail): Creates a detailed error message.
    - save_object(file_path, obj): Saves Python objects (the model and preprocessor) in pickle format.
    - load_object(file_path): Loads the saved pickle objects.
    - evaluate_models(...): Evaluates and tunes the given models, returning a performance report.

6.	Flask Application
- Setup:
    - The Flask app is created with app=Flask(__name__).
- Routes:
    - 	/: Renders index.html as the homepage.
    - 	/predictdata: A GET/POST route that:
        1.	Displays an HTML form for user input (GET).
        2.	Processes form submissions to predict the math score (POST).
- Templates:
    - home.html: Displays the input form and shows the predicted math score.
    - index.html: The main landing page.
________________________________________
#### Application Flow
1.	User visits the app at "/", seeing a simple homepage.
2.	User navigates to "/predictdata", fills out the student information form.
3.	When the form is submitted:
    - The data is collected and transformed into a DataFrame by CustomData.
    - The PredictPipeline loads both the saved preprocessor and model.
    - The preprocessor transforms the user input.
    - The model predicts the student’s Math Score.
    - The result is displayed on the page.
________________________________________
#### Purpose and Usage
This application demonstrates a full machine learning solution pipeline:
1.	Data ingestion and preparation from CSV files.
2.	Data cleaning and transformation through scikit-learn pipelines.
3.	Model selection and training (with hyperparameter tuning).
4.	Deployment via a Flask web app, allowing end-users to input their details and receive real-time predictions of math scores.

________________________________________

#### Step to Build the Application
- Create a new environment: $ conda create -p venv python==3.12.7 -y
- Activate the environment: $ conda activate venv/
- Install required packages: $ pip install -r requirements.txt
- Run the data ingestion script: $ python src/component/data_ingestion.py

#### Step to Run the Flask Application
- Run the Flask application: $ python app.py
- Access the home page: http://127.0.0.1:5000
- Access the predict page: http://127.0.0.1:5000/predictdata/


=====================================

#### Deployment on Azure
- Step 1: Create a New Azure Container Registry
    1. In the Azure Portal, create a new Container Registry.

        - Name: mlopsprojectdocker (example)
        - Resource Group: (select or create one)
        - SKU: (choose an appropriate tier, e.g., Basic or Standard)

    2. After creation, open your container registry and navigate to Settings → Access Keys.

        - Enable Admin user.
        - Copy the Login server (e.g., mlopsprojectdocker.azurecr.io) and the password.

- Step 2: Build and Push Your Docker Image
    Prerequisite: You have a Dockerfile in your project’s root directory.

    1. In your local project terminal, build the Docker image:
    > docker build -t mlopsprojectdocker.azurecr.io/mltest:latest .

    2. Log in to your Azure Container Registry:
    > docker login mlopsprojectdocker.azurecr.io
    
    Use the username mlopsprojectdocker (or the one you copied from the Portal, if different) and the password from Access Keys.

    3. Push the Docker image to your Azure Container Registry:

    > docker push mlopsprojectdocker.azurecr.io/mltest:latest

- Step 3: Create an Azure Web App
    1. In the Azure Portal, go to All resources.
    2. Select Create → Web App:
        - Name: mlopsproject (example)
        - Publish: Container
        - Operating System: Linux
        - Region: (choose the appropriate region for your needs)
        - Plan: (select or create an App Service plan)

    3. In the Configuration or Container settings (depending on the Azure Portal version):

        - Image Source: Azure Container Registry
        - Registry: mlopsprojectdocker (the registry name you created)
        - Image: mltest
        - Tag: latest
    4. Click Create to finalize the Web App.

- Step 4: Configure Deployment Center (Optional)
    1. Navigate to your newly created Web App resource.
    2. Go to Deployment → Deployment Center
    3. If desired, set up Continuous Deployment from a GitHub repository or other source.
    4. Fill out the required information and Save the configuration.
