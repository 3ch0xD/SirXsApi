from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rizz.db'
db = SQLAlchemy(app)

class Rizz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rizz_sentence = db.Column(db.String(2000), unique=True, nullable=False)

@app.route('/rizz', methods=['POST'])
def create_rizz():
    sentences = request.json.get('sentences')
    for sentence in sentences:
        new_rizz = Rizz(rizz_sentence=sentence)
        db.session.add(new_rizz)
    db.session.commit()
    return jsonify({'message': 'New Rizz sentences created.'}), 201

@app.route('/rizz/<int:rizz_id>', methods=['GET'])
def get_rizz(rizz_id):
    rizz = Rizz.query.get(rizz_id)
    if rizz is None:
        return jsonify({'error': 'Rizz not found'}), 404

    template = {
        'id': rizz.id,
        'rizz_sentence': rizz.rizz_sentence,
    }       

    return jsonify(template)

@app.route('/rizz/<int:rizz_id>', methods=['DELETE'])
def delete_rizz(rizz_id):
    rizz = Rizz.query.get(rizz_id)
    if rizz is None:
        return jsonify({'error': 'Rizz not found'}), 404

    db.session.delete(rizz)
    db.session.commit()
    return jsonify({'message': 'Rizz deleted.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)