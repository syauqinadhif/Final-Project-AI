import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import smtplib
import urllib.request
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import wikipedia

class WEATHER:
    def __init__(self):
        self.tempValue = ''
        self.city = ''
        self.currCondition = ''
        self.speakResult = ''

    def updateWeather(self):
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        URL = 'https://weather.com/en-LS/weather/today/l/202d469aad519ecb27eeaac350e06432ce637bbfb3f76de8acb391f6885983c6'
        result = requests.get(URL)
        src = result.content

        soup = BeautifulSoup(src, 'html.parser')

        city = ""
        for h in soup.find_all('h1'):
            cty = h.text
            cty = cty.replace('Weather', '')
            self.city = cty[:cty.find(',')]
            break

        spans = soup.find_all('span')
        for span in spans:
            try:
                if span['data-testid'] == "TemperatureValue":
                    self.tempValue = span.text[:-1]
                    break
            except Exception as e:
                pass

        divs = soup.find_all('div', class_='CurrentConditions--phraseValue--2xXSr')
        for div in divs:
            self.currCondition = div.text
            break

    def weather(self):
        from datetime import datetime
        today = datetime.today().strftime('%A')
        self.speakResult = "Currently in " + self.city + ", its " + self.tempValue + " degree, with " + self.currCondition
        return [self.tempValue, self.currCondition, today, self.city, self.speakResult]


w = WEATHER()


def dataUpdate():
    w.updateWeather()


def weather():
    return w.weather()

def latestNews(news=5):
    URL = 'https://www.cnnindonesia.com/nasional'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlineLinks = []
    headlines = []

    divs = soup.find_all('div', {'class': 'title'})

    count = 0
    for div in divs:
        count += 1
        if count > news:
            break
        a_tag = div.find('a')
        headlineLinks.append(a_tag.attrs['href'])
        headlines.append(a_tag.text)

    return headlines, headlineLinks


def maps(text):
    text = text.replace('maps', '')
    text = text.replace('map', '')
    text = text.replace('google', '')
    openWebsite('https://www.google.com/maps/place/' + text)


def giveDirections(startingPoint, destinationPoint):
    geolocator = Nominatim(user_agent='assistant')
    if 'current' in startingPoint:
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        startinglocation = geolocator.reverse(data['loc'])
    else:
        startinglocation = geolocator.geocode(startingPoint)

    destinationlocation = geolocator.geocode(destinationPoint)
    startingPoint = startinglocation.address.replace(' ', '+')
    destinationPoint = destinationlocation.address.replace(' ', '+')

    openWebsite('https://www.google.co.in/maps/dir/' + startingPoint + '/' + destinationPoint + '/')

    startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
    destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
    total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km  # .mile
    return str(round(total_distance, 2)) + 'KM'


def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)


def jokes():
    URL = 'https://icanhazdadjoke.com/'
    result = requests.get(URL, headers={"Accept": "application/json"})
    joke = result.json()['joke']
    return joke


def youtube(query):
    query = query.replace('play', ' ')
    query = query.replace('on youtube', ' ')
    query = query.replace('youtube', '')

    print("Searching for videos...")
    from youtubesearchpython import VideosSearch
    videosSearch = VideosSearch(query, limit=1)
    results = videosSearch.result()['result']
    print("Finished searching!")

    webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
    return "Enjoy..."


def googleSearch(query):
    if 'image' in query:
        query += "&tbm=isch"
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    webbrowser.open("https://www.google.com/search?q=" + query)
    return "Here you go..."


def sendWhatsapp(phone_no='', message=''):
    phone_no = '+62' + str(phone_no)
    webbrowser.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + message)


def email(rec_email=None, text="Hello, It's F.R.I.D.A.Y. here...", sub='F.R.I.D.A.Y.'):
    USERNAME = os.getenv('MAIL_USERNAME')  # email address
    PASSWORD = os.getenv('MAIL_PASSWORD')
    if not USERNAME or not PASSWORD:
        raise Exception(
            "MAIL_USERNAME or MAIL_PASSWORD are not loaded in environment, create a .env file and add these 2 values")

    if '@gmail.com' not in rec_email:
        return
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(USERNAME, PASSWORD)
    message = 'Subject: {}\n\n{}'.format(sub, text)
    s.sendmail(USERNAME, rec_email, message)
    print("Sent")
    s.quit()


def downloadImage(query, n=4):
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    URL = "https://www.google.com/search?tbm=isch&q=" + query
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')
    imgTags = soup.find_all('img', class_='yWs4tf')  # old class name -> t0fcAb

    if not os.path.exists('Downloads'):
        os.mkdir('Downloads')

    count = 0
    for i in imgTags:
        if count == n:
            break
        try:
            urllib.request.urlretrieve(i['src'], 'Downloads/' + str(count) + '.jpg')
            count += 1
            print('Downloaded', count)
        except Exception as e:
            raise e


def wikiResult(query):
    query = query.replace('wikipedia', '')
    query = query.replace('search', '')
    if len(query.split()) == 0:
        query = "wikipedia"
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return "Desired Result Not Found"


def main():
    while True:
        print("\nHi, I'm your chatbot. How can I assist you today?")
        user_input = input("You: ").lower()

        if user_input in ['quit', 'exit', 'bye']:
            break

        elif 'weather' in user_input or 'temperature' in user_input or 'forecast' in user_input:
            w.updateWeather()
            response = weather()
            print(response[4])

        elif 'news' in user_input:
            headlines, _ = latestNews()
            for i, headline in enumerate(headlines, start=1):
                print(f"{i}. {headline}")

        elif 'directions' in user_input or 'navigate' in user_input or 'maps' in user_input:
            print("Please provide starting and destination points:")
            startingPoint = input("Starting Point: ")
            destinationPoint = input("Destination Point: ")
            distance = giveDirections(startingPoint, destinationPoint)
            print(f"Distance between {startingPoint} and {destinationPoint}: {distance}")

        elif 'wiki' in user_input or 'wikipedia' in user_input or 'search' in user_input:
            query = user_input.replace('wiki', '').replace('wikipedia', '').replace('search', '')
            print(wikiResult(query))

        elif 'joke' in user_input or 'funny' in user_input:
            print(jokes())

        elif 'youtube' in user_input or 'video' in user_input or 'play' in user_input:
            query = user_input.replace('youtube', '').replace('video', '').replace('play', '')
            youtube(query)

        elif 'google' in user_input or 'search' in user_input or 'image' in user_input:
            query = user_input.replace('google', '').replace('search', '').replace('image', '')
            googleSearch(query)

        elif 'whatsapp' in user_input or 'message' in user_input or 'send' in user_input:
            phone_no = input("Enter phone number: ")
            message = input("Enter message: ")
            sendWhatsapp(phone_no, message)

        elif 'email' in user_input or 'mail' in user_input:
            rec_email = input("Enter recipient email address: ")
            subject = input("Enter subject: ")
            content = input("Enter email content: ")
            email(rec_email, content, subject)

        else:
            print("Sorry, I don't understand that. Please ask something else.")

if __name__ == "__main__":
    main()
