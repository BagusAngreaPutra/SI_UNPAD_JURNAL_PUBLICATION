# Pemeriksaan instalasi lokal

Lingkungan: OJS 3.5.0-5, PHP 8.2.12, MariaDB 10.4.32, browser Edge melalui
Playwright. Pemeriksaan dilakukan pada 7 September 2026.

Berhasil diuji:

- Registrasi penulis baru melalui formulir web.
- Login penulis dan administrator; password salah tidak memberikan akses.
- Pengisian judul/abstrak, unggahan DOCX, pemilihan jenis berkas, dan contributor.
- Konfirmasi submit menghasilkan halaman `Submission complete`.
- Naskah yang dikirim muncul pada antrean `Needs editor` administrator.
- Akun penulis ditolak ketika membuka pengaturan manajer.
- Permintaan reset password menghasilkan email pada kotak SMTP lokal.
- Halaman login memakai shell tampilan lama tanpa error JavaScript.
- Berkas PHP tambahan lulus pemeriksaan sintaks.

Naskah dan akun sementara untuk pengujian sudah dihapus. Tidak ada artikel uji
yang dipublikasikan. Hasil smoke test terakhir berada di
`../UNPAD-runtime/smoke-result.json`.

Review, revisi, keputusan editor, dan pengelolaan/publikasi edisi disediakan oleh
OJS resmi. Siklus lengkap review sampai publikasi belum diuji dengan data jurnal
asli. Akun dan riwayat lama belum dimigrasikan. Pengiriman email ke internet dan
deployment hosting juga belum dilakukan.
