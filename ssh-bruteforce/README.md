# SSH Brute Force Vulnerability Container

This Docker setup simulates a basic SSH brute force vulnerability by:

- Running an Ubuntu 20.04 container
- Enabling root SSH access
- Using a weak root password
- Exposing port `22` for external SSH attempts

> 🧠 **Note:** This is a simplified vulnerable setup for educational use only. Real-world scenarios may differ significantly in complexity and security mechanisms.

## 🎯 Goal

Bruteforce and find the root SSH password using tools or custom scripts.

## 🐳 Build

download image from release

https://github.com/user-attachments/files/19765239/ssh-bruteforce.zip

change directory to that folder

```bash
docker build -t vuln-ssh-brute .
```

## 🚀 Run

```bash
docker run -d -p 2222:22 --name vuln-ssh-container vuln-ssh-brute
```

## 🔐 Connect

```bash
ssh root@localhost -p 2222
```

## 👨‍💻 Creator

This Dockerfile was created by [Heshan Thenura](https://github.com/heshanthenura) for educational and ethical hacking practice purposes.
