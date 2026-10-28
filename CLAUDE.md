# CLAUDE.md

Ce fichier est lu automatiquement par Claude au début de chaque session sur ce dépôt.
Il décrit le projet, les conventions et la façon de travailler.

## Le projet

Implémentation pédagogique de l'algorithme de chiffrement **AES** en Python, réalisée dans le cadre
d'un cours au CESI (M1 MAALSI). L'objectif est de comprendre et de pouvoir expliquer chaque étape,
pas de produire une bibliothèque de chiffrement utilisable en production.

Référence unique pour l'algorithme et les valeurs attendues : **FIPS-197** (norme officielle AES).

### Contraintes

- Python standard uniquement : **aucune bibliothèque de cryptographie** (`cryptography`, `pycryptodome`...)
  et aucune dépendance externe pour le code AES.
- Tout est implémenté à la main, étape par étape, pour rester lisible et explicable à l'oral.
- La lisibilité passe avant la performance.

## Organisation du code

Un fichier par étape de l'algorithme, à la racine du dépôt :

| Fichier | Rôle | État |
|---|---|---|
| `calculation.py` | Outils communs : conversion bloc de 16 octets <-> state 4x4, affichage | fait |
| `ByteSub.py` | `subBytes` / `invSubBytes`, S-Box et S-Box inverse | fait |
| `ShiftRow.py` | `shiftRows` / `invShiftRows` | fait |
| `GaloisField.py` | Arithmétique dans GF(2^8) : `xtime`, `gfMultiply` | fait |
| `MixColumn.py` | `mixColumns` / `invMixColumns` | fait |
| `CreateKey.py` | Génération de clé, puis expansion de clé (key schedule) | à reprendre |
| `AddRoundKey.py` | `addRoundKey` | fait |
| `Main.py` | Assemblage : chiffrement et déchiffrement complets | à faire |
| `tests/` | Tests unitaires, un fichier `test_<module>.py` par module | |

### Représentation du state

Le state est une **liste de 4 lignes de 4 entiers** (0 à 255), remplie **colonne par colonne**
comme dans FIPS-197 section 3.4 : `state[row][col] = block[row + 4 * col]`.
Utiliser `bytesToState` et `stateToBytes` de `calculation.py` pour les conversions.

Les fonctions d'étape **renvoient un nouveau state** et ne modifient pas celui reçu en paramètre.

## Conventions de code

- Code, noms, commentaires, docstrings et messages de commit **en anglais**.
- Noms de fonctions et variables en **camelCase** (`subBytes`, `invShiftRows`, `gfMultiply`).
- Fonction inverse préfixée par `inv` (`subBytes` / `invSubBytes`).
- Style du dépôt : un espace avant les deux-points des `def`, `class`, `for`, `if`
  (`def shiftRows(state) :`). Le garder pour rester cohérent.
- Docstring sur chaque fonction, au format :
  ```python
  """
  Short description.
  :param list state: description.
  :return: description.
  """
  ```
- Pas de `print` ni de code exécuté au niveau du module (sauf dans `Main.py` sous
  `if __name__ == "__main__" :`).

## Tests

- Framework : `unittest` (bibliothèque standard).
- Lancer tous les tests depuis la racine du dépôt :
  ```bash
  python -m unittest discover -s tests -v
  ```
- Chaque nouvelle fonction arrive **avec ses tests dans le même commit**.
- Utiliser en priorité les **vecteurs de test de FIPS-197** (exemples des sections 4 et 5,
  annexe B pour une exécution complète round par round, annexe C pour les résultats finaux).
  Indiquer en commentaire la section de FIPS-197 d'où vient chaque valeur.
- Pour chaque étape avec un inverse, tester l'aller-retour : `inv(f(x)) == x`.
- Tous les tests doivent passer avant de proposer un commit.

## Façon de travailler (git)

Léandre débute avec git : expliquer simplement les opérations git quand elles ne sont pas évidentes.

- **Une étape = un commit**, petit et ciblé (une fonction ou une transformation, avec ses tests).
- Avant chaque commit : montrer le diff, résumer ce qui change et attendre la validation de Léandre.
- Les commits vont sur la branche **`dev`**, jamais directement sur `main`.
- Léandre récupère `dev` en local, teste, puis crée et fusionne lui-même la pull request
  `dev` -> `main` (avec GitHub Desktop). Ne pas créer ni fusionner de PR à sa place.
- Messages de commit : un titre court à l'impératif, puis une liste de ce qui a été fait
  et des tests ajoutés.

## Pédagogie

Ce projet sert à apprendre. Pour chaque étape :

1. Expliquer d'abord le principe de l'étape (ce qu'elle fait et pourquoi dans AES).
2. Proposer le code, en restant au plus près de la description de FIPS-197.
3. Signaler ce qui est important à savoir expliquer à l'oral.

Si une demande est ambiguë (taille de clé, format d'entrée...), poser la question avant de coder.

## Points connus à traiter plus tard

- `CreateKey.py` utilise `random`, qui n'est pas sûr pour générer une clé. Pour un projet de cours,
  le mentionner ; `secrets.token_bytes` est l'équivalent sûr de la bibliothèque standard.
- `CreateKey.py` contient un `print` exécuté à l'import, à retirer.
- `Main.py` est un squelette qui ne fonctionne pas encore (`EncryptedMessage` non défini).
- Tailles de clé : commencer par AES-128 ; AES-192 et AES-256 éventuellement ensuite.
