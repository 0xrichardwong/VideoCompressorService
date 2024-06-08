
https://github.com/0xrichardwong/VideoManipulator/assets/24628052/f6953b27-73a8-4379-afc8-3495b258c27e


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>

<h1>Video Compressor and Editor</h1>

<p>This project is a video editor, designed to handle video file reception over a socket, apply various editing functions, and send the edited file back to the client. The project is implemented in Python and supports various video editing functionalities such as compression, resolution change, aspect ratio adjustment, and format conversion.</p>

<h2 id="features">Features</h2>
<ul>
    <li>Receive video files over a socket connection</li>
    <li>Apply various editing functions:
        <ul>
            <li>Convert to MP3</li>
            <li>Compress file size</li>
            <li>Change resolution</li>
            <li>Adjust aspect ratio</li>
            <li>Convert to GIF</li>
            <li>Change playback speed</li>
        </ul>
    </li>
    <li>Send the edited video file back to the client</li>
    <li>Verify file integrity using SHA-256 hashing</li>
</ul>

<h2 id="usage">Usage</h2>
<ol>
    <li>Start the server:
        <pre><code>python s.py</code></pre>
    </li>
    <li>The server will listen for incoming connections on the specified port (default is <code>9001</code>).</li>
    <li>When a client connects and sends a video file along with the desired editing instructions, the server will:
        <ul>
            <li>Receive the file and verify its integrity</li>
            <li>Apply the specified editing functions</li>
            <li>Send the edited file back to the client</li>
        </ul>
    </li>
    <li>Example client code for sending a file to the server can be found in <code>c.py</code>.</li>
</ol>

<h2 id="api-reference">API Reference</h2>
<h3>Functions</h3>
<ul>
    <li><code>receive_file(sock, save_dir, filename)</code>: Receives a file over a socket and saves it to the specified directory.</li>
    <li><code>hashFunc(filepath)</code>: Computes the SHA-256 hash of the file at the given path.</li>
    <li><code>extract_header(header)</code>: Extracts the filename, data length, file hash, and JSON length from the header.</li>
    <li><code>handle_request(function_name, params)</code>: Calls the appropriate editing function based on the provided method name and parameters.</li>
    <li><code>generate_output_header(filename, file_hash)</code>: Generates a header for the output file, including the filename and hash.</li>
    <li><code>delete_temp()</code>: Deletes the temporary directory used for storing files during processing.</li>
    <li><code>send_file(sock, file_path)</code>: Sends a file over a socket.</li>
</ul>

<h3>Editing Functions in <code>editor.py</code></h3>
<ul>
    <li><code>convert_to_mp3(params)</code>: Converts the video to MP3 format.</li>
    <li><code>compressSize(params)</code>: Compresses the video file size.</li>
    <li><code>changeResolution(params)</code>: Changes the video resolution.</li>
    <li><code>changeAspectRatio(params)</code>: Adjusts the video aspect ratio.</li>
    <li><code>convert_to_GIF(params)</code>: Converts the video to GIF format.</li>
    <li><code>change_speed(params)</code>: Changes the video playback speed.</li>
</ul>

</body>
</html>
