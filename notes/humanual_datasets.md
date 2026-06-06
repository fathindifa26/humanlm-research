# Humanual Datasets

Catatan ini merangkum pemahaman kita tentang folder `humanlm/humanual_datasets/`.

## Inti Besarnya

`humanual_datasets` adalah pipeline untuk mengumpulkan data perilaku user dari berbagai platform, lalu mengubahnya menjadi dataset yang bisa dipakai untuk melatih model seperti HumanLM.

Target akhirnya bukan sekadar kumpulan komentar mentah, tetapi dataset dengan pola:

- ada `context` atau `prompt`
- ada `response` target dari user tertentu
- ada `user_id` yang konsisten
- ada `persona` user yang diringkas dari histori responsnya

Secara sederhana, masalah yang ingin dibentuk adalah:

> "Dalam konteks seperti ini, jika yang merespons adalah user X, kira-kira apa responsnya?"

## Sumber Datanya

README menjelaskan ada 6 domain utama:

- `Humanual-News`: komentar berita di YouTube
- `Humanual-Book`: review buku dari Amazon Reviews
- `Humanual-Opinion`: post dan komentar Reddit
- `Humanual-Politics`: artikel dan respons Medium
- `Humanual-Chat`: percakapan multi-turn dari WildChat
- `Humanual-Email`: thread email Enron

Setiap domain punya skrip pengumpulannya sendiri, karena struktur sumber aslinya berbeda.

## Bentuk Raw Data

Setelah data diambil, semuanya dinormalisasi ke schema umum:

```python
{
    "prompt": [...],
    "completion": "...",
    "post_id": "...",
    "user_id": "...",
    "timestamp": 0,
    "metadata": {...},
}
```

Maknanya:

- `prompt`: konteks sebelum respons target
- `completion`: jawaban target user
- `post_id`: id post/thread asal
- `user_id`: id user yang memberi respons target
- `timestamp`: waktu respons
- `metadata`: info tambahan dari platform asal

Jadi semua domain akhirnya dipaksa masuk ke format "context -> user response".

## Bagaimana Persona dan Demografi Muncul

Bagian penting dari pipeline ini adalah `process_raw.py` dan `persona_generator.py`.

Alurnya:

1. ambil beberapa komentar awal dari seorang user
2. gabungkan menjadi history text
3. kirim ke LLM persona generator
4. LLM menghasilkan JSON persona

Isi persona umumnya:

- `demographics`
- `interests`
- `values`
- `communication`
- `statistics`

Hal penting yang kita pahami:

- demografi **bukan** diambil dari profil resmi platform
- demografi disimpulkan dari teks user
- tetapi prompt persona generator mewajibkan hanya memakai informasi yang **eksplisit**
- kalau tidak ada bukti jelas, field demografi harus diisi `NA`

Jadi "demografi" di sini sebenarnya adalah hasil ekstraksi berbasis teks, bukan biodata asli yang diverifikasi.

## Step 1: Collecting Raw Data

README menjelaskan cara mengumpulkan raw data per domain.

Contohnya:

- `humanual_news.py` mengambil channel, playlist, video, komentar, dan optional transcript YouTube
- `humanual_opinion.py` mengambil post Reddit dan seluruh tree komentar
- `humanual_politics.py` mengambil artikel Medium dan response-thread-nya

Makna tahap ini:

- fokusnya mengubah data platform asli menjadi kumpulan contoh `prompt/completion`
- setiap domain tetap boleh punya cara scraping sendiri
- tetapi output akhirnya harus konsisten

## Step 2: Processing Raw Data

Setelah raw data jadi, `process_raw.py` menjalankan pipeline umum:

1. load raw dataset
2. filter berdasarkan jumlah komentar user
3. jalankan filter custom kalau ada
4. jalankan transform custom kalau ada
5. generate persona user dari histori awal
6. split menjadi train / val / seen_test / unseen_test
7. simpan atau upload hasil

Ini artinya raw data saja belum cukup. Data masih perlu dibersihkan, diringkas, dan dibagi secara metodologis.

## Split yang Penting

README menekankan pembagian:

- `train`
- `val`
- `seen_test`
- `unseen_test`

Maknanya:

- `seen_test`: user pernah muncul saat training, tapi contoh tertentu ditahan untuk evaluasi
- `unseen_test`: user tidak pernah muncul saat training

Kenapa ini penting:

- mereka ingin tahu apakah model bisa meniru user yang sudah dikenal
- dan juga apakah model bisa generalisasi ke user baru lewat persona/history

## Contoh Intuisi Per Domain

### Humanual-News

- post = video berita YouTube
- context = deskripsi video, optional transcript, dan mungkin komentar parent
- completion = komentar target user

### Humanual-Opinion

- post = post Reddit
- context = post + rantai parent comments
- completion = komentar target user

### Humanual-Politics

- post = artikel Medium
- context = artikel + response chain di bawahnya
- completion = response target user

## Seperti Apa Bentuk 1 Unit Data

Contoh sederhana dari domain Reddit:

```json
{
  "prompt": [
    {
      "role": "poster_1",
      "content": "AITA for refusing to lend money to my brother?",
      "metadata": {
        "subreddit": "AmItheAsshole"
      }
    },
    {
      "role": "user_parent",
      "content": "NTA. Your brother sounds irresponsible.",
      "metadata": {
        "comment_id": "c1"
      }
    }
  ],
  "completion": "I agree, especially if this has happened before.",
  "post_id": "post_123",
  "user_id": "user_77",
  "timestamp": 1717000000,
  "metadata": {
    "comment_id": "c2"
  }
}
```

Maknanya:

- user target adalah `user_77`
- model diberi konteks post dan komentar parent
- target yang harus dipelajari adalah `completion`

Lalu dari histori awal `user_77`, pipeline bisa membuat persona semacam:

```json
{
  "demographics": {
    "age group": "NA",
    "gender": "NA",
    "location": "NA",
    "occupation": "NA",
    "nationality": "NA",
    "other": "NA"
  },
  "interests": ["family conflict", "moral judgment"],
  "values": ["fairness", "personal responsibility"],
  "communication": ["direct", "advice-giving"],
  "statistics": ["medium-length responses"]
}
```

## Kesimpulan

Pemahaman kita saat ini:

- `humanual_datasets` adalah mesin pembuat dataset HumanLM
- tujuannya bukan sekadar scrape data, tetapi membangun dataset perilaku user
- setiap contoh data adalah relasi `context -> response user`
- persona dibuat dari histori komentar user
- demografi tidak berasal dari profil platform, tetapi dari teks user sendiri jika memang eksplisit
- hasil akhirnya adalah dataset siap training/evaluasi untuk memodelkan "respons user tertentu dalam konteks tertentu"
