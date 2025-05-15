from flask import Flask,render_template,request,redirect 
import pymysql
from otp_validation import otp
from qr_utils import send_qr_email
import cv2
from pyzbar.pyzbar import decode

db_config = {
    "host":"localhost",
    "user":"root",
    "password":"DBpassword@1234",
    "database":"codegnan_Atm"
}

app= Flask(__name__)
@app.route("/")
def land():
    return render_template("index.html")

@app.route("/deposit")
def deposit():
    return render_template("deposit.html")

@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html")

@app.route("/pin")
def pin():
    return render_template("pin.html")

@app.route("/statement")
def statement():
    return render_template("statement.html")
@app.route("/account")
def account():
    return render_template("Account.html")

@app.route("/readdata",methods=["POST","GET"])
def readdata():
    accno=request.form["accno"]
    name=request.form["name"]
    age=request.form["age"]
    email=request.form["email"]
    gender=request.form["gender"]
    pin=request.form["pin"]
    amt=request.form["balance"]
    email=request.form["email"] 
    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "INSERT INTO BankAccounts VALUES (%s,%s,%s,%s,%s,%s,%s); "
    cursor.execute(query,(accno,name,age,gender,pin,amt,email))
    conn.commit()
    conn.close()
    return render_template("account.html",msg="Account Creation Successful")

# ------------------------WITHDRAW DATA -----------------
@app.route("/withdrawdata1",methods=["POST","GET"])
def withdrawdata1():
    #amt=request.form["amount"]
    try:
        global accno_withdraw
        accno_withdraw=request.form["accno"]
        conn=pymysql.connect(**db_config)
        cursor=conn.cursor()
        query = "SELECT email FROM BankAccounts where account_no = %s ;"
        cursor.execute(query,(accno_withdraw))
        data11=cursor.fetchone()
        print(data11)
        conn.close()
        global success
        success = send_qr_email(accno_withdraw)
        print(success)
        if success:
            return render_template('withdraw.html', msg=f"QR sent to your registered email! {data11[0]}")
        else:
            return render_template('withdraw.html', msg="Account not found!")
        #return render_template("withdraw.html",msg=f"QR CODE has been SENT to {data11[0]}")
    except:
        return render_template("withdraw.html",msg="PLEASE CHECK ACCOUNT NUMBER")

    """conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "SELECT balance FROM BankAccounts where account_no = %s and pin =%s ;"
    cursor.execute(query,(accno,pin))
    data=cursor.fetchone()
    print(data)
    conn.close()
    try:
        if float(amt)>float(data[0]) and len(data)<1:
            return render_template("/withdraw",msg="Insufficient Funds")
    except:
        return render_template("withdraw.html",msg="Account Not Exists")

    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "UPDATE BankAccounts SET BALANCE = BALANCE - %s where account_no = %s and pin = %s; "
    cursor.execute(query,(amt,accno,pin))
    conn.commit()
    conn.close()"""
