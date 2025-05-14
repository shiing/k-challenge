import socket
import sqlite3
import threading
import time
import constant
import os


def init_db():
    conn = sqlite3.connect(constant.DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS msg_ascii (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT NOT NULL,
            updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS msg_binary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename VARCHAR(50) NOT NULL,
            updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    
    return conn

def insert_msg_binary_table(conn, filename):
    cursor = conn.cursor()

    # print(f"sql command: INSERT INTO msg_binary (filename) VALUES (\'{filename}\')")

    cursor.execute("INSERT INTO msg_binary (filename) VALUES (?)", (filename,))
    conn.commit()

def insert_msg_ascii_table(conn, payload):
    cursor = conn.cursor()    

    # print(f"sql command: INSERT INTO msg_ascii (payload) VALUES (\'{payload}\')")

    cursor.execute("INSERT INTO msg_ascii (payload) VALUES (?)", (payload,))
    conn.commit()

def parse_ascii_data(data, sock):

    end_index = None
    remaining_buffer = None
    
    while True:
        payload = sock.recv(6)

        try:
            end_index = payload.decode('ascii').find(";")
        except UnicodeDecodeError:
            for i in range(0, 6):
                try:
                    end_index = payload[i].decode('ascii').find(";")
                except UnicodeDecodeError:
                    continue
        
        if end_index == -1:
            data += payload
            continue

        data += payload[:end_index + 1]
        remaining_buffer = payload[end_index + 1:]
        # print(f"parse_ascii_data: {data}")
        # print(f"remaining_buffer: {remaining_buffer}")
        break

    return data, remaining_buffer
    

def parse_bytes_data(data, sock):
    remaining_buffer = None

    current_data_type = None
    # Parse header, 1 byte
    header = data[0]
    print(f"Header: 0x{header:02X}")

    # Parse payload size, 5 bytes
    payload_size_bytes = data[1:6]
    payload_size = int.from_bytes(payload_size_bytes, byteorder='little')
    print(f"Payload Size: {payload_size} bytes")

    # Parse payload
    payload = data
    payload_count = len(payload) - 6

    # Use timestamp to create filename
    ts = time.time()
    print(f"Filename: {ts}.txt")

    # Write payload to file
    with open(f"{constant.BINARY_FILE_PATH}/{ts}.txt", "wb") as f:
        f.write(payload)

        while payload_count < payload_size:
            payload = sock.recv(6)
            payload_count += len(payload)

            if payload_count >= payload_size:
                payload_offset = 6 - (payload_count - payload_size)
                print(f"payload count: {payload_count}")
                print(f"payload size: {payload_size}")
                print(f"payload: {payload}")
                f.write(payload[:payload_offset])
                print(f"payload write: {payload[:payload_offset]}")
                remaining_buffer = payload[payload_offset:]
                print(f"remaining_buffer: {remaining_buffer}")
            else:
                f.write(payload)

    return f"{constant.BINARY_FILE_PATH}/{ts}.txt", remaining_buffer


def receive_messages(sock, db_conn):
    current_buffer = None
    is_binary = None
    while True:
        current_data_type = None
        data = None

        if current_data_type is None:
            data = sock.recv(6)
        elif current_buffer is not None and len(current_buffer) > 0:
            data = current_buffer

        print(f"Data: {data}")

        try:
            data.decode('ascii')
            is_binary = False
        except UnicodeDecodeError:
            is_binary = True

        if is_binary == False and data.decode('ascii')[0] == '$':
            current_data_type = "ascii"
            ascii_data, current_buffer = parse_ascii_data(data, sock)
            insert_msg_ascii_table(db_conn, ascii_data)
        else:
            current_data_type = "binary"
            filename, current_buffer = parse_bytes_data(data, sock)
            insert_msg_binary_table(db_conn, filename)

                


def run_client():
    db_conn = init_db()
    client_socket = None
    is_connected = False

    try:
        os.mkdir(constant.BINARY_FILE_PATH)
    except FileExistsError:
        pass

    host = constant.HOST
    port = constant.PORT
    jwt_token = constant.JWT_TOKEN

    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Jwt token: {jwt_token}")
    print("-------------------------------------")

    try:
        while True:
            cmd = input("Enter command (connect, talk, stop, exit): ").strip()

            if cmd == "connect" and not is_connected:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((host, int(port)))
                    is_connected = True
                    print("Connected to server\n")
                except Exception as e:
                    print(f"Connection failed: {e}")

            elif cmd == "talk" and is_connected:
                try:
                    client_socket.sendall(f"AUTH {jwt_token}".encode())
                    print("Auth success")

                    # Start receiver thread
                    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket, db_conn), daemon=True)
                    receiver_thread.start()
                    print("Start receive messages")
                except Exception as e:
                    print(f"Auth failed: {e}")


            elif cmd == "stop" and is_connected:
                try:
                    client_socket.sendall("STATUS".encode())
                    print("Stop talking success")
                except Exception as e:
                    print(f"Stop talking failed: {e}")

            elif cmd == "exit":
                print("Exiting")
                break

            else:
                print("Invalid command")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if is_connected:
            client_socket.close()

        db_conn.close()

if __name__ == "__main__":
    run_client()