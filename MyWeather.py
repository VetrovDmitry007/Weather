import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class MyWeather:
    """
    __init__(self, name_city)
     wr=MyWeather('Саратов')
    """
    def __init__(self, name_city):
        res = requests.get('https://sinoptik.com.ru/{}'.format(self._get_seo_city(name_city)))
        self._soup = BeautifulSoup(res.text, 'html.parser')
        self.region=self._soup.find('div', 'header__bottom_title-region').text

    def _get_seo_city(self, name_city):
        # из результатов поиска извлекаем name_city == Административный центр
        ls_res = requests.get('https://sinoptik.com.ru/api/suggest.php?q={}&l=ru'.format(name_city.lower())).json()
        if ls_res[0]['descr'].startswith('Административный центр') or ls_res[0]['descr'].startswith('Столица'):
            #i = ls_res[0]
            return ls_res[0]['seo']

    @property
    def get_all_weather(self):
        """
        Возвращает список погоды на 7 дней
        ----------------
        get_all_weather
        return:
        [ {'month':.., 'date':..,  'day':.., temp:.., title_t:..},
        {'month':.., 'date':..,  'day':.., temp:.., title_t:..}]

        wr=MyWeather('саратов')
        ls=wr.get_all_weather
        for i in range(7):
            for key, val in ls[i].items():
                print(key, val)
        """
        ls_weather = []
        for i in range(7):
            dict_weather = {}
            dict_weather['month'] = self._soup.find_all('div', 'weather__content_tab')[i].find('p','weather__content_tab-month').text
            dict_weather['date'] = self._soup.find_all('div', 'weather__content_tab')[i].find('p','weather__content_tab-date').text
            dict_weather['day'] = self._soup.find_all('div', 'weather__content_tab')[i].find('p','weather__content_tab-day').text.strip()
            dict_weather['temp'] = self._soup.find_all('div', 'weather__content_tab')[i].find('div', 'weather__content_tab-temperature').text.replace('\n',' ')
            dict_weather['title_t'] = self._soup.find_all('div', 'weather__content_tab')[i].find('div','weather__content_tab-icon').get('title')
            ls_weather.append(dict_weather)
        return ls_weather

    def get_weather(self,num_day):
        """
        Возвращает список погоды на выбранный день
        --------------
        get_weather()
        return: dict {'month':.., 'date':..,  'day':.., min_t:.., max_t:.., title_t:..}
        """
        dict_weather = {}
        dict_weather['month'] = self._soup.find_all('div', 'weather__content_tab')[num_day].find('p','weather__content_tab-month').text
        dict_weather['date'] = self._soup.find_all('div', 'weather__content_tab')[num_day].find('p','weather__content_tab-date').text
        dict_weather['day'] = self._soup.find_all('div', 'weather__content_tab')[num_day].find('p','weather__content_tab-day').text.strip()
        dict_weather['temp'] = self._soup.find_all('div', 'weather__content_tab')[num_day].find('div','weather__content_tab-temperature').text.replace('\n', ' ')
        dict_weather['title_t'] = self._soup.find_all('div', 'weather__content_tab')[num_day].find('div','weather__content_tab-icon').get('title')
        return dict_weather

    def get_weather_tomorrow(self):
        """
        Возвращает погоду на завтра
        :return: dict {'month':.., 'date':..,  'day':.., min_t:.., max_t:.., title_t:..}
        """
        return self.get_all_weather[1]

    def get_weather_curr(self):
        """
        Возвращает текущую погоду
        :return: dict {'month':.., 'date':..,  'day':.., min_t:.., max_t:.., title_t:..}
        """
        return self.get_all_weather[0]

if __name__=='__main__':
    wr=MyWeather('орел')
    print(wr.get_weather_tomorrow())
    print(wr.get_weather_curr())

    print(wr.region)
    ls=wr.get_all_weather
    [pprint(s) for s in ls]

