# A1:2021 Broken Access Vulnerability Container

This Docker setup simulates a **Broken Access Control / IDOR vulnerability** in a simple Flask web app by:

- Running a lightweight Python 3.10 container
- Serving a Flask app with multiple user profiles stored in a JSON file
- Using **weak authentication** (plain-text passwords in JSON)
- Allowing **Insecure Direct Object Reference (IDOR)** where users can access other users’ profiles by changing the URL

🧠 **Note:** This setup is intentionally insecure for educational purposes only. Do not deploy in production.

---

## 🎯 Goal

- Demonstrate **Broken Authentication**: weak passwords, no session security
- Demonstrate **Broken Access Control / IDOR**: users can access profiles of other users by changing the URL

This directly maps to **[A1:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)** in the OWASP Top 10.

---

## 🐳 Build

[Download](https://github.com/heshanthenura/VulnRepo/releases/download/vuln-img-003/A01-2021.zip) the project files:

Then build the Docker image:

```bash
docker build -t a01:2021 .
```

## 🚀 Run

Run the container and map port 5000:

```bash
docker run -d -p 5000:5000 --name broken-access-app a01:2021
```

Open the app in your browser: [http://localhost:5000](http://localhost:5000)

---

## ⚠️ Warning

- This app is **intentionally insecure** for learning and testing purposes.
- Passwords are stored in plain text.
- No session validation for profile access.
- Exploiting this app outside a controlled environment is **illegal**.

---

## 👨‍💻 Creator

This Dockerfile and Flask demo were created by **Heshan Thenura** for educational and ethical hacking practice purposes.
