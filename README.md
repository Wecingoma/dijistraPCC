# dijistraPCC

## Objectif du projet

Ce projet implémente manuellement l'algorithme de flot à coût minimum primal-dual
pour un graphe orienté avec capacités et coûts sur les arêtes.

Le code fonctionne uniquement avec les bibliothèques standard de Python
(`tkinter`, `heapq` et typeurs standards). Il ne dépend plus de `networkx`
ni de `matplotlib` pour le calcul.

## Exécution

1. Créez un environnement virtuel Python :

   ```powershell
   python -m venv .venv
   ```

2. Activez l'environnement :

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Lancez le script :

   ```powershell
   python .\tproa.py
   ```

## Contenu

- `tproa.py` : application Tkinter avec une entrée manuelle des arêtes,
  calcul du flot à coût minimum et affichage des résultats.

## Remarques

- Le projet est conçu pour être compatible sur Windows.
- Le dossier `.venv/` est ignoré par Git.
- Si le projet doit être mis sur GitHub, créez un dépôt et poussez tout le code
  en veillant à ne pas inclure le dossier `.venv/`.
