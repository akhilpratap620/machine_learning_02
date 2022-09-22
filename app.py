from flask import Flask
from heart_failure.logger import logging
from heart_failure.exception import FailureException
import sys , os

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    try:
        return "this is second project"
    except Exception as e:
        ex = FailureException(e, sys) 
        logging.info(ex.error_message)
        return "second project"



if __name__ == "__main__":
    app.run(debug=True)   
