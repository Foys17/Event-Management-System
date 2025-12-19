# 📅 EventMaster - Event Management System

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django Version](https://img.shields.io/badge/django-5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

> A modern, role-based platform connecting Event Organizers, Clients, Participants, and Sponsors in a seamless digital ecosystem.

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
- [Database Setup (MySQL)](#-database-setup-mysql)
- [Usage Guide](#-usage-guide)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 💡 About the Project

**EventMaster** is a full-stack web application designed to streamline the complex process of event planning. It replaces disjointed spreadsheets and emails with a centralized dashboard for all stakeholders. 

Whether you are a **Client** requesting a birthday bash, an **Organizer** managing budgets and logistics, a **Participant** buying tickets, or a **Sponsor** looking for brand visibility, EventMaster handles it all.

---

## 🚀 Live Demo
Check out the live application here: [https://Foys17.pythonanywhere.com](https://Foys17.pythonanywhere.com)

---

## 🌟 Key Features

### 🛠 For Organizers
- **Dashboard:** Real-time overview of active events and pending requests.
- **Request Management:** Accept or reject client requests with detailed requirements views.
- **Event Creation:** Launch events manually or convert client requests into active events.
- **Budget Tracking:** Monitor event budgets and financial status.

### 👤 For Clients
- **Custom Requests:** Submit detailed event proposals (Budget, Type, Requirements).
- **Status Tracking:** Real-time updates on whether requests are Pending, Accepted, or Rejected.

### 🎫 For Participants
- **Event Discovery:** Browse upcoming public events.
- **One-Click Registration:** Join events instantly.
- **Digital Tickets:** Auto-generated **QR Codes** for event entry.
- **Ticket Wallet:** specialized dashboard to view and manage active tickets.

### 💰 For Sponsors
- **Opportunity Hub:** View active events seeking sponsorship.
- **Asset Management:** Upload logos and branding materials directly.
- **Portfolio:** Track contributions and history.

---

## 🛠 Tech Stack

**Backend**
* **Framework:** Django 5 (Python)
* **Database:** MySQL
* **Authentication:** Django Auth (Custom Role-Based Access Control)
* **Utilities:** `qrcode` (Ticket generation), `Pillow` (Image processing)

**Frontend**
* **Templating:** Django Template Language (DTL)
* **Styling:** Tailwind CSS (via CDN) & FontAwesome 6
* **Design:** Responsive Grid Layouts, Modern Card UI, Glassmorphism effects

---

## 📂 Project Architecture

Event_Management_System/ 
├── core/ # Main App Directory │ 
├── migrations/ # Database Migrations │ 
├── static/ # CSS, JS, Images │ 
├── templates/ # HTML Templates │ │ 
├── core/ # Dashboard & Feature Templates │ │ └── registration/ # Auth Templates │ 
├── models.py # Database Schema │ 
├── views.py # Business Logic │ 
└── forms.py # Form Validations 
├── media/ # User Uploads (QR Codes, Logos) ── event_management/ # Project Configuration 
├── templates/ # Base Templates 
├── manage.py # Django Command Utility 
└── requirements.txt # Python Dependencies


---

## 🚀 Getting Started

Follow these instructions to set up the project locally.

### Prerequisites
* Python 3.10 or higher
* MySQL Server installed and running
* Git

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/event-management-system.git](https://github.com/yourusername/event-management-system.git)
    cd event-management-system
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🗄 Database Setup (MySQL)

1.  **Create the Database**
    Log in to your MySQL shell or Workbench and run:
    ```sql
    CREATE DATABASE event_master_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

2.  **Configure `settings.py`**
    Open `event_management/settings.py` and update the `DATABASES` section:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'event_master_db',
            'USER': 'root',             # Your MySQL Username
            'PASSWORD': 'your_password', # Your MySQL Password
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

3.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000` in your browser.

---

## 📖 Usage Guide

### 1. User Roles
The system uses a unified login but redirects based on role:
* **Organizer:** Access via `/organizer/dashboard/`
* **Client:** Access via `/client/dashboard/`
* **Participant:** Access via `/participant/dashboard/`
* **Sponsor:** Access via `/sponsor/dashboard/`

### 2. Workflow Example
1.  **Client** logs in and submits a "Birthday Party" request with a $5,000 budget.
2.  **Organizer** views the request on their dashboard, clicks "View Details," and **Accepts** it.
3.  **Organizer** fills in the event details (Location, Date) to publish it.
4.  **Sponsor** sees the new event and contributes $1,000, uploading their logo.
5.  **Participant** sees the event on their dashboard, joins, and receives a **QR Code**.

---


## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📞 Contact

**Foysal** - (mhfoysal17@gmail.com)

Project Link: [https://github.com/foys17/event-management-system](https://github.com/foys17/event-management-system)

---

<p align="center">
  Built with ❤️ using Django and Tailwind CSS
</p>