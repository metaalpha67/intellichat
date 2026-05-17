from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import ollama
import json
import random
import os

app = Flask(__name__)
app.secret_key = "informatik-lernbot-geheim-2026"  # Bitte ändern!

FRAGEN_DATEI = "fragen.json"
ADMIN_PASSWORT = "lehrer123"  # Bitte ändern!

# ─── Hilfsfunktionen ─────────────────────────────────────────────

def lade_fragen():
    if not os.path.exists(FRAGEN_DATEI):
        return []
    with open(FRAGEN_DATEI, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_fragen(fragen):
    with open(FRAGEN_DATEI, "w", encoding="utf-8") as f:
        json.dump(fragen, f, ensure_ascii=False, indent=2)

def naechste_id(fragen):
    if not fragen:
        return 1
    return max(f["id"] for f in fragen) + 1

def ist_eingeloggt():
    return session.get("admin") == True

# ─── Schüler-Routen ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/themen")
def themen():
    fragen = lade_fragen()
    alle_themen = sorted(set(f["thema"] for f in fragen))
    return jsonify({"themen": alle_themen})

@app.route("/neue-frage")
def neue_frage():
    fragen = lade_fragen()
    thema = request.args.get("thema", None)
    if thema:
        pool = [f for f in fragen if f["thema"] == thema]
    else:
        pool = fragen
    if not pool:
        return jsonify({"error": "Keine Fragen gefunden"}), 404
    frage = random.choice(pool)
    return jsonify({"id": frage["id"], "thema": frage["thema"], "frage": frage["frage"]})

@app.route("/antwort", methods=["POST"])
def antwort():
    fragen = lade_fragen()
    data = request.json
    frage_id = data.get("frage_id")
    schueler_antwort = data.get("antwort", "").strip()
    if not schueler_antwort:
        return jsonify({"error": "Keine Antwort erhalten"}), 400
    frage_obj = next((f for f in fragen if f["id"] == frage_id), None)
    if not frage_obj:
        return jsonify({"error": "Frage nicht gefunden"}), 404

    prompt = f"""Du bist ein Informatiklehrer und bewertest die Antwort eines Schülers.

Frage: {frage_obj["frage"]}
Musterlösung: {frage_obj["musterloesung"]}
Antwort des Schülers: {schueler_antwort}

Bewerte ob die Antwort inhaltlich korrekt ist. Kleinere Formulierungsunterschiede sind egal,
solange der Kern der Antwort stimmt. Antworte NUR in diesem Format:

ERGEBNIS: RICHTIG oder FALSCH
FEEDBACK: (Ein kurzer Satz was gut war oder was gefehlt hat)
"""
    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )
    bewertung = response["message"]["content"]
    korrekt = "RICHTIG" in bewertung.upper()
    feedbackzeile = next((l for l in bewertung.split("\n") if l.startswith("FEEDBACK:")), "")
    feedback = feedbackzeile.replace("FEEDBACK:", "").strip()

    return jsonify({
        "korrekt": korrekt,
        "feedback": feedback,
        "musterloesung": frage_obj["musterloesung"]
    })

# ─── Admin-Routen ────────────────────────────────────────────────

@app.route("/admin")
def admin():
    if not ist_eingeloggt():
        return redirect(url_for("admin_login"))
    fragen = lade_fragen()
    return render_template("admin.html", fragen=fragen)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    fehler = None
    if request.method == "POST":
        pw = request.form.get("passwort", "")
        if pw == ADMIN_PASSWORT:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            fehler = "Falsches Passwort."
    return render_template("login.html", fehler=fehler)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/frage-hinzufuegen", methods=["POST"])
def frage_hinzufuegen():
    if not ist_eingeloggt():
        return jsonify({"error": "Nicht eingeloggt"}), 401
    fragen = lade_fragen()
    data = request.json
    neue = {
        "id": naechste_id(fragen),
        "thema": data.get("thema", "").strip(),
        "frage": data.get("frage", "").strip(),
        "musterloesung": data.get("musterloesung", "").strip()
    }
    if not alle([neue["thema"], neue["frage"], neue["musterloesung"]]):
        return jsonify({"error": "Alle Felder ausfüllen"}), 400
    fragen.append(neue)
    speichere_fragen(fragen)
    return jsonify({"success": True, "frage": neue})

@app.route("/admin/frage-loeschen/<int:frage_id>", methods=["DELETE"])
def frage_loeschen(frage_id):
    if not ist_eingeloggt():
        return jsonify({"error": "Nicht eingeloggt"}), 401
    fragen = lade_fragen()
    fragen = [f for f in fragen if f["id"] != frage_id]
    speichere_fragen(fragen)
    return jsonify({"success": True})

@app.route("/admin/frage-bearbeiten/<int:frage_id>", methods=["PUT"])
def frage_bearbeiten(frage_id):
    if not ist_eingeloggt():
        return jsonify({"error": "Nicht eingeloggt"}), 401
    fragen = lade_fragen()
    data = request.json
    for f in fragen:
        if f["id"] == frage_id:
            f["thema"] = data.get("thema", f["thema"]).strip()
            f["frage"] = data.get("frage", f["frage"]).strip()
            f["musterloesung"] = data.get("musterloesung", f["musterloesung"]).strip()
            break
    speichere_fragen(fragen)
    return jsonify({"success": True})

def alle(lst):
    return all(lst)

if __name__ == "__main__":
    print("Chatbot läuft auf http://localhost:5000")
    print("Admin-Panel: http://localhost:5000/admin")
    app.run(debug=True)
