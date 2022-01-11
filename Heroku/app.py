from flask import Flask, render_template, request
from flask import jsonify
from simple_search import search, homologous

app = Flask(__name__)


@app.route('/', methods=["GET"])
def homepage():
    return render_template('home.html')


@app.route('/home', methods=["POST", "GET"])
def sonam():
    if request.method == "GET":
        return render_template('home2.html')
    else:
        data = request.form.get("data")
        link1 = "/identical-api/"+data
        link2 = "/homologous-api/"+data
        return render_template('home2.html', data1=link1, data2=link2)


@app.route('/identical', methods=["POST", "GET"])
def newpage():
    if request.method == "POST":
        data = request.form.get("identical_input")
        outputs = search(data)
        seq = outputs[0]
        inf = outputs[1]
        return render_template('display.html', seq=seq, inf=inf)
         # return jsonify(search(data))
    else:
        return "<h1>Please use the form!</h1><br><a href='/'>Go back</a>"


@app.route('/homologous', methods=["POST", "GET"])
def homologous_page():
    if request.method == "POST":
        data = request.form.get("homologous_input")
        output = homologous(data)
        seq,inf = output[0],output[1]
        return render_template('display2.html', seq=seq, inf=inf)
    else:
        return "<h1>Please use the form!</h1><br><a href='/'>Go back</a>"


@app.route('/identical-api/<currid>')
def newpage_api(currid):
    return jsonify(search(currid))


@app.route('/homologous-api/<currid>')
def homologous_page_api(currid):
    return jsonify(homologous(currid))


if __name__ == '__main__':
    app.run()
