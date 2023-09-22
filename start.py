import subprocess

def start_servers():
    # Start server.py
    server_process = subprocess.Popen(['python', 'server.py'])
    
    # Start video.py
    video_process = subprocess.Popen(['python', 'video.py'])

     # Start video.py
    sign_process = subprocess.Popen(['python', 'test2.py'])

     # Start video.py
    shpt_process = subprocess.Popen(['python', 'shpt.py'])

    # Wait for both processes to complete
    server_process.wait()
    video_process.wait()
    sign_process.wait()
    shpt_process.wait()

if __name__ == '__main__':
    start_servers()
