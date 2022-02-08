import requests
import oxr


def request_toponym(toponym_to_find='Варкута'):
    """
    определить картографический объект по его адресу
    :param toponym_to_find: адрес поиска
    :return: кортеж (коды состояния HTTP, первый топоним из ответа геокодера)
    """
    response = requests.request(
        method='GET',
        url="http://geocode-maps.yandex.ru/1.x/",
        params={"apikey": oxr.APP_KEY,
        "geocode": toponym_to_find,
        "format": "json"
                }
    )
    if not response:
        return response.status_code, {}

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return response.status_code, toponym


def get_coordinates(toponym):
    """
    определить координаты объекта
    :param toponym: первый топоним из ответа геокодера (результат работы функции request_toponym)
    :return: кортеж строк (долгота и широта)
    """
    toponym_coodrinates = toponym["Point"]["pos"]
    return tuple(toponym_coodrinates.split(" "))


def get_delta(toponym):
    """
    определить размеры объекта
    :param toponym: первый топоним из ответа геокодера (результат работы функции request_toponym)
    :return: кортеж строк (размер по долготе и широте)
    """
    toponym_envelope = toponym['boundedBy']['Envelope']
    longlower, latlower = [float(i) for i in toponym_envelope['lowerCorner'].split()]
    longupper, latupper = [float(i) for i in toponym_envelope['upperCorner'].split()]
    long = str((longupper - longlower) / 2)
    lat = str((latupper - latlower) / 2)
    return long, lat


def get_postal_code(toponym):
    """
    определить почтовый индекс объекта
    :param toponym: первый топоним из ответа геокодера (результат работы функции request_toponym)
    :return: почтовый индекс
    """
    return toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]


if __name__ == "__main__":
    if request_toponym()[0] == 200:
        print(get_coordinates(request_toponym()[1]))
        print(get_delta(request_toponym()[1]))
        print(get_postal_code(request_toponym('Варкута, ул.Мира')[1]))
    else:
        print(f'Http статус: {request_toponym()[0]}')
