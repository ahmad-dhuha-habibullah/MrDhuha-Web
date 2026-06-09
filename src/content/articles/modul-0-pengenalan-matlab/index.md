---
layout: layouts/article.njk
title: 'Modul 0: Pengenalan MATLAB untuk Sains Atmosfer dan Kelautan'
description: Sebelum membahas data iklim atau toolbox canggih, kita perlu memahami terlebih dahulu apa itu MATLAB, bagaimana cara kerjanya, dan mengapa ia menjadi pilihan.
date: 2026-06-01
thumbnail: https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg
imageCaption: ''
author: Mr Dhuha
tags:
  - matlab
  - tutorial
  - sains data
readingTime: 6
series: Belajar MATLAB
topic: Sains Data
---

Sebelum membahas data iklim atau toolbox canggih, kita perlu memahami terlebih dahulu apa itu MATLAB, bagaimana cara kerjanya, dan mengapa ia menjadi pilihan di banyak laboratorium penelitian di seluruh dunia — termasuk di Indonesia.

## 0.1 Apa itu MATLAB?

MATLAB (Matrix Laboratory) adalah lingkungan komputasi numerik dan bahasa pemrograman yang dikembangkan oleh MathWorks. Pertama kali dirilis pada tahun 1984, MATLAB dirancang dengan filosofi utama: membuat operasi matriks dan vektor semudah menulis persamaan matematika.

Nama MATLAB sendiri merupakan singkatan dari **MATrix LABoratory**, yang mencerminkan fokus utamanya pada komputasi berbasis matriks. Hal ini menjadikannya sangat cocok untuk analisis data saintifik, di mana data iklim dan oseanografi selalu berbentuk array multidimensi.

> **Fakta Menarik tentang MATLAB**
> - Dikembangkan pertama kali oleh Cleve Moler pada akhir 1970-an
> - Versi komersial pertama dirilis tahun 1984 oleh MathWorks
> - Saat ini digunakan oleh lebih dari 4 juta pengguna di seluruh dunia
> - Tersedia dalam lebih dari 100 toolbox khusus untuk berbagai bidang ilmu
> - Digunakan di NASA, CERN, BMKG, dan ribuan universitas riset

### Siapa yang Menggunakan MATLAB di Indonesia?

- BMKG — untuk pemrosesan data observasi dan model cuaca numerik
- BRIN — untuk analisis data iklim dan riset kelautan
- ITB, IPB, UGM, ITS — dalam mata kuliah dan thesis mahasiswa
- LAPAN (kini BRIN) — untuk analisis citra satelit dan data atmosfer
- Perusahaan migas — untuk pemrosesan data geofisika

## 0.2 Kenapa Banyak Peneliti Masih Menggunakan MATLAB?

Di era Python yang semakin populer, wajar jika Anda bertanya: mengapa masih belajar MATLAB? Jawabannya terletak pada ekosistem yang sudah matang dan sangat teroptimasi untuk sains.

**◆ Visualisasi Instan**
Satu baris kode sudah menghasilkan grafik berkualitas tinggi. Tidak perlu import library, tidak perlu konfigurasi backend.

**◆ Matriks sebagai Tipe Data Utama**
Operasi array multidimensi terasa alami dan intuitif, sangat penting untuk data iklim 3D/4D.

**◆ Toolbox Saintifik Berkualitas**
Climate Data Toolbox, Signal Processing Toolbox, Statistics Toolbox — semuanya sudah terintegrasi dan diuji secara ketat.

**◆ Dokumentasi Luar Biasa**
Setiap fungsi memiliki dokumentasi lengkap dengan contoh yang bisa langsung dijalankan.

**◆ Debugging Interaktif**
Lingkungan Command Window memungkinkan eksplorasi data secara real-time tanpa perlu menulis program lengkap.

**◆ Legacy Kode Riset**
Banyak kode riset di jurnal internasional ditulis dalam MATLAB. Memahami MATLAB berarti bisa membaca dan mereplikasi hasil penelitian tersebut.

## 0.3 Kelebihan dan Kekurangan MATLAB

### Kelebihan MATLAB

