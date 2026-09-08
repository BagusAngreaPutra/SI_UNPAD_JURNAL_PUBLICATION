# Migrasi OJS asli

Status: OJS 3.5.0-5 lokal baru sudah disiapkan sesuai arahan untuk melanjutkan
tanpa backup. Sebanyak 246 halaman HTML publik lama tetap dipertahankan.
Database baru dan akun administrator lokal terpisah dari situs asli.
Migrasi akun, naskah privat, dan riwayat lama masih menunggu backup.

Metadata halaman sumber menyebut OJS 3.1.2.4, Academic Pro 2.34, dan OJT Control
Panel 2.0.6.3. Versi sebenarnya harus dicocokkan dengan kode dan database backup.
Instalasi baru memakai PHP 8.2.12 dan MariaDB 10.4.32 dari XAMPP. Kompatibilitas
runtime dan tema dengan versi OJS hasil restore tetap harus diperiksa.

## Backup yang diperlukan

- Dump database lengkap dalam `.sql` atau `.sql.gz`, termasuk akun, peran,
  submission, review, pengaturan, dan publikasi.
- Folder naskah privat yang ditunjuk oleh `files_dir` pada `config.inc.php`.
- Folder `public` untuk logo, sampul, dan aset unggahan jurnal.
- Kode OJS asli, `config.inc.php`, dan seluruh tema/plugin, termasuk Academic Pro/OJT.

Simpan backup di luar folder web yang akan disajikan ke browser, misalnya
`D:\OJS-Backup\UNPAD`. Jangan menempelkan isi konfigurasi atau password ke chat.
Backup database dan berkas harus berasal dari waktu yang konsisten.

Pemeriksaan awal setelah backup diekstrak:

```powershell
python scripts/check_migration_backup.py 'D:\OJS-Backup\UNPAD'
```

Pemeriksaan ini hanya membuat inventaris; tidak mengimpor database, menjalankan
kode backup, atau mencetak nilai password konfigurasi. Kelengkapan berkas naskah
tetap perlu dicocokkan dengan database setelah restore.

## Pelaksanaan setelah backup tersedia

1. Pastikan versi OJS/database dan kebutuhan PHP. Tentukan jalur upgrade yang
   kompatibel dengan tema serta plugin dari backup.
2. Pulihkan ke lingkungan lokal terpisah dengan database baru dan penyimpanan
   privat di luar document root. Matikan pengiriman email dan tugas terjadwal
   selama pengujian agar tidak menghubungi pengguna lama. Instalasi lokal baru
   saat ini memakai penangkap SMTP lokal, bukan SMTP produksi.
3. Sesuaikan alamat lokal dan uji akun/peran, login/logout, registrasi, unggahan
   naskah, penugasan reviewer, revisi, keputusan editor, serta publikasi edisi.
4. Bandingkan isi, jumlah data, berkas, dan tampilan dengan sumber. Hubungkan
   halaman publik ke backend yang sudah tervalidasi.
5. Siapkan hosting/domain tujuan, HTTPS, email, backup, dan pekerjaan terjadwal.
   Pengalihan situs dilakukan setelah hasil lokal dapat ditinjau.

Referensi rilis resmi: https://pkp.sfu.ca/software/ojs/download/
