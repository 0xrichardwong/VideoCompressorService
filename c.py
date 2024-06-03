import socket
import sys
import os

# protocol_header()という関数は、サーバに送信されるファイルのヘッダ情報をフォーマットするために使用されます。このヘッダは、ファイル名の長さ（バイト）、JSONデータの長さ（バイト）、データの長さ（バイト）の3つの値で構成されます。これらの値は、to_bytes()メソッドを用いてバイナリに変換され、1つの64ビットバイナリに結合されます。
def protocol_header(filename_length, data_length):
    return filename_length.to_bytes(1, "big") + data_length.to_bytes(3,"big")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # サーバが待ち受けているポートにソケットを接続します
    packetSize = 4096
    server_address = '0.0.0.0'
    server_port = 9001
    print('connecting to {}'.format(server_address, server_port))

    try:
        # 接続後、サーバとクライアントが相互に読み書きができるようになります 
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
        # ファイルを送信する場合は、2^32までに制限してください
        filepath = input('Type in a file to upload: ')
        if print(filepath[-4:]) != '.mp4':
            return print("Unsupported file type. Please upload .mp4")

        # バイナリモードでファイルを読み込む
        with open(filepath, 'rb') as f:
            # ファイルの末尾に移動し、tellは開いているファイルの現在位置を返します。ファイルのサイズを取得するために使用します
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0,0)

            # ファイルサイズが大きくなりすぎることの警告
            if filesize > pow(2,32):
                raise Exception('File must be below 2GB.')

            filename = os.path.basename(f.name)

            # ファイル名からビット数
            filename_bits = filename.encode('utf-8')
            # protocol_header()関数を用いてヘッダ情報を作成し、ヘッダとファイル名をサーバに送信します。
            header = protocol_header(len(filename_bits), filesize)

            # ヘッダの送信
            sock.send(header)
            # ファイル名の送信
            sock.send(filename_bits)

            # 一度にpacketSizeずつ読み出し、送信することにより、ファイルを送信します。Readは読み込んだビットを返します
            data = f.read(packetSize)
            while data:
                print("Sending...")
                sock.send(data)
                data = f.read(packetSize)

    finally:
        print('closing socket')
        sock.close()

main()