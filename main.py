import requests
import customtkinter as ctk
from PIL import Image
import geocoder
from datetime import datetime, timedelta
import json
from os import environ


# Variables, dictionaries and lists
theme_color = "#2963BC"
theme_color_2 = "#1D468C"
hover_color = "#4f87de"
gray = "#333333"
font_name = ("Noto Sans")

API_endpoint_current_weather = "https://api.openweathermap.org/data/2.5/weather"
API_endpoint_forecast = "https://api.openweathermap.org/data/2.5/forecast"
open_weather_api = environ.get("API_key_open_weather")
google_maps_api = environ.get("API_key_maps")

WEATHER_MAP = {
    "clear sky": "Sunny",
    "few clouds": "Mostly sunny",
    "scattered clouds": "Temporary overcast",
    "broken clouds": "Cloudy",
    "overcast clouds": "Cloudy",
    "mist": "Misty",
    "smoke": "Misty",
    "haze": "Misty",
    "sand, dust whirls": "Misty",
    "fog": "Misty",
    "sand": "Misty",
    "dust": "Misty",
    "volcanic ash": "Misty",
    "squalls": "Windy",
    "tornado": "Windy",
    "snow": "Snowily",
    "light snow": "Snowily",
    "rain": "Rainy",
    "drizzle": "Cloudy",
    "thunderstorm": "Thunderstorm",
    "heavy intensity rain": "Rainy",
    "very heavy rain": "Rainy",
    "extreme rain": "Rainy",
    "freezing rain": "Sleet",
    "light rain": "Patchy rain",
    "shower rain": "Patchy rain",
    "light intensity shower rain": "Patchy rain",
    "heavy intensity shower rain": "Patchy rain",
    "ragged shower rain": "Patchy rain",
    "moderate rain": "Patchy rain",
    "light shower snow": "Sleet",
    "thunderstorm with light rain": "Thunderstorm",
    "thunderstorm with rain": "Thunderstorm",
    "light thunderstorm": "Thunderstorm",
    "heavy thunderstorm": "Thunderstorm",
    "ragged thunderstorm": "Thunderstorm",
    "thunderstorm with light drizzle": "Thunderstorm",
    "thunderstorm with drizzle": "Thunderstorm",
    "thunderstorm with heavy drizzle": "Thunderstorm",
    "light intensity drizzle": "Patchy rain",
    "drizzle": "Patchy rain",
    "heavy intensity drizzle": "Patchy rain",
    "light intensity drizzle rain": "Patchy rain",
    "drizzle rain": "Patchy rain",
    "heavy intensity drizzle rain": "Patchy rain",
    "shower rain and drizzle": "Patchy rain",
    "heavy shower rain and drizzle": "Patchy rain",
    "shower drizzle": "Patchy rain",
    "sleet": "Sleet",
    "heavy snow": "Snowily",
    "light shower sleet": "Snowily",
    "shower sleet": "Snowily",
    "light rain and snow": "Sleet",
    "rain and snow": "Sleet",
    "shower snow": "Sleet",
    "heavy shower snow": "Sleet",
}


IMAGE_MAP = {
    "Cloudy": "Images/cloud.png",
    "Temporary overcast": "Images/temporary overcast.png",
    "Sunny": "Images/sun.png",
    "Mostly sunny": "Images/cloudy.png",
    "Patchy rain": "Images/rain.png",
    "Rainy": "Images/heavy-rain.png",
    "Thunderstorm": "Images/storm.png",
    "Snowily": "Images/snow.png",
    "Misty": "Images/fog.png",
    "Sleet": "Images/snowing.png",
    "Windy": "Images/wind.png",
}

current_weather_parameters = []
forecast_data_list = []