| Aspek | Penjelasan |
| --- | --- |
| Mudah dipelajari | Sintaks yang bersih dan intuitif untuk pemula |
| Visualisasi sangat kuat | plot(), imagesc(), surf() langsung menghasilkan grafik bagus |
| Toolbox saintifik | 100+ toolbox resmi yang sudah teruji secara ilmiah |
| Standar riset | Banyak jurnal dan lab internasional menggunakan MATLAB |
| Debugging mudah | Workspace interaktif untuk inspeksi variabel real-time |
| Dokumentasi kuat | help(), doc(), dan portal online yang komprehensif |

### Kekurangan MATLAB

| Aspek | Penjelasan |
| --- | --- |
| Berbayar | Lisensi komersial bisa sangat mahal; butuh lisensi kampus/institusi |
| Ekosistem lebih kecil | Komunitas lebih kecil dibanding Python; lebih sedikit paket pihak ketiga |
| Kurang fleksibel | Tidak ideal untuk aplikasi web, mobile, atau production software |
| Ketergantungan MATLAB | File .m dan .mat tidak bisa dijalankan tanpa MATLAB (atau Octave) |
| Kecepatan eksekusi | Lebih lambat dari C/Fortran; bisa jadi kendala untuk data sangat besar |

## 0.4 MATLAB vs Python untuk Klimatologi

Pertanyaan paling sering dari pemula: "Haruskah saya belajar MATLAB atau Python?" Jawabannya bergantung pada konteks dan tujuan Anda. Berikut perbandingan objektif keduanya:

| Kriteria | MATLAB | Python |
| --- | --- | --- |
| Harga | Berbayar (ada lisensi kampus) | Gratis & open source |
| Kemudahan belajar | Sangat mudah untuk pemula | Mudah, kurva belajar sedikit lebih panjang |
| Visualisasi | Sangat kuat, built-in | Kuat (matplotlib, seaborn, cartopy) |
| Data NetCDF | ncread, ncinfo built-in | xarray, netCDF4 (install dulu) |
| Komunitas global | Sedang | Sangat besar |
| Machine Learning | Baik (ML Toolbox) | Unggul (scikit-learn, TensorFlow) |
| Operasional BMKG | Digunakan | Semakin banyak digunakan |
| Riset akademik | Standar di banyak lab | Semakin dominan |
| Climate Data Toolbox | Tersedia resmi | Tidak ada padanan langsung |
| Legacy kode riset | Sangat banyak | Sedang berkembang |

> _💡 Rekomendasi: Untuk pemula di bidang iklim/oseanografi Indonesia, mulai dari MATLAB karena kemudahannya. Setelah mahir, menambah Python akan jauh lebih mudah._

## 0.5 Instalasi MATLAB

Untuk menggunakan MATLAB, Anda membutuhkan lisensi yang valid. Beberapa opsi yang tersedia:

- **Lisensi Kampus/Institusi:** Banyak universitas Indonesia (ITB, UI, UGM, ITS, dll) memiliki perjanjian lisensi dengan MathWorks. Tanyakan ke UPT TIK kampus Anda.
- **MATLAB Online:** Tersedia melalui mathworks.com/products/matlab-online.html — tidak perlu instalasi, berjalan di browser.
- **Student License:** Tersedia dengan harga terjangkau untuk mahasiswa aktif.
- **Trial Version:** MathWorks menyediakan trial 30 hari gratis.

| Langkah | Aksi |
| --- | --- |
| 1 | Buka mathworks.com dan buat akun MathWorks |
| 2 | Pilih 'Get MATLAB' dan masukkan lisensi Anda |
| 3 | Download installer sesuai OS (Windows/macOS/Linux) |
| 4 | Jalankan installer dan ikuti wizard instalasi |
| 5 | Aktivasi menggunakan akun MathWorks saat pertama kali membuka |
| 6 | Pilih toolbox yang dibutuhkan (minimal: Statistics, Signal Processing) |

### Struktur Folder MATLAB

Setelah terinstal, MATLAB biasanya membuat folder **MATLAB** di direktori Documents Anda. Gunakan folder ini sebagai tempat menyimpan semua script dan data Anda. Membuat subfolder untuk setiap proyek adalah kebiasaan yang sangat dianjurkan:

```text
Documents/
  MATLAB/
    Modul_0_Pengenalan/
    Modul_1_DataIklim/
    Data/
      ERA5/
      OISST/
    Hasil/
```

## 0.6 Mengenal Antarmuka MATLAB

