import datetime as dt
from email.mime.multipart import MIMEMultipart
import pandas as pd
import smtplib as smtp
from email.mime.text import MIMEText
from person_dict import db as db_dict

# TODO:1. ###DONE###:Aktuell wird mittels "precip_24h:mm > 0 gecheckt ob es regnet. Auf weather_symbol_24h:idx zu
#  checken wäre besser. Das Symbol bzw. deren Beschreibung gibt besser aufschluss auf das allgemeine Wetter.
# TODO:2. ###DON###: Statt Plain Text, HTML Text mit Anhang und Grafiken verschicken.

# TODO:3. ###DONE###: Frei zugängliche Wetterdaten,  mittels JSON https://open-meteo.com/en verwenden.
# TODO:4. ###DONE###: Durchschnittliches Wetter von Morgens Mittags Abend Nachts extrahieren und anzeigen.

# TODO:5. ###DONE###: Dictionary erstellen, hier werden Personen eingetragen mit Email und Koordinaten.
# TODO:6. Der Weathertext Code, bei MORGENS, MITTAGS, ABEND, wird aus der aus der Mitte der Daten genommen. Andere Lösung?

# TODO:7. ###DONE###:Today Sun, Datum entfernen und nur Uhrzeit
# TODO:8. Statt Herz Icon oder Wind Wettericon gefühlt schreiben?
# TODO:9. Überschrift "Wettervorhersage für den 09.Dezember" anpassen.

# TODO.10. ###DONE###: Wenn es regnet wird in daily_time_slots_parent ein Regensymbol eingefügt.
# TODO:11. ###DONE###: Wettersymbole anhand des Wettercodes einfügen. HTML ICONS finden? ->https://worldweather.wmo.int/en/wxicons.html

# TODO:12. API ändern ?https://dataset.api.hub.zamg.ac.at/app/station-new/historical/klima-v1-1h?anonymous=true
# TODO:13. Simpleres HTML Template ? Sollte plattformübergreifend besser dargestellt werden können.

# TODO:14. Zusätzlich zum Wettertext, "windig", "sonnig", "regnerisch", hinzufügen?
# TODO.15. Andere Wettericons suchen und implementieren.
# TODO.16. Je nach Niederschlag wird ein anderes Wettericon eingefügt, Regen, Hagel, Schnee.

morning = 6
midday = 12
evening = 18
night = 23


def weather_text(weathercode_input):
    df = pd.read_csv("wmo_codes.csv")
    w_code = weathercode_input
    for index, row in df.iterrows():
        if row["Code"] == w_code:
            weather_descr = row["Description"]
            return weather_descr


def weather_logo(weathercode_input):
    df = pd.read_csv("wmo_codes.csv")
    w_code = weathercode_input
    for index, row in df.iterrows():
        if row["Code"] == w_code:
            weather_pic = row["Icon"]
            return weather_pic


def avg_calc(value_input, r_start, r_stop):
    value_range = value_input[r_start:r_stop]
    sum_value = 0
    for x in value_range:
        sum_value += float(x)
    avg_sum = round(sum_value / len(value_range), 2)
    return avg_sum


# Aktuelles und Enddatum setzen
today_date = dt.datetime.utcnow().date()
end_date = today_date + dt.timedelta(days=0)
today_date_str = str(today_date)
end_date_str = str(end_date)

