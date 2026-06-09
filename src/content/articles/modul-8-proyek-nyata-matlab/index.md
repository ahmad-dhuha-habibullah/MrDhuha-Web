---
title: "Modul 8: Proyek Nyata MATLAB"
description: "Modul terakhir ini mengintegrasikan semua yang telah dipelajari ke dalam proyek-proyek nyata yang relevan untuk penelitian."
date: 2026-06-09
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "proyek", "publikasi"]
readingTime: 6
layout: layouts/article.njk
---

Modul terakhir ini mengintegrasikan semua yang telah dipelajari ke dalam proyek-proyek nyata yang relevan untuk penelitian dan operasional di Indonesia.

## 8.1 Monitoring ENSO

```matlab
%% ENSO_Monitor.m — Script Monitoring ENSO Komprehensif
% ─────────────────────────────────────────────────────────
% Langkah 1: Load data OISST
fname = 'sst.mnmean.nc';
lon  = ncread(fname, 'lon');
lat  = ncread(fname, 'lat');
time = ncread(fname, 'time');
sst  = ncread(fname, 'sst');
time_dt = datetime(1800,1,1) + days(time);

% Langkah 2: Hitung Nino3.4
i_lon = find(lon >= 190 & lon <= 240);
i_lat = find(lat >= -5 & lat <= 5);

sst_n34 = sst(i_lon, i_lat, :);
nino34_raw = squeeze(mean(reshape(sst_n34, [], size(sst_n34,3)), 1));

% Baseline 1991-2020
i_base = year(time_dt) >= 1991 & year(time_dt) <= 2020;
clim_monthly = nan(12, 1);
for m = 1:12
    idx = i_base & month(time_dt) == m;
    clim_monthly(m) = mean(nino34_raw(idx));
end
clim_full = clim_monthly(month(time_dt));
nino34 = nino34_raw - clim_full;

% 3-month running mean
nino34_3m = movmean(nino34, 3);

% Kategori ENSO
el_nino  = nino34_3m >= 0.5;
la_nina  = nino34_3m <= -0.5;
neutral  = ~el_nino & ~la_nina;

% Dashboard plot
figure('Position', [50 50 1400 500], 'Color', 'w')
area(time_dt, max(nino34_3m, 0), 'FaceColor', '#C62828', 'FaceAlpha', 0.7)
hold on
area(time_dt, min(nino34_3m, 0), 'FaceColor', '#1565C0', 'FaceAlpha', 0.7)
plot(time_dt, nino34_3m, 'k', 'LineWidth', 1.2)
yline(0.5, '--', 'El Nino', 'Color', '#C62828', 'FontSize', 10)
yline(-0.5, '--', 'La Nina', 'Color', '#1565C0', 'FontSize', 10)
yline(0, 'k-', 'LineWidth', 0.5)
xlabel('Tahun', 'FontSize', 12)
ylabel('Indeks Nino3.4 (°C)', 'FontSize', 12)
title('ENSO Monitor — Indeks Nino3.4 (3-bulan running mean)', 'FontSize', 14)
set(gca, 'FontSize', 11)
grid on; box on
```

## 8.2 Monitoring IOD

```matlab
%% IOD_Monitor.m — Indian Ocean Dipole
% IOD = SST anomali Samudera Hindia Barat (WIO) minus Timur (EIO)
% Dipole Mode Index (DMI) = SSTA_WIO - SSTA_EIO

% Wilayah WIO: 50-70E, 10S-10N
% Wilayah EIO: 90-110E, 10S-0N

i_wio_lo = find(lon >= 50 & lon <= 70);
i_wio_la = find(lat >= -10 & lat <= 10);
i_eio_lo = find(lon >= 90 & lon <= 110);
i_eio_la = find(lat >= -10 & lat <= 0);

sst_wio = sst(i_wio_lo, i_wio_la, :);
sst_eio = sst(i_eio_lo, i_eio_la, :);

[nw1, nw2, nt] = size(sst_wio);
[ne1, ne2, ~]  = size(sst_eio);

wio_ts = squeeze(mean(reshape(sst_wio, nw1*nw2, nt), 1))';
eio_ts = squeeze(mean(reshape(sst_eio, ne1*ne2, nt), 1))';

% Hitung anomali dari baseline
wio_anom = detrend(wio_ts - mean(wio_ts(i_base)));
eio_anom = detrend(eio_ts - mean(eio_ts(i_base)));

% DMI = WIO - EIO
dmi = wio_anom - eio_anom;
dmi_3m = movmean(dmi, 3);

% Plot
figure('Position', [50 50 1400 450], 'Color', 'w')
area(time_dt, max(dmi_3m, 0), 'FaceColor', '#E65100', 'FaceAlpha', 0.7)
hold on
area(time_dt, min(dmi_3m, 0), 'FaceColor', '#1A237E', 'FaceAlpha', 0.7)
yline(0.4, '--r'); yline(-0.4, '--b')
xlabel('Tahun'); ylabel('DMI (°C)')
title('IOD Monitor — Dipole Mode Index')
grid on
```

