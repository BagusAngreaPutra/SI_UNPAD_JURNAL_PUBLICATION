# Perbaikan gambar dan CSS di cPanel

Paket `cpanel-assets-fix.zip` berisi halaman HTML publik, folder `assets`, serta
tema UNPAD yang sudah diperbaiki. Paket tidak memuat konfigurasi database OJS,
password, atau database lokal.

1. Simpan salinan file hosting yang akan diganti.
2. Upload ZIP ke folder yang saat ini berisi `index.html`. Jika web ada di
   `public_html/jurnal`, ekstrak di sana; jika di root domain, ekstrak di
   `public_html`. Jangan membuat lapisan folder tambahan.
3. Ekstrak dan gabungkan foldernya. Pastikan `assets/vendor` berada sejajar
   dengan `index.html`, `About`, `issue`, dan `pages`. Pertahankan huruf besar
   kecil nama folder, terutama `About`.
4. Bila memakai OJS, hapus cache template melalui menu administrasi OJS.
   Jangan mengganti `ojs/config.inc.php` hosting dengan file konfigurasi lokal.
5. Bersihkan cache browser/CDN lalu muat ulang dengan Ctrl+F5.

CSS, gambar, font, dan JavaScript tampilan publik kini menggunakan salinan
lokal. Dependensi di dalam CSS juga sudah disalin dan memakai path relatif.
Endpoint Bootstrap sumber yang kosong diganti dengan Bootstrap 3.3.7, sesuai
versi JavaScript Bootstrap asli. Badge jurnal SINTA 4206 diambil dari domain
SINTA pengganti karena domain lamanya tidak dapat diakses.

Situs sumber kini menyajikan stylesheet OJS 3.4.0.10, bukan tema Academic Pro
lama. `assets/theme-compat.css` memulihkan warna merah dan pembagian kolom
berdasarkan tampilan lokal sebelumnya. File ini perlu ikut diunggah.

Widget statistik pengunjung dan analitik tetap menggunakan layanan eksternal.
PDF dan tautan layanan eksternal tetap menuju tujuan sebelumnya.

Path tema OJS mengikuti `base_url` OJS, termasuk prefix subfolder. Contoh untuk
web di `https://contoh.id/jurnal`:

```ini
[general]
base_url = "https://contoh.id/jurnal/ojs"
allowed_hosts = '["contoh.id"]'
```

Sesuaikan nilai tersebut pada bagian `[general]` yang sudah ada. Jangan
menambahkan bagian konfigurasi duplikat. Database, `files_dir`, PHP, dan SMTP
hosting harus dikonfigurasi tersendiri untuk menjalankan backend OJS.

Detail asal aset: `assets/asset-report.json`. Perubahan ini belum diverifikasi
langsung pada hosting sebelum URL hosting diberikan.
