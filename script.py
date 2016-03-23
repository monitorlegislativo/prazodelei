from flask import Flask, render_template
import json, os
import prazo

app = Flask(__name__)

@app.route("/prazo/<data_inicio>")
def hello(data_inicio="21-03-2016", data_fim="21/03/2016"):
    print "Getting " + data_inicio
    if not os.path.isfile("dados/"+data_inicio+".json"):
        lista = prazo.getProposicoes(data_inicio, data_fim)
    else:
        lista = json.load(open("dados/"+data_inicio+".json", 'r'))   
    return render_template('hello.html', data_inicio=data_inicio, lista=lista)

if __name__ == "__main__":
    app.run(debug=True)
