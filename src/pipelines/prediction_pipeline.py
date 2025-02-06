import sys 
import os 
from dataclasses import dataclass

from src.exceptions import CustomException
from src.logger import logging
from src.utils import load_object, reformat_prediction, check_model_exist


@dataclass
class PredictPipelineConfig:
    saved_model_path: str = os.path.join('artifacts', 'trained_pipe.pkl')
    retriever_top_k: int = 10
    reader_top_k: int = 5


class PredictPipeline:
    def __init__(self) -> None:
        self.predict_pipeline_config = PredictPipelineConfig()
        self.prediction_model = None
        self.retriever_params = {"top_k": self.predict_pipeline_config.retriever_top_k}
        self.reader_params = {"top_k": self.predict_pipeline_config.reader_top_k}
        self.allocate_model()
    
    def predict(self, query: str) -> dict:
        '''
        predicts the answer with context using the document reader-retriever model
        Params:
            query: str - query to be answered
        Returns:
            answers with context: dict
        '''
        try:
            logging.info("Prediction pipeline started")
            
            prediction = self.prediction_model.run(
                query=query,
                params= {
                    "Retriever": self.retriever_params,
                    "Reader": self.reader_params
                }
            )
            
            prediction = reformat_prediction(prediction)
            
            logging.info("Prediction Completed")
            
            return prediction
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
    
    def allocate_model(self):
        if check_model_exist(self.predict_pipeline_config.saved_model_path):
            self.prediction_model = load_object(
                self.predict_pipeline_config.saved_model_path
            )    