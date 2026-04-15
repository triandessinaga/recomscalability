# PANDUAN PRAKTIKUM
# Sistem Rekomendasi — Deploy & Testing API
# Pertemuan 14 | Mata Kuliah Sistem Rekomendasi

---

## Apa yang Akan Kita Buat?

Di praktikum ini kita akan membuat sebuah **sistem rekomendasi produk** yang bisa diakses lewat browser. Bayangkan seperti fitur "Produk yang mungkin kamu suka" di Tokopedia atau Shopee — itulah yang akan kita buat, versi sederhananya.

Hasil akhirnya:
- Kamu ketik nama produk di kolom pencarian
- Sistem otomatis menyarankan produk yang mirip
- Semua berjalan lewat API yang kita buat sendiri

---

## Konsep Dasar (Baca Dulu Sebelum Coding)

### Apa itu API?

API (Application Programming Interface) adalah jembatan antara dua program. Saat kamu buka aplikasi cuaca di HP, aplikasi itu tidak punya data cuaca sendiri — dia minta data ke server lewat API, lalu menampilkannya ke kamu.

Di project ini, browser kamu adalah "aplikasi", dan `main.py` adalah "server" yang menyediakan data rekomendasi lewat API.

### Apa itu Content-Based Filtering?

Ini adalah salah satu teknik sistem rekomendasi. Cara kerjanya sederhana:

> "Kalau dua produk punya fitur yang sama, berarti mereka mirip."

Contoh: Smart Watch dan Wireless Earbuds sama-sama punya `category=tech`, `tech_level=high`, `price_range=medium`. Karena fiturnya mirip, keduanya akan saling direkomendasikan.

### Apa itu Cosine Similarity?

Ini adalah cara mengukur seberapa mirip dua produk. Hasilnya angka antara 0 sampai 1:
- Angka mendekati **1** = sangat mirip
- Angka mendekati **0** = sangat berbeda

Kita tidak perlu hafal rumusnya — yang penting paham konsepnya: semakin banyak fitur yang sama, semakin tinggi skornya.

### Apa itu Virtual Environment?

Bayangkan kamu punya dua project Python — satu butuh library versi lama, satu butuh versi baru. Kalau diinstall di tempat yang sama, pasti bentrok.

Virtual environment adalah "ruang terpisah" untuk setiap project. Library yang diinstall di satu project tidak akan mengganggu project lain.

---

## Persiapan

### Yang Harus Diinstall Dulu

1. **Python 3.10+** → https://www.python.org/downloads/
   Saat install, centang "Add Python to PATH"

2. **Visual Studio Code** → https://code.visualstudio.com/
   Text editor untuk menulis kode

Cek Python sudah terinstall — buka Command Prompt, ketik:
```
python --version
```
Harus muncul versi Python, contoh: `Python 3.11.0`

---

## LANGKAH 1 — Siapkan Project

Buka Command Prompt, jalankan perintah berikut:

```
mkdir rekomendasi
cd rekomendasi
python -m venv venv
venv\Scripts\activate
```

Penjelasan:
- `mkdir rekomendasi` → buat folder bernama "rekomendasi"
- `cd rekomendasi` → masuk ke folder tersebut
- `python -m venv venv` → buat virtual environment bernama "venv"
- `venv\Scripts\activate` → aktifkan virtual environment

Kalau berhasil, di depan baris terminal akan muncul `(venv)` seperti ini:
```
(venv) C:\Users\nama\rekomendasi>
```

Sekarang install semua library yang dibutuhkan:

```
pip install -r requirements.txt
```

> File `requirements.txt` sudah a| Menampilkan file HTML di browser |

Kenapa versinya di-pin (dikunci)? Supaya semua mahasiswa pakai versi yang sama dan tidak ada perbedaan perilaku antar komputer.

---

## LANGKAH 3 — Pahami Dataset (data/products.csv)

Buka file `data/products.csv`. Isinya seperti ini:

```
product,category,style,tech_level,price_range
LED Strip Lights,aesthetic,low,medium,low
Gaming Mouse RGB,gaming,high,high,medium
Korean Hoodie,fashion,medium,low,medium
...
```

Dataset ini berisi 15 produk dengan 4 fitur:

| Kolom | Isi | Contoh nilai |
|---|---|---|
| product | Nama produk | Smart Watch |
| category | Kategori produk | tech, gaming, fashion |
| style | Tingkat gaya | low, medium, high |
| tech_level | Tingkat teknologi | low, medium, high |
| price_range | Kisaran harga | low, medium, high |

Fitur-fitur inilah yang digunakan untuk menghitung kemiripan antar produk. Semakin banyak fitur yang sama nilainya, semakin mirip dua produk tersebut.

---

## LANGKAH 4 — Pahami dan Jalankan model.py

File `model.py` adalah otak dari sistem rekomendasi kita. Buka file ini dan perhatikan alurnya:

### Alur kerja model.py

