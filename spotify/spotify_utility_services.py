from ftplib import FTP_TLS
import paramiko
import os
import csv
import glob

# Convert csv data to html
def output_to_html(csvfile):
    # Get base filename, without csv extension
    htmlfile = csvfile.replace(".csv",".html")
    # Read data from CSV file
    with open(csvfile, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)

    # Generate HTML table
    html_table = "<table>\n"
    for row in data:
        html_table += "  <tr>\n"
        for col in row:
            if col.startswith("http"):
               html_table += f"    <td><a href=\"{col}\"> {col}</a></td>\n"
            else:
               html_table += f"    <td>{col}</td>\n"
        html_table += "  </tr>\n"
    html_table += "</table>"

    # Generate complete HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Current Top Tracks - My Spotify</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Current Top Tracks - My Spotify</h1>
        {html_table}
    </body>
    </html>
    """

    # Write HTML content to file
    with open(htmlfile, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    return htmlfile

# Uses paramiko library
# Upload single file
def sftp_upload(host, port, username, password, local_path, remote_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        sftp.put(local_path, os.path.join(remote_path, os.path.basename(local_path)))
        print(f"File uploaded successfully from {local_path} to {remote_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")
    finally:
        sftp.close()
        transport.close()

# Upload multiple files using wildcard
def sftp_upload_mult(host, port, username, password, file_pattern, remote_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        local_files = glob.glob(file_pattern)

        for local_file in local_files:
            # Extract the filename from the local path
            filename = os.path.basename(local_file)
            
            # Upload the file to the remote path
            sftp.put(local_file, os.path.join(remote_path, filename))
            print(f"File '{filename}' uploaded successfully to {remote_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")
    finally:
        sftp.close()
        transport.close()


# uses ftplib
def sftp_uploadx(host, port, username, password, local_path, remote_path):
    # Connect to the SFTP server
    ftp = FTP_TLS()
    ftp.connect(host, port)
    ftp.login(username, password)

    # Switch to binary mode for non-text files
    ftp.sendcmd("TYPE I")

    # Change to the remote directory
    ftp.cwd(remote_path)

    # Open the local file for binary read
    with open(local_path, 'rb') as local_file:
        # Upload the local file to the remote server
        ftp.storbinary(f"STOR {os.path.basename(local_path)}", local_file)

    # Close the connection
    ftp.quit()
    print(f"File uploaded successfully from {local_path} to {remote_path}")

