# 7heknight.py

> A personal collection of Python scripts covering network tools, security research utilities, cross-platform CLI helpers, and code examples — built for learning, CTF practice, and day-to-day tasks.

---

## Overview

**7heknight.py** is a growing toolkit of standalone Python scripts organized by purpose. Each script is self-contained, runnable from the command line, and requires only Python 3.7+ (plus a small number of third-party packages where noted). The project spans four major domains:

| Domain | What it covers |
|---|---|
| `MyTools/` | Practical utilities: port scanning, MAC spoofing, password generation, WiFi credential extraction, duplicate file cleanup, and more |
| `Exploit/` | CTF and lab-environment offensive security demos: SQL injection, SSH brute-force, known CVE reproductions, and AV evasion shellcode |
| `linux2Windows/` | Unix-style command re-implementations (`ls`, `find`, `clear`, `pwd`) that run on Windows |
| `Example/` | Bite-sized reference scripts demonstrating web scraping, proxy handling, XML parsing, and Python idioms |

> **Disclaimer — Exploit folder**: All scripts inside `Exploit/` are written for **authorized lab environments, CTF challenges, and personal learning only**. Running them against systems you do not own or have explicit written permission to test is illegal. Use responsibly.

---

## Features

- **Zero-dependency core** — most tools use only the Python standard library
- **Cross-platform support** — scripts in `MyTools/` and `linux2Windows/` target Linux, macOS, and/or Windows
- **Argparse-driven CLIs** — consistent `--help` flags across all major tools
- **Multithreaded scanning** — `port_scanner.py` uses `ThreadPoolExecutor` for fast parallel probing
- **Auto-privilege escalation** — `MAC_Changer.py` and `getSavedWifiPass.py` self-elevate via `sudo`/UAC when needed
- **Cryptographic utilities** — `md5.py` for file integrity, `priv2pub.py` for RSA key derivation, `payloader.py` for AES payload handling
- **Dry-run safety** — `cleanDup.py` supports `--dry-run` to preview deletions before committing

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.7+ |
| Standard library modules | `socket`, `argparse`, `subprocess`, `threading`, `concurrent.futures`, `hashlib`, `re`, `os`, `ctypes` |
| Optional third-party | `requests`, `beautifulsoup4`, `selenium` (Example scripts only) |
| Platform targets | Linux, macOS, Windows |
| VCS | Git / GitHub |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/7heKnight/7heknight.py.git
cd 7heknight.py
```

### 2. (Optional) Install third-party dependencies

Most scripts need nothing beyond the standard library. The `Example/` scripts that do web scraping require:

```bash
pip install requests beautifulsoup4 selenium
```

### 3. Run any script directly

```bash
# Scan ports on a host
python MyTools/port_scanner.py -t 192.168.1.1 -p 22,80,443,8000-8080

# Change your MAC address
python MyTools/MAC_Changer.py -i eth0 -m AA:BB:CC:DD:EE:FF

# Generate a 20-character secure password
python MyTools/password_generator.py 20

# Compute the MD5 hash of a file
python MyTools/md5.py /path/to/file
```

---

## Configuration

Most scripts accept all configuration via CLI arguments. A few have hard-coded constants at the top of the file that you can edit before running.

### Environment variables

No `.env` file is required. Scripts that need elevated permissions detect this automatically.

### Configurable constants (per-file)

| Script | Constant | Purpose | Default |
|---|---|---|---|
| `MyTools/port_scanner.py` | `DEFAULT_TIMEOUT` | Per-port TCP connect timeout (seconds) | `1.0` |
| `MyTools/port_scanner.py` | `DEFAULT_WORKERS` | Thread-pool size | `100` |
| `MyTools/getSavedWifiPass.py` | `PASSWORD_LOG_FILE` | Output file for extracted WiFi passwords | `ListWifiPassword.txt` |
| `Exploit/Bludit-login.py` | `HOST` | Target Bludit admin URL | `http://[TARGET]/admin` |
| `Exploit/Bludit-login.py` | `USER` | Username to test | `[TARGET_USER]` |

> Replace all values marked `[...]` with your own before running.