for person in db_dict:
    name = person["name"]
    longitude = person["longitude"]
    latitude = person["latitude"]
    city = person["city"]
    email = person["email"]

    # open meteo Wetterdaten mittels json abrufen
    open_meteo_json = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature,precipitation,rain,showers,snowfall,weathercode,windspeed_10m&models=icon_seamless&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,sunrise,sunset,precipitation_sum,windspeed_10m_max&timezone=auto&start_date={today_date_str}&end_date={end_date_str}"
    weather_df = pd.read_json(open_meteo_json)
    # weather_df.to_json("weather_forecast_24.json")

    # Dataframes abspeichern
    daily_weather = weather_df["daily"]
    hourly_weather = weather_df["hourly"]

    # Stündliche Wettervorhersage
    morning = 6
    midday = 12
    evening = 18
    night = 23

    h_time = hourly_weather["time"]
    h_temp = hourly_weather["temperature_2m"]
    h_a_temp = hourly_weather["apparent_temperature"]
    h_prec = hourly_weather["precipitation"]
    h_wind = hourly_weather["windspeed_10m"]
    h_w_code = hourly_weather["weathercode"]

    # Morning Wettervorhersage

    m_h_temp = avg_calc(h_temp, morning, midday)
    m_h_a_temp = avg_calc(h_a_temp, morning, midday)
    m_h_prec = avg_calc(h_prec, morning, midday)
    m_h_wind = avg_calc(h_wind, morning, midday)
    m_h_w_code = avg_calc(h_w_code, morning, midday)
    m_h_w_text = weather_text(h_w_code[8])
    m_h_w_symbol = weather_logo(h_w_code[8])

    # Midday Wettervorhersage
    mi_h_temp = avg_calc(h_temp, midday, evening)
    mi_h_a_temp = avg_calc(h_a_temp, midday, evening)
    mi_h_prec = avg_calc(h_prec, midday, evening)
    mi_h_wind = avg_calc(h_wind, midday, evening)
    mi_h_w_code = avg_calc(h_w_code, midday, evening)
    mi_h_w_text = weather_text(h_w_code[14])
    mi_h_w_symbol = weather_logo(h_w_code[14])

    # Evening Wettervorhersage
    e_h_temp = avg_calc(h_temp, evening, night)
    e_h_a_temp = avg_calc(h_a_temp, evening, night)
    e_h_prec = avg_calc(h_prec, evening, night)
    e_h_wind = avg_calc(h_wind, evening, night)
    e_h_w_code = avg_calc(h_w_code, evening, night)
    e_h_w_text = weather_text(h_w_code[20])
    e_h_w_symbol = weather_logo(h_w_code[20])

    # Tägliche Wettervorhersage
    d_time = today_date.strftime("%d. %B, %Y")
    d_weathercode = daily_weather["weathercode"]
    d_temperature = daily_weather["temperature_2m_max"]
    d_apparent_temperature = daily_weather["apparent_temperature_max"]
    d_precipitation = daily_weather["precipitation_sum"]
    d_sunrise = daily_weather["sunrise"]
    d_sunset = daily_weather["sunset"]
    d_weather_text = weather_text(d_weathercode[0])
    d_symbol = weather_logo(d_weathercode[0])

    # Änderung des Datumsformates
    daily_sunrise_str = str(d_sunrise[0].replace('T', ' '))
    daily_sunrise_convert = dt.datetime.strptime(daily_sunrise_str, '%Y-%m-%d %H:%M')
    daily_sunrise_time = daily_sunrise_convert.strftime('%H:%M')

    daily_sunset_str = str(d_sunset[0].replace('T', ' '))
    daily_sunset_convert = dt.datetime.strptime(daily_sunset_str, '%Y-%m-%d %H:%M')
    daily_sunset_time = daily_sunset_convert.strftime('%H:%M')

    # html template

    html = f'''
    <html>
      <head>
      
        
        </head>
        
        <body class="body" style="background-color: white;margin: 20px;border-radius: 18px;">
       <p style="display: block;padding: 0px;margin-top: 8px;margin-bottom: 30px;"> <img src="https://cdn-icons-png.flaticon.com/512/2480/2480608.png" alt="weather logo" class="img" style="display: inline-block;margin-left: auto;margin-right: auto;margin-top: 0px;width: 100px;height: 100px;"> </p>
        <div class="head-title" style="color: #40514E;font-family: 'Trebuchet MS', sans-serif;display: block;font-size: 33px;margin-bottom: 25px;margin-left: 20px;">Hallo {name}<br> Dein Wetter für heute in {city}</div>
      <div class="today-container" style="position: relative;background-color: #E3FDFD;border-radius: 18px;padding: 5px;display: inline-block;">
        <div class="weather_text-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>Heute:</b>  <br>{d_weather_text}
        </div>
          <div class="highest_temp-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>Höchsttemperatur:</b> <br>{d_temperature[0]}°
        </div>
        <div class="feeled_temp-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>Gefühlt:</b><br>{round(float(d_apparent_temperature[0]), 2)}°
        </div>
        <div class="rain-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>Niederschlag pro qm2: </b> <br>{d_precipitation[0]} mm Regen
        </div>
        </div>
    
    <br>
    <hr class="hr-top" style="display: inline-block;width: 80%;border-style: solid;border-width: 10px;border-color: #71C9CE;margin: 0px;"><br> 
            
    <div class="daily-time-slots-parent" style="position: relative;background-color: white;border-radius: 18px;display: inline-block;">
        <div class="daily-time-slots-child" style="font-family: 'Trebuchet MS', sans-serif;display: inline-block;position: relative;margin: 10px;padding: 5px;background-color: #E3FDFD;border-radius: 18px;border-top: 20px;">
        <p style="padding: 0px;margin-top: 8px;margin-bottom: 10px;"><b>Morgens /</b> 06 - 12 Uhr </p>{m_h_w_text}<hr class="hr2" style="width: 100%;display: block;">
            <div>
                &#x1F321; {m_h_temp}°, &#x2764; {m_h_a_temp}° <br>
            </div>
            <div>
                &#9748; {m_h_prec} mm
            </div>
            <div>
               <img src="https://raw.githubusercontent.com/mcdeedz/green_budgie/main/air.png" alt="Logo" style = "width:30px"> {m_h_wind} kmh
            </div>
            <img src="{m_h_w_symbol}" alt="Logo">
        </div>
    
        <div class="daily-time-slots-child" style="font-family: 'Trebuchet MS', sans-serif;display: inline-block;position: relative;margin: 10px;padding: 5px;background-color: #E3FDFD;border-radius: 18px;border-top: 20px;">
            <p style="padding: 0px;margin-top: 8px;margin-bottom: 10px;"><b>Mittag /</b> 12 - 18 Uhr </p>{mi_h_w_text}<hr class="hr2" style="width: 100%;display: block;">
            <div>
                &#x1F321; {mi_h_temp}°, &#x2764; {mi_h_a_temp}° <br>
            </div>
            <div>
                &#9748; {mi_h_prec} mm
            </div>
            <div>
            <img src="https://raw.githubusercontent.com/mcdeedz/green_budgie/main/air.png" alt="Logo" style = "width:30px"> {mi_h_wind} kmh
            </div>
            <img src="{mi_h_w_symbol}" alt="Logo">
        </div>
    
        <div class="daily-time-slots-child" style="font-family: 'Trebuchet MS', sans-serif;display: inline-block;position: relative;margin: 10px;padding: 5px;background-color: #E3FDFD;border-radius: 18px;border-top: 20px;">
            <p style="padding: 0px;margin-top: 8px;margin-bottom: 10px;"><b>Abends /</b> 18 - 22 Uhr </p>{e_h_w_text} <hr class="hr2" style="width: 100%;display: block;">
            <div>
                &#x1F321; {e_h_temp}°, &#x2764; {e_h_a_temp}°  <br>
            </div>
            <div>
                &#9748; {e_h_prec} mm
            </div>
            <div>
               <img src="https://raw.githubusercontent.com/mcdeedz/green_budgie/main/air.png" alt="Logo" style = "width:30px"> {e_h_wind} kmh
            </div>
            <img src="{e_h_w_symbol}" alt="Logo">
        </div>
            <hr class="hr1" style="width: 50%;border-style: solid;border-width: 10px;border-color: #71C9CE;margin: 10px;">
    <div class="today-sun" style="font-family: 'Trebuchet MS', sans-serif;font-size: 12px;margin-top: 0px;margin-bottom: 5px;padding: 5px;border-radius: 18px;background-color: #E3FDFD;display: inline-block;">
        <div class="sunrise-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>&#9728;&#65039;</b>Sonnenaufgang: {daily_sunrise_time}
         </div>
        <div class="sunset-item box" style="display: inline-block;font-family: 'Trebuchet MS', sans-serif;padding: 10px;">
            <b>&#127751</b>Sonnenuntergang: {daily_sunset_time}
    
        </div>
     </div>
        <hr class="hr-bottom" style="display: inline-block;width: 55%;border-style: solid;border-width: 10px;border-color: #71C9CE;"><br>
        <div class="chip" style="display: inline-block;padding: 10px 30px;height: 80px;font-size: 16px;line-height: 20px;border-radius: 25px;background-color: #E3FDFD;font-family: 'Trebuchet MS', sans-serif;width: 235px;">
            <img src="https://github.com/mcdeedz/green_budgie/blob/main/IMG_0316.jpg?raw=true" alt="Person" width="100" height="100" style="float: left;margin: 0 10px 0 -25px;height: 70px;width: 70px;border-radius: 50%;">
            <span style="line-height: 25px;">Christian Magdits, 32</span> <br>
            <span style="line-height: 25px;">Junior Python Developer</span> <br>
            <span style="line-height: 25px;">Junior Web Developer</span>
          </div>
      </div></body>
      </html>
        '''

    # Versand der Wetterdaten
    my_email = "90mcdeeds@gmail.com"
    my_password = "wgwoftojrwwoemcu"

    # Create a MIMEMultipart class, and set up the From, To, Subject fields

    email_message = MIMEMultipart()
    email_message['From'] = my_email
    email_message['To'] = "christian.magdits@gmail.com"
    email_message['Subject'] = f'Wettervorhersage {d_time}'
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()

    with smtp.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=f"{email}",
            msg=f"{email_string}")
