FROM python:3

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie wymaganych plików aplikacji do kontenera
COPY . .

# Instalacja zależności aplikacji
RUN pip install -r requirements.txt

# Uruchomienie aplikacji
CMD ["python", "app.py"]
