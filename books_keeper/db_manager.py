import sqlite3
import re
from collections import namedtuple


class SqlManager:
    def __init__(self) -> None:
        self.db = "books_storage.db"
        self.table_name = "books"
        self.column1 = "author"
        self.column2 = "name"
        self.column3 = "tags"

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
                cur_select = SEL(*row)
                lst.append(cur_select)
        return lst

    def insert_sql(self, args):
        q = f'''INSERT into {self.table_name}
            ({self.column1}, {self.column2}, {self.column3})
            VALUES (?,?,?)'''
        with sqlite3.connect(self.db) as cursor:
            cursor.execute(q, tuple([*args]))
            cursor.commit()

    def make_condition_str(self, data):
        q1 = data[self.column1]
        q2 = data[self.column2]
        s1 = f"{self.column1} = '{q1}'" if q1 else ""
        s2 = f"{self.column2} = '{q2}'" if q2 else ""

        if data[self.column3]:
            v = data[self.column3]
            # x = [rf'{v}']
            x = rf'{v}'
            s3 = f'{self.column3} REGEXP "{x}"'
        else:
            s3 = ""

        lst = [x for x in [s1, s2, s3] if x]
        condition = " AND ".join(lst)
        if condition:
            s = "WHERE " + condition
        else:
            s = ""
        print(s)
        return s


# d.insert_sql(("Amy", "Worm","tag"))
# data = {"author": "", "name": "Worm", "tags": ("A", "B")}
# data = {"author": "", "name": "", "tags": ()}
# data = {"author": "Amy", "name": "", "tags": ("tag",)}
# cond = d.make_condition_str(data)

# print(list(d.select_sql(cond)))

# s.insert_sql(("Tom", "Worm","tag2"))
# res = s.select_sql("Amy")
# s = SqlManager()
# print((res))
# data = {"author": "", "name": "", "tags": "2"}
# condit = s.make_condition_str(data)
# res = s.select_sql(condit)
# print((res))
# print("--")

# import re
# with sqlite3.connect(s.db) as cursor:
#     cursor.create_function('REGEXP', 2, lambda x, y: 1
# if re.search(x,y) else 0)
#     v = "2"
#     x = [rf'{v}']
#     q = f'SELECT * FROM {s.table_name} WHERE {s.column3} REGEXP "{x}"'
#     res = cursor.execute(q)

#     print(list(res))
