# 🧠 Sistem Deteksi Stroke – Panduan Deploy

## Struktur Folder

```
stroke-detection/
├── app.py                  ← Backend Flask
├── requirements.txt        ← Dependensi Python
├── xgb_stroke_model.pkl    ← ⬅️ Taruh file model Anda di sini
└── static/
    └── index.html          ← Frontend website
```

---

## Langkah-Langkah Menjalankan Secara Lokal

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Salin file model Anda
Taruh file `xgb_stroke_model.pkl` di folder yang sama dengan `app.py`.

### 3. Jalankan server
```bash
python app.py
```

Server akan berjalan di: **http://localhost:5000**

---

## Deploy ke Server (Production)

### Opsi A – Menggunakan Gunicorn (Linux/VPS)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Opsi B – Deploy ke Railway / Render
1. Push folder ini ke GitHub
2. Connect repo ke Railway atau Render
3. Set start command: `gunicorn app:app`
4. Upload file `.pkl` via environment atau taruh di repo

### Opsi C – Deploy ke PythonAnywhere
1. Upload semua file via Files tab
2. Buat Web App baru → pilih Flask
3. Set source code path ke folder ini
4. Reload app

---

## Encoding Nilai Input

| Field             | Nilai                          | Encoding |
|-------------------|-------------------------------|----------|
| gender            | Laki-Laki / Perempuan         | 1.0 / 0.0 |
| hypertension      | Iya / Tidak                   | 1 / 0 |
| heart_disease     | Iya / Tidak                   | 1 / 0 |
| ever_married      | Menikah / Belum menikah       | 1.0 / 0.0 |
| work_type         | Anak-Anak / Belum pernah bekerja / PNS / Swasta / Wiraswasta | 0/1/2/3/4 |
| Residence_type    | Perkotaan / Perdesaan         | 1.0 / 0.0 |
| smoking_status    | Tidak merokok / Mantan Merokok / Perokok aktif | 0/1/2 |

> Pastikan encoding di `app.py` sesuai dengan encoding yang Anda gunakan saat melatih model!
