from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:1@localhost:5432/perpustakaan"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#tabel Buku
class Buku(db.Model):
    __tablename__ = "buku"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    judul = db.Column(db.String, nullable=False)
    id_penulis = db.Column(db.String, db.ForeignKey("penulis.id"), nullable=False)
    id_kategori = db.Column(db.String, db.ForeignKey("kategori.id_kategori"))
    tgl_terbit = db.Column(db.Date, nullable=False)

#tabel penulis
class Penulis(db.Model):
    __tablename__ = "penulis"
    id = db.Column(db.String, primary_key=True, nullable=False)
    nama = db.Column(db.String, nullable=False)
    kebangsaan = db.Column(db.String, nullable=False)
    buku = db.relationship('Buku', backref="penulis", lazy="dynamic")
    
#tabel kategori
class Kategori(db.Model):
    __tablename__ = "kategori"
    id_kategori = db.Column(db.String, primary_key=True, nullable=False)
    nama_kategori = db.Column(db.String, nullable=False)
    buku = db.relationship('Buku', backref="kategori", lazy="dynamic")
    
#table pengguna
class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nama = db.Column(db.String)
    kontak = db.Column(db.String)
    tipe = db.Column(db.String)
    # relation_transaksi = db.relationship('Transaksi', backref='pengguna', lazy='dynamic')
    
def login():
    username = request.authorization.get("username")
    password = request.authorization.get("password")
    
    try:
        global user
        user = Pengguna.query.filter_by(email=username).first_or_404()
    except:
        return {
            'error message' : 'Hayo salah.'
        }
        
    if user.password == password:
        if user.tipe == 'Admin':
            return 'Admin'
        elif user.tipe == 'Member':
            return 'Member'
    else:
        return 'Password salah!'
    
# Endpoint untuk mendapatkan daftar semua buku
@app.route('/buku', methods=['GET'])
def get_books():
    data = Buku.query.all()
    response = [
        {
            'id': b.id,
            'judul' : b.judul,
            'id_penulis' : b.id_penulis,
            'nama_penulis' : b.penulis.nama,
            'kategori' : b.kategori.nama,
            'tgl_terbit' : b.tgl_terbit
        } for b in data
    ]
    return {'count': len(response), 'data':response}

# Endpoint untuk menambahkan daftar buku
@app.route('/buku', methods=['POST'])
def create_book():
    if login() == 'Admin':
        data = request.get_json()
        new_buku = Buku(
            id = data.get('id'),
            judul = data.get('judul'),
            id_penulis = data.get('id_penulis'),
            tgl_terbit = data.get('tgl_terbit')
        )
        db.session.add(new_buku)
        db.session.commit()
        return {"message": "Hore! Buku berhasil di tambahkan."}
    else:
        return {"message": "Eits, kamu bukan admin!"} 
    
# Endpoint untuk menghapus data buku
@app.route('/buku/<id>', methods=['DELETE'])
def delete_buku(id):
    if login() == 'Admin':
        data = Buku.query.filter_by(id=id).first_or_404()
        db.session.delete(data)
        db.session.commit()
        return{
            'success': 'Buku berhasil dihapus'
        }
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk mengupdate buku
@app.route('/buku/<id>', methods=['PUT'])
def update_buku(id):
    if login() == 'Admin':
        buku = Buku.query.filter_by(id=id).first_or_404()
        data = request.get_json()
        buku.judul = data.get('judul'),
        buku.id_penulis = data.get('id_penulis'),
        buku.tgl_terbit = data.get('tgl_terbit')
        db.session.add(buku)
        db.session.commit()
        return {"message": "Hore! Buku berhasil diupdate."}
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk mendapatkan daftar semua penulis
@app.route('/penulis', methods=['GET'])
def get_author():
    data = Penulis.query.all()
    response = [
        {
            'id': p.id,
            'nama' : p.nama,
            'kebangsaan' : p.kebangsaan
        } for p in data
    ]
    return {'count': len(response), 'data':response}

