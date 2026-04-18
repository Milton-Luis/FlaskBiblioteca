from pathlib import Path

def test_instance_path(app):
    db_path = Path(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))
    print(db_path)
    assert db_path.parent == Path(app.instance_path)

# def app_name():
#     assert ...