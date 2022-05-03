from collections import namedtuple
from db_manager import SelectQuery, SqlManager


class BookManager:

    def __init__(self, table_name) -> None:
        DB_init = namedtuple("DB_init", ['db_name', "table_name",
                             "column1", "column2", "column3"])
        init_data = DB_init("books_storage.db", table_name,
                            "author", "title", "tags")
        self.sqlMan = SqlManager(init_data)

    def process_query(self, todo, query):
        if todo == "v-add":
            lst = self.process_strict_search(query)
            if not lst:
                return self.process_add(query)
            else:
                return "that data was inserted previously"

        elif todo == "v-search":
            lst = self.process_regexp_search(query)
            if lst:
                return lst
            else:
                return "no data matches your request"

    def process_add(self, query):
        if (query["author"] or query["title"]):
            if not query["tags"]:
                query["tags"] = "NULL"
            try:
                self.sqlMan.insert_sql(tuple(query.values()))
                return "inserted"
            except Exception:
                return None
        else:
            print("not enough data")
            return "not enough data to add"

    def process_regexp_search(self, book_query):
        lst = []
        query_tags = book_query["tags"].split(",")
        tags = map(str.strip, (query_tags))
        for t in tags:
            print("tag---", t)
            book_query["tags"] = t
            cond = SelectQuery.get_regexp_query(book_query)
            print("process_search cond = ", cond)
            selected_rows = self.sqlMan.select_sql(cond)
            for row in selected_rows:
                if row not in lst:
                    lst.append(row)

        lst.sort(key=lambda k: (len(k.title), len(k.author)), reverse=1)
        return lst

    def process_strict_search(self, book_query):
        lst = []
        for k, v in book_query.items():
            if v:
                c = SelectQuery.strict_search_query(k, v)
                lst.append(c)
        cond = SelectQuery.join_conditions(lst)
        print(cond)
        selected_rows = self.sqlMan.select_sql(cond)
        return selected_rows
