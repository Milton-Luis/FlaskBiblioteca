
def test_app_name(app):
    """checks if the name of the app is correct"""
    assert app.config["APP_NAME"] == "FlaskBiblioteca"


def test_env(app):
    """checks if the environment is correct"""
    assert app.config["ENV_FOR_DYNACONF"] == "testing"


# @pytest.fixture
# def init_database(app_test):
#     with app_test.app_context():
#         yield db


# @pytest.fixture
# def test_create_student(init_database):
#     user = User(
#         firstname="John",
#         lastname="Doe",
#         fullname = "John Doe",
#         email="johnDoe@j.com",
#         students=[Students(classroom="Logistica", grade="2")],
#     )
#     with current_app.app_context():
#         db.session.add(user)
#         db.session.commit()

#         return user

# def test_get_student(test_create_student):
#     user = db.session.query(Students).filter(Students.user_id == 1).first()
#     with current_app.app_context():
#         assert user is not None  # Verifica se o estudante foi encontrado
#         assert user.user_id == 1


# @pytest.fixture
# def test_create_book(init_database):
#     books = Books(
#         title="Inferno", author="Dan Brown", isbn="90um90y098m98h", total_of_books=1, available_quantity=1
#     )
#     with current_app.app_context():
#         db.session.add(books)
#         db.session.commit()
#         assert db


# def test_get_book(test_create_book):
#     book = db.session.query(Books).filter(Books.id == 1).first()
#     with current_app.app_context():
#         assert book is not None  # Verifica se o livro foi encontrado
#         assert book.title == "Inferno"


# def test_lends(test_create_book, test_create_student):
#     get_book = db.session.query(Books).filter(Books.id == 1).first()
#     get_user = db.session.query(User).filter(User.id == 1).first()

#     lending = LendingBooks(
#         lending_date=datetime.now(),
#         return_date=datetime.now() + timedelta(days=10),
#         quantity_lent=1,
#         user_id=get_user.id,
#         book_id=get_book.id,
#     )
#     with current_app.app_context():
#         db.session.add(lending)
#         db.session.commit()
#         assert get_user is not None
#         assert get_book is not None
#         assert lending.user_id == 1
#         assert lending.book_id == 1
