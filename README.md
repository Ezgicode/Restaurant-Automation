
# 🍽️ Restaurant Automation

This project is a smart restaurant automation system that utilizes **cameras mounted on tables** to recognize meals, track orders, automate pricing, and **analyze waiter performance**.

## 🚀 Features

- 📸 Detects and classifies meals using a YOLOv8 model.
- 💰 Matches detected meals with prices from `menu.json`.
- 🪑 Tracks orders specific to each table.
- 👨‍🍳 Waiters are identified via **QR codes**, and the system knows which waiter serves which table.
- 📊 Includes both **table-based and waiter-based** reporting.
- ⏱️ Tracks the time a waiter spends at the table and **automatically reduces points** if it's too long.
- 🧾 Logs all activity and orders into `hesap.json`.

## 🗂️ Project Structure

restaurant_automation/
│
├── app.py                         # Flask web server
├── Restaurant_Automation.py      # Core functions
├── templates/                    # HTML files (web pages)
├── static/                       # CSS & image assets
├── models/                       # YOLO trained model
│
├── restaurant_config.json        # Table and waiter configuration
├── menu.json                     # Menu items and prices
├── hesap.json                    # Order history and logs
├── garson_puan.json              # Waiter points
🛠️ Technologies Used
Python 3.9

Flask – For building the web interface

YOLOv8 – Object detection (meal recognition)

OpenCV – Captures live camera frame

HTML + CSS – UI design

JSON – Data storage

📷 Demo
QR screen, table selection, and automatic food recognition:


🧪 How to Run
Install the dependencies:

bash
Kodu kopyala
pip install flask ultralytics opencv-python
Run the Flask server:

bash
Kodu kopyala
python app.py
Open your browser and navigate to:

cpp
Kodu kopyala
http://127.0.0.1:5000
⚠️ Notes
The YOLO model must be placed in models/best.pt.

A functional webcam is required for live detection.

You can edit the JSON files to customize waiters, tables, or menu items.

👩‍💻 Developer
Ezgicode
