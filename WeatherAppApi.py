import requests
import customtkinter as ctk
from PIL import Image, ImageTk
import io

# Store API Key Here
API_KEY = "7ca0e9b701ce269bf9c323610751ae0a"

# Weather emoji mapping
weather_emojis = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "🌥️",
    "broken clouds": "☁️",
    "shower rain": "🌧️",
    "rain": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "haze": "🌫️",
    "fog": "🌫️",
}

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    try:
        data = response.json()
        if response.status_code == 200:
            weather = {
                "city": data["name"],
                "province": data["sys"].get("state", "N/A"),  # Check for state or province
                "temperature": f"{data['main']['temp']}°C",
                "description": data["weather"][0]["description"].title(),
                "humidity": f"{data['main']['humidity']}%",
                "wind_speed": f"{data['wind']['speed']} m/s",
                "icon": data["weather"][0]["icon"]
            }
            print(weather)  # Print to terminal
            return weather
        else:
            error_message = f"Error: {data.get('message', 'Unable to fetch weather data.')} "
            print(error_message)  # Print error to terminal
            return {"error": error_message}
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Print exception to terminal
        return {"error": error_message}

def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        result_label.configure(text="City name is required.")
        return
    
    weather_data = get_weather(city)
    
    if "error" in weather_data:
        result_label.configure(text=weather_data["error"], fg_color="#ff4c4c")
        icon_label.configure(image="")
    else:
        # Get the emoji based on the weather description
        description_lower = weather_data['description'].lower()
        emoji = weather_emojis.get(description_lower, "🌍")  # Default to Earth emoji if not found
        
        # Display province/state if available
        province = weather_data["province"]
        weather_text = (f"Weather in {weather_data['city']} ({province})\n"
                        f"{emoji} Temperature: {weather_data['temperature']}\n"
                        f"Description: {weather_data['description']}\n"
                        f"Humidity: {weather_data['humidity']}\n"
                        f"Wind Speed: {weather_data['wind_speed']}")
        result_label.configure(text=weather_text, fg_color="#2c3e50")
        
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = Image.open(io.BytesIO(icon_response.content))
        icon_data = icon_data.resize((100, 100))
        icon_img = ImageTk.PhotoImage(icon_data)
        icon_label.configure(image=icon_img)
        icon_label.image = icon_img

# Create GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Weather App")
root.geometry("500x450")
root.resizable(False, False)

frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)

title_label = ctk.CTkLabel(frame, text="Weather App", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

city_entry = ctk.CTkEntry(frame, placeholder_text="Enter city name", width=300)
city_entry.pack(pady=10)

search_button = ctk.CTkButton(frame, text="Get Weather", command=fetch_weather)
search_button.pack(pady=10)

icon_label = ctk.CTkLabel(frame, text="")
icon_label.pack()

result_label = ctk.CTkLabel(frame, text="", wraplength=400, font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
