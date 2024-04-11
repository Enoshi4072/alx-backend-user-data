#!/usr/bin/env python3

"""
filtered_logger module
"""
import typing
import re
from typing import List
import logging
import os
import mysql.connector

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ('name','email', 'phone', 'ssn', 'password')

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values with redaction string
    in the log message
    """
    return re.sub(patterns['extract'](fields, separator), patterns['replace'](redaction), message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method for RedactingFormatter class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format method override.
        Placeholder method for formarring log messages
        """
        message = record.msg
        for field in self.fields:
            message = filter_datum([field], self.REDACTION, message, self.SEPARATOR)
        record.msg = message
        return super().format(record)

def get_logger() -> logging.Logger:
    """ Returns a logger obj configured according to the specifications """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = StreamHandler()
    stream_handler.selLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
   """ Return a connection to the MySQL db using env vars """ 
   username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
   password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
   host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
   database = os.getenv('PERSONAL_DATA_DB_NAME')
   db = mysql.connector.connect(
           user=username,
           password=password,
           host=host,
           database=database
           )
   return db

def main():
    """
    Retrieves data from the users table and logs it under a filtered format.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("user_data")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    filtered_fields = ['name', 'email', 'phone', 'ssn', 'password']
    for row in rows:
        log_message = "name={}; email={}; phone={}; ssn={}; password={}; ip={}; last_login={}; user_agent={};".format(
            *([logging.Filterer().filter(field) for field in row])
        )
        logger.info(log_message)
    logger.info("Filtered fields:")
    for field in filtered_fields:
        logger.info(field)

    cursor.close()
    db.close()
