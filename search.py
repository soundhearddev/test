from faker import Faker
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


faker = Faker()
while True:
    ip = faker.ipv4()
    url = f"http://{ip}"

    print("Teste:", url)

    try:
        response = requests.get(url, timeout=2)
        print("Erfolg:", response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        # Alle Tags auf der Seite holen
        all_tags = soup.find_all(True)  # True == Alle HTML-Tags

        # Liste für CSV
        rows = []

        for tag in all_tags:
            name = tag.name
            text = tag.get_text(strip=True)
            if text:
                rows.append([name, text])

        # In CSV speichern
        zeit = datetime.now().strftime("")
        file = ip + zeit
        with open(f"data/{file}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tag", "Text"])
            writer.writerows(rows)

        print("Fertig! Gespeichert")

    except Exception as e:
        print("Fehler:", e)
