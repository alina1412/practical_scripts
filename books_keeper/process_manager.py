from collections import namedtuple
from db_manager import SelectConditions, SqlManager


class BookManager:

    def __init__(self) -> None:
        DB_init = namedtuple("DB_init", ['db_name', "table_name",
                             "column1", "column2", "column3"])
        init_data = DB_init("books_storage.db", "books",
                            "author", "title", "tags")
        self.sqlMan = SqlManager(init_data)

    def process_query(self, todo, query):
        if todo == "v-add":
            return self.process_add(query)

        elif todo == "v-search":
            lst = self.process_search(query)
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

    def process_search(self, data):
        book_query = {"author": data["author"],
                      "title": data["title"], "tags": ""}
        if not data["tags"]:
            cond = SelectConditions().book_search_condition(book_query)
            lst = self.sqlMan.select_sql(cond)
        else:
            lst = []
            query_tags = data["tags"].split(",")
            tags = map(str.strip, (query_tags))
            for t in tags:
                print("---", t)
                book_query["tags"] = t
                cond = SelectConditions().book_search_condition(book_query)
                print(cond)
                selected_rows = self.sqlMan.select_sql(cond)
                for row in selected_rows:
                    if row not in lst:
                        lst.append(row)

        lst.sort(key=lambda k: (len(k.title), len(k.author)), reverse=1)
        return lst
