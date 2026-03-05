from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "love_secret"

questions = [
"Who apologizes first after a fight?",
"Who is more romantic?",
"Who gets jealous more?",
"Who plans the better dates?",
"Who says 'I love you' more?",
"Who misses the other more?",
"Who would cry first in a breakup movie?",
"Who is more protective?",
"Who texts first usually?",
"Who loves the other more?"
]

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/start", methods=["POST"])
def start():
    session["player1"] = request.form["player1"]
    session["player2"] = request.form["player2"]
    session["index"] = 0
    session["score"] = 0
    return redirect("/game")


@app.route("/game", methods=["GET","POST"])
def game():

    if request.method == "POST":

        answer = request.form.get("answer")

        if answer == "match":
            session["score"] += 1

        session["index"] += 1

    index = session.get("index",0)

    if index >= len(questions):
        return redirect("/results")

    question = questions[index]

    progress = int((index/len(questions))*100)

    return render_template(
        "game.html",
        question=question,
        index=index,
        progress=progress,
        player1=session["player1"],
        player2=session["player2"]
    )


@app.route("/results")
def results():

    score = session.get("score",0)

    percentage = int((score/len(questions))*100)

    player1 = session.get("player1")
    player2 = session.get("player2")

    if percentage >= 80:
        message = "Soulmates ❤️"
    elif percentage >= 60:
        message = "Great Match 💕"
    elif percentage >= 40:
        message = "Could Work 😉"
    else:
        message = "Hmm… Work Needed 😅"

    return render_template(
        "results.html",
        percentage=percentage,
        player1=player1,
        player2=player2,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)