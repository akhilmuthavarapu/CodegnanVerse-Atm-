# CodegnanVerse-Atm-


---

# 💳 ATM Simulation Web Application with QR & OTP Authentication

This project is a full-stack **ATM Simulation Web Application** built using **Flask**, **MySQL**, and **Python libraries** like `OpenCV`, `Pyzbar`, and `smtplib`. It mimics the functionality of a real ATM system and introduces **secure authentication via QR codes and OTPs** for critical actions like withdrawals and PIN changes.

---

## 🧰 Features

* 🔐 **Account Creation** – Register with basic details (name, email, age, gender, etc.)
* 💰 **Deposit/Withdrawal** – Securely manage your account balance
* 📷 **QR Code Authentication** – Email-based QR code verification for withdrawals
* 🔑 **OTP Verification** – Email-based OTP authentication for secure PIN reset
* 🧾 **Mini Statement** – View account details and balance
* 🔁 **PIN Update** – Update PIN with OTP verification

---

## 🛠️ Tech Stack

| Component     | Technology       |
| ------------- | ---------------- |
| Backend       | Flask (Python)   |
| Database      | MySQL            |
| Email Service | SMTP (`smtplib`) |
| QR Scan       | OpenCV + Pyzbar  |
| Frontend      | HTML, CSS        |

---

## 📂 Folder Structure

```
.
├── static/
├── templates/
│   ├── index.html
│   ├── account.html
│   ├── deposit.html
│   ├── withdraw.html
│   ├── pin.html
│   └── statement.html
├── otp_validation.py
├── qr_utils.py
├── app.py
└── README.md
```

---

## 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/atm-flask-app.git
   cd atm-flask-app
   ```

2. **Install Dependencies**

   ```bash
   pip install flask pymysql opencv-python pyzbar
   ```

3. **Configure MySQL Database**

   Create a MySQL database:

   ```sql
   CREATE DATABASE codegnan_Atm;
   ```

   Create the required table:

   ```sql
   CREATE TABLE BankAccounts (
       account_no BIGINT PRIMARY KEY,
       name VARCHAR(255),
       age INT,
       gender VARCHAR(20),
       pin VARCHAR(10),
       balance FLOAT,
       email VARCHAR(255)
   );
   ```

4. **Update DB Credentials**

   In `app.py`, update the `db_config` with your local MySQL credentials:

   ```python
   db_config = {
       "host": "localhost",
       "user": "your_mysql_user",
       "password": "your_mysql_password",
       "database": "codegnan_Atm"
   }
   ```

5. **Run the App**

   ```bash
   python app.py
   ```

6. Open browser and navigate to:

   ```
   http://127.0.0.1:5000/
   ```

---

## 📸 Key Functionalities

### ✅ Account Registration

Form to enter account number, name, age, gender, email, and PIN.

### 💵 Deposit

Input account number and amount, and the balance is updated.

### 📤 Withdrawal

* Enter account number
* QR code is sent to registered email
* Scan the QR using webcam
* Withdraw amount after successful scan

### 🔄 PIN Reset

* Enter account number
* Receive OTP via email
* Verify OTP
* Set new PIN

### 📋 Mini Statement

View account details using account number and PIN.

---

## ⚠️ Notes

* Email sending via `send_qr_email()` and `otp()` should be implemented using SMTP (e.g., Gmail) in `qr_utils.py` and `otp_validation.py`.
* Webcam access is required for QR scanning (`cv2.VideoCapture(0)`).
* This is a simulation project; sensitive operations like money transfers are mocked.

---

## 📬 Contact

If you have any questions, feel free to connect with me on [LinkedIn]([(https://www.linkedin.com/in/venkata-akhil-muthavarapu-12042424a/)]).

---

## 🏷️ License

This project is for educational purposes only. Not intended for production use.

