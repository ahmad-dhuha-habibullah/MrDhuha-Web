---
title: "Modul 1: Dasar MATLAB untuk Data Iklim"
description: "Setelah menguasai dasar MATLAB, kita masuk ke dunia data iklim yang nyata. Format data yang paling umum di bidang ini adalah NetCDF."
date: 2026-06-02
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "netcdf", "iklim"]
readingTime: 6
layout: layouts/article.njk
---

Setelah menguasai dasar MATLAB, kita masuk ke dunia data iklim yang nyata. Format data yang paling umum di bidang ini adalah NetCDF (Network Common Data Form), sebuah format biner yang dirancang khusus untuk data saintifik multidimensi.

## 1.1 Membaca Data NetCDF

NetCDF adalah format standar untuk menyimpan data atmosfer dan kelautan. File NetCDF memiliki ekstensi `.nc` dan berisi variabel, dimensi, dan atribut.

MATLAB memiliki fungsi built-in untuk membaca NetCDF tanpa toolbox tambahan:

```matlab
% ── Melihat Isi File NetCDF ───────────────────────────────
filename = 'sst_data.nc';

% Melihat informasi file
info = ncinfo(filename)
disp(info.Variables)    % Lihat daftar variabel
disp(info.Dimensions)   % Lihat dimensi

% ── Membaca Variabel Tertentu ─────────────────────────────
sst  = ncread(filename, 'sst');       % Baca variabel SST
lon  = ncread(filename, 'longitude'); % Baca longitude
lat  = ncread(filename, 'latitude');  % Baca latitude
time = ncread(filename, 'time');      % Baca waktu

% Periksa ukuran data
fprintf('Ukuran SST: %d x %d x %d\n', size(sst))
fprintf('Range lon: %.1f sampai %.1f\n', min(lon), max(lon))
fprintf('Range lat: %.1f sampai %.1f\n', min(lat), max(lat))

% ── Membaca Sebagian Data (Efficient) ─────────────────────
% Hanya baca data Indonesia: lon 95-141E, lat 11S-6N
i_lon = find(lon >= 95 & lon <= 141);
i_lat = find(lat >= -11 & lat <= 6);

sst_indo = ncread(filename, 'sst', ...
    [i_lon(1), i_lat(1), 1], ...
    [length(i_lon), length(i_lat), Inf]);
```

## 1.2 Memahami Dimensi Data

Data iklim gridded memiliki struktur dimensi yang perlu dipahami. Format paling umum adalah (lon × lat × time) atau (lon × lat × level × time).

```matlab
% Contoh: Data ERA5 suhu permukaan
% Ukuran: [480 × 241 × 12] = [lon × lat × bulan]

% Mengakses snapshot tertentu
sst_jan = sst(:, :, 1);    % Bulan Januari
sst_jul = sst(:, :, 7);    % Bulan Juli

% Mean spasial (rata-rata di semua grid point)
sst_mean_jan = mean(sst_jan(:));    % Rata-rata global Januari

% Mean temporal (rata-rata sepanjang waktu)
% squeeze() menghilangkan dimensi tunggal
sst_clim = mean(sst, 3);           % Rata-rata semua bulan
sst_clim_sq = squeeze(mean(sst, 3));  % Hasilnya 2D

% Perbedaan penting: dimensi longitude-first
% Di MATLAB: sst(i_lon, i_lat, i_time)
% Di Python/xarray: sst.sel(time=..., lat=..., lon=...)
```

## 1.3 Operasi Data 3D dan 4D

```matlab
% ── Data 4D: lon x lat x level x time ───────────────────
% Contoh: angin zonal ERA5 dengan 17 level pressure
% u_wind ukuran: [480 x 241 x 17 x 12]

% Slice pada level 850 hPa (misalnya level ke-5)
u_850 = u_wind(:, :, 5, :);       % 4D, level ke-5
u_850_sq = squeeze(u_wind(:,:,5,:)); % 3D: lon x lat x time

% Rata-rata vertikal (mean di semua level)
u_vmean = mean(u_wind, 3);        % Rata-rata dimensi ke-3 (level)

% Rata-rata temporal
u_tmean = mean(u_wind, 4);        % Rata-rata dimensi ke-4 (time)

% Anomali = data - mean temporal
u_anom = u_wind - repmat(u_tmean, [1 1 1 size(u_wind,4)]);

% Fungsi bsxfun (lebih efisien untuk data besar)
u_anom2 = bsxfun(@minus, u_wind, u_tmean);
```

## 1.4 Time Series

```matlab
% ── Membuat Time Series dari Data Iklim ─────────────────
% Rata-rata area: SST wilayah Nino3.4 (190-240E, 5S-5N)

% Tentukan batas wilayah
i_lon34 = find(lon >= 190 & lon <= 240);
i_lat34 = find(lat >= -5 & lat <= 5);

% Ekstrak data wilayah
sst_nino34 = sst(i_lon34, i_lat34, :);

% Rata-rata spasial menggunakan mean ganda
nino34_ts = squeeze(mean(mean(sst_nino34, 1), 2));
% atau lebih ringkas:
nino34_ts = squeeze(mean(sst_nino34(:), 1));  % Salah! mean semua dimensi

% Cara benar: reshape dulu
[nlon34, nlat34, nt] = size(sst_nino34);
sst_reshaped = reshape(sst_nino34, nlon34*nlat34, nt);
nino34_ts = mean(sst_reshaped, 1)';   % Transpos jadi kolom

% Buat vektor waktu
t_start = datetime(1982, 1, 1);
t_end   = datetime(2023, 12, 1);
time_vec = t_start:calmonths(1):t_end;

% Plot time series
figure
plot(time_vec, nino34_ts, 'k-', 'LineWidth', 1.5)
yline(0, '--', 'color', [0.5 0.5 0.5])
xlabel('Tahun')
ylabel('SST Anomali (°C)')
title('Indeks Nino3.4')
grid on
```

## 1.5 Climatology dan Anomaly

Dua konsep fundamental dalam analisis iklim adalah **climatology** (rata-rata iklim) dan **anomaly** (penyimpangan dari rata-rata). Ini adalah dasar dari hampir semua analisis iklim.

```matlab
% ── Menghitung Climatology Bulanan ───────────────────────
% Asumsikan data berukuran [nlon x nlat x ntime]
% dengan ntime = jumlah bulan total (misal 492 = 41 tahun)

ntime = size(sst, 3);
nyears = ntime / 12;

% Reshape menjadi [nlon x nlat x 12 x nyears]
sst_4d = reshape(sst, size(sst,1), size(sst,2), 12, nyears);

% Climatology: rata-rata sepanjang dimensi tahun (ke-4)
sst_clim = mean(sst_4d, 4);  % Ukuran: [nlon x nlat x 12]

% ── Menghitung Anomali ────────────────────────────────────
% Ulangi climatology sebanyak nyears kali
sst_clim_rep = repmat(sst_clim, [1, 1, 1, nyears]);
% Reshape kembali ke 3D
sst_clim_3d = reshape(sst_clim_rep, size(sst));
% Hitung anomali
sst_anom = sst - sst_clim_3d;

% ── Verifikasi ────────────────────────────────────────────
fprintf('Range anomali: %.2f sampai %.2f C\n', ...
    min(sst_anom(:)), max(sst_anom(:)))
fprintf('Mean anomali global: %.4f C (seharusnya mendekati 0)\n', ...
    nanmean(sst_anom(:)))
```
