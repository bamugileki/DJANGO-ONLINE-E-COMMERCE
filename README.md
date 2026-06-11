# SmartTrade Africa limited

A secure, multi-role e-commerce platform designed to support online buying and selling through both web and mobile applications.

## Project Overview

SmartTrade Africa limited is a secure, multi-role e-commerce platform that consists of four main user roles: **Customer, Vendor, Manager, and Admin**, each with specific responsibilities and access levels within the platform.

The primary goal of the system is to address critical security and trust challenges commonly found in modern e-commerce environments. These challenges include:

- Fake customer accounts and identity impersonation
- Online payment fraud and transaction manipulation
- Unauthorized access to user accounts and system resources
- Identity theft and credential misuse
- Low customer confidence in online payment systems
- Data privacy and protection concerns

To overcome these issues, the system is designed with a strong focus on **security, trust, and user acceptance**, ensuring a safe and reliable digital shopping experience.

### Key Technologies

- **Trusted Computing Platform (TCP)** — secure system execution, trusted sessions, and secure authentication mechanisms
- **Fingerprint and facial biometric authentication** — strengthens user identity verification and prevents unauthorized access
- **Payment API integration (sandbox environment)** — simulates secure and verifiable online transactions
- **Trust Management Models (TAM/UTAUT)** — improves user adoption, perceived usefulness, and ease of use
- **Secure Software Development Practices** — encryption, input validation, role-based access control, and secure API communication

## Roles

| Role | Capabilities |
|------|-------------|
| Admin | Full CRUD over all users, products, orders, settings, system modules |
| Manager | Operations management, employee and vendor oversight |
| Vendor | Store management, product CRUD, order processing, earnings |
| Customer | Browse products, place orders, manage wishlist, track orders |

## Features

- **Multi-factor Authentication** — password + optional biometric (facial) verification
- **Role-Based Access Control** — granular permissions per role
- **Admin Dashboard** — full CRUD on all 36+ models with sidebar navigation
- **Vendor Portal** — product management, orders, earnings, withdrawal requests
- **Shopping Cart & Wishlist** — full cart management with session persistence
- **Order Tracking** — status flow: Pending → Processing → Shipped → Delivered → Cancelled
- **Product Reviews & Ratings** — customer feedback system
- **Notification System** — in-app notifications for orders, payments, delivery
- **Policy Pages** — Privacy, Terms, Payment, Refund, Shipping, Vendor, Security, Admin Rights
- **TAM/UTAUT Surveys** — trust and technology acceptance data collection

## Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (development), PostgreSQL-ready
- **Payment:** Stripe sandbox integration
- **Biometrics:** face-api.js (TensorFlow.js-based face recognition)

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Seed Data

```bash
python manage.py seed_users
python manage.py seed_products
```

**Default admin:** `francispancras` / `Francis@2026!Secure`

## Facial Authentication Integration

Facial authentication is used as a biometric mechanism to enhance security by verifying user identity based on facial features. The system stores encrypted facial embeddings rather than raw images to comply with data protection principles.

### Flow

1. User registers and optionally enrolls face
2. Face data is converted into a numeric descriptor (face embedding)
3. Stored encrypted in the database
4. On login or sensitive action (payment), user verifies via camera
5. System compares live face with stored template and grants/denies access

### Anti-Attack Measures

- Liveness detection (blink detection / head movement)
- Anti-photo spoofing
- Face matching threshold (85% similarity)
- Encrypted storage of embeddings only (no raw images)

## Trust Management (TAM/UTAUT)

The system incorporates Technology Acceptance Model (TAM) and Unified Theory of Acceptance and Use of Technology (UTAUT) frameworks to measure:

- Perceived Usefulness
- Perceived Ease of Use
- Performance Expectancy
- Effort Expectancy
- Social Influence
- Facilitating Conditions
- Trust in System
- Trust in Vendor
- Trust in Payment

## License

MIT
