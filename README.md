![Secure Share](SecureShare/Project/static/images/logo2.png)

<div align="center">

# SecureShare - Decentralized Secure File Sharing

**SecureShare** is a decentralized, secure file-sharing platform focused on **end-to-end encryption** and **user privacy**.  
The system provides a simple and intuitive interface for securely uploading, downloading, and managing files without a central server.

[View Project](https://github.com/AfekAharoni/SecureShare)

</div>

---

## Project Overview

- **End-to-End Encryption** - Secure encryption for both data in transit and at rest.  
- **Decentralized Architecture** - No central servers; peer-to-peer data exchange.  
- **Secure Authentication** - Multi-step user authentication process.  
- **Clean and Responsive UI** - User-friendly interface using HTML/CSS/JS.  
- **Email Notifications** - Secure password reset and registration emails.

---

## How It Works

1. Users register and authenticate through a secure login system.  
2. Uploaded files are encrypted locally before transmission.  
3. Files are accessible only to authenticated users with proper credentials.  
4. Email notifications are sent for registration and password reset events.

---

## Technologies Used

- Python 3  
- Flask (Backend Framework)  
- HTML / CSS / JavaScript (Frontend)  
- SMTP (Email Notifications)

---

## File Structure

```
SecureShare/
├── Book/
│   └── Project Book (Documentation)
│
└── Project/
    ├── mail_templates/
    │   ├── new_password.html
    │   ├── password_mail.html
    │   └── register_mail.html
    │
    ├── static/
    │   ├── images/
    │   │   ├── ggh.jpg
    │   │   ├── logo2.png
    │   │   └── logo3.png
    │   ├── Page-1.css
    │   ├── Page-2.css
    │   ├── Page-3.css
    │   ├── Page-4.css
    │   ├── Page-5.css
    │   ├── Page-6.css
    │   ├── Page-7.css
    │   ├── counters.js
    │   ├── jquery.js
    │   ├── nicepage.css
    │   └── nicepage.js
    │
    ├── templates/
    │   ├── change_password.html
    │   ├── download.html
    │   ├── forgot_password.html
    │   ├── index.html
    │   ├── loading_error.html
    │   ├── login.html
    │   ├── logout.html
    │   ├── page_not_found.html
    │   ├── password_check.html
    │   ├── password_insert.html
    │   ├── register.html
    │   └── upload.html
    │
    ├── app.py
    ├── crypto.py
    ├── mail_sender.py
    ├── pass.key
    ├── requirements.txt
    ├── threaded_functions.py
    ├── tutorial.txt
    ├── user_authentication.py
    └── user_details.py
```

---

## Features

- User Registration & Authentication  
- Password Reset & Recovery via Email  
- File Upload & Download with Encryption  
- Responsive Web Interface  
- Error Handling & User Feedback  
- Multi-threaded File Handling for Performance

---

## Documentation

Project documentation and detailed explanations are available in the `/Book/Project Book` folder.

---

<div align="center">

© 2024 Afek Aharoni | [GitHub Profile](https://github.com/AfekAharoni)

</div>
