import mysql.connector
def stream_users():
        """Generator that streams rows from user_data table one by one"""
        try:
                conn=mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Sh123&*abc",
                        database="Alx_prodev"

                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM user_data")                
                for row in cursor:
                        yield row
        except Exception as e:
                print(f"Error: {e}")
        finally:
                if cursor:
                        cursor.close()
                if conn and conn.is_connected():
                        conn.close()
    

            

