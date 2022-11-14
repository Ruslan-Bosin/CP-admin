from app import  app, logger
import datetime

START_TIME = datetime.datetime.now()

if __name__ == "__main__":
    app.exec()

