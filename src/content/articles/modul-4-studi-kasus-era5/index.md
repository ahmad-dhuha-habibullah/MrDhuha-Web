---
title: "Modul 4: Studi Kasus ERA5"
description: "ERA5 adalah reanalisis atmosfer global terbaru dari ECMWF yang sangat populer dalam riset. Kita akan belajar mengolah data ini."
date: 2026-06-05
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "era5", "studi kasus"]
readingTime: 4
layout: layouts/article.njk
---

ERA5 adalah reanalisis atmosfer global terbaru dari ECMWF (European Centre for Medium-Range Weather Forecasts). Dengan resolusi 0.25° dan data dari 1940 hingga kini, ERA5 adalah dataset yang paling banyak digunakan dalam penelitian iklim modern.

## 4.1 Download ERA5

ERA5 tersedia gratis melalui Copernicus Climate Data Store (CDS). Anda membutuhkan akun di cds.climate.copernicus.eu dan menginstal cdsapi (Python) atau menggunakan web interface.

> **Variabel ERA5 yang Sering Digunakan**
> - 2m temperature (t2m) — suhu udara 2 meter dari permukaan
> - Sea Surface Temperature (sst) — suhu permukaan laut
> - Total Precipitation (tp) — curah hujan total
> - 10m U/V wind components (u10, v10) — angin permukaan
> - Mean sea level pressure (msl) — tekanan muka laut
> - Specific humidity (q) — kelembaban spesifik

## 4.2–4.5 Membaca, Climatology, Anomali, dan Trend ERA5

```matlab
% ── 4.2 Membaca ERA5 ─────────────────────────────────────
fname = 'ERA5_SST_monthly_1982_2023.nc';
lon  = ncread(fname, 'longitude');   % 0 sampai 360 atau -180 sampai 180
lat  = ncread(fname, 'latitude');    % 90 sampai -90 (perhatikan urutan!)
time = ncread(fname, 'time');        % Jam sejak epoch
sst  = ncread(fname, 'sst');
sst  = sst - 273.15;   % Konversi dari Kelvin ke Celsius

% Konversi waktu ERA5 ke datetime MATLAB
time_dt = datetime(1900,1,1) + hours(time);
fprintf('Data dari: %s sampai %s\n', datestr(time_dt(1)), datestr(time_dt(end)))

% ── 4.3 Climatology Bulanan ERA5 ─────────────────────────
ntime = length(time_dt);
nyears = ntime / 12;
sst_4d = reshape(sst, size(sst,1), size(sst,2), 12, nyears);
sst_clim = mean(sst_4d, 4, 'omitnan');   % Klimatologi bulanan [lon x lat x 12]

% Plot klimatologi DJF
djf = mean(sst_clim(:,:,[12 1 2]), 3);    % Desember-Januari-Februari
figure
imagescn(lon, lat, djf')
cmocean('thermal'); caxis([0 30]); colorbar
title('SST Klimatologi DJF (ERA5 1982-2023)')

% ── 4.4 Anomali ERA5 ─────────────────────────────────────
sst_clim_rep = repmat(sst_clim, [1, 1, 1, nyears]);
sst_clim_3d  = reshape(sst_clim_rep, size(sst));
sst_anom = sst - sst_clim_3d;

% ── 4.5 Trend Linear ERA5 ─────────────────────────────────
% Menggunakan fungsi trend dari CDT
[tr, ~, p] = trend(sst, 12);   % trend per tahun (x12 karena data bulanan)
% Satuan: °C/tahun

figure
imagescn(lon, lat, tr')
cmocean('balance', 'pivot', 0)
caxis([-0.05 0.05])
colorbar('Label', '°C/tahun')
title('Trend SST ERA5 (1982-2023, °C/tahun)')

% Mask area tidak signifikan
tr_masked = tr;
tr_masked(p > 0.05) = NaN;
figure
imagescn(lon, lat, tr_masked')
cmocean('balance', 'pivot', 0)
title('Trend SST Signifikan (p < 0.05)')
```
