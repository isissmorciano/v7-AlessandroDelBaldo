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


@bp.route("/channel/<int:id>")
def channel_detail(id):
    category = categoria_repository.get_category_by_id(id)
    if category is None:
        abort(404, "Categoria non trovato.")

    # 2. Prendiamo i video del canale
    piatti = piatto_repository.get_piatti_by_category(id)

    # 3. Passiamo al template
    return render_template("categoria_detail.html", category=category, piatti=piatti)


@bp.route("/crea_categoria", methods=("GET", "POST"))
def create_channel():
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

    return render_template("create_channel.html")

@bp.route("/create_piatto", methods=("GET", "POST"))
def create_video():
    if request.method == "POST":
        categoria_id = request.form.get("categoria_id", type=int)
        nome = request.form["titolo"]
        prezzo = request.form["prezzo"]

        if not nome:
            error = "Il titolo è obbligatorio."
        if durata is None or durata <= 0:
            error = "La durata deve essere un numero positivo."
        if categoria_id is None:
            error = "Seleziona un canale."

        if error is not None:
            flash(error)
        else:
            # Creiamo il video
            video_repository.create_video(canale_id, nome, durata, immagine)
            return redirect(url_for("main.channel_detail", id=canale_id))

    # Per GET, passiamo i canali per il select
    channels = channel_repository.get_all_channels()
    return render_template("create_video.html", channels=channels)
