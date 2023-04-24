Pour executer le script:
    cd src
    python main.py

Cela genere dans scans un fichier anwar4.ply
pour pouvoir visualiser le fichier dans meshlab il faut:
    1. l'ouvrir avec un editeur de texte
    2. supprimer la ligne 8 : property float quality
    3. ajouter avant les points ( dans la ligne 10) la ligne: end_header
Vous trouverez egalement dans le dossier une de nos acquisiton (environ 60000 points) et un resultat a l'issu du script
Pour avoir une visualisation en temps reel des modifications, il faut avoir une ancienne version de matplotlib