---

## Scripts

### MyTools/

| Script | Description | Platforms |
|---|---|---|
| `port_scanner.py` | Multithreaded TCP port scanner; supports individual ports and ranges (e.g. `1-1024`) | Linux, macOS, Windows |
| `MAC_Changer.py` | Read and change the MAC address of a network interface; auto-elevates privileges | Linux, macOS, Windows |
| `password_generator.py` | Cryptographically secure password generator (`secrets` module); configurable length and character sets | All |
| `md5.py` | Print the MD5 hash of any file from the command line | All |
| `ping.py` | Cross-platform ping wrapper that parses reply/TTL output | Linux, macOS, Windows |
| `getSavedWifiPass.py` | Extract saved WiFi profile names and passwords via `netsh wlan`; saves results to a text file | Windows |
| `cleanDup.py` | Recursively scan a directory tree, detect duplicate files by SHA-256 hash, and remove them (supports `--dry-run`) | Linux, macOS, Windows |
| `check-sub-dir_pastebin.py` | Enumerate sub-paths on Pastebin-style targets | Linux, macOS |
| `priv2pub.py` | Derive an RSA public key from a private key (PEM or raw); wraps `openssl` | Linux, macOS, Windows |

### Exploit/ *(authorized environments only)*

| Script | Description |
|---|---|
| `ssh_brute.py` | Test SSH credentials from a wordlist against a target; Python 3.7+, requires OpenSSH client binary |
| `boolBlindi.py` | Boolean-based blind SQL injection demo against `sqli-labs` |
| `Bludit-login.py` | Bludit CMS CSRF-aware login brute-forcer (CVE research / HackTheBox Blunder) |
| `CVE-2018-11776.py` | Apache Struts 2 OGNL RCE reproduction (versions 2.3–2.3.34, 2.5–2.5.16) |
| `AntivirusEvasion_IAM302-Lab_Shell.py` | In-memory shellcode execution demo via `ctypes` (IAM302 lab exercise) |
| `example_payloader/payloader.py` | AES encrypt/decrypt a payload file |

### linux2Windows/

| Script | Unix equivalent | Description |
|---|---|---|
| `ls.py` | `ls` | List files and subdirectories in the current directory |
| `find.py` | `find` | Search for files by name (`-n`), extension (`-f`), or content (`--content`) within a directory tree |
| `clear.py` | `clear` | Clear the terminal screen |
| `pwd.py` | `pwd` | Print the current working directory |

### Example/

| Script | Description |
|---|---|
| `scrappingProxy.py` | Scrape a public HTTP proxy list using `requests` + `BeautifulSoup` |
| `ReFormatProxy.py` | Parse and reformat a raw proxy list file into `ip:port` lines |
| `RemoveUnwanted.py` | Strip unwanted characters or lines from a text file |
| `join&ListComprehensions.py` | Reference snippets for Python `str.join()` and list comprehensions |
| `get-path/get-path.py` | Extract unique URL paths from an XML sitemap (`<url><![CDATA[...]]></url>`) |

### WindowsAPI_CyThon/

| Script | Description |
|---|---|
| `MessageBoxA.py` | Call the Windows `MessageBoxA` API directly via `ctypes` — a minimal Windows API / Cython bridge demo |

---

## Folder Structure

```
7heknight.py/
├── Example/                        # Reference and learning scripts
│   ├── join&ListComprehensions.py
│   ├── ReFormatProxy.py
│   ├── RemoveUnwanted.py
│   ├── scrappingProxy.py
│   └── get-path/
│       ├── example.xml             # Sample XML sitemap input
│       ├── example_output.txt      # Expected output
│       └── get-path.py
├── Exploit/                        # Security research / CTF demos (lab use only)
│   ├── AntivirusEvasion_IAM302-Lab_Shell.py
│   ├── Bludit-login.py
│   ├── boolBlindi.py
│   ├── CVE-2018-11776.py
│   ├── ssh_brute.py
│   └── example_payloader/
│       ├── payload.txt.aes         # Sample AES-encrypted payload
│       └── payloader.py
├── linux2Windows/                  # Unix CLI commands re-implemented in Python
│   ├── clear.py
│   ├── find.py
│   ├── ls.py
│   └── pwd.py
├── MyTools/                        # Practical standalone utilities
│   ├── check-sub-dir_pastebin.py
│   ├── cleanDup.py
│   ├── getSavedWifiPass.py
│   ├── MAC_Changer.py
│   ├── md5.py
│   ├── password_generator.py
│   ├── ping.py
│   ├── port_scanner.py
│   └── priv2pub.py
├── WindowsAPI_CyThon/              # Windows API / Cython experiments
│   └── MessageBoxA.py
└── get-pip.py                      # pip bootstrapper (fallback installer)
```

