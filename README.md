# weather_service

system dependencies - python 3.7, git, virtualenv

API Setup
1) git clone https://github.com/nareshh74/weather_service.git
2) virtualenv venv --python=/usr/bin/python3
3) source venv/bin/activate
4) pip3 install -r requirements.txt
5) place .env file in root folder
6) python3 manage.py runserver

Endpoint documentation

1) Login API
      ENDPOINT
        POST ~/auth/login/
      JSON - mandatory
        {
          "username": <username>,
          "password": <password>
        }
2) Logout API
      ENDPOINT
        POST ~/auth/logout/
        HEADER - mandatory
          Authorization - Bearer <token>
3) Query API
      ENDPOINT
        GET ~/weather/
      HEADER - mandatory
        Authorization - Bearer <token>
      QUERY PARAMS - optional - works like limit offset
        start - <starting index>
        end - <ending index>
4) Email API
      ENDPOINT
        GET ~/weather/sendEmail
      HEADER - mandatory
        Authorization - Bearer <token>
      JSON - mandatory
        {
          "receiverEmailList": <array type - list of emails>
        }


Please feel free to play with endpoints to know about expected responses.
