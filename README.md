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



Initialiser f = 0
Initialiser π = 0

Tant qu'il existe un chemin augmentant :
    Calculer les coûts réduits
    Trouver le plus court chemin (Dijkstra)
    Mettre à jour les potentiels π
    Augmenter le flot le long du chemin
Fin


L’algorithme a été implémenté sans recours à des bibliothèques spécialisées, afin de respecter les contraintes académiques et de maîtriser chaque étape du processus.

| Route          | Coût (temps) | Capacité |
| -------------- | ------------ | -------- |
| Dépôt → Gombe  | 5            | 10       |
| Dépôt → Limete | 3            | 8        |
| Limete → Gombe | 2            | 5        |
