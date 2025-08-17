# PasswordGen

PasswordGen est une application Python permettant de générer des mots de passe sécurisés, de les envoyer par e-mail via Gmail et de les stocker de façon sécurisée dans HashiCorp Vault.

## Fonctionnalités détaillées

- **Génération de mots de passe**  
  L’application crée des mots de passe aléatoires et robustes selon la longueur choisie par l’utilisateur.

- **Interface graphique**  
  Une interface Tkinter permet à l’utilisateur de saisir la longueur du mot de passe et l’adresse e-mail de destination, puis de lancer la génération d’un simple clic.

- **Envoi automatique par e-mail**  
  Le mot de passe généré est envoyé à l’adresse e-mail saisie, via l’API Gmail et OAuth2 (`google-auth`, `google-api-python-client`).  
  L’authentification Google se fait de façon sécurisée : les identifiants OAuth2 sont stockés dans Vault, jamais en clair sur le disque.

- **Stockage sécurisé dans Vault**  
  Chaque mot de passe généré est stocké dans HashiCorp Vault, dans le secret `password/store`.  
  La clé utilisée est composée de l’adresse e-mail et d’un timestamp (`email_timestamp`), ce qui permet de conserver l’historique des mots de passe générés pour chaque utilisateur.

- **Synthèse vocale (optionnelle)**  
  Après l’envoi du mail, un message vocal de confirmation est lu à l’utilisateur.

- **Gestion des secrets**  
  Les identifiants OAuth2 de Gmail sont eux-mêmes stockés dans Vault pour éviter toute fuite de secrets sensibles.

## Prérequis

- Python 3.7+
- Un serveur HashiCorp Vault accessible et configuré
- Un projet Google Cloud avec l’API Gmail activée et un fichier `credentials.json` stocké dans Vault
- Les variables d’environnement suivantes doivent être définies :
  - `VAULT_ADDR` : URL du serveur Vault
  - `VAULT_TOKEN` : Token d’accès Vault

## Installation

1. Clonez ce dépôt.
2. Installez les dépendances :
   ```sh
   pip install -r requirements.txt