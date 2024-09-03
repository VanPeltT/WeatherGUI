import requests
import datetime
import tkinter as tk
from tkinter import ttk

counter = 0

def get_weather_data_by_lat_lon(api_key, latitude, longitude):
    """Fetches weather data from WeatherAPI using latitude and longitude."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&days=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def update_weather(api_key, latitude, longitude, label):
    """Fetch and update weather information on the GUI."""
    global counter
    weather_data = get_weather_data_by_lat_lon(api_key, latitude, longitude)
    counter += 1
    print("Number of calls:", counter)
    if weather_data:
        current_time = datetime.datetime.now()
        date_str = current_time.strftime("%m/%d/%Y")
        time_str = current_time.strftime("\n%I:%M %p")
        current_temp_f = weather_data['current']['temp_f']
        feels_like_f = weather_data['current']['feelslike_f']
        conditions = (
            f"Location: {weather_data['location']['name']}, {weather_data['location']['region']}\n"
            f"{date_str} {time_str}\n"
            f"Temperature: {current_temp_f} °F\n"
            f"Humidity: {weather_data['current']['humidity']}%\n"
            f"Feels Like: {feels_like_f} °F\n"
            f"Cloud Cover: {weather_data['current']['condition']['text']}\n"
            f"Wind: {weather_data['current']['wind_mph']} mph\n"
            f"Wind Gust: {weather_data['current']['gust_mph']} mph\n"
            f"Wind Direction: {weather_data['current']['wind_dir']}\n\n"
        )
        
        forecast = weather_data['forecast']['forecastday'][0]
        forecast_info = (
            f"Forecast for Today:\n"
            f"High Temperature: {forecast['day']['maxtemp_f']} °F\n"
            f"Minimum Temperature: {forecast['day']['mintemp_f']} °F\n"
            f"Chance of Precipitation: {forecast['day']['daily_chance_of_rain']}%\n"
            f"Total Precipitation: {forecast['day']['totalprecip_in']} in\n\n"
        )
        
        astro_info = (
            f"Astronomy Forecast for Today:\n"
            f"Sunrise: {forecast['astro']['sunrise']}\n"
            f"Sunset: {forecast['astro']['sunset']}\n"
            f"Moon Phase: {forecast['astro']['moon_phase']}\n"
            f"Moon Rise: {forecast['astro']['moonrise']}\n"
            f"Moon Set: {forecast['astro']['moonset']}\n"
        )

        label.config(text=conditions + forecast_info + astro_info)
    
    # Refresh the weather information every 5 minutes
    label.after(300000, update_weather, api_key, latitude, longitude, label)

def main():
    api_key = "d2db2aadf20b489fbe4112953242008"
    latitude = 30.5925727
    longitude = -87.0916525
    
    # Create the main window
    root = tk.Tk()
    root.title("Weather Information")
    root.geometry("285x550")
    root.configure(bg="#282c34")

    # Create a label to display the weather information
    weather_label = ttk.Label(root, text="", justify="center", font=("Helvetica", 12), background="#f0f0f0", borderwidth=2, relief="solid", padding=10)
    weather_label.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Create a button for manual refresh
    refresh_button = ttk.Button(root, text="Refresh", command=lambda: update_weather(api_key, latitude, longitude, weather_label))
    refresh_button.pack(pady=10)

    # Start the weather update loop
    update_weather(api_key, latitude, longitude, weather_label)

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
