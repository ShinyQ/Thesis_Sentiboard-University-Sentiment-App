# **Sentiboard**
A Sentiment Analysis Dashboard For Telkom University Social Media

## **Tech Stack**
- Python 3.9
- Django
- Plotly
- Transformer (IndoBERT)

## **Installation Steps:**

Make sure you have the rust programming language installed:
- `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

Install pgsql connector:
- `brew install postgresql` for MAC
- `sudo apt-get install libpq-dev` for Debian/Ubuntu

Manual Installation:
- Create virtual environment (python3 -m venv Scripts)
- Activate virtual environment (source Scripts/bin/activate)
- Upgrade latest pip version (pip3 install --upgrade pip)
- Install Requirements (pip install -r requirements.txt)

## **Running Application**
- Manual : `python3 manage.py runserver localhost:9000`