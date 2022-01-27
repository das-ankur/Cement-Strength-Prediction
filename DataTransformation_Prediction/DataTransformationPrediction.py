from os import listdir
import pandas
from application_logging.logger import App_Logger

class dataTransformPredict:
     """
     This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
     """
     def __init__(self):
          """
          Description: constructor
          """
          self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"  # path of good raw prediction data
          self.logger = App_Logger()    # object for logging

     def addQuotesToStringValuesInColumn(self):
          """
          Description: This method converts all the columns with string datatype such that
                    each value for that column is enclosed in quotes. This is done
                    to avoid the error while inserting string values in table as varchar.
          """
          try:
               log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pandas.read_csv(self.goodDataPath + "/" + file)
                    data['DATE'] = data["DATE"].apply(lambda x: "'" + str(x) + "'")
                    data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                    self.logger.log(log_file, " %s: Quotes added successfully!!" % file)
          except Exception as e:
               log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               log_file.close()
               raise e
          log_file.close()