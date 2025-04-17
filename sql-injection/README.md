# 🐍 SQL Injection Vulnerable Web App Container

This Docker setup simulates a simple web application vulnerable to SQL Injection attacks using Flask and SQLite.

It is designed for learning and demonstrating:

- How SQL injection vulnerabilities are introduced.
- How attackers can exploit them to dump usernames, modify data, or bypass authentication.

> 🧠 **Note:** This is a simplified vulnerable setup for educational use only. Real-world scenarios may differ significantly in complexity and security mechanisms.

# 🎯 Goal

Login as admin or existing user without knowing their original passwords.

## 🐳 Build

download image from release

https://github.com/heshanthenura/VulnRepo/releases/tag/vuln-img-002

change directory to that folder

```bash
docker build -t pawnshop-app .
```

## 🚀 Run

```bash
docker run -d -p 5000:5000 --name pawnshop-container pawnshop-app
```

🌐 Access the App

```bash
http://localhost:5000
```

## 👨‍💻 Creator

This Dockerfile was created by [Heshan Thenura](https://github.com/heshanthenura) for educational and ethical hacking practice purposes.
