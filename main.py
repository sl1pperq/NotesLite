import json
import uuid

from flask import Flask, request, render_template, session, redirect, abort

app = Flask(__name__)
app.secret_key = 'secret'

uniqnums = {}


def save_to_storage():
    with open('file.json', 'w') as file:
        file.write(json.dumps([users, notes], ensure_ascii=False))


def load_to_storage():
    with open('file.json', 'r') as file:
        return json.loads(file.read())


try:
    users, notes = load_to_storage()
except:
    users = {}
    notes = []

def create_initial_note_for(username):
    notes.append({
        'number': '0',
        'title': 'Приветствие',
        'author': username,
        'text': 'Добро пожаловать в Notes Lite! Здесь можно легко создавать заметки, попробуйте!'
    })


@app.route('/')
def homepage():
    if session.get('auth', False) == False:
        return render_template('notreg.html')
    else:
        name = session['auth']
        return render_template('reg.html', name=name)


@app.route('/signin')
def sign_in():
    return render_template('signin.html')


@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    password = request.form['password']
    session['auth'] = name
    users[name] = password
    save_to_storage()

    create_initial_note_for(name)

    return render_template('goodsign.html')


@app.route('/trygoin', methods=['POST'])
def try_sign_up():
    name = request.form['name']
    passw = request.form['password']
    if name in users and users[name] == passw:
        return render_template('reg.html')
    else:
        return render_template('accnotfound.html')


@app.route('/reg')
def mainpage():
    return render_template('reg.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['auth']
    return render_template('notreg.html')


@app.route('/createnote', methods=['GET'])
def newnote():
    return render_template('create_note.html')


@app.route('/createnote', methods=['POST'])
def note_is_create():
    title = request.form['title']
    text = request.form['text']
    uniq_num = str(uuid.uuid4())
    if session['auth']:
        notes.append({
            'number': uniq_num,
            'title': title,
            'text': text,
            'author': session['auth']
        })

        save_to_storage()

        return render_template('sucsessnoteadd.html')
    else:
        pass


@app.route('/watch_notes')
def watch_your_note():
    user_notes = []
    for note in notes:
        if note['author'] == session.get('auth'):
            user_notes.append(note)
        else:
            pass

    # user_notes = filter(lambda x:x.get('author') == session.get('auth'), notes)

    return render_template('watchnotes.html', notes=user_notes)

@app.route('/delnotes')
def delete_note():
    for note in notes:
        if note['author'] == session['auth']:
            del note

@app.route('/delnote/<id>/')
def delnote(id):
    for i, note in enumerate(notes[:]):
        if note['number'] == id:
            del notes[i]
            break
    save_to_storage()
    return render_template('reg.html')

@app.route('/editnote/<id>/')
def edit_task_page(id):
    for i, note in enumerate(notes[:]):
        if note['number'] == id:
            return render_template('editnote.html', note=note, id=id)
            break

@app.route('/editnote/<id>/', methods=['post'])
def edit_note(id):
    title = request.form.get('title')
    text = request.form.get('text')
    if title:
        for i, note in enumerate(notes[:]):
            if note['number'] == id:
                note['title'] = title
                note['text'] = text
                break
    save_to_storage()
    return render_template('reg.html')


@app.route('/test')
def bulma_test():
    return render_template('test.html')


app.run(debug=True, port=4000)
