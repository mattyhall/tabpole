from flask import Flask, request, render_template, make_response
import os
import tempfile
import sys
sys.path.insert(0, '../')
from tabpole import TabToSheetMusic

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

def get_configuration():
    ride = request.form['ride']
    crash = request.form['crash']
    hats = request.form['hihats']
    snare = request.form['snare']
    htom = request.form['htom']
    mtom = request.form['mtom']
    ftom = request.form['ftom']
    bass = request.form['bass']
    lilypond_drums = {ride: 'cymr', crash: 'cymc', hats: 'hh', snare: 'sn', htom: 'tomh', mtom: 'tommh', ftom: 'toml', bass: 'bd'}
    flam = request.form['flam']
    double = request.form['double']
    ohh = request.form['openhh']
    return lilypond_drums, flam, double, ohh

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        lilypond_drums, flam, double, ohh = get_configuration()
        title = request.form.get('title', '')
        artist = request.form.get('artist', '')
        tab = request.form['tab']
        converter = TabToSheetMusic(lilypond_drums, flam, double, ohh)
        name = ''
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            ly = converter.generate_lilypond(tab, title, artist)
            temp.write(bytes(ly, 'UTF-8'))
            name = temp.name
        print(name)
        os.system('lilypond --pdf -o {0} {0}'.format(name))
        os.remove(name)
        pdf = open(name + '.pdf', 'rb').read()
        os.remove(name + '.pdf')
        response = make_response(pdf)
        response.headers['Content-Disposition'] = 'attachment; filename="score.pdf"'
        response.mimetype = 'application/pdf'
        return response

if __name__ == '__main__':
    app.run(debug=True)
