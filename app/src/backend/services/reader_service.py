from src.backend.extensions.database import db
from src.backend.models.reader import Reader



def create_reader(form):
    """Cria um novo livro com base nos dados do formulário e salva no banco de dados."""
    reader = Reader()

    form.populate_obj(reader)

    db.session.add(reader)

    return reader
