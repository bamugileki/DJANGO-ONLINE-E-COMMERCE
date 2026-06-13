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

- **Trusted Computing Platform (TCP)** — secure session management, trusted login validation, secure token handling, encrypted credential storage
- **Facial biometric authentication** — face_recognition (99.38% LFW accuracy) + YOLOv8 liveness detection replaces fingerprint for universal web compatibility
- **Payment API integration (Stripe Checkout)** — PCI SAQ A compliant, never touches card data
- **Trust Management Models (TAM/UTAUT)** — 19-question survey instrument across 8 constructs with automatic PU/PEOU/Trust scoring
- **Secure Software Development Practices** — CSRF, XSS prevention, SQL injection prevention (ORM), PBKDF2 hashing, role-based access control

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
- **Facial Biometric Authentication** — mandatory face enrollment on signup, face-verified payment authorization, facial login
- **Liveness Detection** — YOLOv8-based real/fake face classification preventing photo/video/mask spoofing
- **Printable Receipts** — print-friendly receipts with PDF save, accessible from order history and success page
- **Activity Logging** — comprehensive audit trail with IP tracking for all significant actions
- **Trust Indicators** — 14 visible trust indicators across the UI (HTTPS, face status, badges, policy links)
- **Policy Pages** — Privacy, Terms, Payment, Refund, Shipping, Vendor, Security, Admin Rights
- **TAM/UTAUT Surveys** — 19 Likert-scale questions across 8 constructs with automatic scoring

## Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (development), PostgreSQL-ready
- **Payment:** Stripe sandbox integration
- **Biometrics:** face_recognition (dlib ResNet-34, 128-dim encodings) + YOLOv8 liveness detection
- **HTTPS:** django-sslserver (self-signed cert for development)

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runsslserver  # HTTPS required for camera access
```

> **Note:** Use `runsslserver` (not `runserver`) because browser camera API (`getUserMedia()`) requires a secure origin (HTTPS or localhost).

### Environment Setup

1. Copy `.env.example` to `.env` and configure:
   - `STRIPE_SECRET_KEY` — from Stripe dashboard (test mode)
   - `STRIPE_PUBLISHABLE_KEY` — from Stripe dashboard (test mode)
   - `DJANGO_SECRET_KEY` — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG=True` for development

2. Download the YOLOv8 liveness model (`best.pt`) and place it at:
   ```
   biometric/Liveness_detection_models/best.pt
   ```
   (Optional — app works without it, liveness check defaults to pass)

### Seed Data

```bash
python manage.py seed_users
python manage.py seed_products
```

**Default admin:** `francispancras` / `Francis@2026!Secure`

**Test card:** `4242 4242 4242 4242` (any future expiry, any CVC)

## Facial Authentication Integration

Facial authentication replaces fingerprint biometrics for universal web compatibility — all modern devices have cameras, while fingerprint sensors are not universally available on desktops/laptops. The system stores non-reversible 128-dimensional face encodings (not raw images) to comply with data protection principles.

### Flow

1. User registers → auto-redirect to face enrollment page
2. Camera captures single frame via WebRTC (`getUserMedia()`)
3. Server extracts 128-dim face encoding (ResNet-34) and stores as base64+pickle
4. On login: facial login compares live encoding against all stored descriptors (1:N)
5. On checkout: face verification required before "Pay with Stripe" is enabled
6. `face_verified=True` permanently recorded on Order model for audit trail

### Anti-Attack Measures

- YOLOv8-based liveness detection (real vs. fake face classification)
- Anti-photo/video/mask spoofing (confidence threshold > 80%)
- Face matching threshold (Euclidean distance < 0.6)
- Non-reversible encoding storage only (no raw images ever persisted)
- Single-frame transmission (no video stream exposed to network)
- HTTPS required for camera access (enforced by all major browsers)

## Trust Management (TAM/UTAUT)

The system incorporates Technology Acceptance Model (TAM) and Unified Theory of Acceptance and Use of Technology (UTAUT) frameworks. A 19-question survey instrument at `/survey/` measures 8 constructs (Likert 1-5):

| Construct | Questions | Measures |
|-----------|-----------|----------|
| Perceived Usefulness (PU) | 3 | Task efficiency, shopping performance, overall usefulness |
| Perceived Ease of Use (PEOU) | 3 | Learnability, ease of use, interaction clarity |
| Performance Expectancy (PE) | 2 | Time savings, shopping productivity |
| Effort Expectancy (EE) | 2 | Effortlessness, navigation ease |
| Social Influence (SI) | 2 | Peer recommendation, peer usage |
| Facilitating Conditions (FC) | 2 | Resource availability, support availability |
| Trust (extended TAM) | 3 | System trust, payment trust, vendor trust |
| Behavioral Intention (BI) | 2 | Continued use, recommendation willingness |

Scores for PU, PEOU, and Trust are computed automatically on submission. Trust metrics are stored with timestamps for trend analysis.

## Documentation

- **[REPORT.html](./REPORT.html)** — Comprehensive academic report (17 sections, course assignment deliverable)
- **[COURSE_ASSIGNMENT_2_REPORT.md](./COURSE_ASSIGNMENT_2_REPORT.md)** — Full markdown version of the report
- **[ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md)** — Detailed setup guide with prerequisites, installation steps, and troubleshooting

## License

MIT
