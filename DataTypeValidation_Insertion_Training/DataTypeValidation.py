import shutil                           # for file management
import sqlite3                          # for database management
from os import listdir                  # access all file and folder name inside a folder
import os                               # To perform different functions of files and folders
import csv                              # handling csv files
from application_logging.logger import App_Logger


class dBOperation:
    """
    This class shall be used for handling all the SQL operations.
    """
    def __init__(self):
        """
        Description: constructor
        """
        self.path = 'Training_Database/'        # Path to store database of training files
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"       # path of bad rae data
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"     # path of good raw data
        self.logger = App_Logger()                                      # object for logging

    def dataBaseConnection(self,DatabaseName):
        """
        Description: This method creates the database with the given name and if Database already exists
                then opens the connection to the DB.
        Output: Connection to the DB
        On Failure: Raise ConnectionError
        """
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')            # create connection with database
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):
        """
        Description: This method creates a table in the given database which will be used to insert the
                    Good data after raw data validation.
        Output: None
        On Failure: Raise Exception
        """
        try:
            conn = self.dataBaseConnection(DatabaseName)        # create connection
            c = conn.cursor()
            # create table with the name Good_Raw_Data
            c.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")
            #
            if c.fetchone()[0] == 1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()
                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
            else:
                for key in column_names.keys():
                    type = column_names[key]
                    # we will remove the column of string datatype before loading as it is not needed for training
                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we create the table
                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()
                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self,Database):
        """
        Description: This method inserts the Good data files from the Good_Raw folder into the
                    above created table.
        Output: None
        On Failure: Raise Exception
        """
        conn = self.dataBaseConnection(Database)                # create connection
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]          # read all files from good raw data
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')
        for file in onlyfiles:
            try:
                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                # insert all the data of good raw data files in Good_Raw_data
                                self.logger.log(log_file," %s: File loaded successfully!!" % file)
                                conn.commit()       # commit all the changes
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()             # if any exception occurs during insertion, rollback to previous state
                self.logger.log(log_file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self,Database):

        """
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
                    above created .
        Output: None
        On Failure: Raise Exception
        """
        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)
            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]
            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',',
                                 lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')
            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)
            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()
        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()