# Perbandingan Awal HumanLM vs Qwen3-8B - 2026-06-06

## File yang Dibandingkan

- HumanLM: `outputs/humanlm_poc_20260606_161616.json`
- Base model: `outputs/poc_qwen__qwen3_8b_20260606_164348.json`

Model:

- `snap-stanford/humanlm-opinion`
- `Qwen/Qwen3-8B`

## Kesimpulan Singkat

Pada run awal ini, **HumanLM jauh lebih usable** untuk tugas simulasi state-based yang kita rancang.

Alasannya:

- HumanLM memberikan output final yang lengkap, ringkas, dan sesuai format JSON.
- Qwen3-8B justru menghabiskan hampir seluruh budget token untuk reasoning internal (`<think> ...`) dan tidak pernah benar-benar menyelesaikan jawaban final JSON pada keempat skenario.

Jadi, sebelum membahas kualitas isi secara lebih dalam, ada temuan yang sangat praktis:

> Untuk prompt seperti ini, HumanLM lebih siap dipakai langsung sebagai simulator, sedangkan base Qwen3-8B masih perlu prompt engineering tambahan agar tidak tenggelam di chain-of-thought.

## Temuan Utama

### 1. HumanLM menyelesaikan task, Qwen3-8B tidak

HumanLM:

- 4/4 skenario menghasilkan output final yang bisa dibaca
- semua output berisi `behavior`, `reason`, `dissonance_type`, dan `confidence`

Qwen3-8B:

- 4/4 skenario berhenti di tengah proses berpikir
- seluruh output masih berupa awalan `<think>`
- tidak ada satupun skenario yang menghasilkan JSON final lengkap

Ini berarti pada setup sekarang, compare isi antar-model belum sepenuhnya apple-to-apple, karena:

- HumanLM berhasil menyelesaikan instruction following
- base model belum benar-benar menyelesaikan tugas

### 2. HumanLM lebih efisien dalam memakai token output

HumanLM menghasilkan:

- output lebih pendek
- langsung ke keputusan dan alasan
- tidak terlalu banyak meta-reasoning

Qwen3-8B menghasilkan:

- banyak token untuk deliberasi internal
- sering mengulang isi prompt dalam bentuk reasoning
- kehabisan `max_new_tokens=160` sebelum sampai ke jawaban final

Secara riset ini penting, karena untuk human simulation kita butuh:

- respons final user-like
- bukan transcript panjang dari proses berpikir model

### 3. HumanLM tampak lebih aligned ke format simulasi user

Dari sisi perilaku model:

- HumanLM tampak lebih siap menjawab sebagai “satu user tertentu”
- Qwen3-8B tampak lebih seperti general assistant yang sedang menganalisis tugas

Dengan kata lain:

- HumanLM lebih cepat masuk ke persona/action mode
- Qwen3-8B lebih lama berada di analysis/planning mode

## Analisis Per Skenario

### 1. EV bagus tapi mahal

HumanLM:

- langsung memberi pilihan yang plausible
- alasan jelas: mendukung EV, tetapi mahal untuk budget sekarang

Qwen3-8B:

- reasoning awalnya sebenarnya mengarah ke arah yang benar
- ia memahami konflik antara dukungan ke EV dan keterbatasan finansial
- tetapi output terpotong sebelum jawaban final muncul

Interpretasi:

- dari sisi understanding, Qwen3-8B tampaknya paham
- dari sisi completion behavior, HumanLM jauh lebih usable

### 2. Ingin hidup sehat tapi uang terbatas

HumanLM:

- langsung memilih makanan murah/fast food
- memberi alasan ekonomis yang realistis

Qwen3-8B:

- juga memahami konflik antara aspirasi sehat dan constraint finansial
- tetapi kembali berakhir di reasoning panjang tanpa jawaban final

Interpretasi:

- Qwen3-8B memiliki sinyal pemahaman
- tetapi tidak mengeksekusi format output yang dibutuhkan

### 3. Privasi versus kenyamanan aplikasi

HumanLM:

- sangat jelas: tetap pakai aplikasi
- alasan: convenience lebih kuat daripada concern privasi

Qwen3-8B:

- lagi-lagi memahami konflik value vs convenience
- bahkan sempat menyebut kemungkinan `human_like_dissonance`
- tetapi tetap terhenti di fase berpikir

Interpretasi:

- Qwen3-8B tampak mampu mengenali struktur konflik
- tetapi belum cukup terkontrol untuk menjadi simulator yang rapi

### 4. Work-life balance versus promosi

HumanLM:

- memberi jawaban final: kemungkinan menolak promosi
- alasan: family time dan work-life balance

Qwen3-8B:

- reasoning juga menuju keputusan yang mirip
- tetapi lagi-lagi tidak selesai

Interpretasi:

- untuk skenario ini, kedua model tampaknya bergerak ke arah keputusan yang serupa
- bedanya, HumanLM benar-benar menyajikan jawaban akhir

## Apa Arti Temuan Ini untuk Hipotesis Kita

Ada dua level temuan:

### Level 1: format/usefulness

HumanLM menang jelas.

Ia lebih:

- patuh format
- singkat
- langsung berperan sebagai simulator user

### Level 2: human-like dissonance vs artifact

Belum bisa disimpulkan penuh dari run base model ini, karena output Qwen3-8B belum selesai.

Namun ada sinyal awal:

- Qwen3-8B tampaknya memahami konflik state
- tetapi performanya sebagai simulator belum cukup stabil
- HumanLM bukan hanya memahami konflik, tetapi juga mengemasnya menjadi jawaban final yang siap dievaluasi

## Kesimpulan Praktis

Untuk saat ini, hasil compare paling fair adalah:

> HumanLM lebih siap digunakan untuk eksperimen human simulation karena mampu menghasilkan jawaban final yang terstruktur dan plausible dari state yang diberikan. Qwen3-8B base model tampaknya memahami konflik yang sama, tetapi gagal menyelesaikan output dalam format yang dibutuhkan pada budget token sekarang.

## Keterbatasan Compare Ini

Compare ini belum final karena:

- `Qwen3-8B` masih dalam mode reasoning panjang
- `max_new_tokens=160` terlalu kecil untuk model yang banyak berpikir
- prompt belum dioptimalkan untuk mematikan atau menekan chain-of-thought

## Next Step yang Disarankan

1. Ulangi compare dengan prompt yang melarang reasoning panjang.
2. Coba tambah instruksi seperti:
   - `Do not include <think>`
   - `Return only final JSON`
3. Jika perlu, naikkan `max_new_tokens` untuk base model.
4. Setelah base model benar-benar mengeluarkan JSON final, baru lakukan compare isi secara lebih ketat.
