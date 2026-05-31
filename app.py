from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import mysql.connector
import uuid

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'star_cinema'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)
def call_proc(proc_name, args=()):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc(proc_name, args)
    results = []
    for r in cursor.stored_results():
        rows = r.fetchall()
        for row in rows:
            for key, val in row.items():
                if hasattr(val, 'total_seconds'):
                    total = int(val.total_seconds())
                    row[key] = f"{total//3600:02d}:{(total%3600)//60:02d}"
                elif hasattr(val, 'isoformat'):
                    row[key] = str(val)
        results.extend(rows)
    conn.commit()
    cursor.close()
    conn.close()
    return results
def new_id():
    return str(uuid.uuid4())

def fix_time(saat):
    try:
        return datetime.strptime(saat, '%I:%M %p').strftime('%H:%M')
    except:
        return saat

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/musteriler', methods=['GET'])
def musteriler_listele():
    filtre = request.args.get('q', '')
    if filtre:
        data = call_proc('sc_MusteriBul', (filtre,))
    else:
        data = call_proc('sc_MusterilerHepsi')
    return jsonify(data)

@app.route('/api/musteriler', methods=['POST'])
def musteri_ekle():
    d = request.json
    call_proc('sc_MusteriEkle', (new_id(), d['ad'], d['soyad'], d['tel'], d['mail'], d['adres']))
    return jsonify({'ok': True})

@app.route('/api/musteriler/<id>', methods=['PUT'])
def musteri_guncelle(id):
    d = request.json
    call_proc('sc_MusteriGuncelle', (id, d['ad'], d['soyad'], d['tel'], d['mail'], d['adres']))
    return jsonify({'ok': True})

@app.route('/api/musteriler/<id>', methods=['DELETE'])
def musteri_sil(id):
    call_proc('sc_MusteriSil', (id,))
    return jsonify({'ok': True})

@app.route('/api/musteriler/<id>/harcama')
def musteri_harcama(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT fn_MusteriToplamHarcama(%s)", (id,))
    row = cursor.fetchone()
    cursor.close(); conn.close()
    return jsonify({'toplam': row[0] if row else 0})

@app.route('/api/filmler', methods=['GET'])
def filmler_listele():
    return jsonify(call_proc('sc_FilmlerHepsi'))

@app.route('/api/filmler', methods=['POST'])
def film_ekle():
    d = request.json
    call_proc('sc_FilmEkle', (new_id(), d['ad'], d['tur'], int(d['sure']), d['yonetmen'], int(d['yas']), d['aciklama']))
    return jsonify({'ok': True})

@app.route('/api/filmler/<id>', methods=['PUT'])
def film_guncelle(id):
    d = request.json
    call_proc('sc_FilmGuncelle', (id, d['ad'], d['tur'], int(d['sure']), d['yonetmen'], int(d['yas']), d['aciklama']))
    return jsonify({'ok': True})

@app.route('/api/filmler/<id>', methods=['DELETE'])
def film_sil(id):
    call_proc('sc_FilmSil', (id,))
    return jsonify({'ok': True})

@app.route('/api/salonlar', methods=['GET'])
def salonlar_listele():
    return jsonify(call_proc('sc_SalonlarHepsi'))

@app.route('/api/salonlar', methods=['POST'])
def salon_ekle():
    d = request.json
    call_proc('sc_SalonEkle', (new_id(), d['ad'], int(d['kapasite']), d['tur']))
    return jsonify({'ok': True})

@app.route('/api/salonlar/<id>', methods=['PUT'])
def salon_guncelle(id):
    d = request.json
    call_proc('sc_SalonGuncelle', (id, d['ad'], int(d['kapasite']), d['tur']))
    return jsonify({'ok': True})

@app.route('/api/salonlar/<id>', methods=['DELETE'])
def salon_sil(id):
    call_proc('sc_SalonSil', (id,))
    return jsonify({'ok': True})

@app.route('/api/seanslar', methods=['GET'])
def seanslar_listele():
    return jsonify(call_proc('sc_SeanslarHepsi'))

@app.route('/api/seanslar', methods=['POST'])
def seans_ekle():
    d = request.json
    saat = fix_time(d['saat'])
    call_proc('sc_SeansEkle', (new_id(), d['film_id'], d['salon_id'], d['tarih'], saat, float(d['fiyat'])))
    return jsonify({'ok': True})

@app.route('/api/seanslar/<id>', methods=['PUT'])
def seans_guncelle(id):
    d = request.json
    saat = fix_time(d['saat'])
    call_proc('sc_SeansGuncelle', (id, d['film_id'], d['salon_id'], d['tarih'], saat, float(d['fiyat'])))
    return jsonify({'ok': True})

@app.route('/api/seanslar/<id>', methods=['DELETE'])
def seans_sil(id):
    call_proc('sc_SeansSil', (id,))
    return jsonify({'ok': True})

@app.route('/api/seanslar/<id>/dolu')
def seans_dolu(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT fn_DoluKoltukSayisi(%s)", (id,))
    row = cursor.fetchone()
    cursor.close(); conn.close()
    return jsonify({'dolu': row[0] if row else 0})

@app.route('/api/biletler', methods=['GET'])
def biletler_listele():
    return jsonify(call_proc('sc_BiletlerHepsi'))

@app.route('/api/biletler', methods=['POST'])
def bilet_ekle():
    d = request.json
    try:
        call_proc('sc_BiletEkle', (
            new_id(), d['musteri_id'], d['seans_id'],
            d['koltuk_no'], d['koltuk_tur'],
            d['satis_tarih'], d['odeme_tur'], float(d['tutar'])
        ))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'hata': str(e)}), 400

@app.route('/api/biletler/<id>', methods=['DELETE'])
def bilet_sil(id):
    call_proc('sc_BiletSil', (id,))
    return jsonify({'ok': True})

@app.route('/api/biletler/musteri/<id>')
def musteri_biletleri(id):
    return jsonify(call_proc('sc_MusteriBiletleri', (id,)))

@app.route('/api/rapor/gunluk')
def gunluk_rapor():
    tarih = request.args.get('tarih')
    return jsonify(call_proc('sc_GunlukSatislar', (tarih,)))

if __name__ == '__main__':
    app.run(debug=True, port=5000)