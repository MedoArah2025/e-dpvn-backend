# e-DPVN Backend

API REST Django pour la gestion des activités des unités de police.

## Table des matières

1. [Prérequis](#prérequis)  
2. [Installation](#installation)  
3. [Configuration](#configuration)  
4. [Lancement](#lancement)  
5. [Tests & Couverture](#tests--couverture)  
6. [Documentation API](#documentation-api)  
7. [CI / GitHub Actions](#ci--github-actions)  
8. [Contribuer](#contribuer)  

---

## Prérequis

- Python 3.10+  
- PostgreSQL  
- Git

## Installation

```bash
git clone <votre-repo-url> e-dpvn-backend
cd e-dpvn-backend
python -m venv .venv
.\.venv\Scripts\activate     # sous Windows PowerShell
# ou `source .venv/bin/activate` sur macOS/Linux
pip install -r requirements.txt

