# Screenshot Guide for Project Report

This guide lists all screenshots needed for the 30-page report. Run the server and capture each page.

## Prerequisites
```bash
python manage.py runserver
# Open http://127.0.0.1:8000 in your browser
```

## Screenshots to Capture

### Section 4 — Authentication
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 4.1 | Sign Up | `/accounts/signup/` | Registration form with all fields | No |
| 4.2 | Login | `/accounts/login/` | Login form + "Login with Face" button | No |
| 4.3 | Password Reset | `/accounts/password-reset/` | Email input for reset | No |

### Section 5 — Products
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 5.1 | Product Listing | `/` | Product grid with categories sidebar | Any |
| 5.2 | Product Detail | Click any product | Full product detail page | Any |
| 5.3 | Shopping Cart | `/cart/` | Cart with items + order summary | Any |
| 5.4 | Wishlist | `/cart/wishlist/` | Wishlisted products grid | Yes |

### Section 6 — Payment
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 6.1 | Stripe Checkout | `/checkout/` (with cart items) | Checkout form + Stripe button | Yes |
| 6.2 | Transaction | After successful payment | Success page with order number | Yes |

### Section 8 — Biometrics
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 8.1 | Face Enrollment | `/biometric/enrollment/` | Camera view + enroll button | Yes |
| 8.2 | Liveness Detection | During capture | Scan line animation overlaying face | Yes |
| 8.3 | Enrollment Success | After capture | Success message + green indicator | Yes |
| 8.4 | Facial Login | `/biometric/facial-login/` | Camera view + authenticate button | No |
| 8.5 | Face Verification | `/biometric/verify/` | Verify identity page | Yes |

### Section 9 — Trust
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 9.1 | Trust Footer | Any page scroll to bottom | Footer with all policy links | Any |
| 9.2 | Trust Badges | Product detail / Profile | Stock badges, role badges, face status | Any |
| 9.3 | Notifications | Any page (click bell) | Notification dropdown | Yes |

### Section 10 — Security
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 10.1 | CSRF Token | View page source (Ctrl+U) | `csrfmiddlewaretoken` in form | Any |
| 10.2 | RBAC | `/dashboard/` as admin | Admin dashboard with restricted access | Admin |
| 10.3 | Activity Log | Django admin | Audit trail entries | Admin |

### Section 11 — TAM/UTAUT Survey
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 11.1 | Survey | `/survey/` | Survey form with Likert questions | Yes |

### Section 12 — Vendor
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 12.1 | Vendor Application | `/vendor/apply/` | Vendor registration form | Yes |
| 12.2 | Vendor Dashboard | `/vendor/` | Vendor stats + products | Vendor |
| 12.3 | Vendor Products | `/vendor/products/` | Product list with add/edit/delete | Vendor |
| 12.4 | Vendor Earnings | `/vendor/earnings/` | Earnings + withdrawal form | Vendor |
| 12.5 | Vendor Approvals | `/dashboard/vendors/` | Pending approvals table | Admin |

### Section 13 — Admin Dashboard
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 13.1 | Admin Dashboard | `/dashboard/` | Stats cards + recent orders | Admin |
| 13.2 | Model Manager | `/dashboard/` (sidebar) | 36+ models sidebar navigation | Admin |
| 13.3 | User Management | `/dashboard/users/` | Users table with roles | Admin |
| 13.4 | Employee Management | `/dashboard/employees/` | Employee profiles | Admin |

### Section 14 — Notifications & Support
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 14.1 | Notifications | Any page while logged in | Bell icon with dropdown | Yes |
| 14.2 | Support Ticket | `/admin/support/supportticket/` | Ticket list | Admin |

### Section 15 — CMS
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 15.1 | Site Settings | `/admin/cms/sitesettings/` | Site configuration form | Admin |

### Section 16 — UX
| # | Page | URL | What to Show | Logged In? |
|---|------|-----|--------------|------------|
| 16.1 | Homepage | `/` | Product grid with full layout | Any |
| 16.2 | Mobile View | DevTools mobile mode | Responsive layout | Any |

### Appendices
| # | Page | URL | What to Show |
|---|------|-----|--------------|
| A.1 | ER Diagram | — | Database schema visualization |
| B.1 | Routes | `python manage.py show_urls` | URL route list |

## Quick Capture Script

```python
# save_screenshots.py — Run this while server is running
import requests
import os

BASE_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

pages = {
    "4.1_signup": "/accounts/signup/",
    "4.2_login": "/accounts/login/",
    "5.1_products": "/",
    "5.3_cart": "/cart/",
    "9.1_footer": "/",
    "11.1_survey": "/survey/",
    "12.1_vendor_apply": "/vendor/apply/",
    "13.1_admin": "/dashboard/",
    "16.1_homepage": "/",
}

for name, path in pages.items():
    try:
        resp = requests.get(f"{BASE_URL}{path}")
        with open(f"{OUTPUT_DIR}/{name}.html", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {e}")
```

## Final Steps

1. Insert screenshots into the report at each `[Screenshot X.X: ... — Insert here]` marker
2. Convert `PROJECT_REPORT.md` to PDF using your preferred tool:
   - **VS Code:** Right-click → "Save as PDF" (with Markdown Preview Enhanced)
   - **Pandoc:** `pandoc PROJECT_REPORT.md -o PROJECT_REPORT.pdf --pdf-engine=weasyprint`
   - **Typora:** File → Export → PDF
   - **Online:** Copy-paste to https://md2pdf.netlify.app
