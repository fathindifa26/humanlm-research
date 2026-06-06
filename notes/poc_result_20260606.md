# Hasil POC HumanLM - 2026-06-06

## File Output

Run ini menghasilkan file:

- `outputs/humanlm_poc_20260606_161616.json`

Model yang dipakai:

- `snap-stanford/humanlm-opinion`

## Tujuan Run

Run ini dipakai sebagai proof of concept sederhana untuk mengecek hipotesis:

> HumanLM mungkin tidak selalu sepenuhnya konsisten, tetapi konflik yang muncul cenderung berbentuk human-like dissonance, bukan artifact inconsistency.

## Ringkasan Hasil Umum

Secara umum, hasil awal ini **mendukung hipotesis awal** kita.

Dari 4 skenario:

- 4/4 output diberi label `human_like_dissonance` oleh model
- tidak ada output yang jelas-jelas tampak sebagai `artifact_like`
- semua justifikasi masih cukup masuk akal terhadap knowledge yang diberikan

Artinya, pada POC awal ini HumanLM cenderung:

- mempertahankan opinion atau value awal
- tetapi tetap mengizinkan behavior yang tidak ideal
- lalu menjelaskan behavior itu lewat trade-off yang masih plausible

Ini justru sesuai dengan ide utama riset kita:

> inkonsistensi tertentu bisa tetap terasa manusiawi

## Analisis Per Skenario

### 1. EV bagus tapi mahal

Input state:

- tahu bahwa EV lebih baik untuk lingkungan
- tahu EV mahal
- perlu hati-hati soal pengeluaran keluarga
- opinion: mendukung EV

Output model:

- behavior: mempertimbangkan EV, tetapi kemungkinan belum membeli sekarang
- reason: mendukung EV, tetapi harga terlalu mahal untuk kondisi budget saat ini
- label model: `human_like_dissonance`

Interpretasi:

Ini contoh yang sangat kuat untuk **human-like dissonance**.

Kenapa:

- opinion pro-EV tetap ada
- behavior tidak sepenuhnya sejalan dengan opinion
- tetapi ada trade-off ekonomi yang sangat wajar

Ini bukan artifact, karena alasan yang diberikan justru konsisten dengan knowledge awal.

### 2. Ingin hidup sehat tapi uang terbatas

Input state:

- tahu makanan sehat penting
- tahu makanan sehat lebih mahal
- fast food lebih murah dan mudah diakses
- opinion: ingin makan lebih sehat

Output model:

- behavior: memilih fast food atau makanan yang lebih murah
- reason: ingin makan sehat, tetapi akhir bulan uang menipis
- label model: `human_like_dissonance`

Interpretasi:

Ini juga contoh **human-like dissonance** yang cukup bersih.

Kenapa:

- ada gap antara aspiration dan actual behavior
- justifikasinya realistis: keterbatasan uang dan akses
- tidak ada kontradiksi eksplisit dengan knowledge

Ini terasa sangat manusiawi, karena banyak perilaku manusia memang berbentuk "tahu yang baik, tapi memilih yang praktis atau murah".

### 3. Privasi versus kenyamanan aplikasi

Input state:

- tahu aplikasi mengumpulkan banyak data
- tahu aplikasi sangat membantu kerja
- alternatif lebih privat lebih ribet
- opinion: privasi digital penting

Output model:

- behavior: tetap memakai aplikasi tersebut
- reason: karena sangat memudahkan pekerjaan, sementara alternatif terlalu ribet
- label model: `human_like_dissonance`

Interpretasi:

Ini juga mendukung hipotesis kita dengan cukup baik.

Kenapa:

- value: privasi itu penting
- behavior: tetap pakai aplikasi yang kurang privat
- reason: convenience dan efisiensi kerja

Ini konflik yang sangat plausible dalam kehidupan nyata. Lagi-lagi, bukan artifact, karena justification tidak menabrak knowledge awal.

### 4. Work-life balance versus promosi

Input state:

- promosi memberi gaji lebih tinggi
- promosi membuat kerja lebih panjang dan lebih stres
- waktu bersama keluarga penting
- opinion: work-life balance itu penting

Output model:

- behavior: mungkin menolak promosi
- reason: work-life balance lebih penting daripada gaji lebih tinggi
- label model: `human_like_dissonance`

Interpretasi:

Skenario ini sedikit berbeda dari tiga yang lain.

Di sini output model justru lebih dekat ke **konsisten** daripada dissonant:

- opinion: work-life balance penting
- behavior: menolak promosi
- reason: ingin menjaga waktu keluarga

Jadi secara manual, saya cenderung bilang:

- label model: `human_like_dissonance`
- evaluasi manual awal: **lebih cocok `consistent` atau very low dissonance**

Ini menarik, karena menunjukkan bahwa label dari model sendiri belum tentu akurat. Jadi keputusan akhir tetap perlu evaluasi manual dari peneliti.

## Kesimpulan Awal

### Yang mendukung hipotesis

- HumanLM tidak memaksa semua skenario menjadi jawaban lurus dan hiper-rasional.
- Model mampu menghasilkan trade-off yang masuk akal secara manusiawi.
- Belum terlihat artifact yang kasar seperti:
  - knowledge bilang EV mahal
  - tetapi reason bilang EV murah

### Yang perlu dicatat hati-hati

- Model tampaknya cenderung memakai label `human_like_dissonance` sebagai default.
- Label `dissonance_type` dari model belum bisa dipercaya sebagai ground truth.
- Kita masih perlu pelabelan manual oleh peneliti.

## Kesimpulan untuk Riset Kita

Hasil awal ini memberi sinyal positif bahwa HumanLM memang layak dipakai sebagai objek studi untuk research question kita.

Kenapa:

- model menghasilkan konflik yang tampak plausible
- justifikasi masih mengikuti kondisi sosial-ekonomi atau practical constraints
- bentuk konfliknya lebih dekat ke **messy but believable** daripada **broken**

Dengan kata lain, POC ini memberi dukungan awal pada ide bahwa:

> HumanLM mungkin lebih baik dalam menghasilkan human-like dissonance daripada artifact inconsistency

## Next Step yang Disarankan

1. Tambahkan skenario yang sengaja lebih sulit dan lebih rawan artifact.
2. Buat tabel pelabelan manual:
   - `consistent`
   - `human_like_dissonance`
   - `artifact_inconsistency`
3. Bandingkan HumanLM dengan base model non-HumanLM.
4. Pisahkan evaluasi:
   - kualitas behavior
   - kualitas justification
   - apakah justification menabrak knowledge atau tidak