Ketika pertama kali membuka MATLAB, Anda akan melihat tampilan yang mungkin terasa asing. Jangan khawatir — setiap komponen memiliki fungsi yang jelas dan akan terasa intuitif setelah beberapa jam penggunaan.

▸ **Command Window**
Ini adalah jantung MATLAB. Di sini Anda bisa mengetik perintah dan melihat hasilnya secara langsung. Mirip dengan kalkulator super canggih. Tandanya adalah prompt `>>` yang menunggu input Anda.

▸ **Workspace**
Panel di kanan atas yang menampilkan semua variabel yang sedang aktif dalam memori. Anda bisa melihat nama variabel, tipe data, ukuran, dan nilainya. Sangat berguna untuk memahami data Anda.

▸ **Current Folder**
Panel di kiri yang menampilkan isi folder kerja saat ini. Dari sini Anda bisa membuka file .m, file data, atau berpindah direktori.

▸ **Editor**
Tempat menulis script dan function yang lebih panjang. Mendukung syntax highlighting, auto-indent, dan debugging. Buka dengan mengetik 'edit' di Command Window atau klik New Script.

▸ **Figure Window**
Jendela terpisah yang muncul ketika Anda membuat grafik. Bisa diperbesar, disimpan, atau diedit interaktif langsung dari tampilan.

▸ **Command History**
Rekam jejak semua perintah yang pernah Anda ketik. Tekan tombol ↑ di Command Window untuk menelusuri riwayat perintah.

## 0.7 Script Pertama Anda

Mari kita mulai dengan tradisi klasik pemrograman. Ketik baris berikut di Command Window dan tekan Enter:

```matlab
disp('Halo Dunia')
```

MATLAB akan menampilkan:

```matlab
Halo Dunia
```

Selamat! Anda baru saja menjalankan program pertama Anda di MATLAB. Sekarang mari kita coba beberapa perintah dasar lagi:

```matlab
% Ini adalah komentar — baris yang dimulai dengan % diabaikan MATLAB
disp('Halo dari MATLAB!')

% Operasi matematika sederhana
2 + 3
10 * 4
sqrt(16)    % Akar kuadrat dari 16

% Menampilkan teks dan angka
fprintf('Nilai pi = %.4f\n', pi)
fprintf('Akar kuadrat 2 = %.6f\n', sqrt(2))
```

> **Tips: Menekan Tab untuk Autocomplete**
> Saat mengetik nama fungsi di Command Window, tekan Tab untuk melihat saran autocomplete. Ini sangat berguna untuk menemukan fungsi yang lupa namanya.

## 0.8 Variabel dan Tipe Data

Variabel di MATLAB dibuat tanpa deklarasi tipe data terlebih dahulu. MATLAB secara otomatis menentukan tipe berdasarkan nilai yang Anda masukkan:

```matlab
% Membuat variabel
suhu = 28.5          % double (angka desimal)
nama = 'Jakarta'     % char (teks/string)
aktif = true         % logical (benar/salah)
tahun = 2024         % double (MATLAB default angka = double)

% Memeriksa tipe data
class(suhu)          % Hasil: 'double'
class(nama)          % Hasil: 'char'
whos                 % Tampilkan semua variabel di Workspace
```

| Tipe Data | Keterangan | Contoh |
| --- | --- | --- |
| double | Angka desimal (64-bit) — TIPE DEFAULT | `x = 3.14` |
| single | Angka desimal (32-bit) — hemat memori | `x = single(3.14)` |
| int32 | Bilangan bulat 32-bit | `x = int32(100)` |
| char | Karakter dan teks (string lama) | `s = 'Jakarta'` |
| string | String modern (sejak R2016b) | `s = "Jakarta"` |
| logical | Nilai benar/salah (true/false) | `flag = true` |
| cell | Array yang bisa menyimpan tipe berbeda | `c = {1, 'a', [1 2]}` |
| struct | Struktur data dengan field bernama | `s.nama = 'Ali'` |

## 0.9 Matriks dan Vektor

Ini adalah bagian terpenting dari MATLAB. Ingat: MATLAB = MATrix LABoratory. Semua data di MATLAB pada dasarnya adalah matriks, bahkan angka tunggal pun dianggap sebagai matriks 1×1.

