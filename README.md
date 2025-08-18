# PasswordGen 🔐

**PasswordGen** is a **Python** application that allows you to:  
- Generate secure passwords  
- Send them by email via **Gmail**  
- Store them securely in **HashiCorp Vault**

---

## ✨ Features

- **🔑 Password generation**  
  Create random and strong passwords based on the desired length.

- **🖥️ Graphical interface (Tkinter)**  
  Enter the password length and recipient email address, then generate with a single click.

- **📧 Automatic email sending**  
  The generated password is sent via the Gmail API and **OAuth2** (`google-auth`, `google-api-python-client`).  
  👉 OAuth2 credentials are stored in **Vault** (never in plain text on disk).

- **🗄️ Secure storage in Vault**  
  Each password is stored in the `password/store` secret.  
  - Key = `email_timestamp`  
  - Keeps a history of passwords generated for each user.

- **🔊 Text-to-speech (optional)**  
  A confirmation message is read aloud after sending the email.

- **🔐 Secret management**  
  Gmail OAuth2 credentials are also stored in Vault.

---

## ⚙️ Requirements

- Python **3.7+**
- An accessible and configured **HashiCorp Vault** server
- A **Google Cloud** project with the Gmail API enabled
- A `credentials.json` file stored in Vault
- Environment variables to set:
  ```sh
  export VAULT_ADDR="http://127.0.0.1:8200"
  export VAULT_TOKEN="<VAULT_TOKEN>"
  ```

---

## 🚀 Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/<username>/PasswordGen.git
   cd PasswordGen
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the application:
```sh
python app.py
```

A graphical interface will open to generate and send passwords.

---

## 📖 Notes

- In development mode, use Vault with the **KV v2** engine enabled.  
- For more details on installing and configuring Vault, see the [Vault README](./vault/README.md).

---

## 🛡️ Security

- Never store your secrets in plain text.  
- Always use **Vault** to manage your sensitive tokens and credentials.  
- Enable regular secret rotation in production.  

---