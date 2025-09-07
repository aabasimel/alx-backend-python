
seed = __import__('seed')

def paginate_users(page_size, offset):
        """
    Fetch a page of users from the database.

    Args:
        page_size (int): Number of users per page
        offset (int): Row offset in the table

    Returns:
        list of dict: List of user rows
    """
        connection=seed.connect_to_prodev()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows=cursor.fetchall()
        cursor.close()
        connection.close()
        return rows


def paginate_users(page_size, offset):
         """
    Generator that lazily fetches users from the database page by page.

    Args:
        page_size (int): Number of users per page

    Yields:
        list of dict: One page of users at a time
    """
         offset=0
         while True:
                 page=paginate_users(page_size, offset)
                 if not page:
                         break
                 yield page
                 offset+=page_size # move the offset to next page
         return 

