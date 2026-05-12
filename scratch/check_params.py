import sqlite3

def check_params():
    try:
        conn = sqlite3.connect('comun.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vhv_parameters ORDER BY id DESC LIMIT 1;")
        row = cursor.fetchone()
        print(f"Parameters: {row}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_params()
