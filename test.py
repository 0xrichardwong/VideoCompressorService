import hashlib

filename_length = 32  # Define the byte size for the filename
hash_length = 64  # Define the byte size for the hash (hexadecimal representation of SHA-256)
data_length_size = 4  # Fixed size for data length
json_size = 64  # Fixed size for JSON length

def protocol_header(filename, data_length, hash, json):
    # Pad the filename to the defined size
    filename_bytes = filename.encode().ljust(filename_length, b'\x00')
    return filename_bytes + data_length.to_bytes(data_length_size, "big") + hash.encode() + json.to_bytes(json_size, "big")

def hashFunc(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

filename = 'cat.mp4'
filesize = 211260
hash = hashFunc(filename)

header = protocol_header(filename, filesize, hash, 0)

print(header)

def extract_header(header):
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
