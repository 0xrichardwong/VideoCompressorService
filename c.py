import socket
import sys
import os
import hashlib

# protocol_header()という関数は、サーバに送信されるファイルのヘッダ情報をフォーマットするために使用されます。このヘッダは、ファイル名の長さ（バイト）、JSONデータの長さ（バイト）、データの長さ（バイト）の3つの値で構成されます。これらの値は、to_bytes()メソッドを用いてバイナリに変換され、1つの64ビットバイナリに結合されます。
def protocol_header(filename_length, data_length, hash_length, json_length):
    return filename_length.to_bytes(4, "big") + data_length.to_bytes(4,"big") + hash_length.to_bytes(32,"big") + json_length.to_bytes(4,"big")

def hashFunc(filepath):
    # Convert filepath to bytes before hashing
    with open(filepath, 'rb') as f:
        file_data = f.read()  # Read the entire file as bytes
    return hashlib.sha256(file_data).hexdigest()

def upload():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # サーバが待ち受けているポートにソケットを接続します
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096*10

    print('connecting to {}'.format(server_address, server_port))

    try:
        # 接続後、サーバとクライアントが相互に読み書きができるようになります 
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
        # ファイルを送信する場合は、テキストファイルで2GB以下に制限してください
        filepath = input('Type in a file to upload: ')

        # バイナリモードでファイルを読み込む
        with open(filepath, 'rb') as f:
            # ファイルの末尾に移動し、tellは開いているファイルの現在位置を返します。ファイルのサイズを取得するために使用します
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0,0)

            if filesize > pow(2,32):
                raise Exception('File must be below 2GB.')

            filename = os.path.basename(f.name)

            # ファイル名からビット数
            filename_bits = filename.encode('utf-8')

            # protocol_header()関数を用いてヘッダ情報を作成し、ヘッダとファイル名をサーバに送信します。
            # protocol_header(filename_length, data_length, hash_length, json_length)
            header = protocol_header(len(filename_bits), filesize, hashFunc(filepath), 0)
            return print(header)

            # ヘッダの送信、ファイル名の送信
            sock.send(header)
            sock.send(filename_bits)

            # 一度にstream_rateバイトずつ読み出し、送信することにより、ファイルを送信します。Readは読み込んだビットを返します
            data = f.read(stream_rate)
            while data:
                print("Sending...")
                sock.send(data)
                data = f.read(stream_rate)

    finally:
        print('closing socket')
        sock.close()

upload()