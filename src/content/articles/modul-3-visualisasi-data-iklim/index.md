---
title: "Modul 3: Visualisasi Data Iklim"
description: "Di modul ini, kita belajar cara memvisualisasikan data iklim, mulai dari peta SST, curah hujan, angin, hingga anomali yang siap publikasi."
date: 2026-06-04
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "visualisasi", "plot"]
readingTime: 5
layout: layouts/article.njk
---

## 3.1 Plot SST Indonesia

```matlab
% Setup peta Indonesia
figure('Position', [100 100 1200 600])

% Plot SST
imagescn(lon_indo, lat_indo, sst_indo')
cmocean('thermal')
caxis([26 32])
colorbar('FontSize', 12)

% Tambahkan garis pantai
hold on
% borders('Indonesia', 'k', 'LineWidth', 1.5)  % dari CDT atau Mapping Toolbox
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 1)

% Formatting
xlabel('Longitude (°E)', 'FontSize', 12)
ylabel('Latitude (°N)', 'FontSize', 12)
title('SST Indonesia — Januari 2023', 'FontSize', 14, 'FontWeight', 'bold')
set(gca, 'XLim', [95 141], 'YLim', [-11 6])
set(gca, 'FontSize', 11)

% Export
exportgraphics(gcf, 'SST_Indonesia_Jan2023.png', 'Resolution', 300)
```

## 3.2 Plot Curah Hujan

```matlab
% Curah Hujan dengan colormap yang tepat
figure
imagescn(lon, lat, precip(:,:,1)')
cmocean('rain')      % Colormap khusus curah hujan dari CDT
caxis([0 20])        % mm/hari
colorbar
title('Curah Hujan Harian (mm/hari)')

% Alternatif: contourf dengan lebih banyak kontrol
figure
levels = [1 2 5 10 15 20 30 50];
contourf(lon, lat, precip(:,:,1)', levels, 'LineColor', 'none')
cmocean('rain')
colorbar('Ticks', levels)
```

## 3.3 Plot Angin dan Streamline

```matlab
% ── Quiver Plot (Panah Angin) ────────────────────────────
figure
% Subsample setiap 5 grid point agar tidak terlalu padat
step = 5;
lon_q = lon(1:step:end);
lat_q = lat(1:step:end);
u_q   = u850(1:step:end, 1:step:end);
v_q   = v850(1:step:end, 1:step:end);

quiver(lon_q, lat_q, u_q', v_q', 1.5, 'k')
title('Angin 850 hPa')
xlabel('Longitude'); ylabel('Latitude')
axis equal; grid on

% ── Streamline ────────────────────────────────────────────
figure
[meshlon, meshlat] = meshgrid(lon, lat);
streamslice(meshlon, meshlat, u850', v850', 2)
title('Streamline Angin 850 hPa')
xlabel('Longitude'); ylabel('Latitude')

% ── Wind Speed ────────────────────────────────────────────
ws = sqrt(u850.^2 + v850.^2);   % Kecepatan angin
figure
imagescn(lon, lat, ws')
cmocean('speed')
colorbar
hold on
quiver(lon_q, lat_q, u_q', v_q', 'w', 'AutoScaleFactor', 1.5)
title('Kecepatan dan Arah Angin 850 hPa')
```

## 3.4 Peta Anomali dan Export Publikasi

```matlab
% ── Peta Anomali dengan Signifikansi ─────────────────────
figure('Position', [50 50 1000 500], 'Color', 'w')

% Plot anomali SST
imagescn(lon, lat, sst_anom(:,:,t0)')
cmocean('balance', 'pivot', 0)
caxis([-2 2])
cb = colorbar;
cb.Label.String = 'SST Anomali (°C)';
cb.FontSize = 11;

% Hatching untuk area tidak signifikan
hold on
h = pcolor(lon, lat, double(~sig_mask)');
h.FaceAlpha = 0.3;
h.EdgeColor = 'none';
h.FaceColor = [0.7 0.7 0.7];

% Garis pantai
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.8)

% Label dan formatting
xlabel('Longitude (°E)', 'FontSize', 12)
ylabel('Latitude (°N)', 'FontSize', 12)
title('SST Anomali — Desember 2023 (El Nino)', 'FontSize', 13)
set(gca, 'XLim', [30 180], 'YLim', [-30 30], 'FontSize', 11)

% ── Export Kualitas Publikasi ─────────────────────────────
% Format untuk jurnal (300 DPI, PDF vektor)
exportgraphics(gcf, 'fig1_sst_anomali.pdf', 'ContentType', 'vector')
exportgraphics(gcf, 'fig1_sst_anomali.png', 'Resolution', 300)
% Untuk EPS (beberapa jurnal masih minta ini)
print('-depsc', '-r300', 'fig1_sst_anomali.eps')
```
