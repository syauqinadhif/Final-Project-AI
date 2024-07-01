from easygoogletranslate import EasyGoogleTranslate
import requests
from bs4 import BeautifulSoup
import webbrowser
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import wikipedia
# test


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

        divs = soup.find_all(
            'div', class_='CurrentConditions--phraseValue--mZC_p')
        for div in divs:
            self.currCondition = div.text
            break

    def weather(self):
        from datetime import datetime
        today = datetime.today().strftime('%A')
        self.speakResult = "Currently in " + self.city + ", its " + \
            self.tempValue + " degree, with " + self.currCondition
        return [self.tempValue, self.currCondition, today, self.city, self.speakResult]


w = WEATHER()


def dataUpdate():
    w.updateWeather()


def weather():
    return w.weather()



def latestNews(news=5):
    URL = 'https://detik.com'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlines = []
    headlineLinks = []

    articles = soup.find_all('article', class_='list-content__item column')

    count = 0
    for article in articles:
        if count >= news:
            break
        h2_tag = article.find('h2', class_='media__title')
        if h2_tag:
            a_tag = h2_tag.find('a', class_='media__link')
            if a_tag:
                headline_text = a_tag.text.strip()
                headlines.append(headline_text)
                headlineLinks.append(a_tag.attrs['href'])
                count += 1

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

    openWebsite('https://www.google.co.in/maps/dir/' +
                startingPoint + '/' + destinationPoint + '/')

    startinglocationCoordinate = (
        startinglocation.latitude, startinglocation.longitude)
    destinationlocationCoordinate = (
        destinationlocation.latitude, destinationlocation.longitude)
    total_distance = great_circle(
        startinglocationCoordinate, destinationlocationCoordinate).km  # .mile
    return str(round(total_distance, 2)) + 'KM'


def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)

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
    webbrowser.open('https://web.whatsapp.com/send?phone=' +
                    phone_no + '&text=' + message)

def wikiResult(query):
    query = query.replace('wikipedia', '')
    query = query.replace('search', '')
    if len(query.split()) == 0:
        query = "wikipedia"
    try:
        return wikipedia.summary(query, sentences=4)
    except Exception as e:
        return "Desired Result Not Found"


def translator(input):
    command = input
    translator = EasyGoogleTranslate(
        source_language='id',
        target_language='en',
        timeout=10
    )
    user_input = translator.translate(command)
    return user_input


def main():
    while True:
        print("\nHi, I'm your chatbot. How can I assist you today?")
        command = input("You: ").lower()
        user_input = translator(command)

        # translator = EasyGoogleTranslate(
        #     source_language='id',
        #     target_language='en',
        #     timeout=10
        # )
        # user_input = translator.translate(command)

        if user_input in ['quit', 'exit', 'bye']:
            break

        elif 'weather' in user_input or 'temperature' in user_input or 'forecast' in user_input:
            w.updateWeather()
            response = weather()
            print(response[4])

        elif 'news' in user_input:
            # headlines, _ = latestNews()
            # for i, headline in enumerate(headlines, start=1):
            #     print(f"{i}. {headline}")
            headlines,headlineLinks = latestNews(5)
            for idx, headline in enumerate(headlines, start=1):
                print() 
                print(f"{idx}. {headline}")
                print(f"Link: {headlineLinks[idx-1]}")
                print() 


        elif 'directions' in user_input or 'navigate' in user_input or 'maps' in user_input:
            print("Please provide starting and destination points:")
            startingPoint = input("Starting Point: ")
            destinationPoint = input("Destination Point: ")
            distance = giveDirections(startingPoint, destinationPoint)
            print(
                f"Distance between {startingPoint} and {destinationPoint}: {distance}")

        elif 'wiki' in user_input or 'wikipedia' in user_input or 'search' in user_input:
            query = user_input.replace('wiki', '').replace(
                'wikipedia', '').replace('search', '')
            print(wikiResult(query))

        elif 'youtube' in user_input or 'video' in user_input or 'play' in user_input:
            query = user_input.replace('youtube', '').replace(
                'video', '').replace('play', '')
            youtube(query)

        elif 'google' in user_input or 'search' in user_input or 'image' in user_input:
            query = user_input.replace('google', '').replace(
                'search', '').replace('image', '')
            googleSearch(query)

        elif 'whatsapp' in user_input or 'message' in user_input or 'send' in user_input:
            phone_no = input("Enter phone number: ")
            message = input("Enter message: ")
            sendWhatsapp(phone_no, message)

        else:
            print("Sorry, I don't understand that. Please ask something else.")


if __name__ == "__main__":
    main()
