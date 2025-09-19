# calendar-from-ais-json
Add your AIS (STU Academic Information System) timetable to any calendar. This script takes JSON export from the AIS timetable and converts it to an .ics file, ready to be imported into any calendar app.

1. Download the script by opening terminal and running
  - git clone https://github.com/rusa95/calendar-from-ais-json
  - cd calendar-from-ais-json
(or download make_ics.py directly)
2. Export your personal timetable from the AIS portal
- Go to **Student's portal** -> **Personal Timetable**
- In the URL, find **format=html** and change it to **format=json**
3. Copy the JSON and save it as schedule.json in the same folder as the script
4. Run the script
  - python3 make_ics.py
5. This will generate **output.ics** ready to be imported into any calendar.

Tento skript umoznuje pridanie AIS (STU Akademicky informacny system) rozvrhu do akehokolvek kalendara. Vezme sa JSON export z AIS rozvrhu a konvertuje sa do .ics suboru, ktory mozete importovat do vasho kalendara.
1. Stiahnite si tento script cez terminal pomocou nasledovnych prikazov
  - git clone https://github.com/rusa95/calendar-from-ais-json
  - cd calendar-from-ais-json
(alebo si stiahnite make_ics.py priamo)
2. Exportujte osobny rozvrh v AIS portali
- Chodte na **Portal Studenta** -> **Osobny rozvrh**
- V URL najdite **format=html** a zmente ho na **format=json**
3. Skopirujte obsah JSON a ulozte ho ako schedule.json v tom istom priecinku, kde je script.
4. Spustite script
  - python3 make_ics.py
5. Tento skript vygeneruje output.ics, ktory mozete importovat do lubovolneho kalendara.
