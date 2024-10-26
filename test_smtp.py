# test_smtp.py
import smtplib

smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "jdiaz@cidenet.com.co"
password = "wppm pucb cchs maxo"

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    print("Connected to SMTP server successfully")
    server.quit()
except Exception as e:
    print(f"Failed to connect to SMTP server: {e}")
