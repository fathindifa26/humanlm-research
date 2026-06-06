# POC HumanLM untuk Research Gap

## Tujuan

Proof of concept ini dipakai untuk mengecek hipotesis paling sederhana:

> HumanLM mungkin tidak selalu menghasilkan jawaban yang sepenuhnya konsisten, tetapi pola konflik yang muncul bisa lebih manusiawi daripada sekadar artifact kontradiktif.

## Ide Dasar

Kita belum membuat benchmark penuh. Untuk tahap awal, kita cukup:

1. buat beberapa skenario kecil
2. berikan ke model HumanLM
3. minta model mengeluarkan:
   - behavior
   - reason
   - label dissonance versi model sendiri
4. simpan semua output
5. baca hasilnya secara manual

## File yang Dipakai

- `scenarios/poc_cognitive_dissonance.json`
- `run_humanlm_poc.py`

## Bentuk Skenario

Setiap skenario berisi:

- `knowledge`
- `opinion`
- `question`

Lalu model diminta menghasilkan:

- `behavior`
- `reason`
- `dissonance_type`
- `confidence`

## Cara Membaca Hasil

Kita belum menganggap label dari model sebagai ground truth. Label itu hanya sinyal tambahan.

Fokus utama tetap membaca output manual:

- apakah behavior masih masuk akal given knowledge dan opinion?
- apakah reason menjelaskan trade-off yang plausible?
- apakah reason justru menabrak knowledge secara eksplisit?

## Indikator Awal

### Human-like dissonance

Biasanya terlihat seperti:

- opinion positif, behavior tidak ideal
- tetapi reason masih masuk akal
- ada trade-off biaya, kenyamanan, stres, akses, atau tekanan hidup

### Artifact inconsistency

Biasanya terlihat seperti:

- knowledge bilang A
- behavior atau reason justru menyatakan kebalikan A
- justification bertabrakan langsung dengan fakta yang sudah diberikan

## Output

Script akan menyimpan hasil ke:

- `outputs/humanlm_poc_YYYYMMDD_HHMMSS.json`

## Next Step

Kalau hasil awal ini menjanjikan, langkah berikutnya:

1. tambah lebih banyak skenario
2. buat template pelabelan manual
3. bandingkan HumanLM dengan base model
4. mulai rumuskan metric sederhana untuk `human_like_dissonance` dan `artifact_inconsistency`
