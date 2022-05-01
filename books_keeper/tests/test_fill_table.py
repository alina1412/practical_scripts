
import sys
# from typing import List
import os
address = os.environ.get("address")         # RUN IN DEBUG!!!
sys.path.append(address)                    # type: ignore
from collections import namedtuple          # type: ignore # noqa

from db_manager import SqlManager           # type: ignore # noqa


def prepare():
    DB_init = namedtuple("DB_init", ['db_name', "table_name",
                         "column1", "column2", "column3"])

    init_data = DB_init("books_storage.db", "books",
                        "author", "title", "tags")

    SEL = namedtuple("SEL", ['id', "author",
                     "title", "tags"])
    lst = [
        SEL(id=1, author='Hans Christian Andersen', title='The Ugly Duckling', tags='tale'),
        SEL(id=2, author='Jan Ormerod', title='The Frog Prince', tags='tale'),
        SEL(id=3, author='Robert Southey', title='Goldilocks and the Three Bears ', tags='tale'),
        SEL(id=4, author='Oscar Wilde', title='The Happy Prince', tags='tale'),
        SEL(id=5, author='Michael Morpurgo', title='Hansel and Gretel', tags='tale'),
        SEL(id=6, author='Daniel Kahneman', title='Thinking, Fast and Slow', tags='education, science'),
        SEL(id=7, author='Yuval Noah Harari', title='Sapiens: A Brief History of Humankind', tags='science'),  
        SEL(id=8, author='Sapolski Robert', title='Zapiski Primata', tags='science')
    ]

    s_man = SqlManager(init_data)
    for data in lst:
        # s_man.insert_sql(data)
        # print(data[1])
        d = {"author": data[1], "title": data[2], "tags": data[3]}
        s_man.insert_sql(tuple([*d.values()]))

prepare()
