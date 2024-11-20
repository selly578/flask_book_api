# REST API perpustakaan menggunakan flask

Ini adalah program rest api sederhana yang dapat digunakan untuk mengelola buku,peminjaman,anggota dan user,serta memiliki dukungan JWT untuk autentikasi  

## Cara install

1. Install library
    ```bash
    pip install flask flask-sqlalchemy flask-migrate pyjwt pymysql
    ```
2. Jalankan migrasi
    ```bash
    flask db migrate 

    ```
3. Jalankan 
    ```bash 
    python app.py 
    
    ```

# Dokumentasi Endpoint
Auth (User)

    POST /login – Login dan dapatkan JWT token
    POST /register – Daftar user baru

Buku (Book)

    POST /book – Tambah buku
    GET /book – Lihat semua buku
    GET /book/<id> – Lihat buku berdasarkan ID
    PUT /book/<id> – Edit buku berdasarkan ID
    DELETE /book/<id> – Hapus buku berdasarkan ID

Anggota (Member)

    POST /member – Tambah anggota baru
    GET /member – Lihat semua anggota
    GET /member/<id> – Lihat anggota berdasarkan ID

Peminjaman (Borrow)

    POST /borrow – Pinjam buku
    POST /return – Kembalikan buku
