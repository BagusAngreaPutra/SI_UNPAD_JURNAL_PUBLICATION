# Jurnal Bina Mulia Hukum — web publik dan OJS lokal

Jalankan dari folder proyek:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File start-local.ps1
```

Buka **http://127.0.0.1:8000**. Login ada di
**http://127.0.0.1:8000/ojs/index.php/jbmh/login**.

Username administrator: `admin`. Password ada di file privat
`../UNPAD-runtime/AKSES-LOKAL.txt`, di luar folder web.

Login, registrasi, profil, submission, unggahan berkas, peran penulis/editor,
review, keputusan editor, pengelolaan edisi, dan publikasi menggunakan OJS
3.5.0-5 resmi di `ojs/`. Header, menu, dan sidebar halaman formulir menggunakan
markup halaman publik lama melalui tema lokal `ojs/plugins/themes/unpad/`.
Dashboard pengelolaan memakai antarmuka bawaan OJS.

Gunakan server PHP di atas untuk fungsi OJS. Membuka HTML langsung atau memakai
server Python/Live Server hanya dapat menampilkan halaman statis.

Halaman awal yang sudah ada dipertahankan. Halaman publik tambahan di folder
`pages/` diambil dari https://jurnal.fh.unpad.ac.id/index.php/jbmh/ dan
tautannya diarahkan ke salinan lokal jika tersedia. Pengambilan dibatasi pada
Jurnal Bina Mulia Hukum, termasuk kebijakan, panduan, kontak, arsip, dan artikel.

CSS, JavaScript, gambar, dan font tampilan publik tersedia lokal di `assets/`.
Panduan upload perbaikan cPanel ada di [CPANEL-ASSETS.md](CPANEL-ASSETS.md).
PDF, unduhan sitasi, serta widget statistik tetap memakai sumber daring.
Konten arsip lama tetap berupa HTML; akun, berkas naskah privat,
riwayat review, dan metadata database lama belum dimigrasikan. Pencarian OJS
mencari publikasi dalam database OJS baru. Lihat [MIGRATION.md](MIGRATION.md).

## Data dan email lokal

Runtime tersimpan di `../UNPAD-runtime/`, di luar document root:

- `database/`: MariaDB khusus proyek, port `3308`, database `unpad_ojs`.
- `files/`: berkas privat naskah.
- `mail/`: email uji dalam format `.eml`.
- `local-secrets.json` dan `AKSES-LOKAL.txt`: kredensial lokal.

Email ditangkap oleh SMTP lokal pada `127.0.0.1:1025`; tidak dikirim ke penerima
di internet. Email pemulihan password juga masuk ke folder `mail/`. SMTP nyata,
alamat pengelola, HTTPS/domain, dan pekerjaan terjadwal perlu diatur sebelum
peluncuran online. Server pengembangan terikat ke `127.0.0.1`.

Prasyarat saat ini: XAMPP di `C:\xampp`, Python, serta paket `aiosmtpd==1.4.6`.
Jangan menghapus `UNPAD-runtime` karena database dan unggahan berada di sana.

## Pemeliharaan halaman publik

Daftar halaman, URL sumber, dan kegagalan pengambilan tersedia di
`sync-report.json`. Untuk mengambil halaman yang masih belum tersimpan:

```powershell
python scripts/sync_pages.py
```

Skrip mempertahankan salinan yang sudah ada dan hanya menyesuaikan atribut URL
untuk menghubungkan navigasi serta menjaga alamat aset tetap benar.

Setelah menambahkan halaman publik, jalankan `python scripts/connect_ojs.py`
untuk menyambungkan tautan akun/submission dan membangun ulang shell tema.
Folder aplikasi OJS tidak diproses oleh skrip pengambil HTML.
