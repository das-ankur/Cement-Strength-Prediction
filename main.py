from wsgiref import simple_server
"""
This module implements a simple HTTP server (based on http.server) that serves WSGI applications. Each 
server instance serves a single WSGI application on a given host and port. If you want to serve multiple 
applications on a single host and port, you should create a WSGI application that parses PATH_INFO to 
select which application to invoke for each request. (E.g., using the shift_path_info() function from 
wsgiref.util.)
"""
from flask import Flask, request, render_template, url_for
# To get web app, request from webpages and render webpages
from flask import Response          # To response request
import os                           # To get system functionalities
from flask_cors import CORS, cross_origin
"""
A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
"""
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard

"""
The Flask Monitoring Dashboard is an extension that offers 4 main functionalities 
with little effort from the Flask developer: Monitor the performance and utilization: 
The Dashboard allows you to see which endpoints process a lot of requests and how fast.
"""
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)       # create flask app
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():                 # route to home page
    return render_template('index.html')

@app.route("/predict", methods=['POST'])        # route to predict request
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            pred_val = pred_validation(path) #object initialization
            pred_val.prediction_validation() #calling the prediction_validation function
            pred = prediction(path) #object initialization
            # predicting for dataset present in database
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)
        elif request.form is not None:
            path = request.form['filepath']
            pred_val = pred_validation(path) #object initialization
            #pred_val.prediction_validation() #calling the prediction_validation function
            pred = prediction(path) #object initialization
            # predicting for dataset present in database
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

@app.route("/train", methods=['POST'])          # route to train request
@cross_origin()
def trainRouteClient():
    try:
        path ="Training_Batch_Files"
        print(request.json)
        if request.json is not None:
            if request.json['folderPath'] is not None:
                path = request.json['folderPath']
        train_valObj = train_validation(path) #object initialization
        train_valObj.train_validation()#calling the training_validation function
        trainModelObj = trainModel() #object initialization
        trainModelObj.trainingModel() #training the model for the files in the table
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    host='0.0.0.0'
    httpd = simple_server.make_server( host,port, app)
    print("Serving on %s %d" % ( host,port))
    httpd.serve_forever()
