import socket
import os
from pathlib import Path
import hashlib
import json
import editor

def hashFunc(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def extract_header(header):
    filename_length = 32
    hash_length = 64
    data_length_size = 4
    json_length_size = 64
    # Extract and decode the filename, stripping any padding null bytes
    filename = header[:filename_length].rstrip(b'\x00').decode()
    # Extract and convert the data length from bytes to an integer
    data_length = int.from_bytes(header[filename_length:filename_length + data_length_size], "big")
    # Extract and decode the file hash, stripping any padding null bytes
    file_hash = header[filename_length + data_length_size:filename_length + data_length_size + hash_length].rstrip(b'\x00').decode()
    # Extract and convert the JSON length from bytes to an integer
    json_length = header[filename_length + data_length_size + hash_length:filename_length + data_length_size + hash_length + json_length_size].rstrip(b'\x00').decode()
    
    return filename, data_length, file_hash, json_length

def upload():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096 * 100

    dpath = 'temp'
    if not os.path.exists(dpath):
        os.makedirs(dpath)
    print('Starting up on {} port {}'.format(server_address, server_port))

    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            header = connection.recv(164)
            filename, data_length, clientHash, json = extract_header(header)

            print("Extracted Filename:", filename)
            print("Extracted Data Length:", data_length)
            print("Extracted Hash:", clientHash)
            print("Extracted JSON:", json)

            filepath = os.path.join(dpath, filename)
            with open(filepath, 'wb+') as f:
                while data_length > 0:
                    data = connection.recv(min(data_length, stream_rate))
                    f.write(data)
                    print('received {} bytes'.format(len(data)))
                    data_length -= len(data)

            print('Finished uploading the file from client.')

            if hashFunc(filepath) == clientHash:
                print('Received file hash matches with client hash')
            else:
                print('Error: Please upload the file again.')
                continue

            """
            # Receive the JSON message after file data\
            json_data = connection.recv(json_length)
            json_message = json_data.decode('utf-8')
            message = json.loads(json_message)
            return print("Extracted JSON Message:", message)

            edit_method = message['method']
            edit_method = globals()[edit_method]
            edit_params = message['params']

            edit_method(*edit_params)
            """

        except Exception as e:
            print('Error: ' + str(e))

        finally:
            print("Closing current connection")
            connection.close()

upload()
