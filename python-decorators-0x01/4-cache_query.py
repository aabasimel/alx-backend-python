import time
import sqlite3
import functools

query_cache = {}
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn= sqlite3.connect('users.db')
        try:
            result= func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper



def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        print(f"[CACHE BEFORE] {query_cache}")
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            print("Current cache:", query_cache)
            return query_cache[query]
        
        print(f"[CACHE MISS] Executing and caching result for: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


### First call will cache the result

users = fetch_users_with_cache(query="SELECT * FROM users")

### Second call will use the cached result

users_again = fetch_users_with_cache(query="SELECT * FROM users")