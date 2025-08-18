# PasswordGen – Vault Installation & Configuration

This document describes the local installation of **HashiCorp Vault** and its configuration for the **PasswordGen** project, using the **KV v2** secrets engine.

---

## 📦 Prerequisites

- macOS with **Homebrew** (or a Vault binary available in the PATH).
- **Python 3.9+** if integrating with `hvac` in the app.
- Shell tools: `jq` recommended.
- A user account with local installation rights.

---

## ⚙️ Installation

### Via Homebrew
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/vault
```

### Verify the installation
```bash
vault -v
```

---

## 🚀 Start in Development Mode

The **dev mode** is only meant for local testing (⚠️ do not use in production).

1. Start Vault in dev mode:
   ```bash
   vault server -dev
   ```

2. From the output, retrieve:
   - The address (default: `http://127.0.0.1:8200`)
   - The **root token**

3. Export environment variables:
   ```bash
   export VAULT_ADDR='http://127.0.0.1:8200'
   export VAULT_TOKEN='<DISPLAYED_ROOT_TOKEN>'
   ```

4. Check status:
   ```bash
   vault status
   ```

---

## 🔑 Enable KV v2 Engine

Enable KV v2 on the `secret/` mount (if not already present):
```bash
vault secrets enable -path=secret -version=2 kv
```

List active secrets engines:
```bash
vault secrets list
```

---

## 📂 PasswordGen Path Structure

- Default mount: `secret/`
- Secrets used:
  - `secret/password/...` → passwords/configs
  - `secret/gmail/myapp` → Gmail/OAuth credentials

In code (via API/SDK), use:
- `mount_point = "secret"`
- `path = "password/<name>"` or `gmail/<app>`

---

## 🔐 Policies (RBAC)

### Gmail secrets read-only access
```hcl
# policy_gmail_read.hcl
path "secret/data/gmail/*" {
  capabilities = ["read"]
}
path "secret/metadata/gmail/*" {
  capabilities = ["list"]
}
```

### PasswordGen read/write access
```hcl
# policy_password_rw.hcl
path "secret/data/password/*" {
  capabilities = ["create","update","read"]
}
path "secret/metadata/password/*" {
  capabilities = ["list"]
}
```

Load the policies:
```bash
vault policy write gmail-read policy_gmail_read.hcl
vault policy write password-rw policy_password_rw.hcl
```

---

## 🎟️ Create an Application Token

Create a token limited to the required policies:
```bash
vault token create -policy=gmail-read -policy=password-rw
```

Get only the token value:
```bash
vault token create -policy=gmail-read -policy=password-rw -format=json | jq -r '.auth.client_token'
```

Check a token:
```bash
vault token lookup
```

⚠️ Best practices:
- Never use the root token in an application.
- Use short TTLs and rotate regularly.
- In production: prefer AppRole, OIDC, or GCP auth.

---

## 📖 Managing Secrets (CLI)

Write/create a secret:
```bash
vault kv put secret/password/my-secret username="alice" password="s3cr3t"
```

Read a secret:
```bash
vault kv get secret/password/my-secret
```

Patch (add without overwriting):
```bash
vault kv patch secret/password/my-secret note="personal"
```

List keys:
```bash
vault kv list secret/password/
```

Load from a JSON file:
```bash
vault kv put secret/gmail/myapp @client_credentials.json
```

➡️ KV v2 supports versioning:  
- Read a specific version: `vault kv get -version=N secret/password/my-secret`  
- Soft delete a version: `vault kv delete -versions=N secret/password/my-secret`  
- Permanently destroy a version: `vault kv destroy -versions=N secret/password/my-secret`

---

## 🌍 Environment Variables for PasswordGen

Set the required environment variables in the application environment:

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='<APP_TOKEN>'
export VAULT_MOUNT='secret'
export VAULT_KV_PATH_PASSWORD='password/my-secret'
export VAULT_KV_PATH_GMAIL='gmail/myapp'
```

---
