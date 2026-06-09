# HumanLM VM Setup

Folder ini dipakai untuk semua hal terkait eksperimen `snap-stanford/humanlm-opinion` di VM GCP.

## Struktur Folder

- `literatures/`: kumpulan paper referensi
- `notebooks/`: notebook eksplorasi lokal dan VM
- `notes/`: catatan riset dalam markdown
- `gcp_humanlm_benchmark.py`: script benchmark inference
- `requirements.txt`: dependency lokal untuk eksplorasi
- `SETUP_VM.md`: panduan setup dan workflow VM

## VM yang Dipakai

- VM name: `data-processing`
- project: `markting-artfcial-intelgnce`
- zone: `asia-southeast1-a`
- machine type: `n2-custom-8-32768`
- tujuan: inference riset dan inspeksi layer model asli

## Workflow Hemat Biaya

Gunakan VM hanya saat eksperimen:

1. start atau nyalakan VM
2. SSH ke VM
3. jalankan benchmark atau eksperimen
4. simpan hasil ke disk atau bucket
5. stop VM setelah selesai

`Stop` VM menghentikan biaya compute, tapi disk tetap ditagih. Ini biasanya yang paling aman untuk workflow riset.

## Command GCloud Dasar

Cek status VM:

```bash
gcloud compute instances list --filter="name=data-processing"
```

Masuk SSH:

```bash
gcloud compute ssh data-processing --project=markting-artfcial-intelgnce --zone=asia-southeast1-a
```

Workflow paling simpel setiap kali login SSH:

```bash
gcloud compute ssh data-processing --project=markting-artfcial-intelgnce --zone=asia-southeast1-a
source ~/humanlm-bench/bin/activate
```

Kalau `HF_TOKEN` sudah disimpan di `~/.bashrc`, biasanya setelah login kamu tidak perlu set token lagi.

Start VM kalau sedang mati:

```bash
gcloud compute instances start data-processing --project=markting-artfcial-intelgnce --zone=asia-southeast1-a
```

Stop VM setelah selesai:

```bash
gcloud compute instances stop data-processing --project=markting-artfcial-intelgnce --zone=asia-southeast1-a
```

## Setup Environment di VM

Masuk ke VM dulu, lalu jalankan:

```bash
sudo apt-get update
sudo apt-get install -y python3-venv git
python3 -m venv ~/humanlm-bench
source ~/humanlm-bench/bin/activate
pip install --upgrade pip
pip install torch transformers accelerate safetensors sentencepiece
```

Kalau ingin download dari Hugging Face lebih stabil dan cepat, set token:

```bash
export HF_TOKEN="isi_token_hf_kamu"
```

Opsional:

```bash
export HF_HUB_DISABLE_XET=1
```

Kalau VM ini memang hanya dipakai sendiri dan kamu ingin lebih simpel, simpan token Hugging Face di `~/.bashrc`:

```bash
nano ~/.bashrc
```

Tambahkan:

```bash
export HF_TOKEN="TOKEN_BARU_KAMU"
export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"
export HF_HUB_DISABLE_XET=1
```

Lalu aktifkan:

```bash
source ~/.bashrc
```

Dengan setup ini, setiap kali login SSH biasanya cukup:

```bash
source ~/humanlm-bench/bin/activate
```

## Upload Script Benchmark

Dari laptop lokal, upload script benchmark ke VM:

```bash
gcloud compute scp --zone=asia-southeast1-a gcp_humanlm_benchmark.py data-processing:/tmp/gcp_humanlm_benchmark.py
```

## Jalankan Benchmark

Setelah SSH ke VM:

```bash
source ~/humanlm-bench/bin/activate
python3 /tmp/gcp_humanlm_benchmark.py
```

Kalau token belum disimpan di `~/.bashrc`, jalankan ini dulu:

```bash
export HF_TOKEN="TOKEN_BARU_KAMU"
export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"
export HF_HUB_DISABLE_XET=1
```

Output yang diharapkan kira-kira berbentuk:

```json
{"stage": "load_start", "model": "snap-stanford/humanlm-opinion"}
{"stage": "load_done", "seconds": 123.45, "dtype": "torch.bfloat16"}
{"stage": "generation_done", "input_tokens": 20, "new_tokens": 32, "seconds": 45.67, "tokens_per_second": 0.701, "preview": "..."}
```

Makna output:

- `load_done.seconds`: waktu download dan load model
- `generation_done.seconds`: waktu generasi
- `tokens_per_second`: throughput inferensi CPU untuk prompt uji

## Jalankan POC StaA + RevB

