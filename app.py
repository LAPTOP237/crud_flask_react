from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:3000"], "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        contenu_modif = request.form['content']
        new_contenu = Message(content=contenu_modif)
        try:
            db.session.add(new_contenu)
            db.session.commit()
            return 'Message créé avec succès', 200
        except Exception as e:
            return f'Erreur lors de l\'ajout du message: {e}'
    else:
        messages = Message.query.order_by(Message.created_at).all()
        return [message.content for message in messages], 200

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    message = Message.query.get_or_404(id)
    try:
        db.session.delete(message)
        db.session.commit()
        return 'Message supprimé avec succès'
    except Exception as e:
        return f'Erreur lors de la suppression du message : {e}'

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    message = Message.query.get_or_404(id)
    update_content = request.form['content']
    message.content = update_content
    try:
        db.session.commit()
        return 'Mise à jour du message complète'
    except Exception as e:
        return f'Erreur lors de la mise à jour du message : {e}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
