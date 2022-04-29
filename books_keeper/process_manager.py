from db_manager import SqlManager


class ProcessManager:

    def __init__(self) -> None:
        # self.sql_manager = SqlManager()
        ...

    @staticmethod
    def process_query(todo, query):
        if todo == "v-add":
            return ProcessManager.process_add(query)

        elif todo == "v-search":
            return ProcessManager.process_search(query)

    @staticmethod
    def process_add(query):
        if (query["author"] or query["name"]):
            if not query["tags"]:
                query["tags"] = "NULL"
            try:
                SqlManager().insert_sql(tuple(query.values()))
                return "inserted"
            except Exception:
                return None
        else:
            print("not enough data")
            return "not_enough_to_add"

    @staticmethod
    def process_search(data):
        query = {"author": data["author"],
                 "name": data["name"], "tags": ""}
        if not data["tags"]:
            cond = SqlManager().make_condition_str(query)
            return SqlManager().select_sql(cond)
        else:
            lst = []
            query_tags = data["tags"].split(",")
            tags = map(str.strip, (query_tags))
            for t in tags:
                print("---", t)
                query["tags"] = t
                cond = SqlManager().make_condition_str(query)
                selected_rows = SqlManager().select_sql(cond)
                lst.extend(selected_rows)
                # print("selected_rows", selected_rows)
                return lst