# Endpoint untuk menambahkan daftar penulis
@app.route('/penulis', methods=['POST'])
def create_author():
    if login() == 'Admin':
        data = request.get_json()
        new_penulis = Penulis(
            id = data.get('id'),
            nama = data.get('nama'),
            kebangsaan = data.get('kebangsaan')
        )
        db.session.add(new_penulis)
        db.session.commit()
        return {"message": "Hore! Penulis berhasil di tambahkan."}
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk mengupdate penulis
@app.route('/penulis/<id>', methods=['PUT'])
def update_penulis(id):
    if login() == 'Admin':
        penulis = Penulis.query.filter_by(id=id).first_or_404()
        data = request.get_json()
        penulis.id_penulis = data.get('id_penulis'),
        penulis.nama = data.get('nama'),
        penulis.kebangsaan = data.get('kebangsaan')
        db.session.add(penulis)
        db.session.commit()
        return {"message": "Hore! Penulis berhasil diupdate."}
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk menghapus data penulis
@app.route('/penulis/<id>', methods=['DELETE'])
def delete_penulis(id):
    if login() == 'Admin':
        data = Penulis.query.filter_by(id=id).first_or_404()
        db.session.delete(data)
        db.session.commit()
        return{
            'success': 'Penulis berhasil dihapus'
        }
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk mendapatkan daftar semua kategori
@app.route('/kategori', methods=['GET'])
def get_genre():
    data = Kategori.query.all()
    response = [
        {
            'id_kategori': k.id_kategori,
            'nama_kategori' : k.nama_kategori,
        } for k in data
    ]
    return {'count': len(response), 'data':response}

# Endpoint untuk menambahkan daftar kategori
@app.route('/kategori', methods=['POST'])
def create_genre():
    if login() == 'Admin':
        data = request.get_json()
        new_kategori = Kategori(
            id_kategori = data.get('id_kategori'),
            nama_kategori = data.get('nama_kategori')
        )
        db.session.add(new_kategori)
        db.session.commit()
        return {"message": "Hore! Kategori berhasil di tambahkan."}
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk mengupdate kategori
@app.route('/kategori/<id>', methods=['PUT'])
def update_kategori(id):
    if login() == 'Admin':
        kategori = Kategori.query.filter_by(id_kategori=id).first_or_404()
        data = request.get_json()
        kategori.id_kategori = data.get('id_kategori'),
        kategori.nama_kategori = data.get('nama_kategori'),
        db.session.add(kategori)
        db.session.commit()
        return {"message": "Hore! Kategori berhasil diupdate."}
    else:
        return {"message": "Eits, kamu bukan admin!"}

# Endpoint untuk menghapus data kategori
@app.route('/kategori/<id>', methods=['DELETE'])
def delete_kategori(id):
    if login() == 'Admin':
        data = Kategori.query.filter_by(id_kategori=id).first_or_404()
        db.session.delete(data)
        db.session.commit()
        return{
            'success': 'Kategori berhasil dihapus'
        }
    else:
        return {"message": "Eits, kamu bukan admin!"} 

# # Endpoint untuk membuat peminjaman buku
# @app.route('/transaksi', methods=['POST'])
# def create_transaction():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     book_id = data.get('book_id')
#     user = next((user for user in pengguna if user['id'] == user_id), None)
#     book = next((book for book in buku if book['id'] == book_id), None)

#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#     if not book:
#         return jsonify({'message': 'Book not found'}), 404
#     if user['type'] != 'member':
#         return jsonify({'message': 'Only members can request a book'}), 403
#     if book['status'] != 'available':
#         return jsonify({'message': 'Book is not available'}), 403

#     transaction = {
#         'user_id': user_id,
#         'book_id': book_id,
#         'status': 'requested'
#     }
#     transactions.append(transaction)

#     return jsonify({'message': 'Transaction created', 'transaction': transaction}), 201

# # Endpoint untuk mengubah status peminjaman buku (approve/return)
# @app.route('/transaksi/<int:transaction_id>', methods=['PUT'])
# def update_transaction(transaction_id):
#     data = request.get_json()
#     status = data.get('status')
#     transaction = next((transaction for transaction in transactions if transaction['id'] == transaction_id), None)

#     if not transaction:
#         return jsonify({'message': 'Transaction not found'}), 404

#     if status not in ['approved', 'returned']:
#         return jsonify({'message': 'Invalid status'}), 400

#     transaction['status'] = status

    # # Update status buku jika peminjaman dikembalikan
    # if status == 'returned':
    #     book = next((book for book in buku if book['id'] == transaction['book_id']), None)
    #     if book:
    #         book['status'] = 'available'

    # return jsonify({'message': 'Transaction updated', 'transaction': transaction})

if __name__ == '__main__':
    app.run(debug=True)