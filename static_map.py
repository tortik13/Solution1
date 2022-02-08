import requests
from io import BytesIO


def request_static_map(coordinates, delta=None, z='7', type="map", point=None):
    """
    запрос к StaticMapsAPI
    :param coordinates: кортеж строк (долгота, широта) - результат работы get_coordinates()
    :param delta: кортеж строк (размер по долготе и широте) - результат работы get_delta()
    :param z: строка (уровень масштабирования, макс - 17)
    :param type: строка: (map - тип карты "Схема"; sat - тип карты "Спутник"; sat, skl - тип карты "Гибрид".)
    :param point: строка: метка на карте
    :return: изображение карты
    """
    response = requests.request(
        method='GET',
        url="http://static-maps.yandex.ru/1.x/",
        params={"ll": ",".join(coordinates),
                "spn": (",".join(delta) if delta else None),
                "z": z,
                "l": type,
                "pt": (",".join([coordinates[0], coordinates[1], point]) if point else None)
                }
    )
    map_file = BytesIO(response.content)
    return map_file
