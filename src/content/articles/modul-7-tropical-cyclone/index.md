---
title: "Modul 7: Tropical Cyclone"
description: "IBTrACS adalah database resmi WMO untuk jalur siklon tropis global. Mari kita belajar memvisualisasikan track density."
date: 2026-06-08
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "ibtracs", "tropical cyclone"]
readingTime: 5
layout: layouts/article.njk
---

## 7.1 IBTrACS — Database Siklon Tropis Global

IBTrACS (International Best Track Archive for Climate Stewardship) adalah database resmi WMO yang mengkompilasi data jalur siklon tropis dari seluruh dunia sejak 1842. Data tersedia dalam format NetCDF dan CSV dari ncei.noaa.gov/products/international-best-track-archive.

```matlab
% ── 7.1 Membaca IBTrACS ──────────────────────────────────
fname_tc = 'IBTrACS.WP.v04r00.nc';   % Wilayah Western Pacific

% Variabel utama
lon_tc  = ncread(fname_tc, 'lon');       % [storm x time]
lat_tc  = ncread(fname_tc, 'lat');
wind_tc = ncread(fname_tc, 'wmo_wind'); % Kecepatan angin maksimum (knot)
pres_tc = ncread(fname_tc, 'wmo_pres'); % Tekanan minimum (hPa)
year_tc = ncread(fname_tc, 'season');   % Tahun
name_tc = ncread(fname_tc, 'name');     % Nama siklon

fprintf('Jumlah total storm: %d\n', size(lon_tc, 1))

% ── 7.2 Plot Track Siklon ─────────────────────────────────
% Filter: hanya tahun 2000-2023, wilayah Indonesia (95-141E, 30S-20N)
years = squeeze(year_tc);
i_storms = find(years >= 2000 & years <= 2023);

figure('Position', [50 50 1200 700])
hold on

for i = i_storms'
    lo = lon_tc(i, :);
    la = lat_tc(i, :);
    ws = wind_tc(i, :);
    
    valid = ~isnan(lo) & ~isnan(la);
    if sum(valid) < 2; continue; end
    
    % Warna berdasarkan intensitas
    max_ws = nanmax(ws);
    if max_ws >= 130
        clr = [0.6 0 0];        % Super typhoon: merah tua
    elseif max_ws >= 96
        clr = [0.9 0.2 0.2];    % Typhoon: merah
    elseif max_ws >= 64
        clr = [1 0.6 0];        % Severe TS: oranye
    else
        clr = [0.3 0.5 1];      % TS: biru
    end
    
    plot(lo(valid), la(valid), '-', 'Color', clr, 'LineWidth', 0.8)
end

load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.5)
xlabel('Longitude'); ylabel('Latitude')
title('Track Siklon Tropis Western Pacific 2000-2023')
xlim([90 180]); ylim([-15 35])
grid on
```

## 7.3 Density Map Siklon

```matlab
% Density map menggunakan histogram 2D
res = 2;   % Resolusi 2 derajat
lon_bins = 90:res:180;
lat_bins = -15:res:35;

density = zeros(length(lon_bins)-1, length(lat_bins)-1);

for i = i_storms'
    lo = lon_tc(i, :);
    la = lat_tc(i, :);
    valid = ~isnan(lo) & ~isnan(la);
    
    for t = find(valid)
        [~, il] = histc(lo(t), lon_bins);
        [~, ila] = histc(la(t), lat_bins);
        if il > 0 && ila > 0
            density(il, ila) = density(il, ila) + 1;
        end
    end
end

% Normalisasi ke track density per tahun per degree^2
density_norm = density / (2023-2000+1) / res^2;

figure
imagescn(lon_bins(1:end-1)+res/2, lat_bins(1:end-1)+res/2, density_norm')
cmocean('matter')
colorbar('Label', 'Track density (per tahun per deg^2)')
title('Track Density Siklon Tropis (2000-2023)')
```
