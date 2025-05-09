# Report Lab - Python

This repository contains the source code for Report Lab - Python

## 📦 Setup Instructions

Follow the steps below to set up and run the project in your local environment.

---

### 🐍 1. Install Python

Ensure you have **Python 3.7+** installed.

- **macOS/Linux:**  
  Python is often available as `python3`  
  Check with:
  ```bash
  python3 --version
  ```

- **Windows:**  
  Python is usually installed as `python`  
  Check with:
  ```cmd
  python --version
  ```

If Python is not installed, download it from: https://www.python.org/downloads/

---

### 🏗️ 2. Create a Virtual Environment

#### macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

If you're using `python3` on Windows (e.g., `python3.11`), use:

```cmd
python3 -m venv venv
venv\Scripts\activate
```

---

### 📥 3. Install Dependencies

Once the environment is activated, run:

```bash
pip install -r requirements.txt
```

---

### 🚀 4. Run the Project

Use the appropriate command based on your system:

Sample json files are placed in the data directory
```bash
python main.py /path/to/sample.json
# or
python3 main.py /path/to/sample.json
```

---

## 🧼 Deactivate Environment

When done working:

```bash
deactivate
```

---

## 📝 Notes

- The `venv/` folder is excluded from version control (`.gitignore`).
- All dependencies are listed in `requirements.txt`.
- If you install new packages, run:
  ```bash
  pip freeze > requirements.txt
  ```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make your changes and commit:
   ```bash
   git commit -am "Add your feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request
