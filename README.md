# PasswordGen

PasswordGen est une application Python permettant de générer des mots de passe sécurisés, de les envoyer par e-mail via Gmail et de les stocker de façon sécurisée dans HashiCorp Vault.

## Fonctionnalités

- **Génération de mots de passe** : Crée des mots de passe aléatoires et robustes selon la longueur choisie par l'utilisateur.
- **Interface graphique** : Utilise Tkinter pour une interface simple où l'utilisateur saisit la longueur du mot de passe et l'adresse e-mail de destination.
- **Envoi par e-mail** : Envoie automatiquement le mot de passe généré à l'adresse e-mail saisie, en utilisant l'API Gmail et OAuth2 (via `google-auth` et `google-api-python-client`).
- **Stockage sécurisé** : Enregistre chaque mot de passe généré dans HashiCorp Vault, sous la forme d'une clé unique composée de l'adresse e-mail et d'un timestamp, pour garantir la traçabilité et la sécurité.
- **Gestion des secrets** : Les identifiants OAuth2 de Gmail sont eux-mêmes stockés dans Vault pour éviter toute fuite de secrets sensibles.

## Prérequis

- Python 3.7+
- Un serveur HashiCorp Vault accessible et configuré
- Un projet Google Cloud avec l'API Gmail activée et un fichier `credentials.json` stocké dans Vault
- Les variables d'environnement suivantes doivent être définies :
  - `VAULT_ADDR` : URL du serveur Vault
  - `VAULT_TOKEN` : Token d'accès Vault
  - `VAULT_KV_PATH` : Chemin du secret Vault (ex : `gmail/myapp`)

## Installation

1. Clonez ce dépôt.
2. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```
