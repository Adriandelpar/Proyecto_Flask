import json
from flask import Flask, render_template, request, abort

app = Flask(__name__)

with open("data.json", encoding="utf-8") as f:
    raw = json.load(f)

paises = []
for i, entrada in enumerate(raw["localidades"]):
    pais = entrada["info"]["pais"].copy()
    pais["id"] = i
    pais["continente"] = entrada["info"]["continente"]
    paises.append(pais)

continentes = sorted(set(p["continente"] for p in paises))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paises")
def lista_paises():
    nombre_q  = request.args.get("nombre", "").strip()
    continente_q = request.args.get("continente", "")
    orden = request.args.get("orden", "asc")
    moneda_q = request.args.get("moneda", "")

    resultados = paises

    if nombre_q:
        resultados = [p for p in resultados if nombre_q.lower() in p["nombre"].lower()]

    if continente_q:
        resultados = [p for p in resultados if p["continente"] == continente_q]

    if moneda_q:                                   
        resultados = [p for p in resultados if p["moneda"]["nombre"] == moneda_q]
    
    if not resultados:    
        abort(404)

    resultados = sorted(resultados, key=lambda p: p["nombre"], reverse=(orden == "desc"))

    return render_template(
        "paises.html",
        paises=resultados,
        continentes=continentes,
        nombre_q=nombre_q,
        continente_q=continente_q,
        orden=orden,
        moneda_q=moneda_q,
    )


@app.route("/pais/<int:pais_id>")
def detalle_pais(pais_id):
    pais = next((p for p in paises if p["id"] == pais_id), None)
    if pais is None:
        abort(404)
    return render_template("detalle.html", pais=pais)

@app.route("/top")
def top():
    top5 = sorted(paises, key=lambda p: p["capital"]["poblacion"], reverse=True)[:5]
    return render_template("top.html", top5=top5)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
