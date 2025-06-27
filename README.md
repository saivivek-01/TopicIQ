# 🧠 TopicIQ — AI-Powered Personalized Learning Platform

> 🔐 Live at: [https://topiciq.begetter.me](https://topiciq.begetter.me)  
> 🐳 Deployed with Docker + Terraform + CI/CD (GitHub Actions)

---

## 📚 Overview

**TopicIQ** is an AI-powered educational platform that delivers personalized quizzes, real-time diagnostics, and topic-level insights for students — all integrated with Google Classroom.

Built using **Flask + IBM Granite (LLM) + Pinecone + Google OAuth** and deployed via **Docker + Terraform + GitHub Actions**, it showcases **cloud-native DevOps + AI engineering** practices.

---

## 🚀 Features

| 🔧 Feature                | 🔍 Description |
|--------------------------|----------------|
| 🧠 AI Quiz Generation     | Uses **IBM Granite 13B** to generate MCQs on-demand |
| 🧪 Diagnostic Assessment  | Tailored difficulty detection with adaptive feedback |
| 🧵 Personalized Learning  | Quiz level adjusts based on student performance |
| 📊 Educator Dashboard     | Real-time topic-wise performance analytics |
| 👨‍🏫 Google OAuth & Classroom | Secure login + course fetch with **Google APIs** |
| 🌐 CI/CD & Dockerized     | Full pipeline using **GitHub Actions + DockerHub + Terraform** |
| 🔐 HTTPS Enabled          | NGINX reverse proxy with SSL via **Let's Encrypt** |
| 🔁 Manual Rollback Support| Simple Bash script to redeploy latest build on server |

---

## 🛠️ Tech Stack

| Layer        | Tools |
|--------------|-------|
| 🧠 AI Engine  | IBM Watsonx (Granite 13B), Python |
| 🗄️ Backend    | Flask, Pinecone, Google APIs |
| 💅 Frontend   | HTML, Tailwind CSS, Jinja |
| ☁️ DevOps     | Docker, Terraform, NGINX, GitHub Actions |
| 🔐 Auth       | Google OAuth2.0, HTTPS (Certbot) |

---

## 🔁 CI/CD Workflow

| Step | Description |
|------|-------------|
| 🏗️ Docker Build | On push to `main`, Docker image is built & pushed to DockerHub |
| 🚀 SSH Deploy    | SSH into **DigitalOcean droplet** and redeploy container |
| 🧪 Secrets       | Managed using GitHub Secrets for secure automation |

> Manual Deployment: `bash ~/deploy_topiciq.sh`  
> Docker Image: [`begetter/topiciq:latest`](https://hub.docker.com/r/begetter/topiciq)

---

## 🌍 Live Demo

🧪 Try it here: **[https://topiciq.begetter.me](https://topiciq.begetter.me)**  
🧠 Use a Google Account (OAuth enabled)  
👨‍🏫 Explore Educator Dashboard  
📱 Mobile Responsive

---

## 📦 Local Setup

```bash
# Clone the repo
git clone https://github.com/saivivek-01/TopicIQ.git
cd TopicIQ

# Add your environment file
cp .env.example .env

# Build Docker image
docker build -t topiciq-app .

# Run locally
docker run -p 5000:5000 --env-file .env topiciq-app

👨‍💻 Author

Mallavalli Sai Vivek
🔗 https://www.linkedin.com/in/mallavallisaivivek | 🧠 Cloud & DevOps Enthusiast


⭐ Why This Project Matters

This project not only demonstrates:
	•	Practical cloud deployment
	•	Real-world CI/CD automation
	•	Secure OAuth + HTTPS setup
	•	AI/ML app integration with production workflows

…but also reflects readiness for DevOps, Cloud Engineer, or AI Engineer roles.


🙏 Acknowledgements
	•	IBM Granite / Watsonx
	•	Pinecone for vector DB
	•	Google Classroom & OAuth
	•	DigitalOcean Student Credits
