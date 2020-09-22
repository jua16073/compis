from flask import Flask, render_template, request, session

app  = Flask(__name__)
app.secret_key = "Triceracop:D"

#session.get no truena


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods = ["POST"])
def get_code():
    code = request.form["codigo"]
    print(code)
    return render_template("home.html")





if __name__ == "__main__":
    app.run(host='localhost', port = 5000, debug = True)