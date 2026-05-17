# IntelliChat

Ein lokaler KI-gestützter Lernbot für Gymnasialschüler im Fach Informatik.  
Entwickelt im Rahmen eines Schulprojekts (Projektende: Mai 2026).  
Stakeholder: Susann Leiser (Lehrerin)

\---

## Funktionen

* Schüler können ihren Namen eingeben (optional, DSGVO-konform)
* Der Bot stellt zufällige Fragen aus der Wissensbasis
* Schüler antworten im Freitext – kein Multiple Choice
* Eine lokale KI (Phi-3 Mini via Ollama) bewertet die Antworten inhaltlich
* Sofortiges Feedback mit Musterlösung
* Themenfilter: gezielt nach Thema üben
* **Admin-Panel** für Lehrkräfte: Fragen anlegen, bearbeiten, löschen

\---

## Voraussetzungen

|Tool|Version|Link|
|-|-|-|
|Python|3.10+|[python.org](https://python.org/downloads)|
|Ollama|aktuell|[ollama.com](https://ollama.com)|
|Phi-3 Mini|3.8B|via Ollama|

\---

## Installation

### 1\. Repository klonen

```bash
git clone https://github.com/metaalpha67/intellichat.git
cd DEINREPO
```

### 2\. Python-Abhängigkeiten installieren

```bash
pip install flask ollama
```

### 3\. Ollama \& Phi-3 Mini einrichten

Ollama installieren (falls noch nicht vorhanden): [ollama.com](https://ollama.com)

Dann das Modell herunterladen (\~2 GB):

```bash
ollama pull phi3:mini
```

\---

## Starten

Windows nutzen können einfach durch Doppelclick auf `start\\\_server.bat` das Programm starten.



Für alle anderen Nutzer:

```bash
python app.py
```

Danach im Browser öffnen:

|Bereich|URL|
|-|-|
|Schüler-Chatbot|http://localhost:5000|
|Admin-Panel (Lehrerin)|http://localhost:5000/admin|

> \\\*\\\*Hinweis:\\\*\\\* Ollama muss im Hintergrund laufen. Es reicht, es einmalig zu installieren – es startet automatisch als Dienst.

\---

## Projektstruktur

```
informatik-chatbot/
├── app.py               # Flask-Backend (Server \\\& API)
├── fragen.json          # Wissensbasis (alle Fragen \\\& Musterlösungen)
├── README.md
└── templates/
    ├── index.html       # Schüler-Oberfläche
    ├── admin.html       # Admin-Panel
    └── login.html       # Login für Lehrkräfte
```

\---

## Admin-Panel

Die Lehrerin erreicht das Admin-Panel unter `http://localhost:5000/admin`.

**Standard-Passwort:** `lehrer123`

> ⚠️ Das Passwort sollte vor dem Einsatz in `app.py` geändert werden:
> ```python
> ADMIN\\\_PASSWORT = "lehrer123"  # hier ändern
> ```

Im Admin-Panel können Fragen:

* ➕ neu angelegt werden (Thema, Fragetext, Musterlösung)
* ✏️ bearbeitet werden
* 🗑️ gelöscht werden

\---

## Wissensbasis erweitern

Fragen werden in `fragen.json` gespeichert. Neue Fragen können entweder über das Admin-Panel oder direkt in der Datei hinzugefügt werden:

```json
{
  "id": 13,
  "thema": "Algorithmen",
  "frage": "Was versteht man unter einem Algorithmus?",
  "musterloesung": "Ein Algorithmus ist eine endliche, eindeutige Folge von Anweisungen zur Lösung eines Problems."
}
```

> Die `id` muss einmalig und höher als alle bestehenden IDs sein.

\---

## Wie funktioniert die Bewertung?

1. Der Schüler gibt eine Freitextantwort ein
2. Das Backend schickt Frage, Musterlösung und Schülerantwort an Phi-3 Mini
3. Das Modell bewertet inhaltlich – kleine Formulierungsunterschiede sind egal
4. Ergebnis: **RICHTIG** oder **FALSCH** + kurzes Feedback

Ziel: ≥ 90 % Bewertungsgenauigkeit (gemäß Backlog US3).

\---

## Datenschutz

* Namen werden **nicht gespeichert** – nur für die aktuelle Sitzung im Browser
* Keine Nutzerdaten werden an externe Server gesendet
* Das KI-Modell läuft **vollständig lokal** (kein Internet nötig)
* DSGVO-konform

\---

## Projektteam

Schulprojekt – Gymnasium  
Fach: Informatik  
Projektende: Mai 2026

