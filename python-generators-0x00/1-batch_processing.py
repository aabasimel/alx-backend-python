import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Each batch is a list of dictionaries (rows).
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bw123bw",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)  # fetch a chunk of rows
            if not batch:
                break
            yield batch  # yield the batch

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


## Write a function batch_processing() that processes each batch to filter users over the age of 25
def batch_processing(batch_size):
        for batch in stream_users_in_batches(batch_size):
            for user in batch:
                if user['age']>25:
                    yield user
                
               




