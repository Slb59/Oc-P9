# LitReview

<< mettre une miniature du site ici >>

## Objectif
Ce programme est un exercice proposé par [OpenClassRooms](https://openclassrooms.com/fr/) dans le cadre de la formation :
Développeur d'applications Python. L'objectif est de développer une application web permettant aux utilisateurs de consulter ou de solliciter une critique de livres à la demande.

<< mettre une  image d'une page ici >>

## Fonctionnalités
L'application MVP LitReview permet de :
*-> s'inscrire en tant que nouvel utilisateur
*-> se connecter
*-> creer une demande de critique de livre ou d'article.
*-> publier une critique liée à une demande ou spontannée.
*-> modifier ou supprimer ses publications
*-> suivre les autres utilisateurs via un système d'abonnement.

## Technologie utilisée
*Le projet est développé avec le framework Django. 
*Les données sont sauvegardées dans une base de données sqlite3.

## Installation
*-> Télécharger le package de l'application depuis github : git clone https://github.com/Slb59/Oc-P9.git
*-> Creer un environnement virtuel (Si besoin installer pipenv: pip install pipenv) :
``` bash
cd Op-P9
mkdir .venv
pipenv install
```
## Utilisation
*-> Activer l'environnement virtuel : pipenv shell
*-> Lancer le serveur:
```bash
cd litreview
python manage.py runserver
```
*-> Depuis votre navigateur, vous accédez à l'application via : http:/127.0.0.1:8000

