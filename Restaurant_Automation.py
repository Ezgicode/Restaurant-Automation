
#-------------------------------------------------------------------------------------------------
#4 masa 2 garson tanımla ilkine 1. garson diğerine 2. garson
#masadaki kamera yemekleri tanıyıp sınıflandırmalı

#model = YOLO("yolov8n.pt")
#model.train(
#    data=r"C:\Users\ezgii\OneDrive\Masaüstü\restaurant_otomation\yolo_dataset\data.yaml",
#   epochs=50,
#  imgsz=640 kötü eğitilmiş beni hamburger görüyor fiyat listesine erişmelii yememkten sonra o yemeğin fiyatı yazmalıdır)
#  result = model.predict(source = 0, show= True)
#---- ---------------------------------------------------------------------------------------------
import cv2
from ultralytics import YOLO
import json
import cv2
from ultralytics import YOLO
import datetime
from datetime import datetime
from flask import session

def restaurant_system(qr_input):


    with open("restaurant_config.json") as f:
        restaurant = json.load(f)
    print(restaurant)

    masalar = restaurant["masalar"]
    garsonlar= restaurant["garsonlar"]


    qr = qr_input
    for garson in garsonlar:
        if garson["qr_kod"] == qr:
            garson_id = garson["id"]
            garson_name = garson["name"]
            #print(garson["name"])
    garson_masa = []
    for masa in masalar:
        if masa["garson_id"] == garson_id:
            garson_masa.append(masa)
            secilen_masa = masa["name"]
            masa_name = masa["name"]

    return garson_name,garson_masa


def yemek_tanı():


    model = YOLO(r"C:\Users\ezgii\OneDrive\Masaüstü\restaurant_otomation\models\best.pt")
    #results = model("1.jpg", save= True)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    #cv2.imshow("Görüntü",frame)
    #cv2.waitKey(100)
    # cv2.destroyAllWindows()
    result= model(frame, save= True,conf= 0.3)
    img_with_boxes = result[0].plot()
    cv2.imwrite("static/tahmin.jpg", img_with_boxes)


    if result and result[0].boxes and result[0].boxes.cls.numel() > 0:
        predicted_names = []
        for cls_id in result[0].boxes.cls:
            cls_index= int(cls_id)
            predicted_names.append(result[0].names[cls_index])
            #print("Yemeğiniz", predicted_names)

        with open("menu.json","r") as f:
            menu = json.load(f)
            fiyatlar= []
            for name in predicted_names:
                fiyat= menu.get(name)
                fiyatlar.append(fiyat)
            #print(f"Siparişininz {predicted_names}, Fiyatı: {fiyat}")

        return predicted_names , fiyatlar
    else:
        return ["YEMEK TESPİT EDEMEDİM"], ["--"]

# python abstractions
def masa_hesap(predicted_names,fiyatlar,secilen_masa,garson_name, qr_zamanı_str):
    zaman = datetime.now().strftime("%d/%m/%Y %H:%M")
    if qr_zamanı_str:
        qr_zamanı = datetime.strptime(qr_zamanı_str,"%Y-%m-%d %H:%M:%S")
        fark = datetime.now() - qr_zamanı
        islem_süresi = str(fark)
    else:
        islem_süresi = "bilmiyom ya"

    with open("hesap.json","a", encoding="utf-8") as f:
        for  yemek , fiyat in zip (predicted_names,fiyatlar):
            f.write(f"zaman {zaman} Yemek {yemek} Fiyat {fiyat} TL {secilen_masa} {garson_name}  İşlem Süresi {islem_süresi}  \n ")



# genel tümden rapor
def rapor():
    raporlar = []
    print("İşte Raporunuz")
    with open("hesap.json","r", encoding="utf-8") as f:
        for satır in f:
            raporlar.append(satır.strip())
    return raporlar

# garson bazlı rapor
# masa bazlı rapor
#bu satır data adlı sözlük yapısını json formatında yazıyor
#json.dump json dosyasına yazma komutu indent 4 boşluk girintile demek

def puan_dusur(garson_name):
    with open("garson_puan.json","r",encoding="utf-8") as f:
        data_puan = json.load(f)
        for garson in data_puan["garsonlar"]:

            if garson["name"].strip()==garson_name.strip():
                garson["puan"]= garson["puan"]-10
                break
        with open("garson_puan.json","w",encoding="utf-8") as f:
            json.dump(data_puan,f, indent= 4,ensure_ascii= False)

def masa_rapor(masa_name):
    masaraporlar= []
    with open("hesap.json","r", encoding="utf-8")as f:
        for satır in f:
            if masa_name.lower() in satır.lower():
                masaraporlar.append(satır.strip())
    return masaraporlar

def garson_rapor(garson_name):
    garsonraporlar= []
    with open("hesap.json","r", encoding="utf-8")as f:
        for satır in f:
            if garson_name.lower() in satır.lower():
                garsonraporlar.append(satır.strip())
    return garsonraporlar






