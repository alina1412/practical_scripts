import re
from collections import namedtuple
from sqlite3 import Error as sqlite3_err
from db_manager import SqlManager

# classes UserManager, PasswordLogs


class UserManager:
    def __init__(self) -> None:
        DB_init = namedtuple("DB_init", ['db_name', "table_name",
                             "column1", "column2", "column3"])

        init_data = DB_init("users_logs.db", "logs",
                            "email", "password", "info")

        self.UserMan = SqlManager(init_data)

    def getUserByEmail(self, email):
        if not PasswordLogs.validate_email(email):
            return "not valid email"
        try:
            condition = f"WHERE email = '{email}'"
            res = self.UserMan.select_sql(condition)
            print("res", res)
            if not res:
                print("no such user")
                return False
            return res
        except sqlite3_err:
            print("Error", sqlite3_err)
        return False

    def register_user(self, email, password, info=""):
        if not PasswordLogs.validate_email(email):
            return "not valid email"
        if not PasswordLogs.validate_password(password):
            return "password should have from 5 to 20 symbols, " +\
                    "including digits, letters. Could include: _ - *"

        if not self.getUserByEmail(email):
            password = PasswordLogs.u_hash(password)
            try:
                self.UserMan.insert_sql((email, password, info))
                return "success"
            except sqlite3_err:
                print(sqlite3_err)
                return "something went wrong. " + str(sqlite3_err)
        return "user with this name exists"

    def is_log_in(self, email, password):
        if not password or not email:
            return False
        data = self.getUserByEmail(email)
        if data:
            # password - column 2
            # if data[0][2] == PasswordLogs.u_hash(password):
            if getattr(data[0], 'password') == PasswordLogs.u_hash(password):
                return True
        return False


class PasswordLogs:

    @staticmethod
    def u_hash(password: str) -> str:
        n = 1
        pw = 0
        for i in range(len(password)):
            n += ord(password[i]) * i**pw
            pw += 1
            n = n % 99999999
        return str(n)

    @staticmethod
    def validate_email(email):
        if email.count("@") != 1:
            return False
        r = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+" +
                       r"(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|" +
                       r"(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+" +
                       r"(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if re.fullmatch(r, email):
            return True
        else:
            return False

    @staticmethod
    def validate_password(p):
        if len(p) < 5 or len(p) > 20:
            return False
        for ch in p:
            if not (ch in "_-*" or ch.isdigit() or ch.isalpha()):
                return False
        return True

# u = UDataBase()
# res = u.getUserByEmail("123@1h.ru")
# print(res)
# res = u.is_log_in("123@1h.ru", "qwert")
# print(res)
