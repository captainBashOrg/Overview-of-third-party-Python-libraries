#"""
#Изучены библиотеки pillow и requests
#Очччччччень понравилась библиотека pillow. Пишешь скрипт, натравливаешь его на папку, наливаешь себе кофе  и с интересом наблюдаешь, как автоматика для тысяч карточек делает мини-изображение, преобразует в сепию (тут чуть сложнее) или в монохром, даже в негатив умеет.  Порабовала конверсия в CMYK, печатники оценят.
#
#Вот только "накатить" на карточки тени (по советам с хабра) не получилось. Покопаю еще.
#
#
#Библиотека requests. Получение актуальных данных со специализированных сайтов, рассмотрено получение прогноза погоды и точного времени.
#Самое сложное – подобрать набор для params, но и тут руки делают.
#"""

print("Обзор сторонних библиотек Python")
from PIL import Image, ImageDraw, ImageChops
import os

#files_jpg = []
if __name__ == '__main__':
    for root, dirs, files in os.walk('c:\jpgs'):
        for file in files:
            if  file.endswith(('.jpg', '.JPG', '.jpeg', '.JPEG'  ) ):
                #print(os.path.join(root, file))
                filename = os.path.join(root, file)
                #files_jpg.append(filename)

                with Image.open(filename) as img:
                    img.load()
                a = file.split('.')

                root2 = 'c:\\rez'

                #converted_img_plus_90 = img.transpose(Image.ROTATE_90)   #поворот на 90 град вправо
                #file2= a[0] + '_90.png'
                #filename2 = os.path.join(root, file2)
                #converted_img_plus_90.save(filename2)
                #converted_img_plus_90.show()

                #file3= a[0] + '_270.png'
                #filename3 = os.path.join(root, file3)
                #converted_img_plus_270 = img.transpose(Image.ROTATE_270)   #поворот на 90 град влево (или на 270 град вправо
                #converted_img_plus_270.save(filename3)
                #converted_img_plus_270.show()

                file4= a[0] + '_45.png'
                filename4 = os.path.join(root2, file4)
                converted_img_45 = img.rotate(45)   #поворот на 45 град
                converted_img_45.save(filename4)


                file5= 'rez_'+ a[0] + '_45.png'
                filename5 = os.path.join(root2, file5)
                resized_image_45 = converted_img_45.resize((320, 320)) # уменьшение размера (масштабирование)
                resized_image_45.save( filename5 )


                cmyk_img = img.convert('CMYK') # перегонка в CMYK
                file6 = 'CMYK'+ a[0] + '.' + a[1]
                filename6 = os.path.join(root2, file6)
                cmyk_img.save( filename6 )

                negative_img = ImageChops.invert(img)
                file6 = 'negative'+ a[0] + '.' + a[1]
                filename6 = os.path.join(root2, file6)
                negative_img.save( filename6 )

    import requests

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 56.253862,  # широта  56.253862, сросовываем с янджекс сарт
        "longitude": 43.998967,  # долгота  43.998967
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        # минимальная и максимальная температура, сумма осадков
        "timezone": "Europe/Moscow"  # временная зона для   НН раздают на сайте  https://open-meteo.com/en/docs
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        #  индекс 0 представляет собой данные на текущий день, индекс 1   данные на завтра
        now_temp_min = data['daily']['temperature_2m_min'][0]
        now_temp_max = data['daily']['temperature_2m_max'][0]
        now_precipitation = data['daily']['precipitation_sum'][0]

        tomorrow_temp_min = data['daily']['temperature_2m_min'][1]
        tomorrow_temp_max = data['daily']['temperature_2m_max'][1]
        tomorrow_precipitation = data['daily']['precipitation_sum'][1]

        print(f"Сегодня:")
        print(f"Минимальная температура:  {now_temp_min}°C")
        print(f"Максимальная температура: {now_temp_max}°C")
        print(f"Количество осадков: {now_precipitation} мм")

        print(f"Прогноз погоды на завтра:")
        print(f"Минимальная температура: {tomorrow_temp_min}°C")
        print(f"Максимальная температура: {tomorrow_temp_max}°C")
        print(f"Ожидаемое количество осадков: {tomorrow_precipitation} мм")
    else:
        print(f"Ошибка {response.status_code}: {response.text}")

        #  подумать над сбором статистики, складывать в файл и рисовать что-то наподобие MRTG
        #  нужно прикрутить к расписанию задание, чтобы стартовал приложение в заданный час.



    params = {"format":"dd/MM/yyyy HH:mm", "tz":"Europe/Moscow"}
    response = requests.get('https://tools.aimylogic.com/api/now/', params = params)

    if response.status_code == 200:
        json_response =  response.json()#
        date_time = json_response['formatted'].split(' ')
        print(f"Сегодня  {date_time[0]}, сейчас {date_time[1]} по Москве" )
