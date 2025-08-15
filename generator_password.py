import random
import string
import tkinter as tk
from tkinter import messagebox

from email.mime.text import MIMEText
import base64
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials/client_secret_614924706375-jq8bhmi12m85db2ocru4tneurrfedqhb.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def sendEmail(to, content):
    try:
        service = get_gmail_service()
        message = MIMEText(content)
        message['to'] = to
        message['subject'] = "Votre mot de passe généré"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw}
        service.users().messages().send(userId="me", body=message_body).execute()
        messagebox.showinfo("Succès", "E-mail envoyé avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {e}")

def generer_mot_de_passe(longueur=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe

def generer():
    try:
        longueur = int(entry_longueur.get())
        if longueur <= 0:
            raise ValueError
        mot_de_passe = generer_mot_de_passe(longueur)
        entry_resultat.delete(0, tk.END)
        entry_resultat.insert(0, mot_de_passe)
        to = entry_email.get()
        if to:
            sendEmail(to, "Mot de passe généré : " + mot_de_passe)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif.")

# Interface graphique
root = tk.Tk()
root.title("Générateur de mot de passe")

tk.Label(root, text="Longueur du mot de passe :").pack(padx=10, pady=5)
entry_longueur = tk.Entry(root)
entry_longueur.pack(padx=10, pady=5)

tk.Label(root, text="Adresse e-mail de destination :").pack(padx=10, pady=5)
entry_email = tk.Entry(root)
entry_email.pack(padx=10, pady=5)

btn_generer = tk.Button(root, text="Générer", command=generer)
btn_generer.pack(padx=10, pady=5)

tk.Label(root, text="Mot de passe généré :").pack(padx=10, pady=5)
entry_resultat = tk.Entry(root, width=30)
entry_resultat.pack(padx=10, pady=5)

root.mainloop()