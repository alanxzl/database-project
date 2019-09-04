__author__ = 'salton'

import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert

class User(object):
    def __init__(self, email, password, unick, uname, _id=None):
        self.email = email
        self.password = password
        self._id = _id
        self.unick = unick
        self.uname = uname

    def __repr__(self):
        return "<User {}>".format(self.email)

    @classmethod
    def find_by_email(cls, email):
        sql = "select * from {} where email = '{}'".format(UserConstants.COLLECTION,email)
        tup = Database.fetchone(sql)
        email = tup[4]
        unick = tup[3]
        uname = tup[1]
        _id = tup[0]
        password = tup[2]
        return cls(email, password, unick, uname, _id)

    @classmethod
    def find_by_uid(cls, uid):
        sql = "select * from {} where uid = '{}'".format(UserConstants.COLLECTION, uid)
        tup = Database.fetchone(sql)
        email = tup[4]
        unick = tup[3]
        uname = tup[1]
        _id = tup[0]
        password = tup[2]
        return cls(email, password, unick, uname, _id)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        sql = "select * from {} where email='{}'".format(UserConstants.COLLECTION, email)
        user_data = Database.fetchone(sql)  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        # user_data[2] for password

        if not Utils.check_hashed_password(password, user_data[2]):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password, uname, unick):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        sql = "select * from {} where email='{}'".format(UserConstants.COLLECTION, email)
        user_data = Database.fetchone(sql)

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        hashed_pswd = Utils.hash_password(password)
        sql = "insert into {}(uname, upassword, unick, email)values('{}', '{}','{}', '{}')".format(UserConstants.COLLECTION, uname, hashed_pswd, unick, email)
        Database.execute(sql)

        return True


    @staticmethod
    def exist_user(user_id):
        sql = "select * from {} where uid='{}'".format(UserConstants.COLLECTION, user_id)
        user_data = Database.fetchone(sql)
        if not user_data:
            return False
        else:
            return True


    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "unick": self.unick,
            "uname": self.uname
        }


'''
class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one("users", {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }
'''
