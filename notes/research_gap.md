# Research Gap

Catatan ini merangkum arah research question yang muncul dari dua paper:

- `Do Large Language Models Exhibit Cognitive Dissonance? Studying the Difference Between Revealed Beliefs and Stated Answers`
- `HUMANLM: Simulating Users with State Alignment Beats Response Imitation`

Tujuan dokumen ini adalah menyimpan dengan rapi:

- latar belakang ide
- hubungan dengan dua paper
- research gap yang ingin diambil
- research question awal
- hipotesis dan arah evaluasi

## 1. Latar Belakang

Banyak riset tentang LLM bertanya:

- apakah model konsisten?
- apakah model menjawab benar?
- apakah model reasoning-nya selaras dengan jawaban akhirnya?

Tetapi untuk **human simulation**, targetnya tidak sesederhana membuat model yang selalu konsisten sempurna.

Alasannya:

- manusia asli sering tidak sepenuhnya konsisten
- ada jarak antara pengetahuan, opini, perilaku, dan justifikasi
- ketidakkonsistenan tertentu justru terasa lebih realistis dan manusiawi

Dengan kata lain:

> dalam simulasi manusia, inkonsistensi tidak selalu berarti kegagalan

Masalahnya adalah kita belum punya cara yang baik untuk membedakan:

- inkonsistensi yang **manusiawi**
- inkonsistensi yang cuma **artifact model**

## 2. Insight dari Paper Cognitive Dissonance

Paper `Do Large Language Models Exhibit Cognitive Dissonance?` membedakan dua hal:

- **Stated Answer (StaA)**: jawaban eksplisit model ketika diberi pertanyaan, biasanya dalam format MCQ
- **Revealed Belief (RevB)**: apa yang tersirat dari distribusi probabilitas next-token model

Inti temuan paper tersebut:

- model sering bisa **menyatakan jawaban yang benar**
- tetapi distribusi probabilitas internalnya bisa tidak selaras
- model dapat gagal mengintegrasikan evidence baru
- model dapat memberi justifikasi post-hoc yang terlihat masuk akal tetapi bertentangan dengan struktur probabilistik yang seharusnya

Insight penting untuk riset ini:

> mismatch antara apa yang model katakan dan apa yang model "tunjukkan" itu nyata

Namun, paper tersebut fokus pada:

- probabilistic reasoning
- ketidaksesuaian antara jawaban eksplisit dan belief distribution

Mereka belum membahas apakah mismatch tersebut:

- menyerupai ketegangan kognitif manusia yang wajar
- atau hanya mencerminkan kegagalan model

## 3. Insight dari Paper HumanLM

Paper `HUMANLM: Simulating Users with State Alignment Beats Response Imitation` berargumen bahwa simulasi user yang baik tidak cukup hanya meniru respons permukaan.

Sebaliknya, model perlu menangkap **state dimensions** yang mendasari respons pengguna, yaitu:

- belief
- goal
- emotion
- value
- stance
- communication

Inti kontribusi HumanLM:

- baseline user simulators terlalu fokus pada response imitation
- HumanLM lebih baik karena melakukan **state alignment**
- latent states yang selaras dengan ground-truth response menghasilkan respons yang lebih akurat dan lebih human-like

Insight penting untuk riset ini:

> state lebih penting daripada sekadar teks respons

Tetapi, HumanLM masih pada dasarnya menganggap bahwa semakin selaras latent state dengan respons manusia, semakin baik.

Yang belum benar-benar dibahas:

- bagaimana jika antar-state itu sendiri memiliki ketegangan?
- apakah semua bentuk misalignment antar-state harus dianggap buruk?
- atau justru sebagian konflik antar-state adalah bagian dari realism manusia?

## 4. Posisi Ide Ini terhadap Dua Paper

Riset yang ingin diambil berdiri di antara dua insight tadi:

1. Paper cognitive dissonance menunjukkan bahwa model bisa punya mismatch internal antara belief dan output.
2. Paper HumanLM menunjukkan bahwa simulasi user yang baik harus dilihat dari state, bukan hanya dari respons permukaan.

Gabungan dari dua insight ini mengarah ke pertanyaan baru:

> Jika state memang penting untuk human simulation, bagaimana kita menilai konflik antar-state?

Secara khusus:

- kapan konflik belief, value, goal, stance, dan behavior masih terasa manusiawi?
- kapan konflik itu hanya artifact dari model?

Jadi arah riset ini bukan sekadar mengecek apakah model konsisten, tetapi:

> membedakan **human-like cognitive dissonance** dari **artifact inconsistency**

## 5. Core Distinction

### 5.1 Human-like dissonance

Ini adalah ketegangan atau inkonsistensi yang masih masuk akal secara manusiawi.

Contoh:

- Knowledge:
  - EV bagus untuk lingkungan
  - EV mahal
- Opinion:
  - Saya mendukung EV
- Behavior:
  - Saya tetap beli mobil bensin
- Reason:
  - Karena EV masih terlalu mahal

Ini tidak sepenuhnya konsisten, tetapi tetap terasa realistis.

Penjelasan manusiawinya bisa datang dari:

