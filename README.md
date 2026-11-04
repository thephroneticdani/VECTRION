# VECTRION — Structural Engineering Suite

**Preliminary Design. Engineering Verification. Better Decisions.**

VECTRION adalah aplikasi bantu pra-desain struktur berbasis Python dan Streamlit. Aplikasi membantu memperkirakan dimensi awal dan menyimpan rekap selama sesi aplikasi; hasilnya bukan desain struktur final.

## Fitur

- **Balok:** tinggi minimum awal, rekomendasi tinggi praktis dengan pembulatan ke atas per 50 mm, alternatif lebar, rasio b/h, luas penampang, serta rekap.
- **Pelat:** pemeriksaan tebal awal satu arah dan dua arah/pelat rusuk memakai rasio Tabel 12.1 pada gambar acuan yang diberikan pengguna, untuk empat kondisi tumpuan. Tidak menghitung lendutan.
- **Kolom:** rekomendasi dimensi awal berbasis heuristik aplikasi serta informasi kelangsingan awal.
- **Rekap:** menyimpan ringkasan balok, pelat, dan kolom selama sesi Streamlit aktif.
- **Pasca-ETABS:** belum tersedia.

## Teknologi

- Python
- Streamlit (`streamlit==1.66.1`)

## Menjalankan secara lokal

Di Windows, dari folder proyek:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Atau, jika virtual environment proyek sudah tersedia:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Batasan metode

- Hasil balok dan pelat merupakan pemeriksaan dimensi awal, bukan desain tulangan atau verifikasi kapasitas.
- Antarmuka pelat memakai rasio pada gambar Tabel 12.1 yang diberikan pengguna. Rasio tersebut belum dinyatakan diverifikasi terhadap dokumen SNI 2847:2019.
- Rekomendasi kolom merupakan heuristik aplikasi. Informasi kelangsingan memakai asumsi awal dan bukan pemeriksaan stabilitas lengkap.
- Modul tidak melakukan pemodelan, penentuan beban/kombinasi beban, analisis gaya dalam, desain tulangan, pemeriksaan lendutan, atau verifikasi keselamatan struktur.
- Rekap hanya tersimpan dalam state sesi dan bukan penyimpanan permanen.

## Disclaimer engineering

> **PERHATIAN — VECTRION merupakan alat bantu pra-desain untuk estimasi dan pemeriksaan awal dimensi elemen struktur. Seluruh hasil perhitungan dan rekomendasi dimensi wajib melalui analisis struktur, verifikasi kapasitas, stabilitas, serta pemeriksaan engineering sesuai standar yang berlaku sebelum digunakan dalam desain final. Output aplikasi ini tidak boleh digunakan secara langsung sebagai dasar pelaksanaan konstruksi.**

Analisis dan verifikasi lanjutan dapat dilakukan menggunakan ETABS, SAP2000, STAAD.Pro, atau perangkat lunak lain yang sesuai dengan sistem struktur dan kebutuhan engineering. Penggunaan perangkat lunak analisis saja tidak menjamin desain valid; penilaian profesional dan verifikasi independen tetap diperlukan.

## Status rilis

Pra-desain balok, pelat, dan kolom tersedia sebagai alat bantu awal. Analisis Pasca-ETABS belum diimplementasikan. Seluruh hasil memerlukan analisis dan verifikasi engineering independen sebelum digunakan dalam desain final.

## Pengembangan selanjutnya

Rencana Pasca-ETABS mencakup impor hasil analisis dan pemeriksaan awal pasca-analisis. Fitur tersebut belum termasuk dalam rilis ini.
