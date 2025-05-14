import sqlite3
import constant


def init_db():
    conn = sqlite3.connect(constant.DB_PATH, check_same_thread=False)

    
    return conn


def validate_ascii_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM msg_ascii")

    rows = cursor.fetchall()

    invalid_row_count = 0
    
    for row in rows:
        
        if (row[1][0] != "$") or (row[1][-1] != ";"):
            # print("------- Invalid ascii data -------")
            # print(f"row id: {row[0]}")
            # print(f"row data: {row[1]}")
            invalid_row_count += 1

    print("-------------------------------------")
    print(f"Total ascii data count: {len(rows)}")
    print(f"Invalid ascii data count: {invalid_row_count}")
    print("-------------------------------------")

    return invalid_row_count

def validate_binary_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM msg_binary")

    rows = cursor.fetchall()

    invalid_row_count = 0
    
    for row in rows:
        
        filename = row[1]

        with open(filename, "rb") as f:
            data = f.read()
            
            try:
                data.decode("ascii")
            except Exception as e:
                # print(f"Error: {e}")
                # print("------- Invalid binary data -------")
                # print(f"row id: {row[0]}")
                # print(f"row data: {row[1]}")

                invalid_row_count += 1

    print("-------------------------------------")
    print(f"Total binary data count: {len(rows)}")
    print(f"Invalid binary data count: {invalid_row_count}")
    print("-------------------------------------")

    return invalid_row_count

def main():
    conn = init_db()

    try:
        validate_ascii_data(conn)
        validate_binary_data(conn)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
if __name__ == "__main__":
    main()