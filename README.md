# BLitz-Flow-Projekt 

Dieses Projekt wurde von Herrn Francesco Leonelli und Frau Yanfei Wang für den Wintersemester 2022/2023 HWR-Kurs "Entwicklung von Web-Anwendungen" (Dozent: Prof. Dr. Alexander Eck)
gewählt und entwickelt. Es geht um einer einfachen Kanban-Board für Projektmanagement mit Python Flask. Nach einer Anmeldung und einem Log In kann der Nutzer bzw. die Nutzerin einen Task erstellen und einem/r Teammitglieder*in zuweisen. Je nach Status ("to-do", "doing", "done") wird der Task in die drei entsprechenden Spalten geschoben. Am Ende gibt es die Möglichkeit den Task definitiv (mit einer entsprechenden Entfernung der Daten von der Datenbank) zu löschen. 


Das Projekt wird durch das  **run.py** Module gestartet. Dafür muss man im Terminal das Command 
**```python run.py```** eingeben. Bitte, zuerst kontrollieren, dass ```venv``` aktiviert ist (Falls Problemen mit Admin-Auth gibt, zuerst ```Set-ExecutionPolicy Unrestricted -Scope Proces``` und dann ```venv\Scripts\activate``` eingeben). Alle notwendige imports sind in Code gelassen und in **requirements.txt** zusammengefasst. 

**Achtung! :**

In dieser Repository wird **keine Datenbank-Datei** angegeben, da die Datenbank nach der ersten Einführung automatisch generiert wird. Jedoch muss man vor der ersten Einführung diese zwei einfache Steps folgen:

 1) ```__init.py__``` Datei öffnen
 2) ```app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Pfad/zum/Projekt/site.db'``` **(Zeile 15)** mit dem eigenen Pfad ändern. Wenn ein Windows-System und eine Sqlite Datenbank angewendet werden sowie das Projekt in C: Laufwerk gespeichert wird, kann der Teil ```'sqlite:///C:/'``` unverändert bleiben.  

 Empfohlen wird allerdings, die .db Datei im **project** Ordner zu speichern, ansonsten muss man auch im Module **routes.py** den folgenden Pfad ändern **(Zeile 146)**:

```
#Query for the team member assignment dropdwown menu
def get_db():
    DATABASE = './project/site.db'
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
```

Danke für die Aufmerksamkeit und viel Spaß!

Francesco Leonelli,
Yanfei Wang





