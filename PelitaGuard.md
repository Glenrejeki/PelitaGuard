# PelitaGuard — Project Structure & Build Instructions


## 1. Konteks & Alur Aplikasi

**Nama aplikasi:** PelitaGuard — aplikasi whistleblowing (pelaporan anonim) tingkat komunitas.

**Alur utama (user flow):**

```
[Landing Page] → [Login / Register] → [Home / Fitur Utama] → [Alur Laporan]
```

1. **Landing Page** — Layar pertama yang dilihat user sebelum login/register. Berisi penjelasan singkat aplikasi, value proposition ("laporan Anda aman & anonim"), dan tombol "Masuk" / "Daftar".
2. **Login / Register** — Autentikasi user. Register minimal (email/username + password) — hindari data pribadi berlebih karena ini aplikasi anonim.
3. **Home (Fitur Utama)** — Hub setelah login, entry point ke alur pelaporan (buat laporan baru, lihat status laporan, dsb).
4. **Alur Laporan** — Form input → sanitasi gambar lokal → preview → kirim ke backend → backend jalankan anti-stylometry → simpan.

Catatan desain: karena ini aplikasi anonim, pertimbangkan apakah "akun" benar-benar perlu identitas personal, atau cukup token/pseudonymous ID agar tidak menciptakan titik kebocoran identitas baru lewat sistem auth itu sendiri.

---

## 2. Tech Stack

| Layer | Teknologi |
|---|---|
| Mobile | Kotlin, Jetpack Compose, MVVM, Clean Architecture, Hilt, Retrofit, Google ML Kit |
| Navigasi | Jetpack Navigation Compose |
| Local storage | DataStore (token session) |
| Backend | Python 3.10+, FastAPI, Pydantic, SQLAlchemy |
| Auth | JWT (access token), password hashing (bcrypt/argon2) |
| AI Engine | LLM API (OpenAI/Gemini/Ollama) untuk anti-stylometry |
| Database | PostgreSQL |

---

## 3. Struktur Folder — Mobile App (Android/Kotlin)

```text
com.glen.pelitaguard
│
├── di/
│   └── AppModules.kt              # Hilt: Retrofit, ML Kit, DataStore, dsb
│
├── navigation/
│   ├── Screen.kt                  # sealed class semua route (Landing, Login, Register, Home, Report, Preview)
│   └── NavGraph.kt                # NavHost: mendefinisikan urutan Landing → Auth → Home
│
├── data/
│   ├── api/
│   │   ├── AuthApi.kt             # POST /api/v1/auth/login, /register
│   │   └── ReportApi.kt           # POST /api/v1/report
│   ├── local/
│   │   └── SessionManager.kt      # simpan/baca token via DataStore
│   └── repository_impl/
│       ├── AuthRepositoryImpl.kt
│       └── ReportRepositoryImpl.kt
│
├── domain/
│   ├── model/
│   │   ├── User.kt
│   │   └── ReportData.kt
│   ├── repository/
│   │   ├── AuthRepository.kt
│   │   └── ReportRepository.kt
│   └── usecase/
│       ├── LoginUseCase.kt
│       ├── RegisterUseCase.kt
│       ├── SanitizeImageUseCase.kt    # logika ML Kit: blok wajah & OCR teks sensitif
│       └── SubmitReportUseCase.kt
│
└── presentation/
    ├── landing/
    │   ├── LandingScreen.kt       # halaman pertama, tombol Masuk/Daftar
    │   └── LandingViewModel.kt    # (opsional, jika ada state cek session aktif)
    │
    ├── auth/
    │   ├── LoginScreen.kt
    │   ├── RegisterScreen.kt
    │   └── AuthViewModel.kt       # state login/register + validasi
    │
    ├── home/
    │   ├── HomeScreen.kt          # hub fitur utama setelah login
    │   └── HomeViewModel.kt
    │
    └── report_flow/
        ├── ReportScreen.kt        # form teks & upload gambar
        ├── PreviewScreen.kt       # review gambar tersensor sebelum kirim
        └── ReportViewModel.kt
```

**Logika navigasi (NavGraph.kt) — penting:**
- Start destination = `Screen.Landing`.
- Saat app dibuka, cek dulu apakah ada token tersimpan di `SessionManager` — kalau ada & valid, langsung skip ke `Screen.Home` (jangan paksa user login ulang tiap buka app).
- Landing → tombol "Daftar" ke `Screen.Register`, tombol "Masuk" ke `Screen.Login`.
- Login/Register sukses → `navController.navigate(Screen.Home) { popUpTo(Screen.Landing) { inclusive = true } }` — supaya user tidak bisa back ke landing/login pakai tombol back.

---

## 4. Struktur Folder — Backend (FastAPI)

