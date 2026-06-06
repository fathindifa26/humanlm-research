# Compare HumanLM vs Base Model

## Tujuan

Dokumen ini dipakai untuk membandingkan:

- `snap-stanford/humanlm-opinion`
- `Qwen/Qwen3-8B`

pada skenario cognitive dissonance sederhana yang sama.

## Kenapa Base Model Ini

Berdasarkan dokumentasi lokal repo `humanlm`, base model yang dipakai untuk HumanLM adalah:

- `Qwen/Qwen3-8B`

Jadi ini perbandingan yang paling fair untuk POC awal.

## Command yang Dijalankan di VM

### 1. HumanLM

```bash
cd ~/humanlm-research
source ~/humanlm-bench/bin/activate
python3 run_humanlm_poc.py --model snap-stanford/humanlm-opinion
```

### 2. Base Model

```bash
cd ~/humanlm-research
source ~/humanlm-bench/bin/activate
python3 run_humanlm_poc.py --model Qwen/Qwen3-8B
```

## Lokasi Output

Output akan tersimpan di folder:

- `outputs/`

Dengan nama seperti:

- `poc_snap_stanford__humanlm_opinion_YYYYMMDD_HHMMSS.json`
- `poc_qwen__qwen3_8b_YYYYMMDD_HHMMSS.json`

## Apa yang Perlu Dibandingkan

Untuk tiap skenario, cek:

1. apakah behavior masih plausible?
2. apakah reason menjelaskan trade-off yang manusiawi?
3. apakah ada kontradiksi eksplisit dengan knowledge?
4. apakah model terlalu lurus/robotik?
5. apakah model menghasilkan artifact inconsistency?

## Hipotesis Awal

Yang ingin kita lihat:

- HumanLM mungkin menghasilkan jawaban yang lebih `messy but believable`
- Base model mungkin lebih:
  - terlalu lurus / terlalu bersih
  - atau justru lebih sering menghasilkan kontradiksi yang tidak plausible

## Format Analisis Manual

Untuk setiap skenario, nanti bisa diisi:

- `behavior_quality`
- `reason_quality`
- `manual_label`
- `notes`

Dengan label manual:

- `consistent`
- `human_like_dissonance`
- `artifact_inconsistency`
