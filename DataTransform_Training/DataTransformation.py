from os import listdir                  # To read all files and folders name in a folder
from application_logging.logger import App_Logger
import pandas as pd

class dataTransform:
     """
     This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
     """
     def __init__(self):
          """
          description: Contructor
          """
          self.goodDataPath = "Training_Raw_files_validated/Good_Raw" # All the good raw data needs to be inserted in the database
          self.logger = App_Logger() # Logger object for logging

     def addQuotesToStringValuesInColumn(self):
          """
          Description: This method converts all the columns with string datatype such that
                    each value for that column is enclosed in quotes. This is done
                    to avoid the error while inserting string values in table as varchar.
          """
          log_file = open("Training_Logs/addQuotesToStringValuesInColumn.txt", 'a+')
          try:
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pd.read_csv(self.goodDataPath+"/" + file)
                    data['DATE'] = data["DATE"].apply(lambda x: "'" + str(x) + "'")
                    data.to_csv(self.goodDataPath+ "/" + file, index=None, header=True)
                    self.logger.log(log_file," %s: Quotes added successfully!!" % file)
          except Exception as e:
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               log_file.close()
          log_file.close()