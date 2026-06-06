# HUMANLMSimulating Users with State Alignment Beats Response Imitation

## Ringkasan Singkat

Paper ini memperkenalkan **HumanLM**, sebuah pendekatan untuk simulasi user yang tidak hanya meniru respons permukaan, tetapi mencoba menyelaraskan **state internal user** yang mendasari respons tersebut.

Argumen utamanya adalah:

> user simulation yang baik tidak cukup hanya meniru teks jawaban; model juga harus menangkap state psikologis dan situasional yang membuat jawaban itu muncul

## Masalah yang Ingin Dijawab

Banyak simulator user berbasis LLM dievaluasi dari seberapa mirip respons yang dihasilkan dengan respons manusia.

Masalahnya:

- dua respons bisa terlihat mirip secara tekstual tetapi datang dari state yang berbeda
- model bisa meniru style jawaban tanpa benar-benar menangkap belief, goal, atau stance user
- response imitation saja tidak cukup untuk membangun simulasi manusia yang realistis

## Gagasan Inti Paper

Paper ini mendorong pergeseran dari:

- **response imitation**

menuju:

- **state alignment**

Artinya, model tidak hanya diminta menghasilkan jawaban yang mirip manusia, tetapi juga harus selaras dengan state laten yang relevan.

State yang dibahas dalam paper ini mencakup dimensi seperti:

- belief
- goal
- emotion
- value
- stance
- communication

## Kontribusi Utama

Kontribusi penting paper ini adalah menunjukkan bahwa menyelaraskan state internal user dapat meningkatkan kualitas simulasi dibanding hanya mengejar kemiripan respons.

Secara umum, paper ini memberi pesan bahwa:

- state adalah unit analisis yang lebih bermakna daripada teks jawaban saja
- simulasi user yang realistis perlu menangkap alasan di balik respons, bukan hanya bentuk responsnya

## Inti Temuan

Takeaway utama yang kita pahami dari paper ini:

- Pendekatan berbasis **state alignment** mengungguli pendekatan **response imitation**.
- Model yang lebih selaras dengan state user menghasilkan perilaku yang lebih akurat dan lebih human-like.
- Evaluasi user simulation sebaiknya tidak berhenti pada lexical similarity atau response matching.

## Makna Konseptual

Paper ini penting karena menggeser fokus simulasi user dari:

- "apakah jawabannya mirip?"

menjadi:

- "apakah state yang mendasari jawaban itu juga masuk akal?"

Ini sangat relevan untuk human simulation, karena manusia tidak hanya berbeda pada kata-kata yang mereka pilih, tetapi juga pada:

- apa yang mereka percayai
- apa tujuan mereka
- nilai apa yang mereka pegang
- bagaimana mereka berkomunikasi

## Keterbatasan atau Batas Fokus Paper

Meski sangat relevan, paper ini masih cenderung melihat alignment sebagai sesuatu yang diinginkan:

- semakin selaras state dengan respons manusia, semakin baik

Yang belum banyak dibahas secara eksplisit:

- bagaimana jika antar-state itu sendiri bertentangan?
- apakah semua konflik antar belief, value, dan behavior harus dianggap jelek?
- apakah sebagian konflik justru merupakan ciri manusia yang realistis?

## Relevansi untuk Riset Human Simulation

Paper ini menjadi fondasi penting untuk arah riset kita karena menegaskan bahwa:

> unit evaluasi yang lebih tepat untuk human simulation adalah state, bukan hanya response

Dari sini muncul langkah berikutnya:

- kalau state memang penting, maka konflik antar-state juga harus dievaluasi
- tidak semua inkonsistensi perlu dihukum
- sebagian inkonsistensi bisa jadi adalah bentuk **human-like cognitive dissonance**

## Hubungan dengan Ide Research Gap Kita

Paper ini membantu menjelaskan posisi ide kita:

- HumanLM sudah bergerak melampaui response imitation
- tetapi framework-nya belum secara eksplisit membedakan:
  - konflik state yang masih manusiawi
  - konflik state yang cuma artifact model

Dengan kata lain, paper ini membuka pintu untuk pertanyaan lanjutan:

> jika model sudah state-aware, bagaimana kita menilai apakah konflik state yang muncul itu realistis atau justru menunjukkan kegagalan model?

## Takeaway untuk Kita

Pelajaran paling penting dari paper ini:

1. Simulasi user yang baik harus memahami state internal, bukan hanya teks respons.
2. Belief, goal, emotion, value, dan stance adalah komponen penting dalam perilaku user.
3. Alignment pada level state memberi dasar yang lebih kuat untuk realism.
4. Langkah riset berikutnya adalah mengevaluasi **kualitas konflik antar-state**, bukan hanya keberadaan state itu sendiri.

## Kesimpulan

Paper HumanLM menunjukkan bahwa simulasi manusia menjadi lebih baik ketika model belajar menyelaraskan state laten user, bukan sekadar meniru jawaban mereka. Bagi riset kita, ini menjadi titik awal penting: setelah state dianggap sentral, pertanyaan berikutnya adalah bagaimana membedakan konflik state yang realistis secara manusiawi dari konflik yang hanya merupakan artifact model.
