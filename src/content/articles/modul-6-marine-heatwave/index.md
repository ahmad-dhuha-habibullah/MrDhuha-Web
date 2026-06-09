---
title: "Modul 6: Marine Heatwave"
description: "Marine Heatwave (MHW) memiliki dampak besar pada ekosistem laut. Bagaimana cara kita mendeteksinya menggunakan data iklim?"
date: 2026-06-07
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "mhw", "marine heatwave"]
readingTime: 6
layout: layouts/article.njk
---

## 6.1 Konsep Marine Heatwave

Marine Heatwave (MHW) adalah periode berkepanjangan di mana suhu permukaan laut berada di atas threshold tertentu. Definisi formal menurut Hobday et al. (2016) adalah: **periode di mana SST harian melebihi persentil ke-90 selama minimal 5 hari berturut-turut**, dengan dua event yang terpisah kurang dari 2 hari dianggap sebagai satu event.

MHW memiliki dampak besar pada ekosistem laut, termasuk pemutihan terumbu karang, kematian massal organisme laut, dan gangguan rantai makanan. Indonesia, dengan terumbu karang terkaya di dunia, sangat rentan terhadap MHW.

> **Definisi Resmi Marine Heatwave (Hobday et al., 2016)**
> - SST harian > Persentil ke-90 dari baseline (biasanya 1982-2011 atau 1991-2020)
> - Durasi minimal: 5 hari berturut-turut
> - Gap < 2 hari antara dua event = digabung menjadi satu event
> - Intensitas diukur sebagai selisih SST dari threshold pada setiap hari event

## 6.2–6.7 Deteksi dan Analisis MHW

```matlab
% ── 6.2 Hitung Persentil ke-90 ───────────────────────────
% Untuk satu titik grid (misal lon=115E, lat=8S)
i_lon_pt = find(lon_oi >= 115, 1);
i_lat_pt = find(lat_oi >= -8, 1);

sst_pt = squeeze(sst_oi(i_lon_pt, i_lat_pt, :));   % Time series 1D

% Hitung persentil ke-90 menggunakan baseline 1982-2011
i_base = year(time_oi_dt) >= 1982 & year(time_oi_dt) <= 2011;
sst_base = sst_pt(i_base);

% ── 6.3 Threshold Persentil 90 ───────────────────────────
% Penting: hitung persentil per hari-of-year (bukan global)
% untuk menangkap siklus musiman
doy = day(time_oi_dt, 'dayofyear');
threshold = nan(365, 1);
window = 11;   % ±11 hari window

for d = 1:365
    % Kumpulkan hari dalam window dari baseline
    win_days = mod((d-window-1):(d+window-1), 365) + 1;
    idx_win = ismember(doy(i_base), win_days);
    threshold(d) = prctile(sst_base(idx_win), 90);
end

% Haluskan threshold dengan moving average
threshold_smooth = movmean(threshold, 31, 'Endpoints', 'fill');

% ── 6.4 Deteksi Event MHW ────────────────────────────────
% Bangun threshold time series lengkap
thresh_ts = threshold_smooth(doy);    % Sesuaikan ke time series panjang
exceed = sst_pt > thresh_ts;          % Logical: hari mana yang exceeded?

% Cari event: minimal 5 hari berturut-turut
min_dur = 5;
max_gap = 2;
events = struct('start', {}, 'end', {}, 'duration', {}, ...
                'intensity_mean', {}, 'intensity_max', {});

in_event = false;
gap_count = 0;
e_start = 0;

for t = 1:length(exceed)
    if exceed(t)
        if ~in_event
            e_start = t;
            in_event = true;
        end
        gap_count = 0;
    else
        if in_event
            gap_count = gap_count + 1;
            if gap_count > max_gap
                dur = t - e_start - gap_count;
                if dur >= min_dur
                    n = length(events) + 1;
                    events(n).start = time_oi_dt(e_start);
                    events(n).end   = time_oi_dt(t-gap_count-1);
                    events(n).duration = dur;
                    anom_e = sst_pt(e_start:t-gap_count-1) - thresh_ts(e_start:t-gap_count-1);
                    events(n).intensity_mean = mean(anom_e(anom_e>0));
                    events(n).intensity_max  = max(anom_e);
                end
                in_event = false;
                gap_count = 0;
            end
        end
    end
end

fprintf('Jumlah MHW terdeteksi: %d event\n', length(events))

% ── 6.5–6.6 Durasi dan Intensitas ────────────────────────
dur_all = [events.duration];
int_all = [events.intensity_mean];
fprintf('Durasi rata-rata: %.1f hari\n', mean(dur_all))
fprintf('Intensitas rata-rata: %.2f C\n', mean(int_all))
fprintf('Event terpanjang: %d hari\n', max(dur_all))
fprintf('Intensitas maksimum: %.2f C\n', max(int_all))

% Plot distribusi
figure
histogram(dur_all, 'BinWidth', 5, 'FaceColor', '#E74C3C')
xlabel('Durasi (hari)'); ylabel('Jumlah Event')
title('Distribusi Durasi Marine Heatwave')
```
