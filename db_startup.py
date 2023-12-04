from app import app, db

@app.cli.command()
def initdb():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run()