```
1. Baca products.csv
        ↓
2. Ubah teks → angka (encoding)
        ↓
3. Hitung kemiripan semua produk (cosine similarity)
        ↓
4. Siap menerima keyword dan mengembalikan rekomendasi
```

### Bagian penting yang perlu dipahami

**Encoding — mengubah teks menjadi angka**

Komputer tidak bisa menghitung kemiripan dari teks seperti "gaming" atau "fashion". Kita perlu mengubahnya menjadi angka dulu.

Fungsi `pd.get_dummies()` melakukan ini secara otomatis. Contohnya:

Sebelum encoding:
```
category
gaming
fashion
tech
```

Setelah encoding:
```
category_gaming  category_fashion  category_tech
1                0                 0
0                1                 0
0                0                 1
```

Setiap kategori jadi kolom sendiri. Nilai 1 berarti "ya", nilai 0 berarti "tidak".

**Cache — menyimpan hasil agar tidak dihitung ulang**

```python
_cache = {}

def recommend(keyword):
    if keyword in _cache:
        return _cache[keyword]  # langsung return, tidak hitung ulang
    ...
    _cache[keyword] = result
    return result
```

Kalau user mencari "Smart" dua kali, perhitungan hanya dilakukan sekali. Hasil pertama disimpan di `_cache`, pencarian kedua langsung ambil dari sana. Ini membuat sistem lebih cepat.

### Test model secara langsung

Sebelum lanjut, coba test apakah model bekerja dengan benar. Jalankan di terminal:

```
python -c "from model import recommend; print(recommend('Smart'))"
```

Harus muncul output seperti:
```
['Wireless Earbuds', 'Mechanical Keyboard', 'Gaming Mouse RGB']
```

Kalau muncul, berarti model berjalan dengan benar.

---

## LANGKAH 5 — Pahami dan Jalankan main.py

File `main.py` adalah pintu masuk API kita. Di sinilah kita mendefinisikan endpoint — alamat URL yang bisa diakses oleh browser atau aplikasi lain.

### Endpoint yang tersedia

| URL | Fungsi |
|---|---|
| `GET /` | Tampilkan halaman web utama |
| `GET /recommend/{keyword}` | Ambil rekomendasi berdasarkan keyword |
| `GET /search/{keyword}` | Cari produk untuk auto-suggest |
| `GET /products` | Lihat semua produk |

### Middleware Logging

Di `main.py` ada kode ini:

```python
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {duration:.3f}s - {response.status_code}")
    return response
```

Ini adalah **middleware** — kode yang berjalan otomatis setiap kali ada request masuk. Fungsinya mencatat setiap aktivitas ke terminal, contoh outputnya:

```
INFO: GET /recommend/Smart - 0.003s - 200
INFO: GET /search/gaming - 0.001s - 200
```

Format: `METHOD PATH - DURASI - STATUS`
- `200` = sukses
- `404` = tidak ditemukan
- `500` = error di server

Ini berguna untuk **monitoring** — kita bisa tahu endpoint mana yang lambat atau sering error.

### Jalankan server

```
uvicorn main:app --reload
```

Kalau berhasil, terminal menampilkan:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

Buka browser ke:
- **http://127.0.0.1:8000** → halaman web
- **http://127.0.0.1:8000/docs** → dokumentasi API otomatis (Swagger UI)
- **http://127.0.0.1:8000/recommend/Smart** → test rekomendasi langsung

---

## LANGKAH 6 — Pahami Tampilan Web (templates/index.html)

File `index.html` adalah tampilan yang dilihat user di browser. Ada dua fitur utama:

### Fitur 1 — Auto-suggest

Saat user mengetik, JavaScript mengirim request ke `/search/{keyword}` dan menampilkan dropdown produk yang cocok. Ini terjadi secara real-time tanpa perlu klik tombol.

### Fitur 2 — Rekomendasi

Saat user klik "Cari" atau tekan Enter, JavaScript mengirim request ke `/recommend/{keyword}` dan menampilkan 3 produk rekomendasi beserta response time-nya.

### Coba di browser

1. Buka http://127.0.0.1:8000
2. Ketik "Smart" di kolom pencarian
3. Perhatikan dropdown muncul otomatis
4. Klik salah satu atau tekan Enter
5. Lihat 3 rekomendasi muncul di bawah

---

## LANGKAH 7 — Unit Testing (tests/test_model.py)

### Apa itu Unit Test?

Unit test adalah cara otomatis untuk memastikan fungsi kita bekerja dengan benar. Daripada test manual setiap kali ada perubahan, kita tulis kode test sekali dan jalankan kapanpun dibutuhkan.

Bayangkan seperti checklist otomatis:
- ✓ Apakah fungsi recommend() mengembalikan hasil saat keyword ditemukan?
- ✓ Apakah mengembalikan list kosong saat keyword tidak ada?
- ✓ Apakah "smart" dan "SMART" menghasilkan hasil yang sama?

### Jalankan unit test

Install pytest dulu:
```
pip install pytest
```

Jalankan test:
```
pytest tests/test_model.py -v
```

