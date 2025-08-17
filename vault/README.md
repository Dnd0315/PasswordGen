# PasswordGen – Vault Installation & Configuration

Ce document décrit l’installation locale de **HashiCorp Vault** et sa configuration pour le projet **PasswordGen**, avec le moteur **KV v2**.

---

## 📦 Prérequis

- macOS avec **Homebrew** (ou un binaire Vault dans le PATH).
- **Python 3.9+** si intégration avec `hvac` côté app.
- Outils shell: `jq` recommandé.
- Compte utilisateur avec droits d’installation locale.

---

## ⚙️ Installation

### Via Homebrew
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/vault
```

### Vérifier l’installation
```bash
vault -v
```

---

## 🚀 Démarrage en mode développement

Le mode **dev** est uniquement destiné aux tests en local (⚠️ à ne pas utiliser en production).

1. Lancer Vault en mode dev :
   ```bash
   vault server -dev
   ```

2. Récupérer dans la sortie :
   - L’adresse (par défaut: `http://127.0.0.1:8200`)
   - Le **root token**

3. Exporter les variables d’environnement :
   ```bash
   export VAULT_ADDR='http://127.0.0.1:8200'
   export VAULT_TOKEN='<ROOT_TOKEN_AFFICHE>'
   ```

4. Vérifier le statut :
   ```bash
   vault status
   ```

---

## 🔑 Activer le moteur KV v2

Activer KV v2 sur le mount `secret/` (si absent) :
```bash
vault secrets enable -path=secret -version=2 kv
```

Lister les secrets engines actifs :
```bash
vault secrets list
```

---

## 📂 Structure des chemins PasswordGen

- Mount par défaut : `secret/`
- Secrets utilisés :
  - `secret/password/...` → mots de passe/configs
  - `secret/gmail/myapp` → credentials Gmail/OAuth

Dans le code (via API/SDK), il suffit d’utiliser :
- `mount_point = "secret"`
- `path = "password/<nom>"` ou `gmail/<app>`

---

## 🔐 Policies (RBAC)

### Lecture des secrets Gmail
```hcl
# policy_gmail_read.hcl
path "secret/data/gmail/*" {
  capabilities = ["read"]
}
path "secret/metadata/gmail/*" {
  capabilities = ["list"]
}
```

### Lecture/Écriture des secrets PasswordGen
```hcl
# policy_password_rw.hcl
path "secret/data/password/*" {
  capabilities = ["create","update","read"]
}
path "secret/metadata/password/*" {
  capabilities = ["list"]
}
```

Charger les policies :
```bash
vault policy write gmail-read policy_gmail_read.hcl
vault policy write password-rw policy_password_rw.hcl
```

---

## 🎟️ Créer un token d’application

Créer un token limité aux policies nécessaires :
```bash
vault token create -policy=gmail-read -policy=password-rw
```

Obtenir uniquement la valeur du token :
```bash
vault token create -policy=gmail-read -policy=password-rw -format=json | jq -r '.auth.client_token'
```

Vérifier un token :
```bash
vault token lookup
```

⚠️ Bonnes pratiques :
- Ne jamais utiliser le root token dans une application.
- Utiliser des TTL courts et rotation régulière.
- En production : préférer AppRole, OIDC, GCP auth.

---

## 📖 Gestion des secrets (CLI)

Écrire/créer un secret :
```bash
vault kv put secret/password/mon-secret username="alice" password="s3cr3t"
```

Lire un secret :
```bash
vault kv get secret/password/mon-secret
```

Patch (ajouter sans écraser) :
```bash
vault kv patch secret/password/mon-secret note="perso"
```

Lister les clés :
```bash
vault kv list secret/password/
```

Charger depuis un fichier JSON :
```bash
vault kv put secret/gmail/myapp @client_credentials.json
```

➡️ KV v2 permet le versionnement :  
- Lire une version précise : `vault kv get -version=N secret/password/mon-secret`  
- Supprimer logiquement : `vault kv delete -versions=N secret/password/mon-secret`  
- Détruire définitivement : `vault kv destroy -versions=N secret/password/mon-secret`

---

## 🌍 Variables d’environnement PasswordGen

Configurer les variables nécessaires dans l’environnement de l’application :

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='<TOKEN_APPLICATION>'
export VAULT_MOUNT='secret'
export VAULT_KV_PATH_PASSWORD='password/mon-secret'
export VAULT_KV_PATH_GMAIL='gmail/myapp'
```

---
