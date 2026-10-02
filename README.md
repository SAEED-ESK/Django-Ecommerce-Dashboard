# Django Shop

A full-featured e-commerce web application built with Django, designed with a modular architecture and separate dashboards for administrators and customers.

The project includes product management, shopping cart, checkout, coupon system, order management, payment integration, reviews, wishlist, authentication, and a comprehensive dashboard system.

---
## 🎥 Demo

The following demo shows the main storefront features as well as the customer and administrator dashboards.

![Django Shop Demo](docs/demo.gif)

## ✨ Features

### 🛍️ Store

- Product listing and detail pages
- Product categories
- Product search
- Price filtering
- Product sorting
- Product discounts
- Stock management
- Additional product images
- Rich-text product descriptions
- Similar and latest products

### 🛒 Shopping Cart

- Session-based shopping cart
- Add, update and remove products
- Automatic price calculation
- Product discount calculation
- Cart persistence for authenticated users
- Synchronization between session and database carts

### 👤 Authentication & Accounts

- Custom user model
- Email-based authentication
- User roles and permissions
- Customer and administrator accounts
- User profiles
- Phone number validation
- Password reset functionality

### 📦 Orders

- Checkout system
- Multiple customer addresses
- Order creation and management
- Order status tracking
- Order history
- Order details
- Coupon support

### 🎟️ Coupons

- Percentage-based discounts
- Expiration dates
- Maximum usage limits
- Per-user coupon usage tracking
- Coupon validation during checkout

### 💳 Payment

- ZarinPal payment gateway integration
- Payment request and verification
- Payment status management
- Authority and reference ID handling
- Payment response storage
- Sandbox payment environment

### ⭐ Reviews & Ratings

- Product reviews
- 1–5 star ratings
- Review moderation
- Pending, accepted and rejected review states
- Automatic average rating calculation
- Rating distribution

### ❤️ Wishlist

- Add products to wishlist
- Remove products from wishlist
- User-specific wishlist

---

## 📊 Dashboard System

One of the major parts of this project is its custom dashboard system.

Instead of relying only on Django Admin, the project includes separate interfaces for **administrators and customers**, with role-based access control.

### 🔐 Admin Dashboard

The admin dashboard provides management tools for different parts of the store, including:

- Product management
- Category management
- Order management
- Customer management
- User profiles
- Coupon management
- Review management
- General store management

### 👤 Customer Dashboard

Customers have their own dashboard for managing their account and shopping activity:

- Profile management
- Address management
- Order history
- Order details
- Wishlist
- Account information

The dashboard system was one of the first major sections developed in this project and was designed as a dedicated application-level management interface.

---

### Demo Highlights

- Store homepage
- Product browsing
- Product details
- Shopping cart
- Checkout flow
- Customer dashboard
- Order history
- Wishlist
- Admin dashboard
- Product management
- Order management
- Coupon and review management

---

## 🏗️ Project Structure

```text
core/
├── accounts/
├── cart/
├── dashboard/
│   ├── admin/
│   │   ├── forms/
│   │   ├── urls/
│   │   └── views/
│   └── customer/
│       ├── forms/
│       ├── urls/
│       └── views/
├── order/
├── payment/
├── review/
├── shop/
├── static/
├── templates/
└── website/
```

The project is divided into independent Django applications, keeping authentication, shopping, orders, payments, reviews and dashboard functionality separated.

---

## 🛠️ Tech Stack

- Python
- Django
- PostgreSQL
- Docker
- Redis
- Celery
- Django Templates
- HTML / CSS / JavaScript
- CKEditor
- ZarinPal API
- Git & GitHub

---

## 🐳 Running with Docker

Clone the repository:

```bash
git clone https://github.com/SAEED-ESK/django-shop.git
cd django-shop
```

Build and run the containers:

```bash
docker compose up --build
```

Run migrations:

```bash
docker compose exec backend python manage.py migrate
```

Create a superuser:

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## ⚙️ Environment Variables

Create a `.env` file and configure the required environment variables.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_URL=your-database-url

MERCHANT_ID=your-zarinpal-merchant-id
```

---

## 🧪 Testing

The project includes tests for different parts of the application.

Run the test suite with:

```bash
python manage.py test
```

---

## 📚 What I Practiced

This project gave me practical experience with:

- Building a complete Django e-commerce application
- Custom user models and authentication
- Role-based permissions
- Class-Based Views
- Django Forms
- Session and database-based shopping carts
- Order and checkout workflows
- Coupon systems
- Payment gateway integration
- Product reviews and ratings
- Wishlist functionality
- Custom admin and customer dashboards
- Dockerized Django development
- Working with third-party APIs
- Structuring a multi-app Django project

---

## 📌 Project Status

The project is completed as a portfolio project and demonstrates a complete e-commerce workflow from product browsing to cart, checkout, payment and order management.

The project was also an important step in practicing larger Django application architecture and building custom dashboard interfaces.

---

## 👨‍💻 Author

**Saeed Eskandary**

Python / Django Developer

GitHub:  
https://github.com/SAEED-ESK
