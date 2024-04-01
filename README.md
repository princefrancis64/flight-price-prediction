![Flight Price Prediction](Night-Landing.jpg)

## FLIGHT PRICE PREDICTION

### TABLE OF CONTENTS
1. COMPONENTS
 - A. DATA INGESTION
 - B. DATA VALIDATION
 - C. DATA TRANSFORMATION
 - D. MODEL TRAINER
 - E. MODEL EVALUATION
 - F. MODEL PUSHER
2. HELPER FUNCTION FILES
3. PIPELINE
 - A. TRAINING PIPELINE
 - B. BATCH EVALUATION
4. DAGS
 - A. TRAINING PIPELINE
 - B. BATCH PREDICTION


### 1. COMPONENTS
 - A. DATA INGESTION
   - I have first dumped the train data and test data to the mongodb using the data_dump.py file. 
   - A folder called artifact has been created where in further we are creating data ingestion->feature store and dataset folders.
   - Feature store has the complete train dataset.
   - Dataset folder has the train and test dataset which has been taken of from the train dataset which we were given i.e Data_Train.xlsx.

 - B. DATA VALIDATION
   - Choosign a base dataset which is the initial train dataset Data_train.xlsx itself to compare it with that of our splitted train and test dataset.
   - Checking if all the columns in our base dataset and train,test dataset are comparable.
   - Checking datadrift with the help of chi2_contingency function.
   - This basically checks if each `column` with respect to our base dataset and that with that of the train and the test dataset have similar distributions or not. 
   - report.yaml has got all the recorded observations.
   - report stored in artifact-->data_validation folder

 - C. DATA TRANSFORMATION
   - Firstly removed the na rows since there was only 1 row.
   - Done Feature engineering on top of the train dataset
   - Splitted the dataset and then performed min max scaling on top of it to make all the data in same unit.
   - Done PCA transformation over the dataset to reduce the features.
   - Stored all the objects of min_max_scaler, pca for future use.
   - Objects have been stored in artifact--> data transformation folder.

 - D. MODEL TRAINER
   - Trained the model using Catboost regressor.
   - Dataset is used for overfitting or underfitting.
   - Hyperparameter tuning using the RandomSearchCV
   - Saved the model object in the folder model_trainer for future use.
   - Model object stored in artifact-->model_trainer folder

 - E. MODEL EVALUATION
   - We are checking if we have a folder called saved_models. This is to check the performance with respect to 
   that of that saved_model components to see if our current model is performing better or worse that the previous one.
   - If the current model is performing better then we will push it or else will get rejected.
   

 - F. MODEL PUSHER
   - If the saved_models folder is not available then we are saving our current model in the folder saved_models and denoting
   it as the folder 0.
   - If the saved_models folder is found , the performance of current and previous models are compared. If the performance of the 
   previous model is better then data is not pushed to the saved_models directory and rejected.


### 2. HELPER FUNCTION FILES
   - config.py--> used to store mongodb credential
   - exception.py--> custom exception
   - logger.py--> logging file
   - resolver.py--> used to get all the latest paths of directory being formed. Also to get the paths of the directories in which
   we have to store the objects in case the data is being pushed.
   - transformation.py--> used for feature engineering
   - utils.py --> This is to get small helper functions for eg: load_objects and saving objects to any folder etc.

### 3.PIPELINE
  - A. TRAINING PIPELINE
    - All the components have been arranged in step by step manner to form the training pipeline.
  - B. BATCH PREDICTION
    - In case of batch prediction we created a folder called the input_files. This contains our set dataset i.e Test_set.xlsx
    - We will predict the output column i.e `Price` for this dataset and store it in a folder called predicted_files.

### DAGS
   - A. TRAINING PIPELINE
     - `Note`: The deployment starts on push.
     - Github actions will show Continuous delivery and Continuous deployment on push.
     - Firstly we are logging into AMAZON ECR(ELASTIC CONTAINER REGISTRY) and storing an image of our project. 
     - Then this docker image has been pulled and run on the EC2 machine.
     - Using EC2 we are getting a linux environment.
     - Once the workflow has been successful then we can open up the airflow and trigger our DAG `flight_price_training`.
     - On successfull completion the folders saved_models, artifact folder with all the components would get added on to 
     AMAZON S3 Bucket.

   - B. BATCH PREDICTION
     - Add a folder called input_files in the S3 Bucket. This contains the Test_set.xlsx
     - Trigger the DAG `flight_price_prediction` from Apache Airflow.
     - Upon successful completion the S3 Bucket would show up a new folder called predicted_files with a prediction.csv file in it
    with Timestamp.

    `NOTE`: ALL THE DATA ANALYSIS HAS BEEN DONE IN THE NOTEBOOK CALLED `Flight Price Prediction.ipynb`


## Docker commands
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

.

