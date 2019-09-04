__author__ = 'salton'

#import pymongo
import pymysql


class Database(object):
    host = '127.0.0.1'
    user = 'root'
    password = 'Seow@1234'
    database = 'project'
    port = 3306
    charset = 'utf8'
    DATABASE = None
    cur = None

    @staticmethod
    def initialize():
        try:
            Database.DATABASE = pymysql.connect(host=Database.host, user=Database.user, password=Database.password,
                                                database=Database.database, port=Database.port, charset=Database.charset)
        except:
            print("connectDatabase failed")
            return False
        Database.cur = Database.DATABASE.cursor()
        return True

    @staticmethod
    def close():
        if Database.DATABASE and Database.cur:
            Database.cur.close()
            Database.DATABASE.close()
        return True

    @staticmethod
    def execute(sql, params = None):
        try:
            if Database.DATABASE and Database.cur:
                Database.cur.execute(sql, params)
                Database.DATABASE.commit()
        except:
            print("Execution error, sql: {}, params: {}".format(sql, params))
            return False
        return True

    @staticmethod
    def fetchall(sql, params=None):
        Database.execute(sql, params)
        return Database.cur.fetchall()

    @staticmethod
    def fetchone(sql, params=None):
        Database.execute(sql, params)
        return Database.cur.fetchone()









'''
class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)
'''