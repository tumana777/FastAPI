import time
from datetime import datetime

def send_email(email):
    print("Sending email...")
    time.sleep(5)
    print(f"Email sent to {email}")

def write_log(username):
    print("Writing log...")
    time.sleep(3)

    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - User {username} registered \n")