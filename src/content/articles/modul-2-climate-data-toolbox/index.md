---
title: "Modul 2: Climate Data Toolbox"
description: "Climate Data Toolbox (CDT) adalah koleksi fungsi MATLAB yang dikembangkan khusus untuk analisis dan visualisasi data iklim, cuaca, dan oseanografi."
date: 2026-06-03
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "toolbox", "cdt"]
readingTime: 4
layout: layouts/article.njk
---

## 2.1 Apa itu Climate Data Toolbox?

Climate Data Toolbox (CDT) adalah koleksi fungsi MATLAB yang dikembangkan oleh **Chad A. Greene** dari Jet Propulsion Laboratory (JPL), NASA. Greene adalah peneliti geosains yang juga dikenal sebagai kontributor aktif komunitas MATLAB.

CDT dirilis sebagai open-source dan tersedia gratis melalui GitHub dan MATLAB File Exchange. Toolbox ini berisi lebih dari 100 fungsi yang dirancang khusus untuk analisis dan visualisasi data iklim, cuaca, dan oseanografi.

> **Mengapa CDT Luar Biasa?**
> - Fungsi yang intuitif dan terdokumentasi dengan sangat baik
> - Terintegrasi dengan colormap cmocean yang dirancang untuk data saintifik
> - Mendukung analisis trend, anomali, dan climatology secara efisien
> - Fungsi grid seperti cdtarea dan regrid sangat berguna untuk data global
> - Gratis dan open-source — berbeda dengan banyak toolbox MATLAB lainnya
> - Dipercaya dan digunakan dalam publikasi jurnal internasional

## 2.2 Instalasi Climate Data Toolbox

```matlab
% Cara 1: Dari MATLAB Add-On Explorer (Cara Termudah)
% Home > Add-Ons > Get Add-Ons
% Cari "Climate Data Toolbox"
% Klik Install

% Cara 2: Dari GitHub
% git clone https://github.com/chadagreene/CDT.git
% Kemudian di MATLAB:
addpath(genpath('/path/to/CDT'))
savepath  % Simpan path agar permanen

% Verifikasi instalasi
cdt  % Akan menampilkan daftar fungsi CDT yang tersedia
```

## 2.3 Fungsi-fungsi Penting CDT

**◆ imagescn**
Menampilkan gambar/peta dengan penanganan NaN yang benar. Alternatif imagesc yang lebih baik untuk data dengan nilai kosong.

**◆ cmocean**
Koleksi colormap perceptually-uniform untuk data saintifik. Termasuk colormap untuk SST, kedalaman laut, anomali, dan banyak lagi.

**◆ trend**
Menghitung trend linear pada data time series. Mendukung data 3D sehingga bisa menghitung trend di setiap grid point sekaligus.

**◆ anomaly**
Menghitung anomali bulanan atau musiman secara otomatis. Menggantikan perhitungan manual climatology dan pengurangan.

**◆ climatology**
Menghitung rata-rata iklim untuk setiap bulan atau musim. Sangat berguna untuk membuat climatological mean dari data panjang.

**◆ cdtarea**
Menghitung luas area setiap sel grid dalam km persegi. Penting untuk rata-rata area-weighted yang akurat secara geografis.

**◆ regrid**
Menginterpolasi data dari satu grid ke grid lain. Berguna ketika menggabungkan dataset dengan resolusi berbeda.

Contoh penggunaan fungsi CDT:

```matlab
% ── cmocean ──────────────────────────────────────────────
figure
contourf(lon, lat, sst(:,:,1), 20, 'LineColor','none')
cmocean('thermal')   % Colormap termal yang bagus untuk SST
colorbar
title('SST dengan cmocean thermal')

% ── imagescn ─────────────────────────────────────────────
figure
imagescn(lon, lat, sst_anom(:,:,1)')  % NaN ditampilkan transparan
cmocean('balance', 'pivot', 0)        % Colormap diverging, pivot di 0
colorbar
title('SST Anomali dengan imagescn')

% ── trend ─────────────────────────────────────────────────
% Hitung trend SST di setiap grid point
% Input: data [nlon x nlat x ntime], time vector
[tr, p] = trend(sst, 1);  % trend per satuan waktu
% tr: ukuran [nlon x nlat]
% p: p-value untuk signifikansi statistik

% Tampilkan hanya trend yang signifikan (p < 0.05)
tr_sig = tr;
tr_sig(p > 0.05) = NaN;

% ── anomaly ──────────────────────────────────────────────
sst_anom = anomaly(sst, 'monthly');   % Anomali bulanan otomatis

% ── climatology ──────────────────────────────────────────
sst_clim = climatology(sst, time, 'monthly');  % Climatology bulanan
```
