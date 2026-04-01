from app.db import get_db


# TODO: Implementa le funzioni richieste dall'esercizio 1 e 2

def get_all_piatti():
    db = get_db()
    query = """
        SELECT id, categoria_id, nome, prezzo
        FROM piatti
        ORDER BY nome
    """
    piatti = db.execute(query).fetchall()
    return [dict(piatto) for piatto in piatti]


def get_piatti_by_category(category_id):
    db = get_db()
    query = """
        SELECT id, categoria_id, nome, prezzo
        FROM piatti
        WHERE categoria_id = ?
    """
    piatti = db.execute(query, (category_id,)).fetchall()
    return [dict(piatto) for piatto in piatti]

def get_piatto_by_id(piatto_id):
    """Recupera un singolo video per ID."""
    db = get_db()
    query = """
        SELECT id, categoria_id, nome, prezzo
        FROM piatti
        WHERE id = ?
    """
    piatto = db.execute(query, (piatto_id,)).fetchone()
    if piatto:
        return dict(piatto)
    return None
    


def create_piatto(category_id, nome, prezzo):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO piatti (categoria_id, nome, prezzo) VALUES (?, ?, ?)", 
        (category_id, nome, prezzo)
    )
    db.commit()
    return cursor.lastrowid

def find_piatti_by_name(search_term):
    db = get_db()
    # %testo% → contiene  |  testo% → inizia con  |  %testo → finisce con
    query = 'SELECT * FROM piatti WHERE nome LIKE ? ORDER BY nome'
    piatti = db.execute(query, (f'%{search_term}%',)).fetchall()
    return [dict(piatto) for piatto in piatti]