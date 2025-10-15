# Utiliser une image Python officielle comme base
FROM python:3.9-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'app Flask va tourner
EXPOSE 5000

# Commande pour lancer l'application Flask
CMD ["python", "app.py"]
