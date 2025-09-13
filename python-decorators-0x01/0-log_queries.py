import sqlite3
import functools



#decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)   #preserves the function name, docstring
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None) 
        if query:
            print(f'[LOG] Executing query: {query}')
        else:
            print("[LOG] query not provided")
        return func(*args, **kwargs) #call the original function
    return wrapper

@log_queries
def fetch_all_users(query):
    conn=sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users("SELECT *FROM users")
print(users)