# 🚀 Guide de Déploiement : Streamlit Community Cloud

Ce guide explique comment mettre en ligne l'application **Airbnb Albany Explorer** de manière professionnelle et gratuite.

## 📋 Prérequis
Avant de commencer, assurez-vous que votre projet contient ces trois fichiers indispensables à la racine :
1.  **`app.py`** : Le code principal de l'application.
2.  **`requirements.txt`** : La liste des bibliothèques à installer (`streamlit`, `pandas`).
3.  **`listings.csv`** : Le fichier de données (car `app.py` le lit localement).

---

## 🛠 Étape 1 : Préparer le dépôt GitHub
Le Cloud de Streamlit déploie directement depuis GitHub.
1.  Créez un nouveau dépôt sur votre compte GitHub (ex: `airbnb-albany-app`).
2.  Envoyez votre code local vers ce dépôt :
    ```bash
    git add .
    git commit -m "🚀 Initial commit: App avec tests et CI/CD"
    git branch -M main
    git push -u origin main
    ```

## ☁️ Étape 2 : Connexion à Streamlit Cloud
1.  Rendez-vous sur [share.streamlit.io](https://share.streamlit.io).
2.  Cliquez sur **"Continue with GitHub"**.
3.  Autorisez Streamlit à accéder à vos dépôts publics.

## 🚀 Étape 3 : Déployer l'Application
1.  Une fois connecté, cliquez sur le bouton **"New app"**.
2.  **Repository** : Sélectionnez votre dépôt `airbnb-albany-app`.
3.  **Branch** : Choisissez `main` (ou `master`).
4.  **Main file path** : Tapez `app.py`.
5.  Cliquez sur **"Deploy!"**.


