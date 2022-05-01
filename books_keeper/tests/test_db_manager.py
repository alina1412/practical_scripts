from collections import namedtuple
import sys
# from typing import List
import os
address = os.environ.get("address")                     # RUN IN DEBUG!!!
sys.path.append(address)                                # type: ignore

from db_manager import SelectConditions, SqlManager     # type: ignore # noqa


def prepare():
    DB_init = namedtuple("DB_init", ['db_name', "table_name",
                         "column1", "column2", "column3"])

    init_data = DB_init("test_fhsyrbvY.db", "test_test",
                        "author", "title", "tags")

    s_man = SqlManager(init_data)
    res = s_man.select_sql("")

    was_there = False
    for r in res:
        # SEL(id=1, author='Amy', title='Book one', tags='tale, light')
        if r.author == 'Amy' and r.title == 'Book one two' and r.tags == 'tale, light':
            was_there = True
    if not was_there:
        s_man.insert_sql(("Amy", "Book one two", "tale, light"))
    return s_man


s_man = prepare()


test_data = {"author": "Amy", "title": "", "tags": ""}
cond = SelectConditions().book_search_condition(test_data)
assert cond == 'WHERE author REGEXP "([Aa][Mm][Yy])"'
# print(cond)

res = s_man.select_sql(cond)
# print(res)

SEL = namedtuple("SEL", ['id', "author",
                         "title", "tags"])
assert res == [SEL(id=1, author='Amy', title='Book one two',
                   tags='tale, light')]

# col_name = "title"

# test_data = {"author": "", "title": "two", "tags": ""}
# cond = SelectConditions().book_search_condition(test_data)

# cond = rf'WHERE title REGEXP "([Oo][Nn][Ee])|([Tt][Ww][Oo])"'
# res = s_man.select_sql(cond)
# print(cond)

# print((res))
