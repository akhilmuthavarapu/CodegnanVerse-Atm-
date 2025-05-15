import qrcode
import smtplib
import pymysql
from email.message import EmailMessage
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "DBpassword@1234",
    "database": "codegnan_Atm"
}


def generate_qr(account_no):
    qr = qrcode.make(account_no)
    qr.save(f"{account_no}.png")
    return f"{account_no}.png"

def send_qr_email(account_no):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM BankAccounts WHERE account_no=%s", (account_no,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False

    receiver_email = user[0]
    qr_path = generate_qr(account_no)

    msg = EmailMessage()
    msg["Subject"] = "Your ATM Login QR Code"
    msg["From"] = "akhilmuthavarapu1@gmail.com"
    msg["To"] = receiver_email
    msg.set_content("Please scan this QR code at the ATM interface to login securely.")

    with open(qr_path, "rb") as f:
        qr_data = f.read()
        msg.add_attachment(qr_data, maintype="image", subtype="png", filename="qrcode.png")

    # Use your Gmail App Password here (not account password!)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('akhilmuthavarapu1@gmail.com', 'bbgu elqr qynh flib')
        smtp.send_message(msg)

    return True
