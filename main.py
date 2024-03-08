from flight.pipeline.logger import logging
from flight.pipeline.exception import FlightException
import sys,os

def test_logger_and_exception():
    try:
        result=3/0
        print(result)
    except Exception as e:
        raise FlightException(e,sys)
    

if __name__=="__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)
