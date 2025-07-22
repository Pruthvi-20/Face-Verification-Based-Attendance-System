# 📸 Face Verification Based Attendance System

A smart attendance system using face recognition technology built with Django. The system captures real-time face data through a webcam, verifies the identity of a student, and records their attendance securely in the database. The platform offers both admin and student views.

---

## 🧱 Tech Stack

| Component  | Technology              |
|------------|--------------------------|
| Backend    | Django (Python)          |
| Frontend   | HTML, CSS                |
| Face Recognition | OpenCV, face_recognition |
| Database   | SQLite (default Django DB) |

---

## 🌟 Features

- 🔐 Admin Login Panel  
- 🎓 Student Enrollment with Photo  
- 📸 Real-Time Face Verification via Webcam  
- 📅 Attendance Logging with Timestamps  
- 🗂 Attendance History (view/download)  
- 🖥 Clean Web UI using HTML/CSS  

---
## 📁 Folder Structure

Face_Verification_based_Attendance_system/
├── attendance_app/ # Django app
│ ├── views.py
│ ├── models.py
│ ├── urls.py
│ ├── templates/
│ │ ├── index.html
│ │ ├── attendance.html
│ └── static/
│ └── css/
│ └── style.css
├── face_recognition/ # Face recognition scripts
├── media/ # Uploaded student images
├── db.sqlite3
├── manage.py
└── README.md


---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Face_Verification_based_Attendance_system.git
cd Face_Verification_based_Attendance_system

2️⃣ Create Virtual Environment (Optional but recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
3️⃣ Install Requirements
bash
Copy code
pip install -r requirements.txt
4️⃣ Run Database Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
5️⃣ Run Server
bash
Copy code
python manage.py runserver
Visit: http://127.0.0.1:8000

🧪 Key Functional Modules
🎓 Student Registration
Admin adds student with name, ID, and image

Face encoding saved for future verification

🕵️‍♂️ Face Verification
Live webcam feed checks face in real-time

Matches against registered encodings

On success, logs date & time in attendance table

📊 Attendance Reporting
View attendance list by student/date

requirements.txt:

txt
Copy code
Django>=4.0
opencv-python
face_recognition
dlib
numpy
