from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.static_folder = 'static'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=True)
    note = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        category_content = request.form['category']
        note_content = request.form['note']
        new_note = Note(category=category_content, note=note_content, date_created=datetime.now(pytz.timezone("CET")))
        
        print(datetime.now().strftime("%d%m%Y, %H:%M:%S"))

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding the note."


    else:
        notes = Note.query.order_by(Note.date_created).all()
        return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>') 
def delete(id):   
    note_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the note."

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note_to_update = Note.query.get_or_404(id)

    if request.method == 'POST':
        note_to_update.category = request.form['category']
        note_to_update.note = request.form['note']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating the note"
    else:
        return render_template('update.html', note=note_to_update)

if __name__ == "__main__":
    app.run(debug=True)