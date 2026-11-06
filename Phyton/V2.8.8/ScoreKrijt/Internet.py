# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 22:48:50 2026

@author: BramI
"""

import socket
import smtplib
from email.message import EmailMessage
from tkinter import messagebox

def has_internet(timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False

def send_csv_via_email(csv_path, to_email, settings):
    try:
        if not settings['SenderMail'].get() or not settings['MailAppPassword'].get():
            raise RuntimeError(
                "Geen verzend-email ingesteld.\n"
                "Ga naar Instellingen → E-mail instellingen."
            )
        SENDER = settings['SenderMail'].get() 
        PASSWORD = settings['MailAppPassword'].get()  
    
        msg = EmailMessage()
        msg["Subject"] = "Biljart wedstrijd"
        msg["From"] = SENDER
        msg["To"] = to_email
        msg.set_content("Bijgevoegd het CSV bestand van de gespeelde wedstrijd.")
    
        with open(csv_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename=csv_path.split("/")[-1]
            )
    
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(SENDER, PASSWORD)
                smtp.send_message(msg)
    
            messagebox.showinfo("Gelukt", "Wedstrijd is verzonden via e-mail")
        except Exception as e:
            messagebox.showerror("Fout", f"Verzenden mislukt:\n{e}")
    
    except Exception as e:
        raise RuntimeError(str(e))