import requests


api_key = "6e5abcfd-cc04-4cdf-91af-1be710a5c50a"


def find_with_city(city, resp=15):
    lst = []
    response = requests.get(f"https://search-maps.yandex.ru/v1/?apikey={api_key}&text={city}+институт&format=json&lang=ru_RU&type=biz&results={resp}")
    res = response.json()
    res = res["features"]
    for elem in res:
        dct = elem["properties"]["CompanyMetaData"]
        result = {}
        for el in (dct):
            if el == "name":
                result[el] = (dct[el])
            if el == "url":
                result[el] = (dct[el])
            if el == "Phones":
                result[el] = (dct[el][0]["formatted"])
        if "url" not in result:
            result['url'] = 'Сайт не найден'
        if 'Phones' not in result:
            result["Phones"] = 'Телефоны не найдены'

        lst.append(result)
    return lst


# print(find_with_city("Пятигорск"))