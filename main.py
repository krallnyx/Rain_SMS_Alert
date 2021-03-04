import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Note! For the code to work you need to replace all the placeholders with
# Your own details. e.g. account_sid, lat/lon, from/to phone numbers.


class RainAlert:
    def __init__(self):
        owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
        # We are using Environment Variables, they need to be set via export OWM_API_KEY=xxx where xxx is your variable
        # If using a script, you can set the environment variables before the "python3 main.py" call, ending lines with
        # a semi-column
        api_key = os.environ.get("OWM_API_KEY")
        account_sid = "YOUR ACCOUNT SID"
        auth_token = os.environ.get("AUTH_TOKEN")

        weather_params = {
            "lat": "YOUR LATITUDE",
            "lon": "YOUR LONGITUDE",
            "appid": api_key,
            "exclude": "current,minutely,daily"
        }

        response = requests.get(owm_endpoint, params=weather_params)
        response.raise_for_status()
        weather_data = response.json()
        weather_slice = weather_data["hourly"][:12]

        will_rain = False

        for hour_data in weather_slice:
            condition_code = hour_data["weather"][0]["id"]
            if int(condition_code) < 700:
                will_rain = True

        if will_rain:
            proxy_client = TwilioHttpClient()
            proxy_client.session.proxies = {'https': os.environ['https_proxy']}

            client = Client(account_sid, auth_token, http_client=proxy_client)
            message = client.messages \
                .create(
                body="It's going to rain today. Remember to bring an ☔️",
                from_="YOUR TWILIO VIRTUAL NUMBER",
                to="YOUR TWILIO VERIFIED REAL NUMBER"
            )
            print(message.status)


if __name__ == '__main__':
    rain_alert = RainAlert()

