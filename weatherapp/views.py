import requests


from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=your api  key' #api key
    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    
    form = CityForm()
    cities = City.objects.all()
    
    weather_data =[]
    
    for city in cities:
        
        r = requests.get(url.format(city)).json()
        temperature_fahrenheit = r['main']['temp']
        temperature_celsius = round((temperature_fahrenheit - 32) * 5/9)
        
        city_weather={
            'city': city.name,
            'temperature': temperature_celsius,
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)
    
    weather_data.reverse()
    
    context ={"weather_data": weather_data, "form":form}
    
    
    return render(request, 'weather/weather.html', context)
