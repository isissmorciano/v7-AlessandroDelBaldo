from app.db import get_db




def get_all_categories():

    db = get_db()
    query = """
        SELECT id, nome
        FROM categorie
        ORDER BY nome
    """
    categorie = db.execute(query).fetchall()
    return [dict(categoria) for categoria in categorie]

def get_category_by_id(category_id):
    """Recupera un singolo gioco per ID."""
    db = get_db()
    query = """
        SELECT id, nome
        FROM categorie
        WHERE id = ?
    """
    categoria = db.execute(query, (category_id,)).fetchone()
    if categoria:
        return dict(categoria)
    return None


def create_category(nome):
    """Crea un nuovo gioco."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO categorie (nome) VALUES (?)", 
        (nome,)
    )
    db.commit()
    return cursor.lastrowid