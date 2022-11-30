from flask import Flask, request
import base64
import fast_bitrix24
import asyncio
from urllib.request import urlopen

app = Flask(__name__)

languagespisok = {'Английский базовый': '1358', 'Английский продвинутый': '1360', 'Немецкий базовый': '1362', 'Немецкий продвинутый': '1364', 'Другое': '1366'}
citizenshipspisok = {'гражданин РФ': '400', 'нерезидент РФ': '1356', 'СНГ': '402'}
tripsspisok = {'Да, на короткий срок': '710', 'Да, на длительный срок': '710', 'Нет': '712'}
educationspisok = {'Среднее': '1458', 'Специальное': '1462', 'Неоконченное высшее': '1456', 'Высшее': '1454'}
statusspisok = {'Трудоустроен': '1464', 'Безработный': '1466', 'Студент': '1468', 'Пенсионер': '1470', 'Самозанятый': '3298'}
facehairspisok = {'Отсутствует': '3118', 'Усы': '1308', 'Борода': '1310', 'Щетина': '1312', 'Американская бородка': '1314', 'Монобровь': '1316'}
stomatospisok = {'Без особенностей': '1288', 'Голливудская улыбка': '1296', 'Брекеты': '4696', 'Редкие зубы': '1290', 'Кривые зубы': '1292', 'Отсутствие видимых зубов': '1294'}
speechspisok = {'Отчётливая': '1298', 'Искаженная': '1300', 'Картавость': '1302', 'Шепелявость': '1304', 'Акцент': '1306'}
tattoospisok = {'Без татуировок': '390', 'Невидимая (под одеждой)': '388', 'На видном месте': '1324', 'Многочисленные татуировки': '1326'}
cosmetologyspisok = {'Естественная': '1328', 'Имплантаты': '1330', 'Ботокс': '1332'}
cosmeticspisok = {'Отсутствуют': '1334', 'Татуаж': '1336', 'Нарощенные ресницы': '1338', 'Пирсинг': '1340', 'Другое': '3242'}
breastspisok = {'нет':'680', '0':'680', '1':'680', '2':'682', '3':'684', '4':'686','5':'686','6':'686','7':'686','8':'686'}
clothesspisok = {'XS 40-42': '670', 'S 44': '672', 'M 46':'674', 'L 48': '676', 'XL 50-52':'678', 'XXL 54-56': '1174', 'XXXL 56-58': '1176'}
hairstylespisok = {'Наголо': '1202', 'Коротко': '1204', 'Средняя длина': '1206', 'Длинные': '1208', 'Редкие/С плешью': '1210'}
hairspisok = {'Блонд': '660', 'Темно-русый': '662', 'Брюнет/ка': '664', 'Рыжий': '666', 'Светло-русый': '668', 'Шатен/ка': '1212', 'Седой': '1214', 'Седой, но крашенный': '1216', 'Креативное окрашивание': '1216'}
eyecolorspisok = {'Серыe': '646', 'Зеленый': '648', 'Синий': '650', 'Голубой': '650', 'Янтарный': '1248', 'Ореховый': '652', 'Карий': '652', 'Черный':'1250', 'Смешанный': '1250'}
eyesspisok = {'Миндалевидные': '1236', 'Восточный разрез':'1238', 'Круглые': '1240', 'Выпуклые глаза': '1242', 'Близко посаженные': '1244', 'Широко посаженные': '1246'}
nosespisok = {'Прямой': '1264', 'Греческий': '1268', 'Римский': '1270', 'Курносый': '1272', 'Картошкой': '1274', 'Ястрибиный': '1276', 'С горбинкой': '1266'}
facespisok = {'Круглое': '1194', 'Овальное': '1192', 'Удлиненное': '1196', 'Треугольное': '1200', 'Квадратное': '1198'}
racespisok = {'Американоидная': '1344', 'Европеоидная': '1342', 'Монголоидная': '1346', 'Негроидная': '1348', 'Эфиопская': '1350', 'Метис': '1352', 'Мулат': '1354'}
hobbyspisok = {'Танцы' : '1398', 'Вокал': '1400', 'Спорт': '1402', 'Массовка': '3158', 'Блогер': '3162', 'Домоводство': '3260', 'Компьютерные игры': '3258', 'Кулинария': '3256', 'Любительская живопись': '3254', 'Любительская фотография': '3252', 'Рукоделие': '3250', 'Стилист/визажист': '3164', 'ДАЛЕЕ': 'ДАЛЕЕ'}
profspisok = {'Моделью': '356', 'Актером': '364', 'Актер Массовых сцен': '364', 'Хостес': '362',
              'Актером дубляжа': '5845', 'Арт-директором': '386', 'Артистом цирка': '1432', 'Бариста': '500', 'Барменом': '370', 'Блогером': '360',
              'Букером/Рекрутом': '384', 'Визажистом': '1422', 'Водитель': '1436', 'Диджеем': '372', 'Звукорежиссёром': '1424', 'Ичар менеджером': '570',
              'Каскадёром': '1434', 'Кастинг директором': '1426', 'Онлайн ведущий': '358', 'Организатором Event мероприятий': '1418', 'Официант': '1430', 'Певцом': '366',
              'Переводчиком': '376', 'Промоутером': '380', 'Скаут': '382', 'Стилистом': '1420', 'Танцором': '368', 'Телохранителем': '374', 'Фотографом': '1428', 'ДАЛЕЕ': 'ДАЛЕЕ'}
