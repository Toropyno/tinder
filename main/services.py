import os

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
