from app import create_app, db

app = create_app()

# IMPORT MODEL BEFORE create_all()
#from app.models import Task

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)