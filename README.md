# Keil Auto Build Script
## Description
* The script will auto build the specific Keil project and send email which attach the hex file and compiling log to user at 8 am every day.
  ![image](https://github.com/user-attachments/assets/f6bc876a-0ef6-4255-a25f-2858d228d904)  

## Main Document
The process mainly use **autoKeil.py**, **autoEmail.py**, and **dailySchedule.py**.
## Others
* **autoMISRACv2.py** is used MISRA C to scan the whole directory.
* **webSocketsClient.py** and **webSocketsServer.py** use WebSocket to allow R&D to remotely trigger real-time compilation on the build server.  
