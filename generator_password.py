import random
import pyttsx3
import string
import tkinter as tk
from tkinter import messagebox

from email.mime.text import MIMEText
import base64
import json
import os
import time

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import hvac

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_KV_PATH = os.getenv("VAULT_KV_PATH", "gmail/myapp")  # correspond à secret/gmail/myapp
client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

def read_client_credentials_json_from_vault():
    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed.")
    # KV v2 -> resp['data']['data']
    resp = client.secrets.kv.v2.read_secret_version(path=VAULT_KV_PATH)
    data = resp["data"]["data"]
    raw = data.get("client_credentials_json")
    if raw is None:
        raise KeyError("Missing 'client_credentials_json' in Vault secret.")
    # raw peut être soit un dict (si écrit via API), soit une chaîne JSON
    if isinstance(raw, str):
        creds_dict = json.loads(raw)
    else:
        creds_dict = raw
    return creds_dict

def get_gmail_service():
    creds = None
    client_config = read_client_credentials_json_from_vault()
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def sendEmail(to, content):
    try:
        engine = pyttsx3.init() # Initialisation du moteur de synthèse vocale   
        service = get_gmail_service()
        message = MIMEText(content)
        message['to'] = to
        message['subject'] = "Votre mot de passe généré"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw}
        service.users().messages().send(userId="me", body=message_body).execute()
        message_succes = "E-mail envoyé avec succès !"
        messagebox.showinfo("Succès",message_succes)
        data = input(message_succes)
        engine.say(data)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {e}")

def generer_mot_de_passe(longueur=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe

def store_password_in_vault(email, password):
    """
    Ajoute une nouvelle entrée clé-valeur dans le même secret Vault.
    La clé est email+timestamp, la valeur est le mot de passe généré.
    """
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed.")
    # Lire les données existantes
    try:
        resp = client.secrets.kv.v2.read_secret_version(path=VAULT_KV_PATH)
        data = resp["data"]["data"]
    except Exception:
        data = {}
    # Générer la clé unique
    timestamp = int(time.time())
    key = f"{email}_{timestamp}"
    data[key] = password
    # Réécrire le secret
    client.secrets.kv.v2.create_or_update_secret(
        path=VAULT_KV_PATH,
        secret=data
    )

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
            store_password_in_vault(to, mot_de_passe)
            sendEmail(to, "Mot de passe généré : " + mot_de_passe)     
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement dans Vault : {e}")

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