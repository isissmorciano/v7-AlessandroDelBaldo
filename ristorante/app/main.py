from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.repositories import categoria_repository, piatto_repository

bp = Blueprint("main", __name__)


# TODO: Implementa le route richieste dall'esercizio 1 e 2

@bp.route("/")
def index():
    # 1. Prendiamo i canali dal database
    categories: list[dict] = categoria_repository.get_all_categories()

    # 2. Passiamo la variabile 'channels' al template
    return render_template("index.html", categories=categories)


@bp.route("/categoria/<int:id>")
def categoria_detail(id):
    category = categoria_repository.get_category_by_id(id)
    if category is None:
        abort(404, "Categoria non trovata.")

    # 2. Prendiamo i video del canale
    piatti = piatto_repository.get_piatti_by_category(id)

    # 3. Passiamo al template
    return render_template("categoria_detail.html", category=category, piatti=piatti)


@bp.route("/crea_categoria", methods=("GET", "POST"))
def crea_categoria():
    if request.method == "POST":
        nome = request.form["nome"]
        error = None

        if not nome:
            error = "Il nome è obbligatorio."

        if error is not None:
            flash(error)
        else:
            # Creiamo il canale
            categoria_repository.create_category(nome)
            return redirect(url_for("main.index"))

    return render_template("create_categoria.html")

@bp.route("/create_piatto", methods=("GET", "POST"))
def crea_piatto():
    if request.method == "POST":
        categoria_id = request.form.get("categoria_id", type=int)
        nome = request.form["nome"]
        prezzo = request.form.get("prezzo", type=int)
        error = None

        if not nome:
            error = "Il nome è obbligatorio."
        if prezzo is None or prezzo <= 0:
            error = "Il prezzo deve essere un numero positivo."
        if categoria_id is None:
            error = "Seleziona una categoria."

        if error is not None:
            flash(error)
        else:
            # Creiamo il video
            piatto_repository.create_piatto(categoria_id, nome, prezzo)
            return redirect(url_for("main.categoria_detail", id=categoria_id))

    # Per GET, passiamo i canali per il select
    categories = categoria_repository.get_all_categories()
    return render_template("create_piatto.html", categories=categories)

@bp.route('/ricerca')
def ricerca():
    testo = request.args.get('q', '')   # prende il parametro GET dalla URL
    risultati = piatto_repository.find_piatti_by_name(testo)
    return render_template('index.html', lista_elementi=risultati, ricerca=testo)