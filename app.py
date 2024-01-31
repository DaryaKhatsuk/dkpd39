from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSONB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://otter:1234@localhost/otter_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(JSONB)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form.to_dict(flat=False)
    cleaned_data = {key: value[0].strip() for key, value in data.items() if value[0].strip()}
    for current_key, current_data in cleaned_data.items():
        form_data = FormData(json_data=current_data)
        db.session.add(form_data)
        db.session.commit()
    return redirect(url_for('view_data'))


@app.route('/view')
def view_data():
    data = FormData.query.all()
    return render_template('view.html', data=data)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
