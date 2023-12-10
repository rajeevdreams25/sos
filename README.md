# sos
 Web bakend with Fastapi
 
If you want to create an virtual env named sos then open cmd and enter the below command
****************************************************************************************
python -m venv sos

To install python Packages open your cmd and enter the below command
********************************************************************

pip install fastapi uvicorn databases[sqlite] sqlalchemy

To run your app copy the below line and enter into the terminal
***************************************************************

uvicorn main:app --host 0.0.0.0 --port 80 --reload


if you want to show the details of the api's then open your system browser and enter the below link
***************************************************************************************************

http://<your_ip_address>/docs
