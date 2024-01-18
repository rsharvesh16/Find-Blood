# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    donors = Donor.query.all()
    return render_template('index.html', donors=donors)

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        blood_group = request.form['blood_group']
        city = request.form['city']

        new_donor = Donor(name=name, contact=contact, blood_group=blood_group, city=city)
        db.session.add(new_donor)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_donor.html')

@app.route('/update_donor/<int:id>', methods=['GET', 'POST'])
def update_donor(id):
    donor = Donor.query.get(id)

    if request.method == 'POST':
        donor.name = request.form['name']
        donor.contact = request.form['contact']
        donor.blood_group = request.form['blood_group']
        donor.city = request.form['city']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update_donor.html', donor=donor)

@app.route('/delete_donor/<int:id>')
def delete_donor(id):
    donor = Donor.query.get(id)
    db.session.delete(donor)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
