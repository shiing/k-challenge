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
        try:
            tmp_row = row[1].decode("ascii")
        except UnicodeDecodeError:
            invalid_row_count += 1
            # print("------- Invalid ascii data -------")
            # print(f"row id: {row[0]}")
            # print(f"row data: {row[1]}")
            continue

        if (tmp_row[0] == "$") and (tmp_row[-1] == ";"):
            tmp_str = tmp_row[1:-1]

            if tmp_str.find('$') != -1 or tmp_str.find(';') != -1:
                invalid_row_count += 1
        else:
            invalid_row_count += 1
            # print("------- Invalid ascii data -------")
            # print(f"row id: {row[0]}")
            # print(f"row data: {row[1]}")

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
            
            # Extract byte header
            header = data[0]
            
            # Extract 5-byte payload size and convert to int (little endian)
            payload_size_bytes = data[1:6]
            payload_size = int.from_bytes(payload_size_bytes, byteorder='little')  # or 'big'
            
            # Extract payload
            payload = data[6:]

            # Debug log
            # print(f"header: {header}")
            # print(f"payload size: {payload_size}")
            # print(f"payload length: {len(payload)}")
            
            # Validate
            if len(payload) != payload_size:
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