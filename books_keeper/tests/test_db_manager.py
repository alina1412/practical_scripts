from collections import namedtuple
import sys
# from typing import List
import os
address = os.environ.get("address")                     # RUN IN DEBUG!!!
sys.path.append(address)                                # type: ignore
from book_manager import BookManager

from db_manager import SelectQuery, SqlManager     # type: ignore # noqa


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
        if (r.author == 'Amy' and r.title == 'Book one two'
                and r.tags == 'tale, light'):
            was_there = True
    if not was_there:
        s_man.insert_sql(("Amy", "Book one two", "tale, light"))
    return s_man


s_man = prepare()


test_data = {"author": "Amy", "title": "", "tags": ""}
cond = SelectQuery.get_regexp_query(test_data)
assert cond == 'WHERE author REGEXP "([Aa][Mm][Yy])"'
# print(cond)

res = s_man.select_sql(cond)
# print(res)

SEL = namedtuple("SEL", ['id', "author",
                         "title", "tags"])
assert res == [SEL(id=1, author='Amy', title='Book one two',
                   tags='tale, light')]


# print(getattr(res[0], 'author'))
# col_name = "title"


# s_man = BookManager("[books]")
# test_data = {"author": "ro", "title": "", "tags": ""}
# res = s_man.process_search(test_data)
# print((res))


# s_man = BookManager("[1@r.ru]")
# test_data = {"author": "Mo ro", "title": "HP", "tags": "tale"}
# s_man.process_add(test_data)
# res = s_man.process_search(test_data)
# print((res))

