# E-commerce Platform (Django, AWS, PayPal)

A full-featured e-commerce web application built using **Django**, integrated with **PayPal** for payments and deployed on **AWS** for scalability. This platform allows users to browse products, manage carts, and securely checkout using PayPal, with an admin backend for store management.

---

## ✨ Features

- 🔐 User registration, login, logout, and profile updates  
- 🛍️ Product browsing, filtering, and individual product pages  
- 🛒 Cart management with quantity editing and removal  
- 💳 Checkout and payment using PayPal REST API  
- 📦 Order tracking, admin product management, and order fulfillment  
- ☁️ Deployed using AWS: Elastic Beanstalk, S3, and optionally RDS

---

## 🛠 Tech Stack

- **Backend:** Django, Python 3  
- **Frontend:** HTML, CSS, Bootstrap (via Django templates)  
- **Database:** SQLite (development), PostgreSQL/RDS (production)  
- **Payment Gateway:** PayPal (REST API)  
- **Cloud Hosting:** AWS Elastic Beanstalk, S3 (media), optional RDS  

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/<SANK-0311>/<E-commerce-Platform-Django-AWS-PayPal>.git
cd <E-commerce-Platform-Django-AWS-PayPal>

# Setup virtual environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver