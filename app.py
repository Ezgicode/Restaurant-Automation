#QR AL GARSON BLİGLERİYLE EŞLE
#KAMERAYI AÇ BİR KARE AL
#YOLO MODELİ İLE TAHMİN YAP
#TAHMİN EDİLEN YEMEĞİ MENU.JSONDAN FİYATLA EŞLE
#SONUCU HTMLDE GÖSTER
from flask import Flask
from flask import render_template
from flask import request
import cv2
from ultralytics import YOLO
from Restaurant_Automation import (restaurant_system, yemek_tanı, masa_hesap)
from Restaurant_Automation import rapor,puan_dusur, masa_rapor, garson_rapor
import json
import datetime
from datetime import datetime
from flask import session
from flask import redirect
# session için flask başına eklediğimiz kısım
app = Flask(__name__)
app.secret_key = "passwordçok_gizli_bişi"

@app.route('/', methods = ["GET","POST"])
def index():
    return render_template("index.html")


@app.route("/qr", methods=["GET","POST"])
def qr_page():
    if request.method == "POST":
        qr_kod = int(request.form["qr_kod"])
        garson_name , garson_masa = restaurant_system(qr_kod)
        qr_zamanı = datetime.now()
        session["masa_name"] =garson_masa
        session ["garson_name"] =garson_name
        session["qr_zamanı"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return render_template("masa.html",  garson_name = garson_name, garson_masa=garson_masa)
    return render_template("qr.html")


@app.route("/masa", methods =["GET","POST"])
def masa_page():
    if request.method == "POST":
        secilen_masa = request.form["masa_name"]
        session["secilen_masa"] =secilen_masa
        return redirect("/yemek")

    return render_template("yemek.html")

@app.route("/yemek", methods = ["GET","POST"])
def yemek_page():
    predicted_names,fiyatlar = yemek_tanı()
    garson_name = session.get("garson_name")
    secilen_masa = session.get("secilen_masa")
    qr_zamanı_str = session.get("qr_zamanı")
    masa_name = session.get("masa_name")
    qr_zamanı = datetime.strptime(qr_zamanı_str, "%Y-%m-%d %H:%M:%S")
    sure = datetime.now() - qr_zamanı

    # 10 saniyeyi geçtiyse veya yemek bulunamadıysa
    if sure.total_seconds() > 5 or predicted_names == ["YEMEK TESPİT EDEMEDİM"]:
        puan_dusur(garson_name)
        if predicted_names == ["YEMEK TESPİT EDEMEDİM"]:
            puan_dusur(garson_name)
            return render_template ("yemek.html", predicted_names = predicted_names, fiyatlar = fiyatlar)

        masa_hesap(predicted_names,fiyatlar,secilen_masa, garson_name,qr_zamanı_str)
        return render_template ("yemek.html", predicted_names = predicted_names, fiyatlar = fiyatlar)

@app.route("/rapor", methods = ["GET","POST"])
def rapor_page():
    raporlar= rapor()
    return render_template("rapor.html", raporlar= raporlar)

@app.route("/ozellesmisrapor", methods = ["GET","POST"])
def ozellesmisrapor_page():
    return render_template("ozellesmis.html")


@app.route("/masarapor", methods = ["GET","POST"])
def masarapor_page():
    masa_name= request.form.get("masa", "").strip()
#YENİ EKLEDİĞİM KISIM ÇOK ANLAMSIZ AMA SİLİNCE BOZULUYOR
    masaraporlar = []
    if masa_name:
        masaraporlar= masa_rapor(masa_name)

    return render_template("masarapor.html", masaraporlar= masaraporlar ,secilen_masa = masa_name)



@app.route("/garsonrapor", methods = ["GET","POST"])
def garsonrapor_page():
    if request.method == "POST":
        garson_name = request.form.get("garson", "").strip()
        garsonraporlar = garson_rapor(garson_name)
        return render_template("garsonrapor.html", garsonraporlar=garsonraporlar)

    return render_template("garsonrapor.html", garsonraporlar=[])

###@app.route("/garsonrapor", methods=["GET","POST"])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