Hasil yang diharapkan:
```
tests/test_model.py::test_recommend_found           PASSED
tests/test_model.py::test_recommend_not_found       PASSED
tests/test_model.py::test_recommend_case_insensitive PASSED
tests/test_model.py::test_recommend_cached          PASSED
tests/test_model.py::test_search_found              PASSED
tests/test_model.py::test_search_not_found          PASSED

6 passed in 1.23s
```

Kalau ada yang FAILED, berarti ada bug di kode yang perlu diperbaiki sebelum deploy.

---

## LANGKAH 8 — Load Testing (tests/locustfile.py)

### Apa itu Load Test?

Unit test memastikan fungsi bekerja dengan benar. Load test memastikan sistem tetap bekerja dengan baik saat **banyak user mengakses bersamaan**.

Bayangkan 100 orang membuka website kamu di waktu yang sama — apakah server masih bisa merespons dengan cepat? Load test menjawab pertanyaan ini.

### Jalankan load test

Pastikan server masih berjalan di terminal pertama. Buka terminal baru, lalu:

```
pip install locust
locust -f tests/locustfile.py --host=http://localhost:8000
```

Buka browser ke **http://localhost:8089**, lalu:
1. Number of users: isi `10`
2. Spawn rate: isi `2`
3. Klik **Start swarming**

### Cara membaca hasil

| Kolom | Arti | Target |
|---|---|---|
| RPS | Request per detik yang ditangani | Semakin tinggi semakin baik |
| Response time (ms) | Kecepatan server merespons | Di bawah 500ms |
| Failures | Request yang gagal | Harus 0% |

Kalau response time tinggi atau ada failures, berarti server perlu dioptimasi sebelum deploy ke production.

---

## LANGKAH 9 — Docker (Dockerfile)

### Apa itu Docker?

Masalah klasik programmer: "Di komputer saya jalan, tapi di komputer teman tidak jalan."

Penyebabnya biasanya perbedaan versi Python, library, atau sistem operasi. Docker menyelesaikan masalah ini dengan cara membungkus aplikasi beserta semua dependensinya ke dalam satu paket yang disebut **container**.

Container ini bisa dijalankan di komputer manapun yang punya Docker — hasilnya selalu sama.

### Analogi sederhana

Docker seperti **toples kaca** yang berisi makanan. Isi di dalam toples tidak terpengaruh oleh lingkungan luar. Kamu bisa pindahkan toples ke mana saja, isinya tetap sama.

### Install Docker Desktop

Download di: https://www.docker.com/products/docker-desktop/

Pastikan Docker Desktop sudah berjalan (ada ikon Docker di taskbar).

### Jalankan dengan Docker

Build image (buat "toples"-nya):
```
docker build -t recommender-app .
```

Jalankan container:
```
docker run -p 8000:8000 recommender-app
```

Buka browser ke http://localhost:8000 — aplikasi berjalan di dalam Docker.

Perintah lain yang berguna:

```bash
# Jalankan di background
docker run -d -p 8000:8000 --name rekomendasi recommender-app

# Lihat container yang sedang berjalan
docker ps

# Stop container
docker stop rekomendasi
```

---

## Checklist Sebelum Selesai

Pastikan semua poin ini sudah terpenuhi:

- [ ] Virtual environment aktif (ada tulisan `(venv)`)
- [ ] Semua library terinstall (`pip install -r requirements.txt`)
- [ ] Server berjalan di http://127.0.0.1:8000
- [ ] Auto-suggest berfungsi saat mengetik di kolom pencarian
- [ ] Rekomendasi muncul saat klik tombol Cari
- [ ] Semua 6 unit test PASSED
- [ ] Load test berjalan tanpa failures
- [ ] Docker berhasil build dan run

---

## Troubleshooting

| Error | Kemungkinan Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError` | Library belum terinstall | Jalankan `pip install -r requirements.txt` |
| `Address already in use` | Port 8000 sudah dipakai | Ganti port: `uvicorn main:app --port 8001` |
| `No such file: products.csv` | File tidak ada di folder `data/` | Pastikan file ada di lokasi yang benar |
| `Internal Server Error` | Error di kode server | Cek pesan error di terminal uvicorn |
| `(venv) tidak muncul` | Virtual environment belum aktif | Jalankan `venv\Scripts\activate` |

---

## Tugas

Kembangkan project ini dengan dataset kamu sendiri:

1. Buat dataset baru minimal 20 produk/item dengan minimal 3 fitur
2. Ganti isi `data/products.csv` dengan dataset kamu
3. Jalankan server dan pastikan rekomendasi berjalan
4. Jalankan unit test — semua harus PASSED
5. Lakukan load test dengan 20 user, screenshot hasilnya
6. Build Docker image dan pastikan berjalan

Kumpulkan:
- File `products.csv` yang sudah dimodifikasi
- Screenshot hasil unit test (semua PASSED)
- Screenshot hasil load test (RPS dan response time)
- Screenshot Docker container berjalan
