# 📦 Zip Daemon: Auto File Compressor and Email Reporter

This project originated as a take-home coding assignment and has since been refactored into a modern, modular Python utility. It watches a directory for large files, compresses them into zip archives, and sends an email report with compression stats and attachments.

---

## 🧭 Features

- ✅ Command-line interface with `argparse`
- ✅ Graceful shutdown with `SIGTERM` / `SIGINT`
- ✅ File filtering by size and type
- ✅ Zip compression with per-file ratio tracking
- ✅ Automated email report with zip attachments
- ✅ Background thread daemon-like loop

---

## 🔧 How It Works

1. Monitor a directory (e.g., `/my/folder/`)
2. Find files exceeding a size threshold (e.g., `> 500KB`)
3. Skip images and existing `.zip` files
4. Compress selected files using `zipfile`
5. Generate a report (savings + compression ratio)
6. Send an email with attachments and report text

---

## 🛠 Technologies Used

- Python 3.6+
- `zipfile`, `os`, `signal`, `threading`, `argparse`
- `smtplib`, `email.mime` (for email sending)

---

## 🚀 Getting Started

```bash
python zip_daemon.py -d /path/to/folder -e recipient@example.com -s 500
```

| Flag | Description |
|------|-------------|
| `-d` | Target directory to monitor |
| `-e` | Email address to send report to |
| `-s` | Size threshold in KB |

⚠️ This script requires you to edit your local email credentials in `send_email()`.

---

## 🧱 Project Structure

```
zip-daemon/
├── zip_daemon.py        # Main executable script
├── compressor.py        # Handles file filtering + zipping
├── reporter.py          # Report text + email sending
├── watcher.py           # Daemon loop
├── legacy/              # Original version from 8 years ago
│   └── original_script.py
├── README.md
├── .gitignore
└── requirements.txt
```

---

## ✨ Planned Improvements

- Replace hardcoded email login with `.env` config
- Add logging and retry support
- Make cross-platform compatible (Linux/macOS/Windows)
- Add optional JSON log output or SQLite tracking

---

## 📚 Background
This script was originally written in 2016–2017 as part of a take-home assignment. It has since been revived and restructured as a production-style utility showcasing real-world scripting, automation, and modular Python practices.

---

## 📜 License
MIT
