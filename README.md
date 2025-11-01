# 🍽️ Trupti - Community Food Waste Management

A web platform connecting food donors with recipients to reduce waste and feed communities. Built with Django and Bootstrap 5.

---

## ✨ Key Features

- **Dual User Roles:** Seamless experience for food donors and recipients with separate dashboards. 👥
- **Smart Search:** Find food donations by location or food type with intelligent matching. 🔍
- **Request Management:** Easy request/approval workflow for food donations. ✅
- **Real-time Updates:** Track donation status and requests in real-time. ⚡
- **Responsive Design:** Works perfectly on desktop and mobile devices. 📱💻

---

## ⚙️ Setup Guide (Windows)

### Before You Start
- **Install Python** version 3.11 or newer from [python.org](https://www.python.org/downloads/).
- During install, make sure to check **"Add Python to PATH"**.
- **Clone the repository** or download the ZIP file.

### Step 1. Open PowerShell in the Project Folder
```powershell
# Navigate to your project directory
Set-Location "C:\path\to\Community-Food-Waste-Management-System"
```

### Step 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate it (you'll see (.venv) in the prompt)
.\.venv\Scripts\Activate
```

### Step 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4. Set Up Database
```powershell
# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### Step 5. Run the Development Server
```powershell
python manage.py runserver
```
- Visit `http://127.0.0.1:8000/` in your browser.
- Use the admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials.

### Step 6. Stop the Server
- Press **Ctrl + C** in the terminal.
- Deactivate the virtual environment when done:
  ```powershell
  deactivate
  ```

---

## 📸 Screenshots

### 🏠 Landing & Auth
- **Splash Screen**  
  ![Splash](screenshots/splash.png)

- **Home Page**  
  ![Home](screenshots/home.png)

- **About Page**  
  ![About](screenshots/about.png)

### 🔑 Authentication
- **Registration**  
  ![Register](screenshots/register.png)

- **Login**  
  ![Login](screenshots/login.png)

### 👨‍🍳 Donor Views
- **Donor Dashboard**  
  ![Donor Dashboard](screenshots/ddashboard.png)

- **My Donations**  
  ![My Donations](screenshots/ddonations.png)

- **Create Donation**  
  ![Create Donation](screenshots/create.png)

### 👥 Receiver Views
- **Receiver Dashboard**  
  ![Receiver Dashboard](screenshots/rdashboard.png)

- **Browse Donations**  
  ![Browse Donations](screenshots/rdonations.png)

- **Receiver Profile**  
  ![Receiver Profile](screenshots/rprofile.png)

### ℹ️ Additional
- **Contact Page**  
  ![Contact](screenshots/contact.png)

- **Donor Profile**  
  ![Donor Profile](screenshots/dprofile.png)

