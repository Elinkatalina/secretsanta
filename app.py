from flask import Flask, render_template, request, redirect, url_for
import os
import random

app = Flask(__name__)

# In-memory list to store participants
participants = []
matches = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']  # Get the name from the form
        if name and name not in participants:  # Avoid duplicates
            participants.append(name)  # Add name to participants list
        return redirect(url_for('home'))  # Redirect to the home page
    return render_template('index.html', participants=participants)

@app.route('/generate', methods=['POST', 'GET'])
def generate_matches():
    global matches
    if len(participants) < 2:
        return "At least two participants are required to generate matches.", 400

    # Shuffle and generate matches
    shuffled = participants[:]
    random.shuffle(shuffled)
    matches = {shuffled[i]: shuffled[(i + 1) % len(shuffled)] for i in range(len(shuffled))}

    return redirect(url_for('check_match'))

@app.route('/check', methods=['GET', 'POST'])
def check_match():
    if request.method == 'POST':
        name = request.form['name']
        if name in matches:
            match = matches[name]
            return render_template('check_match.html', name=name, match=match)
        else:
            return "Name not found. Please try again.", 404
    return render_template('check_form.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

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


@app.route('/clear', methods=['POST'])
def clear_participants():
    global participants, matches
    participants = []  # Clear the participants list
    matches = {}  # Clear the matches
    return redirect(url_for('home'))  # Redirect to the home page

@app.route("/reset")
def reset():
    global participants, pairings
    participants = []
    pairings = {}
    flash("All participants and matches have been reset.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
