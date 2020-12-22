import sqlite3
from settings import get_startup

query_dict = {
    'rss_information_create': """
    CREATE TABLE rss_information(id integer primary key autoincrement, name text, url text)""",
    'rss_add': """
    INSERT INTO rss_information (name, url)
    VALUES (\"{name}\", \"{url}\")
    """,
    'rss_list': """
    SELECT * FROM rss_information
    """,
    'rss_del': """
    DELETE FROM rss_information WHERE id is {id}
    """,
    'rss_log_create': """
    CREATE TABLE rss_log(id integer primary key autoincrement, rss_org integer, post_title text, post_published text)
    """,
    'rss_log_insert': """
    INSERT INTO rss_log (rss_org, post_title, post_published)
    VALUES ({rss_org}, \"{post_title}\", \"{post_published}\")
    """,
    'rss_log_search': """
    SELECT * FROM rss_log 
    WHERE rss_org=\"{rss_org}\" 
    AND post_title=\"{post_title}\" 
    AND post_published=\"{post_published}\"
    """,
    'rss_log_del': """
    DELETE FROM rss_log WHERE rss_org is {rss_org}
    """,
}


def startup():
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_information_create'])
        cur.execute(query_dict['rss_log_create'])
    except sqlite3.OperationalError as e:
        print(f"{e}")

    try:
        cur.execute(query_dict['rss_log_create'])
    except sqlite3.OperationalError as e:
        print(f"{e}")

    con.commit()
    con.close()


def add_query(name, url):
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_add'].format(name=name, url=url))
        res = True
        msg = None
    except sqlite3.OperationalError as e:
        msg = f"예외 발생: {e}"
        res = False
    finally:
        con.commit()
        con.close()

    return res, msg


def del_query(id):
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_del'].format(id=id))
        cur.execute(query_dict['rss_log_del'].format(rss_org=id))
        res = True
        msg = None
    except sqlite3.OperationalError as e:
        msg = f"예외 발생: {e}"
        res = False
    finally:
        con.commit()
        con.close()

    return res, msg


def list_query():
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_list'])
        res = cur.fetchall()
        msg = None
    except sqlite3.OperationalError as e:
        msg = f"예외 발생: {e}"
        res = None
    finally:
        con.commit()
        con.close()

    return res, msg


def log_update(rss_org, post_title, post_published):
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_log_insert'].format(
            rss_org=rss_org, post_title=post_title, post_published=post_published)
        )
        res = True
        msg = None
    except sqlite3.OperationalError as e:
        msg = f"예외 발생: {e}"
        res = False
    finally:
        con.commit()
        con.close()

    return res, msg


def has_log(rss_org, post_title, post_published):
    con = sqlite3.connect(get_startup()['db_name'])
    cur = con.cursor()
    try:
        cur.execute(query_dict['rss_log_search'].format(
            rss_org=rss_org, post_title=post_title, post_published=post_published)
        )
        res = True if any(cur.fetchall()) else False
    except sqlite3.OperationalError as e:
        res = None
    finally:
        con.commit()
        con.close()

    return res
