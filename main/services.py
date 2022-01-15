import os
from math import acos, sin, cos

from PIL import Image
from django.core.mail import send_mail

from tinder import settings


def watermark_photo(image_path):
    """
    Накладывает водяной знак на фото
    """
    base_image = Image.open(image_path)
    watermark = Image.open('static/main/images/water_mark.png')
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (30, 30), mask=watermark)
    transparent = transparent.convert('RGB')

    image_path = os.path.join(settings.MEDIA_ROOT, image_path)
    transparent.save(image_path)


def check_match(user1, user2):
    """
    Проверяет взаимна ли симпатия пользователей

    Если симпатия взаимна, возвращает True, иначе False
    """
    if user1 in user2.likes.all() and user2 in user1.likes.all():
        return True
    return False


def report_mutual_sympathy(user1, user2):
    """
    Оповещает пользователей о взаимной симпатии
    """
    mail_subject = 'Взаимная симпатия'  # тема сообщения
    mail_message = 'Вы понравились {name}! Почта участника: {email}'  # текст сообщения
    from_email = 'toropyno.evgeny@gmail.com'  # email host
    send_mail(
        mail_subject,
        mail_message.format(name=user1.get_full_name(), email=user1.email),
        from_email,
        [user2.email],
    )
    send_mail(
        mail_subject,
        mail_message.format(name=user2.get_full_name(), email=user2.email),
        from_email,
        [user1.email],
    )


def get_distance_between_clients(user1, user2):
    """
    Возвращает расстояние между двумя пользователями
    """
    if user1.has_coords and user2.has_coords:
        return get_distance_between_points(user1.longitude, user1.latitude, user2.longitude, user2.latitude)


def get_distance_between_points(lon1, lat1, lon2, lat2):
    """
    Рассчитывает и возвращает расстояние между двумя точками

    lon1, lat1 - долгота и широта первой точки
    lon2, lat2 - долгота и широта второй точки
    """
    # переводим градусы в радианы, т.к. этого требуют тригонометрические функции
    args = [lon1, lat1, lon2, lat2]
    lon1, lat1, lon2, lat2 = map(lambda x: float(x) / 57.3, args)

    earth_radius = 6371.009  # радиус Земли в км

    # расчет расстояния между точками https://en.wikipedia.org/wiki/Great-circle_distance
    delta = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1))
    distance = delta * earth_radius
    return distance


def get_longitude_delta(distance):
    """
    На основе значения distance рассчитывает отклонение значения longitude в градусах
    """
    # один градус географической долготы равен 111км
    delta = distance / 111
    return delta


def get_latitude_delta(distance, latitude):
    """
    На основе значения distance рассчитывает отклонение значения latitude в градусах
    """
    # количество км в одном градусе географической широты непостоянно
    # и рассчитывается по следующей формуле
    delta = distance / (111.3 * cos(float(latitude) / 57.3))
    return abs(delta)
