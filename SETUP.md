# FityFeed — Complete Setup Guide

## Your Project Structure
```
FityFeed/
├── calorieCalc/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Fityfeed/
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── user.html
│   │   ├── main.html
│   │   ├── fooditem.html
│   │   ├── createfooditem.html
│   │   └── addUserFooditem.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── filters.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   └── main.css
├── manage.py
└── requirements.txt
```

## Step-by-Step Setup in VS Code

### Step 1 — Create the project folder
Open a NEW folder anywhere on your PC (e.g. D:\FityFeed)
Place ALL the files provided into that folder, matching the structure above.

### Step 2 — Open in VS Code
```
File → Open Folder → select D:\FityFeed
```

### Step 3 — Open Terminal
Press Ctrl + ` (backtick)

### Step 4 — Create virtual environment
```powershell
python -m venv venv
```

### Step 5 — Activate virtual environment
```powershell
venv\Scripts\activate
```
You will see (venv) in the terminal.

### Step 6 — Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 7 — Run migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 8 — Create superuser (admin account)
```powershell
python manage.py createsuperuser
```
Enter: username, email, password when asked.

### Step 9 — Run the server
```powershell
python manage.py runserver
```

### Step 10 — Set up groups in admin panel
Go to: http://127.0.0.1:8000/admin/
Login with your superuser credentials.

Go to: Authentication → Groups → Add Group
Create group named: admin
Create group named: user

### Step 11 — Add food categories
Go to: Fityfeed → Category → Add Category
Add these 4 categories one by one:
- breakfast
- lunch
- dinner
- snacks

### Step 12 — Assign your superuser to admin group
Go to: Authentication → Users → click your superuser
Scroll to Groups → add "admin" group → Save

### Step 13 — Test the app
| URL | Page |
|-----|------|
| http://127.0.0.1:8000/login/ | Login |
| http://127.0.0.1:8000/register/ | Register new user |
| http://127.0.0.1:8000/ | Admin dashboard |
| http://127.0.0.1:8000/user/ | User calorie tracker |
| http://127.0.0.1:8000/admin/ | Django admin |

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| No module named django_filters | pip install django-filter |
| TemplateDoesNotExist | Check templates folder is inside Fityfeed/ |
| venv not activating | Run PowerShell as admin, then: Set-ExecutionPolicy RemoteSigned |
| Category IndexError | Add all 4 categories in admin panel first |
| Port already in use | python manage.py runserver 8080 |
