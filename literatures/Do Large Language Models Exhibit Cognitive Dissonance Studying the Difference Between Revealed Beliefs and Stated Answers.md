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
