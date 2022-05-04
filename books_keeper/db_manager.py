import sqlite3
import re
from collections import namedtuple

# classes SqlManager, SelectQuery


class SqlManager:
    def __init__(self, init_data) -> None:
        # self.init_data = init_data
        self.db = init_data.db_name    # "books_storage.db"
        self.table_name = init_data.table_name  # "books"
        self.column1 = init_data.column1        # "author"
        self.column2 = init_data.column2        # "title"
        self.column3 = init_data.column3        # "tags"
        print("self.table_name", self.table_name,
              type(self.table_name, ), self.db)

        self.create_q = f"""CREATE table IF NOT EXISTS
            {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,
            {self.column1} TEXT,
            {self.column2} TEXT,
            {self.column3} TEXT
            )"""
        with sqlite3.connect(self.db) as cursor:
            cursor.execute(self.create_q)
            cursor.commit()

    def select_sql(self, condition="", add=""):
        q = (f"SELECT * FROM {self.table_name}" +
             " " + condition)
        SEL = namedtuple("SEL", ['id', self.column1,
                         self.column2, self.column3])
        lst = []
        with sqlite3.connect(self.db) as cursor:
            cursor.create_function('REGEXP', 2, lambda x, y:
                                   bool(re.search(x, y)))
            for row in cursor.execute(q, add):
                lst.append(SEL(*row))
        print("select_sql", lst)
        return lst

    def insert_sql(self, args):
        q = f'''INSERT into {self.table_name}
            ({self.column1}, {self.column2}, {self.column3})
            VALUES (?,?,?)'''
        with sqlite3.connect(self.db) as cursor:
            cursor.execute(q, tuple([*args]))
            cursor.commit()


class SelectQuery:

    @staticmethod
    def get_regexp_query(data):
        cond_lst = []
        for col_name, col_val in data.items():
            if not col_val:
                continue
            pattern = SelectQuery.low_up_pattern(col_val)
            cond = SelectQuery.regexp_query(pattern, col_name)
            cond_lst.append(cond)
        if not cond_lst:
            return ""
        else:
            return SelectQuery.join_conditions(cond_lst)

    @staticmethod
    def low_up_pattern(words):
        case_lst = []
        for w in words.split(" "):
            case_lst.append("(")
            for ch in w:
                L = ch.upper()
                lo = ch.lower()
                case_lst.append("[" + L + lo + "]")
            case_lst.append(")|")
        return "".join(case_lst)[:-1]

    @staticmethod
    def regexp_query(pattern, col_name):
        x = rf'{pattern}'
        s_cond = f'{col_name} REGEXP "{x}"'
        return s_cond

    @staticmethod
    def strict_search_query(col_name, col_val):
        return f"{col_name} = '{col_val}'" if col_val else ""

    @staticmethod
    def join_conditions(cond_lst):
        condition = " AND ".join(cond_lst)
        if condition:
            return "WHERE " + condition
        else:
            return ""
