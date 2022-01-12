import MySQLdb

def connexion():
    mysql = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="root",
        db="todo")
    return mysql