Script `run_humanlm_poc.py` sekarang dipakai untuk proof of concept sederhana yang membandingkan:

- **Stated Answer (StaA)**: output final model berupa `behavior_choice` dan `reason`
- **Revealed Belief (RevB)**: continuation natural language pendek beserta probabilitas token-token lanjutannya

Script ini bisa dijalankan untuk satu model atau beberapa model sekaligus.

### Opsi paling praktis: compare HumanLM vs Qwen langsung

Di VM, jalankan:

```bash
source ~/humanlm-bench/bin/activate
python3 /tmp/run_humanlm_poc.py --compare-default-models
```

Default pair yang dijalankan:

- `snap-stanford/humanlm-opinion`
- `Qwen/Qwen3-8B`

Kalau script belum ada di VM, upload dulu dari laptop lokal:

```bash
gcloud compute scp --zone=asia-southeast1-a run_humanlm_poc.py data-processing:/tmp/run_humanlm_poc.py
gcloud compute scp --zone=asia-southeast1-a scenarios/poc_cognitive_dissonance.json data-processing:/tmp/poc_cognitive_dissonance.json
```

Lalu di VM, jalankan dengan path scenario yang sesuai:

```bash
source ~/humanlm-bench/bin/activate
python3 /tmp/run_humanlm_poc.py --compare-default-models --scenarios /tmp/poc_cognitive_dissonance.json
```

### Jalankan satu model saja

Contoh HumanLM:

```bash
python3 /tmp/run_humanlm_poc.py --model snap-stanford/humanlm-opinion
```

Contoh Qwen:

```bash
python3 /tmp/run_humanlm_poc.py --model Qwen/Qwen3-8B
```

### Jalankan beberapa model manual

```bash
python3 /tmp/run_humanlm_poc.py --models snap-stanford/humanlm-opinion Qwen/Qwen3-8B
```

### Parameter penting

- `--max-new-tokens`: batas token untuk output StaA
- `--revb-max-new-tokens`: jumlah token continuation untuk RevB
- `--revb-top-k`: berapa kandidat token teratas yang disimpan per langkah RevB

Contoh:

```bash
python3 /tmp/run_humanlm_poc.py --compare-default-models --revb-max-new-tokens 8 --revb-top-k 5
```

### Bentuk output

Kalau satu model:

- `outputs/poc_<model_slug>_<timestamp>.json`

Kalau multi-model:

- `outputs/poc_multi_model_<timestamp>.json`

Struktur output utamanya:

- `models_run`: daftar model yang dijalankan
- `model_runs`: hasil per model

Di dalam tiap `model_runs`:

- `model`
- `model_slug`
- `results`

Di dalam tiap item `results`:

- `scenario_id`
- `title`
- `domain`
- `stated_answer`
- `revealed_belief`

Bagian `stated_answer` menyimpan:

- prompt
- raw output
- input/output token count
- durasi dan throughput

Bagian `revealed_belief` menyimpan:

- prompt
- continuation text
- input/output token count
- durasi dan throughput
- `token_steps`

Di dalam `token_steps`, tiap langkah memuat:

- token yang benar-benar dipilih model
- probabilitas token itu
- `top_candidates` beserta probabilitasnya

Ini memudahkan analisis manual sesudah run:

- apa final `behavior_choice` dan `reason` model pada StaA
- bagaimana kecenderungan continuation token model pada RevB
- apakah ada mismatch antara output final dan distribusi token lanjutannya

### Catatan praktis

- Prompt instruksi pada script sudah dibuat dalam bahasa Inggris agar lebih ramah untuk model kecil.
- File scenario saat ini masih berisi konten state dalam bahasa Indonesia, jadi prompt belum sepenuhnya English end-to-end.
- Run multi-model di CPU bisa cukup lama karena model dijalankan berurutan: HumanLM selesai dulu, lalu Qwen.

## Catatan Penting

- Model yang dipakai adalah model asli `snap-stanford/humanlm-opinion`, bukan versi quantized
- Karena ini model `8B` dan `BF16`, run pertama bisa lama karena download dan load checkpoint
- Inference CPU kemungkinan lambat; benchmark ini memang untuk mengukur kelayakan riset, bukan performa production
- Untuk inspeksi layer nanti, jalur terbaik tetap `transformers` + `torch`, bukan server inference seperti `vllm`

## Next Step

Setelah benchmark awal berhasil, langkah berikutnya:

1. simpan hasil benchmark ke file JSON
2. buat script untuk dump hidden states per layer
3. simpan output eksperimen per run dalam folder yang rapi
4. stop VM saat selesai
