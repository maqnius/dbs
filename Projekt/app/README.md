# Database App
Die Anwendung startet einen Server, der Daten aus einer Datenbank abfragt und das Ergebnis über eine REST API verfügbar
macht. Zu jeder Datenmanipulation gibt es eine URL, in der automatisch die Daten per Javascript über
die API werden und anschließend eine Javascript Methode `processData` übergeben werden.

## Erezugen der Datenbank anhand der Quelldateien
1. Erstelle und starte eine *leere* Postgresql Datenbank und ändere die `main.conf` entsprechend.
2. Kopiere die Dateien  `transactions_input.csv`, `transactions_output.csv` und `transactions_blocks.csv`
in den Ordner `data`.
3. Führe `python db.py` aus.
