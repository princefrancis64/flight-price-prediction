from flight.pipeline.training_pipeline import start_training_pipeline
from flight.pipeline.batch_prediction import start_batch_prediction
input_file_path = "input_files\Test_set.xlsx"
    

if __name__=="__main__":
    try:
        start_training_pipeline()
        start_batch_prediction(input_file_path=input_file_path)

    except Exception as e:
        print(e)


    
