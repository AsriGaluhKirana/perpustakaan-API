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
    
#table pengguna
# class Pengguna(db.Model):

transactions = []
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
            'tgl_terbit' : b.tgl_terbit
        } for b in data
    ]
    return {'count': len(response), 'data':response}

# Endpoint untuk menambahkan daftar buku
@app.route('/buku', methods=['POST'])
def create_book():
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

# Endpoint untuk menghapus data buku
@app.route('/buku/<id>', methods=['DELETE'])
def delete_buku(id):
    data = Buku.query.filter_by(id=id).first_or_404()
    db.session.delete(data)
    db.session.commit()
    return{
        'success': 'Buku berhasil dihapus'
    } 

# Endpoint untuk mengupdate buku
@app.route('/buku/<id>', methods=['PUT'])
def update_buku(id):
    buku = Buku.query.filter_by(id=id).first_or_404()
    data = request.get_json()
    buku.judul = data.get('judul'),
    buku.id_penulis = data.get('id_penulis'),
    buku.tgl_terbit = data.get('tgl_terbit')
    db.session.add(buku)
    db.session.commit()
    return {"message": "Hore! Buku berhasil diupdate."}

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
    data = request.get_json()
    new_penulis = Penulis(
        id = data.get('id'),
        nama = data.get('nama'),
        kebangsaan = data.get('kebangsaan')
    )
    db.session.add(new_penulis)
    db.session.commit()
    return {"message": "Hore! Penulis berhasil di tambahkan."}

# Endpoint untuk mengupdate penulis
@app.route('/penulis/<id>', methods=['PUT'])
def update_penulis(id):
    penulis = Penulis.query.filter_by(id=id).first_or_404()
    data = request.get_json()
    penulis.id_penulis = data.get('id_penulis'),
    penulis.nama = data.get('nama'),
    penulis.kebangsaan = data.get('kebangsaan')
    db.session.add(penulis)
    db.session.commit()
    return {"message": "Hore! Penulis berhasil diupdate."}

# Endpoint untuk menghapus data penulis
@app.route('/penulis/<id>', methods=['DELETE'])
def delete_penulis(id):
    data = Penulis.query.filter_by(id=id).first_or_404()
    db.session.delete(data)
    db.session.commit()
    return{
        'success': 'Penulis berhasil dihapus'
    } 

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