# FetchRewardsAssignment
FetchRewardsAssignment

Assignment is done in python using flask framework.

Here are steps to run:
  1) Copy this file in python editor, preferred pycharm. any other will also work.
  2) Download all dependency, Following packages need to be installed to run this python file
    i) flask
  3) After downloading all required packages, just run the programm
  4) If you are using terminal, go to folder containing python file and type command "python3 filename.py" and hit enter. 
  5) Server will run on port 8080, to access, goto browser and type localhost:8080
  6) Following routes available to access
    i) "/addPayerEntry" - **POST** request type - expect one entry at a time - sample url request is **localhost:8080/addPayerEntry?pointEntry={ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }**
    ii) "/spendPoints" - **GET** request type - expect dictionary of points and its value - sample url is **localhost:8080/spendPoints?spendPoints={"points":500}**
    iii) "/getPointTable" - **GET** request type - expect no argument - sample url is **http://localhost:8080/getPointTable**
    
  7) Since fisrt url is post, you cannot test it on browser, use postman to hit the url with values
