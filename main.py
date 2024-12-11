from flask import Flask, render_template, request, redirect
import speech_recognition as speech_recog
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    mic = speech_recog.Microphone()
    recog = speech_recog.Recognizer()
    
    with mic as audio_file:
        recog.adjust_for_ambient_noise(audio_file)
        audio = recog.listen(audio_file)
    
    try:
        text = recog.recognize_google(audio, language="en-GB")
        print("Texto reconocido:", text)
        return text 
    except speech_recog.UnknownValueError:
        return "No se pudo entender lo que dijiste."
    except speech_recog.RequestError:
        return "Error en la conexión con el servicio de Google."


@app.route('/')
def index():
    cards = Card.query.order_by(Card.id).all() 
    return render_template('index.html', cards=cards)


@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)  
    return render_template('card.html', card=card)

@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route('/form_create', methods=['POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/')

@app.route('/delete_all', methods=['POST'])
def delete_all():
    Card.query.delete()  
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
