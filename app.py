from flask import Flask, render_template, request, redirect, url_for
import os

# Initialize Flask app
app = Flask(__name__)

# Define a route
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')  # This will render index.html
        if request.method == 'POST':
        name = request.form['name']  # Get the name from the form
        if name and name not in participants:  # Avoid duplicates
            participants.append(name)  # Add name to participants list
        return redirect(url_for('home'))  # Redirect to the home page
    return render_template('index.html', participants=participants)

if __name__ == "__main__":
    # Ensure app runs on the correct host and port when deployed
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

@app.route("/reset")
def reset():
    global participants, pairings
    participants = []
    pairings = {}
    flash("All participants and matches have been reset.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
