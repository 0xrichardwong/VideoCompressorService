import socket
import sys
import os
import hashlib
from pathlib import Path
import glob
import shutil
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

def receive_file(sock, save_dir, filename):
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'wb') as f:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            f.write(data)
    print(f"File received and saved to {save_path}")

param_list = {
    "mp3": "Select file(e.g. cat.mp4): ",
    "compress": "Select file(e.g. cat.mp4): ",
    "resolution": "Select file(e.g. cat.mp4), width(e.g. 1280), height(e.g. 720): ",
    "aspect": "Select file(e.g. cat.mp4) and aspect ratio(e.g. 16:9): ",
    "GIF": "Select file(e.g. cat.mp4), starting time(e.g. 00:00:10) and duration (e.g. 5): ",
    "speed": "Select file(e.g. cat.mp4), speed(e.g. 2.0): "
}

def extract_output_header(header):
    filename_length = 32
    hash_length = 64
    # Extract and decode the filename, stripping any padding null bytes
    output_filename = header[:filename_length].rstrip(b'\x00').decode()
    # Extract and decode the file hash, stripping any padding null bytes
    output_file_hash = header[filename_length:filename_length + hash_length].rstrip(b'\x00').decode()
    return output_filename, output_file_hash

def main():

    dpath = 'received'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    # Connect the socket to the port where the server is listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        # receive output header
        output_header = sock.recv(96)
        print(output_header)
        output_filename, output_file_hash = extract_output_header(output_header)
        print(output_filename)
        print(output_file_hash)

        # receive output file
        receive_file(sock, '/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/received/',output_filename)

        # check if the received file is complete
        output_path = Path(glob.glob('received/*output*')[0])
        output_path = output_path.resolve()

        if hashFunc(output_path) == output_file_hash:
            print('Received file hash matches with the client hash.')
        else:
            print('Error: Please upload the file again.')

    finally:
        print('closing socket')
        sock.close()

# Run the upload function
main()
