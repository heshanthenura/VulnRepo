# A1:2025 Vulnerable Demo App Container

This Docker setup simulates a **SQL Injection and Stored XSS vulnerable web app** in Flask by:

- Running a lightweight Python 3.11 container
- Serving a Flask app with an SQLite database for login (`/sqli`)
- Providing a comment/review system vulnerable to stored XSS (`/xss`)
- Using **unsafe query construction** and **no input sanitization**

🧠 **Note:** This setup is intentionally insecure for educational purposes only. Do not deploy in production.

## 🎯 Goal

- Demonstrate **SQL Injection**: bypass login by manipulating input
- Demonstrate **Stored XSS**: inject malicious JavaScript into comments
- Teach how input validation and sanitization are critical in web apps

This directly maps to **OWASP Web Application Security Risks** such as **Injection** and **Cross-Site Scripting (XSS)**.

## 🐳 Build

[Download](https://github.com/heshanthenura/VulnRepo/releases/download/vuln-img-004/A03-2021.zip) the project files:

```bash
docker build -t a03:2021 .
```

## 🚀 Run

Run the container and map port 5000:

```bash
docker run -d -p 5000:5000 --name vuln-demo-app a03:2021
```

Open the app in your browser: [http://localhost:5000](http://localhost:5000)

- `/sqli` → SQL Injection login demo
- `/xss` → Stored XSS comment system demo

## ⚠️ Warning

- This app is **intentionally insecure** for learning and testing purposes only.
- SQL queries are constructed with **unsanitized user input** → SQL Injection possible.
- User input in comments is **not sanitized** → Stored XSS possible.
- Exploiting this app outside a controlled environment is **illegal**.

## 👨‍💻 Creator

This Dockerfile and Flask demo were created by **Heshan Thenura** for educational and ethical hacking practice purposes.
