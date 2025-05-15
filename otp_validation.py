#----------------------------Modules Required----------------------------------------
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#--------------------------OTP Creation----------------------------------------------
def otp(receiver):
    otp=str(random.randint(0,9))+chr(random.randint(65,97))+str(random.randint(0,9))+chr(random.randint(97,123))+chr(random.randint(91,96))
    msg = MIMEMultipart()

    text = f"OTP for Verification is {otp}"     #OTP message

    msg["From"] = "akhilmuthavarapu1@gmail.com" #sender email address
    msg["To"] = receiver      #Receiver  email address
    msg["Subject"] = "OTP For Validation"       #subject text
    msg.attach(MIMEText(text,"plain"))          #OTP Msg appended with type of plain text
    #-------------------------Server Execution------------------------------------------
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login("akhilmuthavarapu1@gmail.com","bbgu elqr qynh flib")
    server.send_message(msg)
    server.quit()
    return otp


    


#bbgu elqr qynh flib 

