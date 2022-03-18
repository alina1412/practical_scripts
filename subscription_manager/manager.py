import os.path
import csv
import json
import sqlite3


def read_from_sql(filename) -> dict:
    tablename = "subscriptions"
    data_dict = {}
    try:
        connect = sqlite3.connect(filename)
        query = f"""SELECT url, name FROM {tablename}
                ORDER BY name"""
        selected = connect.execute(query)
        for row in selected:
            url = row[0]
            title = row[1]
            id = url.split("/")[-1]
            data_dict[id] = (url, title)
        connect.close()
    except sqlite3.Error as error:
        print(error)

    return data_dict


def write_to_sql(data) -> None:
    filename = "./util/merged_sub.db"
    tablename = "subscriptions"
    try:
        connect = sqlite3.connect(filename)
        print("connect succ", filename)
        query = f"""CREATE TABLE IF NOT EXISTS {tablename}
                (uid integer PRIMARY KEY AUTOINCREMENT,
                url text,
                name text);"""
        connect.execute(query)
        print("created")

        query = f'''INSERT INTO {tablename}
                (url, name) VALUES (?,?);'''

        for k in data:
            connect.execute(query, (data[k][0], data[k][1]))
        connect.commit()

        connect.close()
    except sqlite3.Error as error:
        print(error)
    return


def read_from_csv(filename) -> dict:
    data_dict = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        _ = next(reader)    # headers
        for row in reader:
            if row:
                # id : [url, title]
                data_dict[row[0]] = row[1:]
    return data_dict


def write_to_csv(data) -> None:
    new_name = "./util/merged_sub.csv"
    with open(new_name, "w", encoding="utf-8", newline='') as file:
        fieldnames = ["Channel ID", "Channel URL", "Channel title"]
        writer = csv.writer(file, dialect='excel')
        writer.writerow(fieldnames)
        for k, v in data.items():
            writer.writerow([k, v[0], v[1]])


def print_dict_data(added, deleted) -> None:
    if added:
        print("new subscriptions:")
        print(*[r[2] for r in sorted(added, key=lambda x: x[2])], sep="\n")
    else:
        print("No added subscriptions to the first file\n")

    if deleted:
        print("deleted subscriptions:")
        print(*[r[2] for r in sorted(deleted, key=lambda x: x[2])], sep="\n")
    else:
        print("No deleted subscriptions from the first file\n")


def compare_dicts(dnew, dold={}) -> dict:
    deleted = set()
    added = set()
    repeated = set()
    for k in dold:
        if k not in dnew:
            deleted.add((k, dold[k][0], dold[k][1]))
        else:
            repeated.add((k, dold[k][0], dold[k][1]))

    for k in dnew:
        if k not in dold:
            added.add((k, dnew[k][0], dnew[k][1]))

    print_dict_data(added, deleted)
    if not added and not deleted:
        print("subscriptions are the same\n")
        return None, None, None
    return repeated, added, deleted


def opts_merging(repeated, added, deleted):
    ans = ""
    while ans not in ("1", "2", "3"):
        print("Do you want to create a merged file?\n"
              "--input '1' for adding new subscriptions "
              "to the first collection and\n"
              "Not deleting anything from the first collection.\n"

              "--input '2' for adding new subscriptions"
              "And deleting from the first\n"
              "collection 'deleted subscriptions' (if they were found)\n"

              "--input '3' for not creating a merged file at all.\n")
        ans = input()

    new_data = {}
    if ans == "3":
        return

    for k, v0, v1 in repeated:
        new_data[k] = (v0, v1)

    for k, v0, v1 in added:
        new_data[k] = (v0, v1)

    if ans == "1":
        for k, v0, v1 in deleted:
            new_data[k] = (v0, v1)
    return new_data


def read_from_json(filename) -> dict:
    data_dict = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = json.loads(file.read())
        # print()
        for elem in reader['subscriptions']:
            url = elem['url']
            title = elem['name']
            id = url.split("/")[-1]
            data_dict[id] = (url, title)
    return data_dict


def write_to_json(dict_data) -> None:
    dict_j = {"subscriptions": [],
              "app_version": "0.19.8",
              "app_version_int": 953}
    for k, [v0, v1] in dict_data.items():
        dict_j["subscriptions"].append({"url": v0, "name": v1})
    data = json.dumps(dict_j)
    # print(data)
    with open("./util/merged_sub.json", "w", encoding="utf-8") as file:
        file.writelines(data)


def read_file(filename) -> dict:
    data = {}
    try:
        end = filename.split(".")[-1]
        if end == "csv":
            data = read_from_csv(filename)
        elif end == "json":
            data = read_from_json(filename)
        elif end == "db":
            data = read_from_sql(filename)
        else:
            return None
    except Exception as x:
        print(x)
    return data


def is_correct_name(name) -> bool:
    if not os.path.exists(name):
        print(f"{name} not exists")
        return False
    try:
        end = name.split(".")[-1]
        if end not in ("csv", "json", "db"):
            print("unfortunately, we can't work with file "
                  f"{name} and it's format {end}")
            return False
    except Exception as x:
        print(x)
        return False
    return True


def ask_convert_format() -> str:
    ans = ""
    while ans not in ("j", "c", "s"):
        print('Input "j" to save new subscriptions to merged_sub.json,\n'
              '"c" - to save it to merged_sub.csv,\n'
              '"s" - to save it to merged_sub.sql')
        ans = input()
    return ans


def write_data(format, merged) -> None:
    if format == "j":
        write_to_json(merged)
    elif format == "c":
        write_to_csv(merged)
    elif format == "s":
        write_to_sql(merged)


def main():
    filename_old = old_data = ""
    filename_new = ""
    # filename_old = "./util/combine.txt"
    filename_old = "./util/subs_old.csv"
    # filename_new = "./util/subs_new.csv"
    # filename_new = "./util/subs_new.db"
    filename_new = "./util/subs_old.json"

    if not is_correct_name(filename_new):
        return
    if not (filename_old == "" or is_correct_name(filename_old)):
        return

    old_data = read_file(filename_old) if filename_old else {}
    new_data = read_file(filename_new)
    repeated, added, deleted = compare_dicts(new_data, old_data)
    if (repeated, added, deleted) == (None, None, None):
        print("not merging")
        return
    merged = opts_merging(repeated, added, deleted)

    if not merged:
        print("not merging")
        return
    else:
        format = ask_convert_format()
        write_data(format, merged)
    return


if __name__ == "__main__":
    main()
