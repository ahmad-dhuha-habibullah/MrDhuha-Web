---
title: "Modul 5: Studi Kasus OISST"
description: "NOAA OISST adalah dataset SST harian yang sangat populer. Mari kita gunakan data ini untuk memonitor ENSO."
date: 2026-06-06
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "oisst", "enso"]
readingTime: 4
layout: layouts/article.njk
---

NOAA OISST (Optimum Interpolation Sea Surface Temperature) adalah dataset SST harian dengan resolusi 0.25°, tersedia dari September 1981 hingga sekarang. Dataset ini sangat populer untuk analisis variabilitas SST, terutama untuk studi ENSO dan Marine Heatwave karena resolusi temporalnya yang tinggi.

## 5.1–5.4 OISST: Dari Pembacaan hingga ENSO

```matlab
% ── 5.1 Membaca OISST ────────────────────────────────────
% OISST tersedia sebagai file netCDF harian atau bulanan
% Download dari: https://www.ncei.noaa.gov/products/optimum-interpolation-sst

fname_oisst = 'sst.mnmean.nc';
lon_oi = ncread(fname_oisst, 'lon');   % 0.125 sampai 359.875, step 0.25
lat_oi = ncread(fname_oisst, 'lat');   % -89.875 sampai 89.875
time_oi = ncread(fname_oisst, 'time'); % Hari sejak 1800-01-01
sst_oi  = ncread(fname_oisst, 'sst');  % °C, sudah dalam Celsius
% Nilai fill: sst > 35 atau < -5 biasanya adalah land/ice mask
sst_oi(sst_oi > 35) = NaN;

time_oi_dt = datetime(1800,1,1) + days(time_oi);

% ── 5.2 SST Climatology (1991-2020) ──────────────────────
% Pilih periode referensi WMO 1991-2020
i_ref = time_oi_dt.Year >= 1991 & time_oi_dt.Year <= 2020;
sst_ref = sst_oi(:,:, i_ref);
nref = sum(i_ref);  % = 360 bulan

sst_ref_4d = reshape(sst_ref, size(sst_ref,1), size(sst_ref,2), 12, nref/12);
sst_clim_oi = mean(sst_ref_4d, 4, 'omitnan');

% ── 5.3 SST Anomaly (SSTA) ───────────────────────────────
ntime_oi = size(sst_oi, 3);
nyears_oi = floor(ntime_oi / 12);
months_all = repmat(1:12, 1, nyears_oi);

sst_anom_oi = nan(size(sst_oi));
for m = 1:12
    idx = (months_all == m);
    sst_anom_oi(:,:,idx) = bsxfun(@minus, sst_oi(:,:,idx), sst_clim_oi(:,:,m));
end

% ── 5.4 ENSO Monitoring (Nino3.4 Index) ──────────────────
% Wilayah Nino3.4: 190-240°E, 5°S-5°N
i_lon34 = find(lon_oi >= 190 & lon_oi <= 240);
i_lat34 = find(lat_oi >= -5 & lat_oi <= 5);

sst_n34 = sst_anom_oi(i_lon34, i_lat34, :);
[nl, nlt, nt] = size(sst_n34);
nino34 = squeeze(mean(reshape(sst_n34, nl*nlt, 1, nt), 1));

% Plot dengan shading El Nino / La Nina
figure('Position', [50 50 1200 400])
area(time_oi_dt, max(nino34, 0), 'FaceColor', [0.8 0.2 0.2], 'FaceAlpha', 0.6)
hold on
area(time_oi_dt, min(nino34, 0), 'FaceColor', [0.2 0.4 0.8], 'FaceAlpha', 0.6)
plot(time_oi_dt, nino34, 'k', 'LineWidth', 1)
yline(0.5, '--r'); yline(-0.5, '--b')
xlabel('Tahun'); ylabel('SST Anomali (°C)')
title('Indeks Nino3.4 (OISST) — ENSO Monitor')
legend('El Nino', 'La Nina'); grid on
```
