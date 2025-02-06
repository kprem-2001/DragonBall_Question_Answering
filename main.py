import sys 

from src.pipelines.training_pipeline import TrainPipeline
from src.logger import logging

train_pipeline = TrainPipeline()


logging.info("Training model")
train_pipeline.train()


    
    
    
