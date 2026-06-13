import requests
import smtplib
from email.message import EmailMessage
import os

API_KEY = "your_openweathermap_api_key"
CITY = "Kochi"

EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
 receiver = os.environ.get("RECEIVER_EMAIL")
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

print(data)

if data.get("cod") == 200:

    temperature = data["main"]["temp"]
    condition = data["weather"][0]["main"]

    print(f"Temperature: {temperature}°C")
    print(f"Condition: {condition}")

    if temperature > 35 or condition.lower() == "rain":

        msg = EmailMessage()

        msg["Subject"] = "Weather Alert"
        msg["From"] = EMAIL
     msg["To"] = receiver

        msg.set_content(
            f"Weather Alert!\n\n"
            f"Temperature: {temperature}°C\n"
            f"Condition: {condition}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        print("Weather alert email sent!")

    else:
        print("No alert needed.")

else:
    print("Weather API error:", data)
