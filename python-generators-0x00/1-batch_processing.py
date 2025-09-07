import mysql.connector

def batch_process_users(batch_size):
        """Generator that streams rows from user_data in batches of batch_size"""
        conn=None
        cursor=None
        try:
                conn=mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Sh123&*abc",
                        database="ALX_prodev"
                )
                cursor=conn.cursor(dictionary=True)
                cursor.execute("SELECT *FROM user_data")
                
                batch=[]
                for row in cursor:
                        batch.append(row)
                        if len(batch)==batch_size:
                                yield batch
                                batch=[]
                if batch:
                        yield batch
        except Exception as e:
                print(f"Error: {e}")
        finally:
                if cursor:
                        cursor.close()
                if conn and conn.is_connected():
                        conn.close()

## Write a function batch_processing() that processes each batch to filter users over the age of25`
def batch_processing(batch_size):
        for batch in batch_process_users(batch_size):
                filtered_users=[user for user in batch if user['age']>25]
                for user in filtered_users:
                        print(user)
               




