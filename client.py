import socket
import sqlite3
import threading
import time
import constant


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

    print(f"sql command: INSERT INTO msg_binary (filename) VALUES (\'{filename}\')")

    cursor.execute("INSERT INTO msg_binary (filename) VALUES (?)", (filename,))
    conn.commit()

def insert_msg_ascii_table(conn, payload):
    cursor = conn.cursor()    

    print(f"sql command: INSERT INTO msg_ascii (payload) VALUES (\'{payload}\')")

    cursor.execute("INSERT INTO msg_ascii (payload) VALUES (?)", (payload,))
    conn.commit()

def save_bytes_data(data, sock):
    # Parse header, 1 byte
    header = data[0]
    print(f"Header: 0x{header:02X}")

    # Parse payload size, 5 bytes
    payload_size_bytes = data[1:6]
    payload_size = int.from_bytes(payload_size_bytes, byteorder='little')
    print(f"Payload Size: {payload_size} bytes")

    # Parse payload
    payload = data[6:]
    payload_count = len(payload)

    # Use timestamp to create filename
    ts = time.time()
    print(f"Filename: file_{ts}.txt")

    # Write payload to file
    with open(f"file_{ts}.txt", "wb") as f:
        f.write(payload)

        while payload_count < payload_size:
            payload = sock.recv(1024)
            payload_count += len(payload)
            f.write(payload)

    return f"file_{ts}.txt"


def receive_messages(sock, db_conn):
    while True:
        data = None
        try:
            data = sock.recv(1024)
            if not data:
                print("Server closed the connection.")
                break

            message = data.decode('utf-8').strip()
            print(f"Ascii data")
            insert_msg_ascii_table(db_conn, message)
            
        except Exception as e:
            print(f"Binary data")
            file_name = save_bytes_data(data, sock)
            insert_msg_binary_table(db_conn, file_name)


def run_client():
    db_conn = init_db()
    client_socket = None
    is_connected = False

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