```matlab
% ── Membuat Vektor ──────────────────────────────────────
v_baris = [1 2 3 4 5]         % Vektor baris (1x5)
v_kolom = [1; 2; 3; 4; 5]     % Vektor kolom (5x1)
v_range = 1:10                 % Vektor 1 sampai 10
v_step  = 0:0.5:5              % Vektor 0 sampai 5, step 0.5
v_linsp = linspace(0, 1, 100)  % 100 titik dari 0 ke 1

% ── Membuat Matriks ──────────────────────────────────────
A = [1 2 3; 4 5 6; 7 8 9]     % Matriks 3x3

% ── Informasi Ukuran ─────────────────────────────────────
size(A)          % [3 3] — baris dan kolom
size(A, 1)       % 3 — jumlah baris
size(A, 2)       % 3 — jumlah kolom
numel(A)         % 9 — total elemen
length(v_baris)  % 5 — dimensi terpanjang

% ── Indexing (Mengakses Elemen) ───────────────────────────
A(2, 3)          % Baris ke-2, kolom ke-3 = 6
A(1, :)          % Seluruh baris ke-1 = [1 2 3]
A(:, 2)          % Seluruh kolom ke-2 = [2; 5; 8]
A(2:3, 1:2)      % Sub-matriks baris 2-3, kolom 1-2

% ── Operasi Matriks ───────────────────────────────────────
B = A * A        % Perkalian matriks
C = A .* A       % Perkalian elemen per elemen (elemenwise)
D = A + 10       % Tambahkan 10 ke semua elemen
E = A > 5        % Logical: elemen mana yang > 5?

% ── Fungsi Berguna ────────────────────────────────────────
zeros(3, 4)      % Matriks 3x4 berisi nol
ones(2, 5)       % Matriks 2x5 berisi satu
eye(4)           % Matriks identitas 4x4
rand(3, 3)       % Matriks 3x3 angka acak [0,1]
nan(2, 6)        % Matriks berisi NaN — berguna untuk missing data
```

> **Mengapa Ini Penting untuk Data Iklim?**
> Data iklim selalu berupa array multidimensi. Misalnya, data SST dari OISST berukuran [1440 × 720 × 365] yang berarti 1440 titik bujur, 720 titik lintang, dan 365 hari. MATLAB sangat efisien dalam menangani operasi pada array sebesar ini dengan sintaks yang ringkas dan intuitif.

## 0.10 Membuat Grafik Pertama

Salah satu kekuatan terbesar MATLAB adalah kemampuan visualisasinya. Mari kita buat beberapa grafik sederhana yang relevan dengan data iklim:

```matlab
% ── Grafik 1: Plot Garis (Time Series Sederhana) ─────────────
bulan = 1:12;
curah_hujan = [180 160 120 90 70 50 45 55 95 130 175 200];

figure(1)
plot(bulan, curah_hujan, 'b-o', 'LineWidth', 2, 'MarkerSize', 6)
xlabel('Bulan')
ylabel('Curah Hujan (mm)')
title('Pola Curah Hujan Bulanan Jakarta')
xticks(1:12)
xticklabels({'Jan','Feb','Mar','Apr','Mei','Jun', ...
             'Jul','Agu','Sep','Okt','Nov','Des'})
grid on
xlim([1 12])

% ── Grafik 2: Plot dengan Multiple Lines ──────────────────
suhu_max = [32 32 33 34 35 35 34 34 34 33 32 31];
suhu_min = [24 24 25 25 26 25 24 24 24 24 24 24];

figure(2)
plot(bulan, suhu_max, 'r-s', 'LineWidth', 2)
hold on
plot(bulan, suhu_min, 'b-s', 'LineWidth', 2)
hold off
legend('Suhu Maksimum', 'Suhu Minimum')
xlabel('Bulan')
ylabel('Suhu (C)')
title('Suhu Bulanan Jakarta')
grid on

% ── Grafik 3: Peta Kontur Sederhana ───────────────────────
[lon, lat] = meshgrid(-10:1:10, -10:1:10);
SST = 28 + 2*sin(lon/5) + cos(lat/3);  % SST buatan

figure(3)
contourf(lon, lat, SST, 20, 'LineColor', 'none')
colorbar
colormap('jet')
xlabel('Longitude')
ylabel('Latitude')
title('Contoh Peta SST (Data Simulasi)')
```

> _Selamat! Anda telah menyelesaikan Modul 0. Anda sekarang memahami dasar-dasar MATLAB yang cukup untuk mulai bekerja dengan data iklim nyata di modul-modul berikutnya._
