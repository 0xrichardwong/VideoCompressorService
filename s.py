import socket
import os
from pathlib import Path
import hashlib
import video_editor
import json

def hashFunc(filepath):
    # Convert filepath to bytes before hashing
    with open(filepath, 'rb') as f:
        file_data = f.read()  # Read the entire file as bytes
    return hashlib.sha256(file_data).hexdigest()

def extract_header(header):
    filename_length = 32  # Define the byte size for the filename
    hash_length = 64  # Define the byte size for the hash (hexadecimal representation of SHA-256)
    data_length_size = 4  # Fixed size for data length
    json_size = 4  # Fixed size for JSON length
    total_length = filename_length+hash_length+data_length_size+json_size
    
    filename = header[:filename_length].rstrip(b'\x00').decode()  # Remove padding and decode
    data_length = int.from_bytes(header[filename_length:filename_length + data_length_size], "big")
    hash = header[filename_length + data_length_size:filename_length + data_length_size + hash_length].decode()
    json = int.from_bytes(header[filename_length + data_length_size + hash_length:filename_length + data_length_size + hash_length + json_size], "big")
    return filename, data_length, hash, json

def upload():
    # まず、必要なモジュールをインポートし、ソケットオブジェクトを作成して、アドレスファミリ（AF_INET）とソケットタイプ（SOCK_STREAM）を指定します。サーバのアドレスは、任意のIPアドレスからの接続を受け入れるアドレスである0.0.0.0に設定し、サーバのポートは9001に設定されています。
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096*100

    # 次に、現在の作業ディレクトリに「temp」という名前のフォルダが存在するかどうかをチェックします。存在しない場合は、os.makedirs() 関数を使用してフォルダを作成します。このフォルダは、クライアントから受信したファイルを格納するために使用されます。
    dpath = 'temp'
    if not os.path.exists(dpath):
        os.makedirs(dpath)
    print('Starting up on {} port {}'.format(server_address, server_port))

    # 次に、サーバは bind()関数を使用して、ソケットをサーバのアドレスとポートに紐付けします。その後、listen()関数を呼び出すことで、サーバは着信接続の待ち受けを開始します。サーバは一度に最大1つの接続を受け入れることができます。
    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        # その後、サーバは無限ループに入り、クライアントからの着信接続を継続的に受け付けます。このコードでは、accept()関数を使用して、着信接続を受け入れ、クライアントのアドレスを取得します。

        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # 次に、クライアントから受信したデータのヘッダを読み取り、変数headerに格納します。ヘッダには、ファイル名の長さ、JSON データの長さ、クライアントから受信するデータの長さに関する情報が含まれています。
            header = connection.recv(164)
            filename, data_length, clientHash, json = extract_header(header)

            print("Extracted Filename:", filename)
            print("Extracted Data Length:", data_length)
            print("Extracted Hash:", clientHash)
            print("Extracted JSON:", json)

            # 次に、コードはクライアントから受け取ったファイル名で新しいファイルをtempフォルダに作成します。このファイルは、withステートメントを使用してバイナリモードで開かれ、write()関数を使用して、クライアントから受信したデータをファイルに書き込みます。データはrecv()関数を使用して塊単位で読み込まれ、データの塊を受信するたびにデータ長がデクリメントされます。
            # w+は終了しない場合はファイルを作成し、そうでない場合はデータを切り捨てます
            with open(os.path.join(dpath, filename),'wb+') as f:
                # すべてのデータの読み書きが終了するまで、クライアントから読み込まれます
                while data_length > 0:
                    data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                    f.write(data)
                    print('recieved {} bytes'.format(len(data)))
                    data_length -= len(data)
                    print(data_length)

            print('Finished uploading the file from client.')

            # checking the hash of the file 
            uploadedFilePath = '/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/cat.mp4'
            if hashFunc(uploadedFilePath) != clientHash:
                return print('Error: Please upload the file again.')
            

            """
            # edit the video

            # convert_to_mp3('cat.mp4')
            # compressSize('cat.mp4')
            # changeResolution('cat.mp4', 1280, 720)
            # changeAspectRatio('cat.mp4', '16:9')
            # convert_to_GIF('cat.mp4', '00:00:10', '5')
            # change_speed('cat.mp4', 2.0)

            edit_method = json[method]
            edit_params = json[params]

            message = {
                "method": method,
                "params": params,
            }
            """

        except Exception as e:
            print('Error: ' + str(e))

        finally:
            print("Closing current connection")
            connection.close()

upload()
