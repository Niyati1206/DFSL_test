import psycopg2
from psycopg2 import OperationalError, Error

def test_pgadmin_connection(host, port, database, user, password):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Create a cursor object using cursor() method
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT version();")

        # Fetch result
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL database. Server version: {db_version[0]}")

        # Close communication with the PostgreSQL database server
        cursor.close()
        conn.close()

    except OperationalError as e:
        print(f"Error connecting to PostgreSQL database: {e}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("PostgreSQL connection is closed")

# Example usage
if __name__ == "__main__":
    # Replace with your PostgreSQL connection details
    host = "localhost"
    port = "5432"
    database = "LetterGeneration"
    user = "DFSL_users"
    password = "admin"

    test_pgadmin_connection(host, port, database, user, password)
