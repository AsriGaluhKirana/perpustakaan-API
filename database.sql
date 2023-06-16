CREATE TABLE IF NOT EXISTS Buku(
	id SERIAL Primary Key,
	judul VARCHAR NOT NULL,
	id_penulis VARCHAR NOT NULL REFERENCES Penulis (id),
	tgl_terbit DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS Penulis(
	id VARCHAR Primary Key,
	nama VARCHAR NOT NULL,
	kebangsaan VARCHAR NOT NULL,
);
CREATE TABLE IF NOT EXISTS Kategori(
	id VARCHAR Primary Key,
	nama VARCHAR NOT NULL,
);
CREATE TABLE IF NOT EXISTS Pengguna(
	id VARCHAR Primary Key,
	nama VARCHAR NOT NULL,
	kebangsaan VARCHAR NOT NULL,
);

SELECT * FROM buku;
SELECT * FROM penulis