## 8.4 Analisis Marine Heatwave Indonesia

```matlab
%% MHW_Indonesia.m — Peta Frekuensi MHW Perairan Indonesia
% ─────────────────────────────────────────────────────────
% Hitung frekuensi MHW per grid point untuk seluruh Indonesia

% Subset Indonesia
i_lo = find(lon >= 95 & lon <= 141);
i_la = find(lat >= -15 & lat <= 10);

lon_id = lon(i_lo);
lat_id = lat(i_la);
sst_id = sst(i_lo, i_la, :);

[nlo, nla, nt] = size(sst_id);
mhw_freq = nan(nlo, nla);    % Frekuensi event per tahun
mhw_dur  = nan(nlo, nla);    % Durasi rata-rata (hari)

fprintf('Menghitung MHW untuk %d x %d grid points...\n', nlo, nla)

for il = 1:nlo
    for ila = 1:nla
        sst_pt = squeeze(sst_id(il, ila, :));
        if all(isnan(sst_pt)); continue; end
        
        % Hitung threshold persentil 90
        thresh = prctile(sst_pt(i_base), 90);
        
        % Deteksi event sederhana
        exceed = sst_pt > thresh;
        events = bwconncomp(exceed);  % Image processing toolbox
        
        durations = cellfun(@length, events.PixelIdxList);
        valid_ev  = durations >= 5;
        
        n_years = (time_dt(end) - time_dt(1)).Days / 365.25;
        mhw_freq(il, ila) = sum(valid_ev) / n_years;
        if any(valid_ev)
            mhw_dur(il, ila) = mean(durations(valid_ev));
        end
    end
end

% Plot frekuensi MHW
figure('Position', [50 50 1200 600])
imagescn(lon_id, lat_id, mhw_freq')
cmocean('matter')
caxis([0 3])
cb = colorbar;
cb.Label.String = 'Frekuensi MHW (event/tahun)';
hold on
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.8)
set(gca, 'XLim', [95 141], 'YLim', [-15 10])
xlabel('Longitude (°E)'); ylabel('Latitude (°N)')
title('Frekuensi Marine Heatwave Perairan Indonesia (1982-2023)')
```

## 8.5 Dari Analisis ke Paper Publikasi

Setelah menghasilkan analisis dan visualisasi yang baik, langkah berikutnya adalah menulis paper ilmiah. Berikut panduan singkat untuk mempersiapkan output MATLAB untuk publikasi:

**◆ Kualitas Gambar**
Export semua figure dengan resolusi minimal 300 DPI untuk jurnal. Gunakan format PDF atau EPS untuk gambar vektor. Command: exportgraphics(gcf, 'fig1.pdf', 'ContentType', 'vector')

**◆ Konsistensi Warna**
Gunakan colormap yang sama untuk variabel yang sama di semua figure. Hindari colormap 'jet' — gunakan cmocean yang perceptually uniform. Pastikan gambar bisa dibaca oleh orang dengan color blindness.

**◆ Caption dan Label**
Semua sumbu harus berlabel dengan satuan. Semua gambar harus memiliki caption yang lengkap. Ukuran font minimal 10pt untuk teks dalam gambar.

**◆ Reprodusibilitas**
Simpan semua script yang menghasilkan setiap figure. Beri komentar yang jelas pada setiap bagian kode. Upload data dan kode ke Zenodo atau GitHub saat paper terbit untuk open science.

**◆ Statistik**
Selalu tampilkan signifikansi statistik (p-value) untuk trend dan korelasi. Gunakan bootstrap atau Monte Carlo untuk confidence interval jika diperlukan. Nyatakan periode baseline yang digunakan untuk anomali dan climatology.

```matlab
% Template Script untuk Figure Kualitas Jurnal
function export_fig_journal(fig_handle, filename, fig_title)
    % Set font size konsisten
    set(findall(fig_handle, 'Type', 'axes'), 'FontSize', 11, ...
        'FontName', 'Helvetica')
    set(findall(fig_handle, 'Type', 'text'), 'FontSize', 11)
    
    % Set ukuran figure (misal untuk double column: 19cm x 9cm)
    fig_handle.Units = 'centimeters';
    fig_handle.Position = [1 1 19 9];
    
    % Export PDF vektor
    exportgraphics(fig_handle, [filename '.pdf'], ...
        'ContentType', 'vector', 'BackgroundColor', 'white')
    
    % Export PNG 300 DPI
    exportgraphics(fig_handle, [filename '.png'], 'Resolution', 300)
    
    fprintf('Figure "%s" berhasil disimpan!\n', fig_title)
end
```
