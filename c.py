import socket
import sys
import os
import hashlib
import json

# protocol_header() function formats the header information of the file to be sent to the server.
def protocol_header(filename, data_length, file_hash, json_data):
    filename_length = 32  # Define the byte size for the filename
    hash_length = 64  # Define the byte size for the hash (hexadecimal representation of SHA-256)
    data_length_size = 4  # Fixed size for data length
    json_length_size = 64  # Fixed size for JSON length to store the length of the JSON message

    # Encode filename and hash, padded with null bytes if necessary
    filename_bytes = filename.encode().ljust(filename_length, b'\x00')
    file_hash_bytes = file_hash.encode().ljust(hash_length, b'\x00')

    # Convert data length to bytes
    data_length_bytes = data_length.to_bytes(data_length_size, "big")

    # Encode the JSON data
    # json_bytes = json_data.encode('utf-8')
    json_bytes = json_data.encode().ljust(json_length_size, b'\x00')
    
    return filename_bytes + data_length_bytes + file_hash_bytes + json_bytes

def hashFunc(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

param_list = {
    "mp3": "Select file(e.g. cat.mp4): ",
    "compress": "Select file(e.g. cat.mp4): ",
    "resolution": "Select file(e.g. cat.mp4), width(e.g. 1280), height(e.g. 720): ",
    "aspect": "Select file(e.g. cat.mp4) and aspect ratio(e.g. 16:9): ",
    "GIF": "Select file(e.g. cat.mp4), starting time(e.g. 00:00:10) and duration (e.g. 5): ",
    "speed": "Select file(e.g. cat.mp4), speed(e.g. 2.0): "
}

def upload():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096 * 100

    print('connecting to {} port {}'.format(server_address, server_port))

    try:
        # After connection, the server and client can read and write to each other
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
        # File to be uploaded must be a text file and below 2GB
        filepath = '/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/cat.mp4'
        # filepath = input('Type in a file to upload: ')

        # 1. file name
        with open(filepath, 'rb') as f:
            filename = os.path.basename(f.name)

            # Move to the end of the file to get its size
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0, 0)

        # 2. file size
        if filesize > pow(2, 32):
            raise Exception('File must be below 2GB.')

        # 3. client hash
        clientHash = hashFunc(filepath)
        print('Client Hash:',clientHash)

        # 4. JSON
        edit_method = input('Choose from mp3/compress/resolution/aspect/GIF/speed: ')
        edit_params = input(param_list[edit_method]).split(',')

        message = {
            "method": edit_method,
            "params": edit_params
        }
        json_message = json.dumps(message)

        # Create header information using protocol_header() and send the header and filename to the server
        header = protocol_header(filename, filesize, clientHash, json_message)
        sock.send(header)
        print(header)

        # Send the file data in chunks
        with open(filepath, 'rb') as f:
            data = f.read(stream_rate)
            while data:
                print("Sending...")
                sock.send(data)
                data = f.read(stream_rate)

    finally:
        print('closing socket')
        sock.close()

# Run the upload function
upload()
