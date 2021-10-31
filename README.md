# Inventory-Management-System
 
Inventory managemt app that I've created for having better overview over items (Video Equipment) location in my video production company.

This app was made purely for our needs and is meant to run on **local network** (lacks some security features recommended for hosting on the internet).

**Info:**
- Based on **Python / Flask**
- Using **MongoDB** 
-  **3rd parties:** Bootstrap and Google Fonts/Icons library

 
**Functions:**
 - User login via **Username** and **Pin** 
 - View all the items you have in database and their locations (to who are they assigned)
- Easily assign items using **"code 39"** barcode
- Sort items using **tag** (type of item/group)

 
**How to run:**
 - Requirements:
     - Python 3 + PIP 3
     - MongoDB (in our case CE)
    
 
  - Open cmd/terminal and navigate to the project folder
  - Install required python libraries:
  `pip3 install -a requirements.txt`
- Start the server using **gunicorn** (may use different server if preferred):
`gunicorn --bind "ip address":"host" app:app`
  - For example:
  `gunicorn --bind 10.0.1.50:5050 app:app`

- Access the site via your internet browser on specified url and host
  - In our case - **10.0.1.50:5050**

**Default credentials**:
- Username: **"admin"**
- Pin: **"1111"**


**Notes**
 - The **description** input when creating new item supports **HTML Code**
 - **"Tags"** can be changed in the "config.json" file

 
