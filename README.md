# PasswordGen 🔐

**PasswordGen** est une application **Python** permettant de :  
- Générer des mots de passe sécurisés  
- Les envoyer par e-mail via **Gmail**  
- Les stocker de façon sécurisée dans **HashiCorp Vault**

---

## ✨ Fonctionnalités

- **🔑 Génération de mots de passe**  
  Création de mots de passe aléatoires et robustes selon la longueur choisie par l’utilisateur.

- **🖥️ Interface graphique (Tkinter)**  
  Saisie de la longueur du mot de passe et de l’adresse e-mail de destination, puis génération d’un simple clic.

- **📧 Envoi automatique par e-mail**  
  Le mot de passe généré est envoyé via l’API Gmail et **OAuth2** (`google-auth`, `google-api-python-client`).  
  👉 Les identifiants OAuth2 sont stockés dans **Vault** (jamais en clair sur le disque).

- **🗄️ Stockage sécurisé dans Vault**  
  Chaque mot de passe est stocké dans le secret `password/store`.  
  - Clé = `email_timestamp`  
  - Permet de conserver l’historique des mots de passe générés par utilisateur.

- **🔊 Synthèse vocale (optionnelle)**  
  Un message vocal de confirmation est lu après l’envoi de l’e-mail.

- **🔐 Gestion des secrets**  
  Les identifiants OAuth2 Gmail sont eux-mêmes stockés dans Vault.

---

## ⚙️ Prérequis

- Python **3.7+**
- Un serveur **HashiCorp Vault** accessible et configuré
- Un projet **Google Cloud** avec l’API Gmail activée
- Un fichier `credentials.json` stocké dans Vault
- Variables d’environnement à définir :
  ```sh
  export VAULT_ADDR="http://127.0.0.1:8200"
  export VAULT_TOKEN="<TOKEN_VAULT>"
  ```

---

## 🚀 Installation

1. Clonez ce dépôt :
   ```sh
   git clone https://github.com/<username>/PasswordGen.git
   cd PasswordGen
   ```

2. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```

---

## ▶️ Utilisation

Lancez l’application :
```sh
python app.py
```

Une interface graphique s’ouvre pour générer et envoyer les mots de passe.

---

## 📖 Notes

- En mode développement, utilisez Vault avec le moteur **KV v2** activé.  
- Pour plus de détails sur l’installation et la configuration de Vault, référez-vous au fichier [README Vault](./vault/README.md).

---

## 🛡️ Sécurité

- Ne stockez jamais vos secrets en clair.  
- Utilisez toujours **Vault** pour gérer vos tokens et credentials sensibles.  
- Activez la rotation régulière des secrets en production.  

---