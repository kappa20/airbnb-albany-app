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

---

## 🔍 Ce qu'il se passe "sous le capot" (Pour la présentation)
Lors de votre présentation, vous pouvez expliquer que Streamlit Cloud :
-   **Instancie un conteneur Linux** isolé.
-   **Installe Python** et les dépendances listées dans votre `requirements.txt`.
-   **Exécute `streamlit run app.py`** automatiquement.
-   **Synchronise le code** : Chaque fois que vous ferez un `git push`, l'application en ligne se mettra à jour en quelques secondes sans intervention manuelle.

## 💡 Astuces Pro
-   **Fichiers Volumineux** : Si `listings.csv` dépasse 100 Mo, utilisez **Git LFS** ou hébergez le fichier sur un URL (S3, Google Drive) et modifiez `load_data()` pour lire cet URL.
-   **Secrets** : Si vous aviez des clés API, elles ne doivent jamais être dans le code. Utilisez le menu "Settings > Secrets" du dashboard Streamlit pour les stocker en toute sécurité.
