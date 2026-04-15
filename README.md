# Sistem Rekomendasi Produk
### Pertemuan 13 — Scalability & Production Deployment
Mata Kuliah Sistem Rekomendasi | Sub-CPMK 2.3 & 4.2

---

## Deskripsi

Project ini adalah implementasi sistem rekomendasi produk berbasis content-based filtering menggunakan cosine similarity, di-deploy sebagai REST API dengan FastAPI dan dilengkapi tampilan web interaktif.

---

## Fitur

- Rekomendasi produk berdasarkan kemiripan fitur
- Auto-suggest saat mengetik nama produk
- REST API dengan dokumentasi otomatis (Swagger UI)
- Logging response time setiap request
- Cache sederhana untuk efisiensi
- Unit test dengan pytest
- Load test dengan Locust
- Siap containerisasi dengan Docker

---

## Struktur Project

```
├── main.py                  # API FastAPI
├── model.py                 # Logika rekomendasi
├── requirements.txt         # Dependencies
├── Dockerfile               # Konfigurasi Docker
├── data/
│   └── products.csv         # Dataset produk
├── templates/
│   └── index.html           # Tampilan web
└── tests/
    ├── test_model.py        # Unit test
    └── locustfile.py        # Load test
```

---

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2. Buat dan aktifkan virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan server

```bash
uvicorn main:app --reload
```

Buka browser ke http://127.0.0.1:8000

---

## Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | / | Halaman web utama |
| GET | /recommend/{keyword} | Ambil rekomendasi produk |
| GET | /search/{keyword} | Cari produk (auto-suggest) |
| GET | /products | Daftar semua produk |
| GET | /docs | Dokumentasi API (Swagger UI) |

Contoh request:
```
GET http://127.0.0.1:8000/recommend/Smart
```

Contoh response:
```json
{
  "input": "Smart",
  "recommendations": ["Wireless Earbuds", "Mechanical Keyboard", "Gaming Mouse RGB"]
}
```

---

## Testing

### Unit Test

```bash
pip install pytest
pytest tests/test_model.py -v
```

### Load Test

```bash
pip install locust
locust -f tests/locustfile.py --host=http://localhost:8000
```

Buka http://localhost:8089, set jumlah user dan klik Start.

---

## Docker

Pastikan Docker Desktop sudah terinstall dan berjalan.
Download: https://www.docker.com/products/docker-desktop/

### Build image

```bash
docker build -t recommender-app .
```

Tunggu hingga proses selesai. Ini akan menginstall semua dependencies di dalam container.

### Jalankan container

```bash
docker run -p 8000:8000 recommender-app
```

Buka browser ke http://localhost:8000

### Jalankan di background (opsional)

```bash
docker run -d -p 8000:8000 --name rekomendasi recommender-app
```

### Stop container

```bash
docker stop rekomendasi
```

### Cek container yang sedang berjalan

```bash
docker ps
```

---

## Tugas Mahasiswa

Kembangkan project ini dengan:
1. Ganti dataset dengan produk/item pilihan sendiri (minimal 20 data, minimal 3 fitur)
2. Pastikan semua endpoint berjalan
3. Jalankan unit test — semua harus PASSED
4. Lakukan load test dan screenshot hasilnya
5. Build Docker image

---

## Lisensi

MIT License — bebas digunakan untuk keperluan pendidikan.
