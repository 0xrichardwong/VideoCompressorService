import socket
import sys
import os
import hashlib

# protocol_header() function formats the header information of the file to be sent to the server.
def protocol_header(filename, data_length, hash, json_length):
    filename_length = 32  # Define the byte size for the filename
    hash_length = 64  # Define the byte size for the hash (hexadecimal representation of SHA-256)
    data_length_size = 4  # Fixed size for data length
    json_size = 64  # Fixed size for JSON length

    filename_bytes = filename.encode().ljust(filename_length, b'\x00')
    return filename_bytes + data_length.to_bytes(data_length_size, "big") + hash.encode().ljust(hash_length, b'\x00') + json_length.to_bytes(json_size, "big")

def hashFunc(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def upload():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096 * 10

    print('connecting to {} port {}'.format(server_address, server_port))

    try:
        # After connection, the server and client can read and write to each other
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
        # File to be uploaded must be a text file and below 2GB

        filepath = '/home/ubuntu/mydir/Backend2/Video/cat.mp4'
        # filepath = input('Type in a file to upload: ')

        with open(filepath, 'rb') as f:
            filename = os.path.basename(f.name)

            # Move to the end of the file to get its size
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0, 0)

            if filesize > pow(2, 32):
                raise Exception('File must be below 2GB.')

            clientHash = hashFunc(filepath)

            # Create header information using protocol_header() and send the header and filename to the server
            header = protocol_header(filename, filesize, clientHash, 0)
            print(header)
        

            """
            def extract_header(header):
                filename_length = 32  # Define the byte size for the filename
                hash_length = 64  # Define the byte size for the hash (hexadecimal representation of SHA-256)
                data_length_size = 4  # Fixed size for data length
                json_size = 64  # Fixed size for JSON length
                
                filename = header[:filename_length].rstrip(b'\x00').decode()  # Remove padding and decode
                data_length = int.from_bytes(header[filename_length:filename_length + data_length_size], "big")
                hash = header[filename_length + data_length_size:filename_length + data_length_size + hash_length].decode()
                json = int.from_bytes(header[filename_length + data_length_size + hash_length:filename_length + data_length_size + hash_length + json_size], "big")
                return filename, data_length, hash, json

            # Extract the components from the header
            extracted_filename, extracted_data_length, extracted_hash, extracted_json = extract_header(header)

            print("Extracted Filename:", extracted_filename)
            print("Extracted Data Length:", extracted_data_length)
            print("Extracted Hash:", extracted_hash)
            print("Extracted JSON:", extracted_json)

            return print("well done")
            """

            # Send the header
            sock.send(header)

            # Send the file data in chunks
            data = f.read(stream_rate)
            while data:
                print("Sending...")
                sock.send(data)
                data = f.read(stream_rate)

    finally:
        print('closing socket')
        sock.close()


# def download():

upload()