```text
pelitaguard-backend/
│
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── auth.py            # POST /api/v1/auth/register, /login
│   │       └── report.py          # POST /api/v1/report (perlu token valid)
│   │
│   ├── core/
│   │   ├── config.py              # env vars, secret key JWT
│   │   ├── database.py            # SQLAlchemy session
│   │   └── security.py            # hash password, create/verify JWT
│   │
│   ├── deps.py                    # dependency get_current_user (validasi token)
│   │
│   ├── models/
│   │   └── domain_models.py       # tabel: users, reports
│   │
│   ├── schemas/
│   │   ├── auth_schemas.py        # UserCreate, UserLogin, Token
│   │   └── report_schemas.py      # ReportCreate, ReportResponse
│   │
│   └── ai_engine/
│       ├── llm_client.py          # HTTP client ke LLM (default: Ollama lokal)
│       └── stylometry_killer.py   # fungsi prompt anti-stylometry
│
├── requirements.txt
└── main.py                        # entry point, include_router auth & report
```

---

## 5. Urutan Pembuatan (untuk AI code editor)

Kerjakan bertahap, jangan langsung semua, agar mudah direview:

1. **Backend dulu:** `main.py`, `core/config.py`, `core/database.py`, `models/domain_models.py` (tabel `users` + `reports`).
2. **Backend auth:** `core/security.py`, `schemas/auth_schemas.py`, `api/endpoints/auth.py`, `deps.py`.
3. **Backend report + AI engine:** `schemas/report_schemas.py`, `api/endpoints/report.py`, `ai_engine/llm_client.py`, `ai_engine/stylometry_killer.py`.
4. **Mobile — navigasi & landing:** `navigation/Screen.kt`, `navigation/NavGraph.kt`, `presentation/landing/LandingScreen.kt`.
5. **Mobile — auth:** `domain/model/User.kt`, `data/api/AuthApi.kt`, `data/local/SessionManager.kt`, `presentation/auth/*`.
6. **Mobile — home & report flow:** `presentation/home/*`, lalu `presentation/report_flow/*` (termasuk `SanitizeImageUseCase.kt` pakai ML Kit).

---

## 6. Catatan Keamanan & Privasi (jangan diskip)

- **Strip EXIF metadata** dari gambar sebelum upload (GPS, timestamp, device model) — ini celah deanonimisasi paling gampang dieksploitasi, terpisah dari redaksi wajah.
- **OCR + face detection**, bukan cuma face detection — plat nomor/teks di background juga harus diblok.
- **LLM anti-stylometry**: default ke self-hosted (Ollama) bukan API cloud pihak ketiga, supaya isi laporan sensitif tidak keluar ke provider luar.
- **Logging server**: jangan log IP address user secara permanen di endpoint report.
- **Password**: hash pakai bcrypt/argon2, jangan pernah simpan plaintext.
- **JWT**: expiry pendek untuk access token, pertimbangkan refresh token terpisah.
- **Database**: pisahkan akses baca tabel `reports` dengan role terbatas, bukan superuser default.

---

## 7. System Prompt — Anti-Stylometry Engine (`stylometry_killer.py`)

```
Kamu adalah 'Stylometry Sanitizer', sebuah sistem keamanan data tingkat tinggi.
Tugasmu adalah menerima laporan kronologi kejadian dari pelapor anonim dan
menulisnya ulang menjadi laporan formal, obyektif, dan sepenuhnya netral.

ATURAN KETAT:
1. HILANGKAN GAYA BAHASA: Hapus semua singkatan gaul, dialek daerah, kebiasaan
   tanda baca yang unik (seperti "!!!!", "wkwk", atau "...."), dan idiom personal.
2. PERTAHANKAN FAKTA: Waktu, lokasi, jumlah, nama pelaku (jika ada), dan tindakan
   fisik/verbal yang terjadi harus tetap ada tanpa distorsi.
3. SUDUT PANDANG KETIGA: Ubah sudut pandang dari "aku/saya" menjadi "Pelapor".
4. NADA JURNALISTIK: Gunakan bahasa Indonesia baku (EYD) yang kering, prosedural,
   dan bebas emosi.
5. SENSOR IDENTITAS: Jika pelapor secara tidak sengaja menyebutkan namanya,
   jabatannya, atau ciri fisiknya, ganti dengan [IDENTITAS DISENSOR].

FORMAT OUTPUT:
Hanya kembalikan teks hasil netralisasi. Jangan tambahkan komentar apapun.
```

---

## 8. Instruksi Tugas untuk AI

Berdasarkan spesifikasi di atas, mulai coding secara bertahap sesuai urutan di Bagian 5.
Langkah pertama: buatkan boilerplate Backend FastAPI (`main.py`, `core/config.py`,
`core/database.py`, `models/domain_models.py`) untuk tabel `users` dan `reports`.
