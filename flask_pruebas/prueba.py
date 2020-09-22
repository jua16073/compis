from flask import Flask, render_template, request

app  = Flask(__name__)

@app.route('/')
def index():
    codigo = request.form.get("codigo")
    print(codigo)
    return render_template("home.html")



if __name__ == "__main__":
    app.run(host='localhost', port = 5000, debug = True)