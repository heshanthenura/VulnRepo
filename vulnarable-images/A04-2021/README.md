# A04:2021 Rate Limiting Demo App Container

This Docker setup simulates a **login system with and without rate limiting** in Flask by:

- Running a lightweight Python 3.11 container
- Serving a Flask app with two login routes:

  - `/login-nolimit` → no rate limiting (insecure)
  - `/login-limit` → rate-limited login (secure design demonstration)

- Using **hardcoded credentials** (`admin/admin123`) for demonstration
- Showing how **rate limiting protects against brute-force attacks**

🧠 **Note:** This setup is for **educational purposes only**. Do not deploy in production.

---

## 🎯 Goal

- Demonstrate **insecure design**: unlimited login attempts allow brute force attacks
- Demonstrate **secure design**: rate limiting blocks excessive login attempts
- Teach the importance of **secure design principles** in web applications

## 🐳 Build

[Download](https://github.com/heshanthenura/VulnRepo/releases/download/vuln-img-005/A04-2021.zip) the project files:

```bash
docker build -t a04:2021 .
```

---

## 🚀 Run

Run the container and map port 5000:

```bash
docker run -d -p 5000:5000 --name rate-limit-demo a04:2021
```

Open the app in your browser: [http://localhost:5000](http://localhost:5000)

- `/login-nolimit` → Login **without rate limiting** (vulnerable to brute force)
- `/login-limit` → Login **with rate limiting** (demonstrates secure design)

Use `ffuf` or manual login attempts to see the **difference between insecure and secure design**.

---

## ⚠️ Warning

- This app is **intentionally designed for demonstration** of secure vs insecure design
- `/login-nolimit` is **vulnerable to brute-force attacks**
- `/login-limit` implements **basic rate limiting** using Flask-Limiter
- Only use this in a **controlled environment for educational purposes**

---

## 👨‍💻 Creator

This Dockerfile and Flask demo were created by **Heshan Thenura** for educational purposes and ethical hacking practice.

---

If you want, I can also **write the Dockerfile and folder structure README references** so you can release it like your previous container demo.

Do you want me to do that?
