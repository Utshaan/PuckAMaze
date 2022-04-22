from screen import resource_path
from ftplib import FTP
from encryption_functions import Clyde_decrypt
from rich import print

url = "files.000webhost.com"
username = "C#0E0G#0C0Eb0G0F#1A1C#2G0Bb0D1G0Bb0D1Ab0Cb0Eb1G1Bb1D2G1Bb1D2E0G0B0F1Ab1C2"
password = "A0C#1E1C0E0G0C#0F0G#0C0E0G0D0F#0A0G0B0D1C#0F0G#0Ab0C1Eb1D0F#0A0C0E0G0C0E0G0C0E0G0D0F#0A0"
def login_ftp():
    global ftp_manager
    done = False
    max_tries = 15
    while not done and max_tries > 0:
        try:
            ftp_manager = FTP(url, Clyde_decrypt(username), Clyde_decrypt(password))
            done = True
        except Exception as e:
            max_tries -=1
            print(f"Error: {e}")
    

def quit_ftp():
    ftp_manager.quit()

def ftp_update_site():
    try:
        ftp_manager.cwd("/public_html/")
        with open(resource_path("Assets/index.html"), "rb") as htmlfile:
            ftp_manager.storbinary("STOR index.html", htmlfile)
        ftp_manager.cwd("/public_html/Assets/")
        with open(resource_path("Assets/passwords.json"), "rb") as passwords:
            ftp_manager.storbinary("STOR passwords.json", passwords)
    finally:
        pass

def ftp_get_siteData():
    try:
        ftp_manager.cwd("/public_html/")
        with open(resource_path("Assets/index.html"), "wb") as htmlfile:
            ftp_manager.retrbinary("RETR index.html", htmlfile.write)
        ftp_manager.cwd("/public_html/Assets/")
        with open(resource_path("Assets/passwords.json"), "wb") as passwords:
            ftp_manager.retrbinary("RETR passwords.json", passwords.write)
    finally:
        pass