# App


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Initial functions, variables
        self.user_location, self.user_country, self.latitude, self.longitude = self.get_location()

        self.get_weather_data(
            self.latitude, self.longitude)

        self.today_date = self.today()

        self.temp_unit = ctk.StringVar()
        self.temp_unit.set("Degrees Celsius - °C")

        self.toplevel_opened = False

        # UI
        self.title("Weather App by Marek Baranski")
        self.geometry("875x750")
        self.iconbitmap("Images/clouds-and-sun.ico")
        self.configure(fg_color=theme_color)

        # User's location
        self.user_city = ctk.CTkLabel(
            master=self, text=f"{self.user_location}, {self.user_country}", font=(font_name, 45, "bold"), text_color="white")
        self.user_city.grid(row=0, column=0, padx=35,
                            pady=10, sticky="nw")

        # Settings
        self.settings_image = ctk.CTkImage(
            Image.open("Images/setting.png"), size=(40, 40))
        self.settings_image_label = ctk.CTkButton(
            master=self, width=40, height=40, text="", image=self.settings_image, hover_color=hover_color, fg_color=theme_color, corner_radius=100, command=self.settings)
        self.settings_image_label.grid(
            row=0, column=2, padx=(140, 0),  pady=20, sticky="nw")

        # Today's date
        self.today_date_label = ctk.CTkLabel(
            master=self, text=self.today_date, text_color="white", font=(font_name, 25))
        self.today_date_label.grid(row=1, column=0, padx=35, sticky="nw")

        # Today's weather image
        self.weather_image = ctk.CTkImage(
            Image.open(IMAGE_MAP.get(current_weather_parameters[0])), size=(170, 170))
        self.weather_image_label = ctk.CTkLabel(
            master=self, text="", image=self.weather_image)
        self.weather_image_label.grid(
            row=2, column=0, padx=35, pady=30, sticky="nw")

        # Today's temperature
        self.temperature_label = ctk.CTkLabel(
            master=self, text=f"{current_weather_parameters[1]}°C", text_color="white", font=(font_name, 85))
        self.temperature_label.grid(
            row=2, column=2, pady=(45, 70), sticky="nw")

        # Today's weather basic description
        self.weather_description_label = ctk.CTkLabel(
            master=self, text=current_weather_parameters[0], text_color="white", font=(font_name, 25), wraplength=200)
        self.weather_description_label.grid(
            row=2, column=2, pady=150, sticky="nw")

        # Today's weather detailed description (Frame)
        self.weather_details = ctk.CTkFrame(
            master=self, width=600, height=200, fg_color=theme_color, border_color=theme_color)
        self.weather_details.grid(
            row=2, column=0, padx=(200, 0),  pady=(220, 0), sticky="w")
        self.weather_details.grid_columnconfigure(1, weight=1)

        # Max temperature
        self.max_temperature_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[2]}°C", font=(font_name, 25), text_color="white")
        self.max_temperature_label.grid(
            row=0, column=0, pady=(20, 0), sticky="nw")
        self.max_temperature_label_description = ctk.CTkLabel(
            master=self.weather_details, text="High", font=(font_name, 20), text_color="white")
        self.max_temperature_label_description.grid(
            row=1, column=0, pady=(0, 20), sticky="nw")

        # Minimal temperature
        self.min_temperature_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[3]}°C", font=(font_name, 25), text_color="white")
        self.min_temperature_label.grid(
            row=2, column=0, sticky="nw")
        self.min_temperature_label_description = ctk.CTkLabel(
            master=self.weather_details, text="Low", font=(font_name, 20), text_color="white")
        self.min_temperature_label_description.grid(
            row=3, column=0, pady=0, sticky="nw")

        # Wind speed
        self.wind_speed_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[4]} km/h", font=(font_name, 25), text_color="white")
        self.wind_speed_label.grid(
            row=0, column=1, padx=75, pady=(20, 0), sticky="nw")
        self.wind_speed_label_description = ctk.CTkLabel(
            master=self.weather_details, text="Wind", font=(font_name, 20), text_color="white")
        self.wind_speed_label_description.grid(
            row=1, column=1, padx=75, pady=(0, 20), sticky="nw")

        # Pressure
        self.pressure_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[5]} hPa", font=(font_name, 25), text_color="white")
        self.pressure_label.grid(
            row=2, column=1, padx=75, sticky="nw")
        self.pressure_label_description = ctk.CTkLabel(
            master=self.weather_details, text="Pressure", font=(font_name, 20), text_color="white")
        self.pressure_label_description.grid(
            row=3, column=1, padx=75, pady=0, sticky="nw")

        # Sunrise timestamp
        self.sunrise_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[6]}", font=(font_name, 25), text_color="white")
        self.sunrise_label.grid(
            row=0, column=2, pady=(20, 0), sticky="nw")
        self.sunrise_label_description = ctk.CTkLabel(
            master=self.weather_details, text="Sunrise", font=(font_name, 20), text_color="white")
        self.sunrise_label_description.grid(
            row=1, column=2, pady=(0, 20), sticky="nw")

        # Sunset timestamp
        self.sunset_label = ctk.CTkLabel(
            master=self.weather_details, text=f"{current_weather_parameters[7]}", font=(font_name, 25), text_color="white")
        self.sunset_label.grid(
            row=2, column=2, sticky="nw")
        self.sunset_label_description = ctk.CTkLabel(
            master=self.weather_details, text="Sunset", font=(font_name, 20), text_color="white")
        self.sunset_label_description.grid(
            row=3, column=2, pady=0, sticky="nw")

        # Main frame
        self.forecast_frame = ctk.CTkScrollableFrame(
            master=self, fg_color=theme_color, bg_color=theme_color, width=625, scrollbar_button_hover_color=theme_color_2, label_text_color="white")
        self.forecast_frame.grid(row=4, column=0, pady=10)

        # Creating forecast labels
        for day in range(0, 5):
            # Label for the day name
            forecast_day_label_name = f"forecast_day_label_{day}"
            self.forecast_day_label = ctk.CTkLabel(master=self.forecast_frame, text=(datetime.now(
            ) + timedelta(days=day)).strftime("%A"), font=(font_name, 20), text_color="white")
            self.forecast_day_label.grid(
                row=4+day, column=0, padx=50, pady=(20, 0), sticky="nw")
            setattr(self, forecast_day_label_name, self.forecast_day_label)

            # Image label for the weather icon
            forecast_weather_image_label_name = f"forecast_weather_image_label_{day}"
            self.forecast_weather_image = ctk.CTkImage(
                Image.open(forecast_data_list[day][3]), size=(40, 40))
            self.forecast_weather_image_label = ctk.CTkLabel(
                master=self.forecast_frame, text="", image=self.forecast_weather_image)
            self.forecast_weather_image_label.grid(
                row=4+day, column=1, padx=0, pady=(20, 0), sticky="nsew")
            setattr(self, forecast_weather_image_label_name,
                    self.forecast_weather_image_label)

            # Label for the weather description
            forecast_weather_label_name = f"forecast_weather_label_{day}"
            self.forecast_weather_label = ctk.CTkLabel(
                master=self.forecast_frame, text=forecast_data_list[day][2], font=(font_name, 20), text_color="white")
            self.forecast_weather_label.grid(
                row=4+day, column=2, padx=20, pady=(20, 0), sticky="w")
            setattr(self, forecast_weather_label_name,
                    self.forecast_weather_label)

            # Label for the temperature
            forecast_temp_label_name = f"forecast_temp_label_{day}"
            self.forecast_temp_label = ctk.CTkLabel(
                master=self.forecast_frame, text=f"{forecast_data_list[day][0]}/{forecast_data_list[day][1]}°C", font=(font_name, 20), text_color="white")
            self.forecast_temp_label.grid(
                row=4+day, column=3, padx=60, pady=(20, 0), sticky="nw")
            setattr(self, forecast_temp_label_name, self.forecast_temp_label)

    # Functions

    def get_location(self):
        g = geocoder.ip("me")
        city = g.city
        country = g.country
        latitude, longitude = g.latlng
        return city, country, latitude, longitude

    def get_weather_data(self, latitude, longitude):

        weather_API_parameters = {
            "lat": latitude,
            "lon": longitude,
            "appid": open_weather_api
        }

        current_weather_response = requests.get(
            API_endpoint_current_weather, params=weather_API_parameters)
        current_weather_response.raise_for_status()
        weather_data = current_weather_response.json()

        # Current weather data
        weather_description = weather_data['weather'][0]['description']
        weather_description = WEATHER_MAP.get(weather_description)

        temperature = int(weather_data['main']['temp'] - 273.15)
        max_temperature = int(
            weather_data['main']['temp_max'] - 273.15)
        min_temperature = int(
            weather_data['main']['temp_min'] - 273.15)

        wind_speed = int(weather_data['wind']['speed'] * 3.6)

        pressure = weather_data['main']['pressure']

        sunrise_timestamp = datetime.fromtimestamp(
            weather_data['sys']['sunrise'])

        sunset_timestamp = datetime.fromtimestamp(
            weather_data['sys']['sunset'])

        sunrise_time = sunrise_timestamp.strftime('%H:%M')
        sunset_time = sunset_timestamp.strftime('%H:%M')

        current_weather_parameters.extend((weather_description, temperature, max_temperature,
                                          min_temperature, wind_speed, pressure, sunrise_time, sunrise_time))

        # Forecast data
        forecast_response = requests.get(API_endpoint_forecast,
                                         params=weather_API_parameters)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        for weather in forecast_data["list"][1:7]:
            min_temperature_forecast = int(
                weather["main"]["temp_min"] - 273.15)
            max_temperature_forecast = int(
                weather["main"]["temp_max"] - 273.15)
            forecast_description = weather["weather"][0]["description"]
            forecast_description = WEATHER_MAP.get(forecast_description)
            forecast_image = IMAGE_MAP.get(forecast_description)
            forecast_data_list.append(
                [min_temperature_forecast, max_temperature_forecast, forecast_description, forecast_image])

    def search_city(self):
        # Search city thanks to google api
        city = self.change_city_input.get()
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_maps_api}"
        current_weather_response = requests.get(url)
        data = json.loads(current_weather_response.text)

        if data["status"] == "OK":
            lat_for_other_city = data["results"][0]["geometry"]["location"]["lat"]
            lng_for_other_city = data["results"][0]["geometry"]["location"]["lng"]
            city_and_country = data['results'][0]['formatted_address']
            city_name = city_and_country.split(",")[0]
            country_name = city_and_country.split(",")[1]

            # Shortcut for country
            try:
                url = f"https://restcountries.com/v2/name/{country_name}"
                current_weather_response = requests.get(url)
                if current_weather_response.ok:
                    data = current_weather_response.json()[0]
                    country_name_shortcut = data["alpha2Code"]
                    self.user_city.configure(
                        text=f"{city_name}, {country_name_shortcut}")
            except:
                self.user_city.configure(
                    text=city_and_country)

            weather_API_parameters = {
                "lat": lat_for_other_city,
                "lon": lng_for_other_city,
                "appid": open_weather_api
            }

            current_weather_response = requests.get(
                API_endpoint_current_weather, params=weather_API_parameters)
            current_weather_response.raise_for_status()
            current_weather_data = current_weather_response.json()

            # Current weather data
            weather_description = current_weather_data['weather'][0]['description']
            weather_description = WEATHER_MAP.get(weather_description)

            self.temperature = int(
                current_weather_data['main']['temp'] - 273.15)
            self.max_temperature = int(
                current_weather_data['main']['temp_max'] - 273.15)
            self.min_temperature = int(
                current_weather_data['main']['temp_min'] - 273.15)

            wind_speed = int(current_weather_data['wind']['speed'] * 3.6)

            pressure = current_weather_data['main']['pressure']

            sunrise_timestamp = datetime.fromtimestamp(
                current_weather_data['sys']['sunrise'])

            sunset_timestamp = datetime.fromtimestamp(
                current_weather_data['sys']['sunset'])

            sunrise_time = sunrise_timestamp.strftime('%H:%M')
            sunset_time = sunset_timestamp.strftime('%H:%M')

            self.weather_description_label.configure(text=weather_description)
            self.weather_image = ctk.CTkImage(
                Image.open(IMAGE_MAP.get(weather_description)), size=(170, 170))
            self.weather_image_label.configure(image=self.weather_image)
            self.temperature_label.configure(text=f"{self.temperature}°C")
            self.max_temperature_label.configure(
                text=f"{self.max_temperature}°C")
            self.min_temperature_label.configure(
                text=f"{self.min_temperature}°C")
            self.wind_speed_label.configure(text=f"{wind_speed} km/h")
            self.pressure_label.configure(text=f"{pressure} hPa")
            self.sunrise_label.configure(text=sunrise_time)
            self.sunset_label.configure(text=sunset_time)

            self.temperature_choice.set("Degrees Celsius - °C")
            self.temperature_choice.configure(
                values=["Degrees Fahrenheit - °F"])
            self.error_label.configure(text="")

            # Forecast data
            forecast_data_list.clear()

            forecast_response = requests.get(
                API_endpoint_forecast, params=weather_API_parameters)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            for weather in forecast_data["list"][1:7]:
                min_temperature_forecast = int(
                    weather["main"]["temp_min"] - 273.15)
                max_temperature_forecast = int(
                    weather["main"]["temp_max"] - 273.15)
                forecast = weather["weather"][0]["description"]
                forecast = WEATHER_MAP.get(forecast)
                forecast_image = IMAGE_MAP.get(forecast)
                forecast_data_list.append(
                    [min_temperature_forecast, max_temperature_forecast, forecast, forecast_image])

            # Updating data
            for day in range(0, 5):
                # Label for the day name
                forecast_day_label_name = f"forecast_day_label_{day}"
                if hasattr(self, forecast_day_label_name):
                    self.forecast_day_label = getattr(
                        self, forecast_day_label_name)
                    self.forecast_day_label.configure(
                        text=(datetime.now() + timedelta(days=day)).strftime("%A"))
                else:
                    self.forecast_day_label = ctk.CTkLabel(master=self.forecast_frame, text=(datetime.now(
                    ) + timedelta(days=day)).strftime("%A"), font=(font_name, 20), text_color="white")
                    self.forecast_day_label.grid(
                        row=4+day, column=0, padx=(50, 0), pady=(20, 0), sticky="nw")
                    setattr(self, forecast_day_label_name,
                            self.forecast_day_label)

                # Image label for the weather icon
                forecast_weather_image_label_name = f"forecast_weather_image_label_{day}"
                if hasattr(self, forecast_weather_image_label_name):
                    self.forecast_weather_image_label = getattr(
                        self, forecast_weather_image_label_name)
                    self.forecast_weather_image = ctk.CTkImage(
                        Image.open(forecast_data_list[day][3]), size=(40, 40))
                    self.forecast_weather_image_label.configure(
                        image=self.forecast_weather_image)
                else:
                    self.forecast_weather_image = ctk.CTkImage(
                        Image.open(forecast_data_list[day][3]), size=(40, 40))
                    self.forecast_weather_image_label = ctk.CTkLabel(
                        master=self.forecast_frame, text="", image=self.forecast_weather_image)
                    self.forecast_weather_image_label.grid(
                        row=4+day, column=1, padx=0, pady=(20, 0), sticky="nsew")
                    setattr(self, forecast_weather_image_label_name,
                            self.forecast_weather_image_label)

                # Label for the weather description
                forecast_weather_label_name = f"forecast_weather_label_{day}"
                if hasattr(self, forecast_weather_label_name):
                    self.forecast_weather_label = getattr(
                        self, forecast_weather_label_name)
                    self.forecast_weather_label.configure(
                        text=forecast_data_list[day][2])
                else:
                    self.forecast_weather_label = ctk.CTkLabel(
                        master=self.forecast_frame, text=forecast_data_list[day][2], font=(font_name, 20), text_color="white")
                    self.forecast_weather_label.grid(
                        row=4+day, column=2, padx=0, pady=(20, 0), sticky="w")
                    setattr(self, forecast_weather_label_name,
                            self.forecast_weather_label)

                # Label for the temperature
                forecast_temp_label_name = f"forecast_temp_label_{day}"
                if hasattr(self, forecast_temp_label_name):
                    self.forecast_temp_label = getattr(
                        self, forecast_temp_label_name)
                    self.forecast_temp_label.configure(
                        text=f"{forecast_data_list[day][0]}/{forecast_data_list[day][1]}°C")
                else:
                    self.forecast_temp_label = ctk.CTkLabel(
                        master=self.forecast_frame, text=f"{forecast_data_list[day][0]}/{forecast_data_list[day][1]}°C", font=(font_name, 20), text_color="white")
                    self.forecast_temp_label.grid(
                        row=4+day, column=3, padx=50, pady=(20, 0), sticky="nw")
                    setattr(self, forecast_temp_label_name,
                            self.forecast_temp_label)

        elif data["status"] == "ZERO_RESULTS":
            self.error_label.configure(
                text="The specified city name could not be found. Make sure you typed it correctly and try again.")

    def today(self):
        now = datetime.now()
        day_of_week = now.strftime("%A")
        day_of_month = now.strftime("%d")
        month = now.strftime("%B")

        data = f"{day_of_week} {day_of_month} {month}"
        return data

    def settings(self):
        if not self.toplevel_opened:
            self.toplevel_opened = True
            self.settings_window = ctk.CTkToplevel(self)
            self.settings_window.title("Settings")
            self.settings_window.geometry("670x500")
            self.settings_window.after(
                201, lambda: self.settings_window.iconbitmap("Images/clouds-and-sun.ico"))
            self.settings_window.configure(fg_color=theme_color)

            # Scaling settings
            self.scaling_label = ctk.CTkLabel(
                master=self.settings_window, text="Scaling", text_color="white", font=(font_name, 25))
            self.scaling_label.grid(
                row=0, column=0, padx=(35, 0), pady=10, sticky="nw")

            self.scaling_choice = ctk.CTkOptionMenu(master=self.settings_window, values=[
                "80%", "90%", "100%", "110%", "120%"], fg_color=gray, button_color=theme_color_2, button_hover_color=hover_color, dropdown_hover_color=theme_color_2, command=self.change_scaling, width=270, height=37)
            self.scaling_choice.set("100%")
            self.scaling_choice.grid(row=0, column=2, sticky="e")

            # Temperature unit
            self.temperature_unit_label = ctk.CTkLabel(
                master=self.settings_window, text="Temperature unit", text_color="white", font=(font_name, 25))
            self.temperature_unit_label.grid(
                row=1, column=0, padx=(35, 0), pady=10, sticky="nw")

            self.temperature_choice = ctk.CTkOptionMenu(master=self.settings_window, values=["Degrees Fahrenheit - °F"], variable=self.temp_unit, fg_color=gray,
                                                        button_color=theme_color_2, button_hover_color=hover_color, dropdown_hover_color=theme_color_2, command=self.change_degrees, width=270, height=37)
            self.temperature_choice.grid(row=1, column=2, sticky="e")

            # Speed unit
            self.speed_unit_label = ctk.CTkLabel(
                master=self.settings_window, text="Speed unit", text_color="white", font=(font_name, 25))
            self.speed_unit_label.grid(
                row=2, column=0, padx=(35, 0), pady=10, sticky="nw")

            self.speed_unit_choice = ctk.CTkOptionMenu(master=self.settings_window, values=["Miles per hour - mph", "Meters per second - m/s"], fg_color=gray,
                                                       button_color=theme_color_2, button_hover_color=hover_color, dropdown_hover_color=theme_color_2, command=self.change_speed, width=270, height=37)
            self.speed_unit_choice.grid(row=2, column=2, sticky="e")
            self.speed_unit_choice.set("Kilometers per hour - km/h"
                                       )

            # Change city
            self.change_city_label = ctk.CTkLabel(
                master=self.settings_window, text="Change city", text_color="white", font=(font_name, 25))
            self.change_city_label.grid(
                row=3, column=0, padx=(35, 0), pady=20, sticky="w")

            self.change_city_input = ctk.CTkEntry(
                master=self.settings_window, placeholder_text="Type name of the city", placeholder_text_color=hover_color, font=(font_name, 25), width=270, height=10)
            self.change_city_input.grid(
                row=3, column=2, pady=20, sticky="e")

            self.change_city_button = ctk.CTkButton(master=self.settings_window, text="Search", font=(
                font_name, 25), fg_color=theme_color_2, hover_color=hover_color, command=self.search_city)
            self.change_city_button.grid(
                row=4, column=2, sticky="nsew")

            self.error_label = ctk.CTkLabel(master=self.settings_window, text="", font=(
                font_name, 15), text_color="red", wraplength=270)
            self.error_label.grid(
                row=5, column=2, pady=10, sticky="ne")

            # Quit settings window
            self.save_changes = ctk.CTkButton(master=self.settings_window, text="OK", font=(
                font_name, 25), fg_color=theme_color_2, hover_color=hover_color, command=self.close_settings)
            self.save_changes.grid(
                row=6, column=1, pady=(80, 0), sticky="s")

    def change_degrees(self, _):
        if self.temp_unit.get() == "Degrees Celsius - °C":
            # Convert temperatures to Celsius
            current_weather_parameters[1] -= 273.15
            current_weather_parameters[2] -= 273.15
            current_weather_parameters[3] -= 273.15

            for day in forecast_data_list:
                day[0] -= 273.15
                day[1] -= 273.15

            # Update temperature labels
            self.temperature_label.configure(
                text=f"{round(current_weather_parameters[1])}°C")
            self.max_temperature_label.configure(
                text=f"{round(current_weather_parameters[2])}°C")
            self.min_temperature_label.configure(
                text=f"{round(current_weather_parameters[3])}°C")

            for day, day_label in enumerate([self.forecast_temp_label_0, self.forecast_temp_label_1, self.forecast_temp_label_2, self.forecast_temp_label_3, self.forecast_temp_label_4]):
                day = forecast_data_list[day]
                day_label.configure(text=f"{round(day[0])}/{round(day[1])}°C")

            self.temperature_choice.configure(
                values=["Degrees Fahrenheit - °F"])

        else:
            # Convert temperatures to Fahrenheit
            current_weather_parameters[1] += 273.15
            current_weather_parameters[2] += 273.15
            current_weather_parameters[3] += 273.15

            for day in forecast_data_list:
                day[0] += 273.15
                day[1] += 273.15

            # Update temperature labels
            self.temperature_label.configure(
                text=f"{round(current_weather_parameters[1])}°F")
            self.max_temperature_label.configure(
                text=f"{round(current_weather_parameters[2])}°F")
            self.min_temperature_label.configure(
                text=f"{round(current_weather_parameters[3])}°F")

            for day, day_label in enumerate([self.forecast_temp_label_0, self.forecast_temp_label_1, self.forecast_temp_label_2, self.forecast_temp_label_3, self.forecast_temp_label_4]):
                day = forecast_data_list[day]
                day_label.configure(text=f"{round(day[0])}/{round(day[1])}°F")

            self.temperature_choice.configure(values=["Degrees Celsius - °C"])

    def change_speed(self, _):
        # Miles per hour
        wind_speed_list = []
        wind_speed_list.append(current_weather_parameters[4])

        if self.speed_unit_choice.get() == "Miles per hour - mph":
            mph = int(wind_speed_list[0] * 0.621371)
            self.wind_speed_label.configure(
                text=f"{mph} mph")
            self.speed_unit_choice.configure(
                values=["Kilometers per hour - km/h", "Meters per second - m/s"])

        elif self.speed_unit_choice.get() == "Meters per second - m/s":
            # Meters per second
            mps = int(wind_speed_list[0] / 3.6)
            self.wind_speed_label.configure(
                text=f"{mps} m/s")
            self.speed_unit_choice.configure(
                values=["Kilometers per hour - km/h", "Miles per hour - mph"])

        else:
            self.wind_speed_label.configure(
                text=f"{wind_speed_list[0]} km/h")
            self.speed_unit_choice.configure(
                values=["Meters per second - m/s", "Miles per hour - mph"])

    def close_settings(self):
        self.toplevel_opened = False
        self.settings_window.destroy()
        self.settings_window.update()

    def change_scaling(self, new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    App = App()
    App.mainloop()