artspisok = {'Аранжировщик': '1406', 'Исполнитель': '1408', 'Комик': '1414', 'Композитор': '1404', 'Писатель/поэт': '1410', 'Стендапер': '1412', 'ДАЛЕЕ': 'ДАЛЕЕ'}
qualitiesspisok = {'Дружелюбность': '1370', 'Коммуникабельность': '1368', 'Активность': '1374', 'Ответственность': '1372', 'Пунктуальность': '1376', 'ДАЛЕЕ': 'ДАЛЕЕ'}
characterspisok = {'Агрессивный': '1378', 'Импульсивный': '1380', 'Замкнутый': '1382', 'Нерешительный': '1384', 'Вспыльчивый': '1386', 'Безэмоциональный': '1388',
                   'Жизнерадостный': '3126', 'Отзывчивый': '3128', 'Решительный': '3130', 'Спокойный': '3132', 'ДАЛЕЕ': 'ДАЛЕЕ'}
typespisok = {'Веселый': '1392', 'Драматический': '1390', 'Коммерческий': '1394', 'Представительный': '1396', 'ДАЛЕЕ': 'ДАЛЕЕ'}







@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            print('VSE OK')
            hobby1 = []
            prof1 = []
            art1 = []
            qualities1 = []
            character1 = []
            type1 = []
            name = request.form.get('Imya')
            family = request.form.get('Familiya')
            otchestvo = request.form.get('Otchestvo')
            phone = request.form.get('Telefon')
            email = request.form.get('Email')
            link = request.form.get('Ssylka')
            photo = str(request.form.get('photo'))
            city = request.form.get('gorod')  #
            pol = request.form.get('Pol') #
            date = str(request.form.get('Data_rozhdeniya'))
            age = request.form.get('Vozrast')
            marriage = request.form.get('Semejnoe_polozhenie') #
            kids = request.form.get('Nalichie_detej') #
            trips = request.form.get('Komandirovka') #
            citizenship = request.form.get('Grazhdanstvo') #
            passport = request.form.get('zagran_pasport') #
            language = request.form.get('Inostrannye_yazyki')
            language2 = request.form.get('Inostrannye_yazyki2')
            person = request.form.get('Tip_vneshnosti') #
            race = request.form.get('Rasovaya_prinadlezhnost') #
            skin = request.form.get('Cvet_kozhi') #
            face = request.form.get('Forma_lica') #
            nose = request.form.get('Forma_nosa')
            eyes = request.form.get('Forma_glaz')
            eyecolor = request.form.get('Cvet_glaz')
            lips = request.form.get('Guby')
            hair = request.form.get('Cvet_volos')
            haircut = request.form.get('Strizhka')
            hairlength = int(str(request.form.get('Dlina_volos')))
            rost = request.form.get('Rost1')
            rost2 = int(str(request.form.get('Rost2')))
            shoes = int(str(request.form.get('Razmer_obuvi')))
            clothes = request.form.get('Razmer_odezhdy')
            body = request.form.get('Teloslozhenie')
            waist = int(str(request.form.get('Taliya')))
            hips = int(str(request.form.get('Bedra')))
            bust = int(str(request.form.get('Byust')))
            chest = request.form.get('Razmer_grudi')
            cosmetic = request.form.get('Kosmeticheskie')
            cosmetology = request.form.get('Kosmetologicheskie')
            tattoo = request.form.get('Tatu')
            stomato = request.form.get('Stomatologicheskie')
            speech = request.form.get('Rechevye')
            facehair = request.form.get('Rastitelnost_lico')
            bodyhair = request.form.get('Rastitelnost_grud')
            status = request.form.get('Social_status')
            education = request.form.get('Obrazovanie')
            hobby = str(request.form.get('Hobbi')).split('; ')
            prof = str(request.form.get('Professiya')).split('; ')
            achievments = request.form.get('Professional_dostizheniya')
            dopnaviki = request.form.get('Dopolnitelnye_navyki')
            art = str(request.form.get('Tvorcheskaya_deyatelnost')).split('; ')
            qualities = str(request.form.get('Osnovnye_kachestva')).split('; ')
            character = str(request.form.get('Harakter')).split('; ')
            type = str(request.form.get('Tipazh')).split('; ')
            under = request.form.get('Reklama_belya')
            orientation = request.form.get('Seksualnaya_orientaciya')
            print('VSE OK2')
            print(photo)
            date = date.replace('-', '.')
            if city == 'Москва':
                city = '564'
            else:
                city = '566'

            if pol == 'Женский':
                pol = '554'
            else:
                pol = '552'

            if marriage == 'Женат/замужем':
                marriage = '698'
            else:
                marriage = '700'

            if kids == 'Да':
                kids = '706'
            else:
                kids = '708'

            if language in languagespisok:
                language = languagespisok[language]

            if trips in tripsspisok:
                trips = tripsspisok[trips]

            if citizenship in citizenshipspisok:
                citizenship = citizenshipspisok[citizenship]
            else:
                citizenship = None

            if passport == 'действующий':
                passport = 392
            else:
                passport = 394

            if person == 'Славянский':
                person = 638
            elif person == 'Европейский':
                person = 640
            elif person == 'Монгольский':
                person = 642
            elif person == 'Афро-американский':
                person = 644

            if race in racespisok:
                race = racespisok[race]
            else:
                race = None

            if skin == 'Белый':
                skin = '654'
            elif skin == 'Смуглый':
                skin = '656'
            elif skin == 'Загорелый':
                skin = '658'
            elif skin == 'Чёрный':
                skin = '1190'
            else:
                skin = None

            if face in facespisok:
                face = facespisok[face]
            else:
                face = None

            if nose in nosespisok:
                nose = nosespisok[nose]
            else:
                nose = None

            if eyes in eyesspisok:
                eyes = eyesspisok[eyes]
            else:
                eyes = None

            if eyecolor in eyecolorspisok:
                eyecolor = eyecolorspisok[eyecolor]
            else:
                eyecolor = None

            if lips == 'Естественные':
                lips = 3214
            elif lips == 'Тонкие':
                lips = 3216
            elif lips == 'Пухлые':
                lips = 3218
            elif lips == 'Неровные':
                lips = 3220
            else:
                lips = 3214

            if hair in hairspisok:
                hair = hairspisok[hair]
            else:
                hair = None

            if haircut in hairstylespisok:
                haircut = hairstylespisok[haircut]

            if rost == 'Низкий (до 160 см)':
                rost = '1156'
            elif rost == 'Средний (до 180)':
                rost = '1158'
            elif rost == 'Высокий (свыше 180)':
                rost = '1160'

            if clothes in clothesspisok:
                clothes = clothesspisok[clothes]
            else:
                clothes = None

            if body == 'Статный':
                body = '1164'
            elif body == 'Сутулый':
                body = '1166'
            elif body == 'Стройный':
                body = '1168'
            elif body == 'Дистрофия':
                body = '1170'
            elif body == 'Полное':
                body = '1172'
            elif body == 'Спортивный':
                body = '1162'

            if chest in breastspisok:
                chest = breastspisok[chest]
            else:
                chest = None

            if cosmetic in cosmeticspisok:
                cosmetic = cosmeticspisok[cosmetic]
            else:
                cosmetic = '3242'

            if cosmetology in cosmetologyspisok:
                cosmetology = cosmetologyspisok[cosmetology]
            else:
                cosmetology = None

            if tattoo in tattoospisok:
                tattoo = tattoospisok[tattoo]
            else:
                tattoo = None
            print('VSE OK4')
            if stomato in stomatospisok:
                stomato = stomatospisok[stomato]
            else:
                stomato = None

            if speech in speechspisok:
                speech = speechspisok[speech]
            else:
                speech = None

            if facehair in facehairspisok:
                facehair = facehairspisok[facehair]
            else:
                facehair = None

            if bodyhair == 'Отсутствует':
                bodyhair = '1318'
            elif bodyhair == 'Немного':
                bodyhair = '1320'
            elif bodyhair == 'Много':
                bodyhair = '1322'

            if status in statusspisok:
                status = statusspisok[status]
            else:
                status = None

            if education in educationspisok:
                education = educationspisok[education]
            else:
                education = None

            for i in hobby:
                if i in hobbyspisok:
                    hobby1.append(hobbyspisok[i])
                else:
                    continue

            for i in prof:
                if i in profspisok:
                    prof1.append(profspisok[i])
                else:
                    continue

            for i in art:
                if i in artspisok:
                    art1.append(artspisok[i])
                else:
                    continue

            for i in qualities:
                if i in qualitiesspisok:
                    qualities1.append(qualitiesspisok[i])
                else:
                    continue

            for i in character:
                if i in characterspisok:
                    character1.append(characterspisok[i])
                else:
                    continue

            for i in type:
                if i in typespisok:
                    type1.append(typespisok[i])
                else:
                    continue

            if orientation == 'Гетеросексуальность':
                orientation = '1472'
            elif orientation == 'Гомосексуальность':
                orientation = '1474'
            elif orientation == 'Бисексуальность':
                orientation = '1476'

            if under == 'Да':
                under = '702'
            elif under == 'Нет':
                under = '704'

            print('Beginning file download with urllib2...')
            datatowrite = urlopen(photo).read()
            encoded_string = base64.b64encode(datatowrite)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = {'fields': {
                'NAME': name,
                'LAST_NAME': family,
                'SECOND_NAME': otchestvo,
                'UF_CRM_1628506279': city,
                'SOURCE_ID': 'UC_ZFRLHN',
                'PHONE': [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
                'EMAIL': [{"VALUE": email, "VALUE_TYPE": "WORK"}],
                'UF_CRM_1628805417': {"fileData": [f'Дада image_file.jpg', str(encoded_string)[2:-1]]},
                'UF_CRM_T_SSYLKANASOC': link,
                'UF_CRM_1628012402': pol,
                'BIRTHDATE': date,
                'UF_CRM_1629229853': age,
                'UF_CRM_1628804126': marriage,
                'UF_CRM_1628804713': kids,
                'UF_CRM_1628804986': trips,
                'UF_CRM_1627590723': [citizenship],
                'UF_CRM_1627589901': passport,
                'UF_CRM_1629237872': [language],
                'UF_CRM_1629237914': language2,
                'UF_CRM_1628801734': person,
                'UF_CRM_1629237675': race,
                'UF_CRM_1628801990': skin,
                'UF_CRM_1629230716': face,
                'UF_CRM_1629236858': nose,
                'UF_CRM_1629231263': [eyes],
                'UF_CRM_1628801902': eyecolor,
                'UF_CRM_1630579845': [lips],
                'UF_CRM_1628802115': hair,
                'UF_CRM_1629230810': haircut,
                'UF_CRM_1628802217': hairlength,
                'UF_CRM_1629230008': rost,
                'UF_CRM_1628802392': rost2,
                'UF_CRM_1628802811': shoes,
                'UF_CRM_1628802517': clothes,
                'UF_CRM_1629230103': body,
                'UF_CRM_1628802611': waist,
                'UF_CRM_1628802735': hips,
                'UF_CRM_1628802909': bust,
                'UF_CRM_1628803011': chest,
                'UF_CRM_1629237578': [cosmetic],
                'UF_CRM_1629237486': [cosmetology],
                'UF_CRM_1627589850': tattoo,
                'UF_CRM_1629237039': stomato,
                'UF_CRM_1629237136': [speech],
                'UF_CRM_1629237245': [facehair],
                'UF_CRM_1629237308': bodyhair,
                'UF_CRM_1629239167': [status],
                'UF_CRM_1629239095': [education],
                'UF_CRM_1629238198': hobby1,
                'UF_CRM_1627586659': prof1,
                'UF_CRM_1628803639': achievments,
                'UF_CRM_1628803565': dopnaviki,
                'UF_CRM_1629238306': art1,
                'UF_CRM_1629237984': qualities1,
                'UF_CRM_1629238087': character1,
                'UF_CRM_1629238156': type1,
                'UF_CRM_1628804410': under,
                'UF_CRM_1629239229': orientation
            }}
            b = fast_bitrix24.Bitrix('bitrix_api_link-key')
            with b.slow():
                results = b.call('crm.lead.add', tasks)
            hobby1.clear()
            prof1.clear()
            art1.clear()
            qualities1.clear()
            character1.clear()
            type1.clear()
            print('VSE OKEY')
            return 'test'

        except:
            print('PEREZAPUSK')
            return 'test'

    else:
        print('PIZDEC')
        return 'test'

app.run(host='0.0.0.0', port=8000)
