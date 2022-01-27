from datetime import datetime                   # To access date and time of system

class App_Logger:
    """
    The class is used for logging
    """
    def __init__(self):                         # Constructor
        pass

    def log(self, file_object, log_message):
        """
        description: logs all the runtime details in a file
        file_object: writes data in this file
        log_message: the message to be logged in the file
        """
        self.now = datetime.now()                               # date and time of the system
        self.date = self.now.date()                             # extract date of the system
        self.current_time = self.now.strftime("%H:%M:%S")       # write time in the specified format
        # logs message in the specified file
        file_object.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
