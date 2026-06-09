# Do Large Language Models Exhibit Cognitive Dissonance Studying the Difference Between Revealed Beliefs and Stated Answers

## Ringkasan Singkat

Paper ini mempertanyakan apakah evaluasi LLM berbasis jawaban eksplisit, terutama multiple-choice question (MCQ), benar-benar mencerminkan "keyakinan" internal model. Ide utamanya adalah membedakan antara:

- **Stated Answer (StaA)**: jawaban yang secara eksplisit dipilih atau diucapkan model
- **Revealed Belief (RevB)**: keyakinan yang tersirat dari distribusi probabilitas next-token model

Kesimpulan besarnya: model sering terlihat benar pada level jawaban akhir, tetapi distribusi probabilitas internalnya menunjukkan belief yang tidak sepenuhnya selaras.

## Masalah yang Ingin Dijawab

Banyak benchmark LLM menilai performa model dari:

- jawaban final
- akurasi pada MCQ
- reasoning yang tampak benar di permukaan

Paper ini berargumen bahwa pendekatan itu bisa menyesatkan, karena model mungkin:

- memilih jawaban yang benar
- tetapi memberi probabilitas internal yang tidak konsisten
- atau gagal memperbarui belief saat diberi evidence baru

Jadi, performa yang terlihat baik belum tentu berarti model benar-benar memiliki representasi belief yang stabil dan koheren.

## Kontribusi Utama

Paper ini memperkenalkan kerangka evaluasi **Revealed Belief** untuk melihat belief model langsung dari perilaku probabilistiknya, bukan hanya dari jawaban eksplisitnya.

Fokus evaluasinya adalah tugas-tugas yang melibatkan:

- reasoning di bawah ketidakpastian
- belief updating
- konsistensi probabilistik

## Cara Paper Ini Menguji Model

Metode evaluasinya sengaja dibagi menjadi dua jalur yang dibandingkan langsung:

- **Stated Answer (StaA)**
- **Revealed Belief (RevB)**

### 1. Stated Answer (StaA)

Pada setup ini, model diuji dengan format **multiple-choice question (MCQ)** biasa.

Contohnya:

- model diberi soal probabilistik
- tersedia beberapa opsi jawaban
- hanya ada satu jawaban yang benar

Lalu performa model diukur dari:

- apakah model memilih opsi yang benar
- atau apakah output akhirnya bisa diparse menjadi pilihan yang benar

Secara sederhana, StaA mengukur:

> apa yang model **katakan secara eksplisit**

### 2. Revealed Belief (RevB)

Pada setup ini, soal yang sama **tidak** diberikan dalam bentuk MCQ, tetapi diubah menjadi **text completion**.

Caranya:

- model diberi konteks skenario yang sama
- prompt dihentikan tepat sebelum token outcome penting
- lalu peneliti mengambil **raw logits** model
- logits itu diubah menjadi distribusi probabilitas next-token atau token-sequence

Distribusi probabilitas inilah yang disebut paper sebagai **Revealed Belief**.

Secara sederhana, RevB mengukur:

> apa yang model **tunjukkan lewat distribusi probabilitasnya**

### 3. Perbandingan StaA vs RevB

Jadi alur pengujiannya kira-kira begini:

1. Buat satu skenario probabilistik yang punya ground-truth jelas.
2. Formulasikan skenario itu dalam bentuk MCQ untuk mengukur StaA.
3. Formulasikan skenario yang sama dalam bentuk generatif untuk mengukur RevB.
4. Ambil distribusi probabilitas model atas semua outcome yang mungkin.
5. Bandingkan hasil StaA dan RevB terhadap ground-truth.

Dengan cara ini, paper bisa melihat apakah:

- model **memilih jawaban yang benar** pada MCQ
- tetapi belief laten yang terlihat dari distribusi probabilitasnya ternyata tidak selaras

### 4. Jenis Skenario yang Dipakai

Paper ini tidak hanya memakai satu contoh, tetapi beberapa keluarga task:

- `Dice`
- `Coins`
- `Preference`
- `Choice`

Variannya juga cukup kaya, misalnya:

- single event
- repeated event
- independent vs dependent event
- partial observation
- belief updating setelah evidence baru
- bias karena label outcome

Ini penting karena mereka ingin menguji bukan hanya akurasi statis, tetapi juga:

- apakah model bisa mengalokasikan probabilitas dengan benar
- apakah model bisa meng-update belief
- apakah model terpengaruh oleh format atau label yang seharusnya tidak relevan

