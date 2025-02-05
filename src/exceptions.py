import sys

def error_message_details(error, error_detail :sys) -> str:
    _,_,error_message = error_detail.exc_info()
    
    