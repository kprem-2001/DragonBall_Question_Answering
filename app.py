from flask import Flask, request, render_template
import os
import time
import logging  # Ensure you import logging

from src.pipelines.training_pipeline import TrainPipelineConfig
from src.pipelines.prediction_pipeline import PredictPipeline
from src.utils import check_model_exist

# Initialize Flask app
app = Flask(__name__)

# Function to check and initialize model pipelines
def get_prediction_pipeline():
    if check_model_exist(TrainPipelineConfig().model_save_path):
        return PredictPipeline()
    return None

@app.route('/', methods=['GET', 'POST'])
def predict():
    try:
        prediction_pipeline = get_prediction_pipeline()

        if request.method == 'GET':
            return render_template('index.html', 
                                   trained_stand=check_model_exist(TrainPipelineConfig().model_save_path))

        # Handle POST request
        start_time = time.time()
        query = request.form.get('query')

        if not query:
            return render_template('index.html', result={'Error': "Enter a query"}, completed=True, time_taken=0)

        retriever = request.form.get('cCB1') is not None
        result = {}

        if prediction_pipeline:
            if retriever:
                result['ret'] = prediction_pipeline.predict(query=query)
        else:
            result['Error'] = "No trained model found."

        total_time = time.time() - start_time

        return render_template('predict.html', result=result, completed=True, time_taken=total_time,
                               trained_stand=check_model_exist(TrainPipelineConfig().model_save_path))

    except Exception as e:
        logging.exception(f"Error in prediction: {e}")
        return render_template('predict.html', result={'Error': f"Internal Server Error: {str(e)}"}, completed=True, time_taken=0)

if __name__ == '__main__':
    # Configuration could be moved to environment variables or a config file
    app.run(host='0.0.0.0', port=8080, debug=False)