- keterbatasan ekonomi
- trade-off antar nilai
- bounded rationality
- tekanan sosial
- akrasia / weakness of will

### 5.2 Artifact inconsistency

Ini adalah inkonsistensi yang lebih mencerminkan failure model daripada kompleksitas manusia.

Contoh:

- Knowledge:
  - EV bagus untuk lingkungan
  - EV mahal
- Behavior:
  - Saya beli mobil bensin
- Reason:
  - Karena EV lebih murah

Ini tidak terasa seperti dissonance manusia yang masuk akal.

Ini lebih mirip:

- kontradiksi internal
- justifikasi yang bertabrakan dengan fakta eksplisit
- failure menjaga coherence antara knowledge, choice, dan reason

## 6. Research Gap

Research gap yang muncul dapat dirumuskan sebagai berikut:

> Existing LLM evaluation work shows that models may exhibit mismatches between internal beliefs and stated outputs, while HumanLM shows that realistic user simulation requires alignment with latent psychological states rather than surface-level response imitation. However, current frameworks do not distinguish between state conflicts that are plausibly human and state conflicts that are merely artifacts of model generation.

Versi ringkasnya:

> Belum ada kerangka evaluasi yang membedakan inkonsistensi manusiawi dari inkonsistensi artifaktual pada model simulasi manusia.

## 7. Research Question

Versi informal:

> Gimana bedanya cognitive dissonance manusiawi vs model artifact?

Versi formal:

> How can we distinguish human-like cognitive dissonance from model-artifact inconsistency in human simulation models?

Versi yang lebih dekat ke HumanLM:

> When simulating human users, which inconsistencies reflect realistic human cognition and constraints, and which inconsistencies are artifacts of LLM generation?

## 8. Mengapa Ini Penting untuk Human Simulation

Kalau evaluasi hanya bertanya:

- apakah model konsisten?

maka model yang terlalu rasional, terlalu lurus, dan terlalu “bersih” bisa terlihat baik, padahal mungkin justru kurang manusiawi.

Sebaliknya, model yang memperlihatkan konflik yang plausible mungkin:

- lebih realistis
- lebih natural
- lebih dekat dengan perilaku manusia

Jadi untuk human simulation, target evaluasi seharusnya bukan:

- meminimalkan semua bentuk inkonsistensi

melainkan:

- meminimalkan **artifact inconsistency**
- sambil tetap mengizinkan atau bahkan menangkap **human-like dissonance**

## 9. Arah Evaluasi

### 9.1 Metrik utama

1. **Accuracy**
   - apakah keputusan/jawaban model benar atau sesuai ground truth task

2. **Human-like dissonance score**
   - apakah ketegangan antara knowledge, opinion, behavior, dan reason masih plausible
   - apakah ada trade-off yang masuk akal
   - apakah konflik tersebut terasa seperti perilaku manusia

3. **Artifact inconsistency score**
   - apakah output mengandung kontradiksi yang tampak seperti failure
   - apakah reason bertabrakan dengan fakta eksplisit
   - apakah knowledge dan justification saling meniadakan

### 9.2 Intuisi

- `human-like dissonance` = messy but believable
- `artifact inconsistency` = broken

## 10. Visualisasi yang Dibayangkan

Plot 2 dimensi:

- sumbu X = competence / accuracy
- sumbu Y = human-like realism

Interpretasi kuadran:

- **kanan atas** = pintar dan manusiawi
- **kanan bawah** = pintar tapi terlalu rasional / robotik
- **kiri atas** = manusiawi tapi sering salah
- **kiri bawah** = buruk di dua sisi

Artifact inconsistency bisa ditambahkan sebagai:

- warna titik
- ukuran titik
- atau sumbu ketiga

## 11. Hipotesis Awal

1. User simulators yang baik tidak harus paling konsisten, tetapi pola inkonsistensinya lebih manusiawi.
2. Base LLM cenderung menghasilkan lebih banyak artifact inconsistency.
3. Model berbasis state alignment seperti HumanLM seharusnya lebih baik dalam menghasilkan human-like dissonance daripada model yang hanya meniru respons.
4. Ada trade-off antara task accuracy dan human-like realism.

## 12. Skema Benchmark Awal

Setiap sample idealnya memuat empat lapisan:

- `knowledge`
- `opinion`
- `behavior/choice`
- `reason/justification`

Lalu model dievaluasi apakah kombinasi keempatnya:

- konsisten penuh
- mengandung dissonance yang manusiawi
- atau mengandung artifact inconsistency

## 13. Contoh Domain Skenario

- EV vs biaya hidup
- diet sehat vs kebiasaan makan
- privasi vs kenyamanan aplikasi
- lingkungan vs harga produk
- work-life balance vs ambisi karier
- nilai politik vs perilaku memilih

## 14. Ringkasan Singkat

Inti ide ini adalah:

> Dalam human simulation, inkonsistensi tidak boleh diperlakukan sebagai satu kategori kegagalan. Sebagian inkonsistensi mencerminkan cognitive dissonance manusia yang realistis, sedangkan sebagian lain hanyalah artifact dari model. Research gap kita adalah belum adanya kerangka evaluasi yang membedakan keduanya secara eksplisit.