---

## Deployment

These are standalone scripts — there is no server or package to deploy. To make any tool globally accessible from your terminal:

### Option A — Add the directory to PATH (temporary)

```bash
export PATH="$PATH:/path/to/7heknight.py/MyTools"
```

### Option B — Create a shell alias

```bash
# Add to ~/.zshrc or ~/.bashrc
alias portscan="python /path/to/7heknight.py/MyTools/port_scanner.py"
alias macchanger="python /path/to/7heknight.py/MyTools/MAC_Changer.py"
```

### Option C — Install as a pip-editable package (future)

If a `setup.py` / `pyproject.toml` is added in the future:

```bash
pip install -e .
```

---

## Troubleshooting

### `Permission denied` when running MAC_Changer or getSavedWifiPass

Both scripts attempt to auto-elevate. If that fails, run them explicitly with elevated privileges:

```bash
# Linux / macOS
sudo python MyTools/MAC_Changer.py -i eth0 -m AA:BB:CC:DD:EE:FF

# Windows (run terminal as Administrator)
python MyTools\getSavedWifiPass.py
```

### `ModuleNotFoundError: No module named 'requests'`

Install the required third-party packages:

```bash
pip install requests beautifulsoup4 selenium
```

### Port scanner returns no results

- Confirm the host is reachable: `ping <target>`
- Try increasing the timeout: add `-T 2.0` (if your version supports it) or edit `DEFAULT_TIMEOUT` at the top of `port_scanner.py`
- Some hosts silently drop packets — a lack of results may be expected

### `ssh_brute.py` hangs or exits immediately

- Ensure `ssh` is installed and available in your `PATH`: `which ssh`
- The script requires Python 3.7+ and a Unix-like OS with `pty` module

### `cleanDup.py` removed files I did not expect

Always run with `--dry-run` first to preview what would be deleted:

```bash
python MyTools/cleanDup.py /target/directory --dry-run
```

### `priv2pub.py` reports `openssl not found`

Install OpenSSL and ensure it is on your `PATH`:

```bash
# macOS (Homebrew)
brew install openssl

# Debian / Ubuntu
sudo apt install openssl
```

---

## Contributing

Contributions, bug reports, and new tool ideas are welcome.

### Steps

1. **Fork** the repository on GitHub.

2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/[YOUR_USERNAME]/7heknight.py.git
   cd 7heknight.py
   ```

3. **Create a branch** for your change:

   ```bash
   git checkout -b feature/my-new-tool
   ```

4. **Write your script** and make sure it:
   - Runs with `python script.py --help` producing useful output
   - Uses `argparse` (or `optparse`) for CLI argument handling
   - Includes a module-level docstring describing what it does
   - Is placed in the appropriate folder (`MyTools/`, `Example/`, etc.)

5. **Commit** with a descriptive message:

   ```bash
   git add MyTools/my_new_tool.py
   git commit -m "Add my_new_tool: brief description of what it does"
   ```

6. **Push** and open a **Pull Request** against `main`.

### Guidelines

- Keep scripts self-contained and dependency-light (standard library preferred)
- Do not commit real credentials, API keys, or personally identifiable information
- Scripts in `Exploit/` must include a comment at the top stating their intended lab/CTF target and that they are for authorized use only
- Match the existing code style (PEP 8, type hints where practical)

---

*Maintained by [7heKnight](https://github.com/7heKnight)*