@app.route('/scanqrwithdraw',methods=["POST","GET"])
def scan_qr():
    cap = cv2.VideoCapture(0)
    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "SELECT account_no FROM BankAccounts where account_no=%s  ;"
    cursor.execute(query,(accno_withdraw))
    data=cursor.fetchone()
    print(data)
    conn.close()
    global sc
    sc=False
    if int(accno_withdraw) not in data and success==False:
        
        return render_template('/withdraw.html', msg="Scan not possible")
    while True:
        ret, frame = cap.read()
        for code in decode(frame):
            account_no = code.data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            sc=True
            return  render_template('/withdraw.html', msg="Scan Successful")

        cv2.imshow('Scan Your QR', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render_template("withdraw.html",msg="Scan cancelled")
@app.route('/withdrawfinal',methods=["POST","GET"])
def withdrawdata():
    
    
    try:
        amt=request.form["amount"]
        conn=pymysql.connect(**db_config)
        cursor=conn.cursor()
        query = "SELECT account_no FROM BankAccounts where account_no=%s  ;"
        cursor.execute(query,(accno_withdraw))
        data=cursor.fetchone()
        print(data)
        conn.close()
        if sc==False:
            return render_template('/withdraw.html', msg="you bloody idiot without account no from where i can get you money")
        if int(accno_withdraw) not in data and sc==False :
            return render_template('/withdraw.html', msg="you bloody idiot without account no from where i can get you money")
         
    
        conn=pymysql.connect(**db_config)
        cursor=conn.cursor()
        query = "UPDATE BankAccounts SET BALANCE = BALANCE - %s where account_no = %s ; "
        cursor.execute(query,(amt,accno_withdraw))
        conn.commit()
        conn.close()
        return render_template('withdraw.html', msg="with draw successful")
        #return render_template("withdraw.html",msg=f"QR CODE has been SENT to {data11[0]}")
    except:
        return render_template("withdraw.html",msg="PLEASE CHECK ACCOUNT NUMBER")

#------------------------- DEPOSIT WINDOW -------------------------------
@app.route("/depositdata",methods=["POST","GET"])
def depositdata():
    accno=request.form["accno"]
    amt=request.form["amount"]
    #----------------Account existence checking--------------------------
    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "SELECT account_no  FROM BankAccounts where account_no=%s ;"
    cursor.execute(query,(accno))
    data=cursor.fetchone()
    print(data)
    conn.close()
    try:
        if data[0]==None:
            return render_template("deposit.html",msg="ACCOUNT NOT EXISTS")
    except:
        return render_template("deposit.html",msg="ACCOUNT NOT EXISTS")
    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "UPDATE BankAccounts SET BALANCE = BALANCE + %s where account_no = %s; "
    cursor.execute(query,(amt,accno))
    conn.commit()
    conn.close()
    return render_template("deposit.html",msg="Deposit Successful")

#---------------------------STATEMENT DATA-----------------------------------
@app.route("/statementdata",methods=["POST","GET"])
def getdata():
    accno=request.form["accno"]
    pin=request.form["pin"]
    conn=pymysql.connect(**db_config)
    cursor=conn.cursor()
    query = "SELECT * FROM BankAccounts where account_no = %s and pin =%s ;"
    cursor.execute(query,(accno,pin))
    data=cursor.fetchall()
    print(data)
    conn.close()
    return  render_template("/statement.html",MSG=data)


#---------------------------PIN CHANGE DATA-----------------------------------
@app.route("/pinaccnodata",methods=["POST","GET"])
def pindata():
    try:
        global accno_pin
        accno_pin=request.form["accno"]
        conn=pymysql.connect(**db_config)
        cursor=conn.cursor()
        query = "SELECT email FROM BankAccounts where account_no = %s ;"
        cursor.execute(query,(accno_pin))
        data11=cursor.fetchone()
        print(data11)
        conn.close()
        global otp_re
        otp_re=otp(data11[0])
        return render_template("pin.html",msg=f"OTP SENT to {data11[0]}")
    except:
        return render_template("pin.html",msg="PLEASE CHECK ACCOUNT NUMBER")

@app.route("/otpdata",methods=["POST","GET"])
def valid():
    try:
        global otppin
        otppin=request.form["otppin"]
        if otp_re!=otppin:
            return render_template("pin.html",msg="OTP INVALID")
        return render_template("pin.html",msg="OTP VALID")
    except:
        return render_template("pin.html",msg="PLEASE DON'T TRY TO BE OVER SMART")
@app.route("/pindata",methods=["POST","GET"])
def setpin():
    try:
        if otp_re==otppin:
            pin=request.form["pin"]
            cpin=request.form["cpin"]
            if cpin==pin:
                conn=pymysql.connect(**db_config)
                cursor=conn.cursor()
                try:
                    query = "UPDATE BankAccounts SET pin=%s where account_no = %s; "
                    cursor.execute(query,(pin,accno_pin))
                    conn.commit()
                    conn.close()
                except:
                    return render_template("pin.html",msg="ACCOUNT NUMBER IS INVALID")
                return render_template("pin.html",msg="PIN GENERATION SUCCESSFUL")   
            else:
                return render_template("pin.html",msg="PIN NOT MATCHED")  
        else:
            return render_template("pin.html",msg="OTP INVALID")
    
    except:
        return render_template("pin.html",msg="PLEASE DON'T TRY TO BE OVER SMART")
        



#------------------------------------- QR CODE AUTHENTICATION ------------------------------------------------------




app.run()