### 5. Metrik untuk RevB

Untuk StaA, metrik utamanya relatif sederhana: akurasi memilih jawaban benar.

Untuk RevB, mereka tidak hanya melihat outcome tunggal, tetapi kualitas distribusi probabilitas secara keseluruhan. Dari paper, distribusi model dibandingkan dengan distribusi ground-truth menggunakan:

- **Chebyshev distance**
- **Manhattan distance**
- **Kullback-Leibler divergence**

Artinya, paper ini tidak hanya bertanya:

- apakah top answer model benar?

tetapi juga:

- seberapa dekat keseluruhan belief distribution model dengan distribusi yang seharusnya?

### 6. Kenapa Ini Disebut Mirip Cognitive Dissonance

Istilah "cognitive dissonance" di paper ini dipakai untuk menyebut adanya mismatch antara dua level evaluasi:

- **jawaban eksplisit** model
- **belief laten** yang terlihat dari distribusi probabilitas tokennya

Jadi maksudnya bukan cognitive dissonance manusia dalam arti psikologis penuh, melainkan:

> model bisa tampak benar di permukaan, tetapi struktur probabilistik internalnya tidak mendukung jawaban itu secara konsisten

Contoh intuisinya:

- pada format MCQ, model memilih diagnosis yang benar
- tetapi pada text completion, probability mass justru lebih berat ke diagnosis lain yang salah

Dalam situasi seperti itu:

- `StaA` terlihat baik
- `RevB` menunjukkan belief yang tidak selaras

Inilah inti mismatch yang ingin diungkap paper.

## Inti Temuan

Beberapa temuan utama yang bisa kita ambil:

- Model sering **menyatakan jawaban yang benar**, tetapi distribusi probabilitas tokennya masih mengandung bias atau ketidakkonsistenan.
- Model dapat gagal melakukan **belief update** secara benar ketika informasi baru diberikan.
- Ada gap antara apa yang model **katakan** dan apa yang model **tunjukkan** lewat probabilitasnya.
- Evaluasi berbasis jawaban final saja hanya memberi gambaran parsial tentang kemampuan model.

## Makna Konseptual

Paper ini penting karena memperjelas bahwa "jawaban benar" dan "belief internal yang benar" bukan hal yang sama.

Secara intuitif:

- StaA menangkap hasil akhir yang tampak di permukaan
- RevB menangkap struktur keyakinan laten yang mendasari keluaran model

Ketika keduanya tidak selaras, muncul fenomena yang oleh paper ini dibahas sebagai bentuk mirip **cognitive dissonance** pada LLM.

## Keterbatasan atau Batas Fokus Paper

Meskipun menarik, paper ini utamanya membahas:

- probabilistic reasoning
- belief calibration
- belief updating
- gap antara explicit answer dan token probability

Paper ini **belum** benar-benar membedakan apakah mismatch tersebut:

- menyerupai ketegangan kognitif manusia yang masih masuk akal
- atau hanya artifact dari model

## Relevansi untuk Riset Human Simulation

Untuk arah riset kita, paper ini sangat penting karena memberi dasar bahwa:

> output permukaan tidak cukup untuk menilai apakah model benar-benar "percaya" pada sesuatu

Hubungannya dengan human simulation:

- simulasi manusia tidak cukup dinilai dari respons akhir
- kita juga perlu melihat apakah belief, opinion, behavior, dan justification saling selaras
- kalau tidak selaras, kita perlu membedakan mana yang masih manusiawi dan mana yang artifact

## Takeaway untuk Kita

Pelajaran paling penting dari paper ini:

1. Evaluasi LLM tidak boleh berhenti di jawaban final.
2. Distribusi probabilitas model bisa mengungkap belief laten yang berbeda dari jawaban eksplisit.
3. Mismatch internal model adalah fenomena nyata.
4. Untuk human simulation, mismatch ini perlu dipisahkan lagi menjadi:
   - **human-like dissonance**
   - **artifact inconsistency**

## Kesimpulan

Paper ini menunjukkan bahwa LLM bisa terlihat benar di permukaan sambil tetap menyimpan belief internal yang tidak koheren. Ini membuka ruang penting untuk riset lanjutan: bukan hanya mengukur apakah model konsisten, tetapi juga memahami jenis inkonsistensi apa yang muncul dan apakah inkonsistensi itu masuk akal secara manusiawi atau hanya kegagalan model.
