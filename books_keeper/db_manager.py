import sqlite3
import re
from collections import namedtuple


class SqlManager:
    def __init__(self, init_data) -> None:
        # self.init_data = init_data
        self.db = init_data.db_name    # "books_storage.db"
        self.table_name = init_data.table_name  # "books"
        self.column1 = init_data.column1        # "author"
        self.column2 = init_data.column2        # "title"
        self.column3 = init_data.column3        # "tags"

        self.create_q = f"""CREATE table IF NOT EXISTS
            {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,
            {self.column1} TEXT,
            {self.column2} TEXT,
            {self.column3} TEXT
            )"""
        with sqlite3.connect(self.db) as cursor:
            cursor.execute(self.create_q)
            cursor.commit()

    def select_sql(self, condition=""):
        q = (f"SELECT * FROM {self.table_name}" +
             " " + condition)
        SEL = namedtuple("SEL", ['id', self.column1,
                         self.column2, self.column3])
        lst = []
        with sqlite3.connect(self.db) as cursor:
            cursor.create_function('REGEXP', 2, lambda x, y:
                                   bool(re.search(x, y)))
            for row in cursor.execute(q):
                lst.append(SEL(*row))
        return lst

    def insert_sql(self, args):
        q = f'''INSERT into {self.table_name}
            ({self.column1}, {self.column2}, {self.column3})
            VALUES (?,?,?)'''
        with sqlite3.connect(self.db) as cursor:
            cursor.execute(q, tuple([*args]))
            cursor.commit()


class SelectConditions:

    def book_search_condition(self, data):
        cond_lst = []
        for k, v in data.items():
            cond = self.search_part(k, v)
            if cond:
                cond_lst.append(cond)
        if not cond_lst:
            return ""
        else:
            return self.join_conditions(cond_lst)

    def search_part(self, col_name, col_val):
        if not col_val:
            return ""

        def get_lower_upper_pattern(words):
            case_lst = []
            for w in words.split(" "):
                case_lst.append("(")
                for ch in w:
                    L = ch.upper()
                    lo = ch.lower()
                    case_lst.append("[" + L + lo + "]")
                case_lst.append(")|")
            return "".join(case_lst)[:-1]

        pattern = get_lower_upper_pattern(col_val)
        x = rf'{pattern}'
        s_cond = f'{col_name} REGEXP "{x}"'
        return s_cond

    # def strict_search_condition(self, col_name, col_val):
    #     s1 = f"{col_name} = '{col_val}'" if col_val else ""

    def join_conditions(self, cond_lst):
        condition = " AND ".join(cond_lst)
        if condition:
            return "WHERE " + condition
        else:
            return ""
