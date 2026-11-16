# VECTRION — Structural Engineering Suite

**Preliminary Sizing. Better Engineering Decisions.**

VECTRION adalah aplikasi bantu untuk pemeriksaan awal dimensi elemen beton bertulang sebelum pemodelan, serta pemeriksaan dasar kebutuhan tulangan dari ringkasan analisis ETABS. Hasil aplikasi bukan desain final dan tidak menggantikan analisis serta verifikasi engineering.

## Alur dan fitur

- **Pra-Modelling — Balok:** estimasi tinggi minimum awal, rekomendasi praktis, alternatif lebar, rasio b/h, luas penampang, dan rekap.
- **Pra-Modelling — Pelat:** pemeriksaan tebal awal pelat satu arah dan dua arah/pelat rusuk berdasarkan rasio acuan yang tersedia di aplikasi. Tidak menghitung lendutan.
- **Pra-Modelling — Kolom:** rekomendasi dimensi persegi berbasis heuristik VECTRION dan informasi kelangsingan awal.
- **Pasca-Modelling — Balok:** membaca ringkasan desain ETABS `.xlsx`, mengelompokkan kebutuhan As per DesignSect dan story, lalu membandingkan konfigurasi tulangan pilihan.
- **Pasca-Modelling — Kolom:** pemeriksaan dasar luas tulangan longitudinal terhadap target minimum dan batas input maksimum.
- **Rekap dan ekspor:** rekap lintas modul tersedia selama sesi aktif dan dapat diunduh sebagai HTML untuk dicetak atau disimpan sebagai PDF.

## Menggunakan Pasca-Modelling Balok

Unggah workbook `.xlsx` yang berisi kolom `Story`, `DesignSect`, `AsTopTotal`, dan `AsBotTotal`. Header dapat memakai variasi huruf besar/kecil dan tanda baca; pembaca mencari header pada 30 baris pertama. Nilai kebutuhan As harus benar-benar menggunakan satuan mm². Baris station/kombinasi untuk pasangan DesignSect dan story yang sama diringkas dengan mengambil nilai maksimum atas dan bawah.

Setelah file dibaca, buka pilihan tulangan, isi jumlah batang atas dan bawah, tinjau status masing-masing sisi, lalu simpan hasil ke rekap. Membaca workbook baru akan mengganti ringkasan dan pilihan tulangan yang belum disimpan pada sesi tersebut. Rekap yang telah disimpan tetap terpisah.

## Menjalankan secara lokal

Gunakan versi Python yang sama dengan environment deployment. Dependensi aplikasi tersedia di `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Logo berada di `assets/`; video Beranda berada di `static/`. Static serving diaktifkan melalui `.streamlit/config.toml`.

## Batasan engineering

- **Balok dan pelat Pra-Modelling** hanya pemeriksaan dimensi awal. Modul ini bukan desain tulangan, analisis gaya dalam, atau verifikasi kapasitas.
- **Pelat** tidak menghitung lendutan. Rasio pelat dua arah mengikuti acuan yang digunakan aplikasi dan perlu diverifikasi oleh engineer terhadap dokumen standar yang berlaku.
- **Kolom Pra-Modelling** menggunakan heuristik rekomendasi ukuran dan asumsi kelangsingan awal. Klasifikasi goyangan, momen ujung, faktor k aktual, stabilitas lengkap, dan pemeriksaan strong-column–weak-beam tidak dilakukan.
- **Pasca-Modelling Balok** hanya membandingkan luas tulangan pilihan dengan kebutuhan As dalam workbook. Aplikasi tidak memverifikasi kapasitas, detailing, penyaluran, sengkang, atau desain balok lengkap.
- **Pasca-Modelling Kolom** hanya memeriksa luas tulangan longitudinal terhadap target yang dimasukkan. Gaya aksial, momen, stabilitas, sengkang, dan detailing tidak diperiksa.
- Rekap disimpan di session state, bukan database permanen. Unduh hasil sebelum sesi berakhir.

> **PERHATIAN — Hasil VECTRION adalah estimasi dan pemeriksaan awal, bukan desain final. Verifikasi dengan analisis struktur, standar yang berlaku, dan insinyur sebelum digunakan. Output aplikasi tidak boleh digunakan langsung sebagai dasar pelaksanaan konstruksi.**
