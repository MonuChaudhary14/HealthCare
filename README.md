# 🏥 Healthcare Backend API

A production-ready RESTful Backend Application built with **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **Docker**. The system manages patient and doctor records securely with JWT-based authentication and role-based data isolation.

🌐 **Live Deployment**: [https://healthcare.monu14.me/api](https://healthcare.monu14.me/api)

---

## 🚀 Features

- **🔐 JWT Authentication**: Secure user registration and login using `djangorestframework-simplejwt`.
- **👨‍⚕️ Doctor Management**: Full CRUD operations for doctor records with experience and specialization validations.
- **🧑‍🤝‍🧑 Patient Management**: Scoped patient management ensuring authenticated users only access and modify their own patient records.
- **🔗 Patient-Doctor Mapping**: Assign doctors to patients with duplicate-assignment prevention and data-privacy scoping.
- **🛡️ Enterprise Validations**:
  - Email case-normalization and uniqueness checks.
  - Strict 10-digit phone number sanitization.
  - Custom password strength validator enforcement.
  - User-level API rate limiting / throttling.
- **🐳 Containerized Deployment**: Dockerfile and multi-container Docker Compose with PostgreSQL health checks and Nginx reverse proxy.
- **⚡ Code Quality**: Automated linting and formatting configured with `ruff`.

---

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.x & Django REST Framework (DRF)
- **Database**: PostgreSQL 16
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Containerization**: Docker & Docker Compose
- **Web Server / Reverse Proxy**: Nginx with Let's Encrypt SSL
- **Linter & Formatter**: Ruff

---

## 📋 API Endpoints Reference

### 1. Authentication APIs
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/auth/register/` | Register a new user (`name`, `email`, `password`) | ❌ No |
| `POST` | `/api/auth/login/` | Authenticate user and receive JWT access/refresh tokens | ❌ No |
| `POST` | `/api/auth/token/refresh/` | Obtain a new access token using a refresh token | ❌ No |

### 2. Doctor Management APIs
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/doctors/` | Add a new doctor record | ✅ Yes |
| `GET` | `/api/doctors/` | Retrieve all registered doctors | ✅ Yes |
| `GET` | `/api/doctors/<id>/` | Retrieve details of a specific doctor | ✅ Yes |
| `PUT` | `/api/doctors/<id>/` | Update a doctor's details | ✅ Yes |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor record | ✅ Yes |

### 3. Patient Management APIs
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/patients/` | Register a new patient (auto-linked to user) | ✅ Yes |
| `GET` | `/api/patients/` | Retrieve all patients created by the authenticated user | ✅ Yes |
| `GET` | `/api/patients/<id>/` | Retrieve details of a specific patient | ✅ Yes |
| `PUT` | `/api/patients/<id>/` | Update a patient record | ✅ Yes |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record | ✅ Yes |

### 4. Patient-Doctor Mapping APIs
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/mappings/` | Assign a doctor to a patient | ✅ Yes |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings for the user | ✅ Yes |
| `GET` | `/api/mappings/<patient_id>/` | Retrieve all doctors assigned to a specific patient | ✅ Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor assignment record | ✅ Yes |

---