from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = "secretkey"  # Required for flashing messages

# Store participants and pairings
participants = []
pairings = {}

@app.route("/", methods=["GET", "POST"])
def home():
    global participants, pairings
    if request.method == "POST":
        # Add a participant
        name = request.form.get("name")
        if name and name not in participants:
            participants.append(name)
        elif name in participants:
            flash(f"{name} is already added!")
        return redirect(url_for("home"))
    return render_template("index.html", participants=participants)

@app.route("/generate", methods=["POST"])
def generate():
    global pairings
    if len(participants) < 2:
        flash("You need at least two participants to generate matches.")
        return redirect(url_for("home"))

    # Generate Secret Santa pairs
    receivers = participants[:]
    random.shuffle(receivers)
    while any(giver == receiver for giver, receiver in zip(participants, receivers)):
        random.shuffle(receivers)
    pairings = dict(zip(participants, receivers))
    return redirect(url_for("reveal"))

@app.route("/reveal", methods=["GET", "POST"])
def reveal():
    if request.method == "POST":
        name = request.form.get("name")
        if name in pairings:
            match = pairings[name]
            return render_template("reveal.html", name=name, match=match)
        else:
            flash("Name not found or not a participant!")
    return render_template("reveal_input.html")

@app.route("/reset")
def reset():
    global participants, pairings
    participants = []
    pairings = {}
    flash("All participants and matches have been reset.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)