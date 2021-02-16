import requests
import pygame
import os
import sys
# Чтобы переключать слои карты нужно нажимать на правую кнопку миши


def if_ll(lon):
    if lon[1] > 85:
        lon[1] = lon[1] - 170
    elif lon[1] < -85:
        lon[1] = lon[1] + 170
    if lon[0] > 180:
        lon[0] = lon[0] - 360
    elif lon[0] < -180:
        lon[0] = lon[0] + 360
    return lon


index = 0
delta = '2'
post_adress = False
post_adress_have = False
layers = ["map", "sat", "skl"]
api_server = "http://static-maps.yandex.ru/1.x/"
params = {
    "spn": ",".join([delta, delta]),
    "l": layers[index]
}

running = True
pygame.init()
post_code = ''
search_text = ''
name = ''
font_post = pygame.font.Font(None, 24)
sl = {97: 'Ф', 98: 'И', 99: 'С', 100: 'В', 101: 'У', 102: 'А', 103: 'П',
      104: 'Р', 105: 'Ш', 106: 'О', 107: 'Л', 108: 'Д', 109: 'Ь', 110: 'Т',
      111: 'Щ', 112: 'З', 113: 'Й', 114: 'К', 115: 'Ы', 116: 'Е', 117: 'Г',
      118: 'М', 119: 'Ц', 120: 'Ч', 121: 'Н', 122: 'Я', 32: ' ', 48: '0',
      49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8',
      57: '9', 1093: 'Х', 1098: 'Ъ', 1078: 'Ж', 1101: 'Э', 1073: 'Б', 1102: 'Ю'}

screen = pygame.display.set_mode((600, 550))
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 24)
pygame.draw.rect(screen, pygame.Color('Yellow'), [(5, 5), (450, 35)], 2)
pygame.draw.line(screen, (0, 0, 0), [0, 50], [600, 50], 3)
pygame.draw.line(screen, (0, 0, 0), [0, 500], [600, 500], 3)
pygame.draw.rect(screen, pygame.Color('Yellow'), [(559, 10), (30, 30)], 3)
pygame.draw.rect(screen, pygame.Color('Red'), [(561, 12), (26, 26)])
string = font.render('P', 1, pygame.Color('black'))
screen.blit(string, (567, 16))
string = font.render('Search', 1, pygame.Color('black'))
pygame.draw.rect(screen, pygame.Color('Yellow'), [(470, 10), (80, 30)])
screen.blit(string, (475, 15))
string = font.render('Reset', 1, pygame.Color('black'))
screen.blit(string, (10, 520))
Start_input = False
Start = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                index += 1
                if index == 3:
                    index = 0
                params['l'] = layers[index]
            if event.button == 1:
                if event.pos[0] >= 559 and event.pos[1] >= 10 and \
                   event.pos[0] <= 589 and event.pos[1] <= 40:  # кнопка переключения почтового адреса
                    if post_adress:
                        font = pygame.font.Font(None, 24)
                        pygame.draw.rect(screen, pygame.Color('Red'), [(561, 12), (26, 26)])
                        string = font.render('P', 1, pygame.Color('black'))
                        screen.blit(string, (567, 16))
                        post_adress = False
                        post_adress_have = True
                        if name != '':
                            font = pygame.font.Font(None, 20)
                            pygame.draw.rect(screen, pygame.Color('White'), [(100, 510), (500, 50)])
                            string = font.render(name, 1, pygame.Color('black'))
                            if string.get_rect()[2] > 475:
                                name2 = ', '.join(name.split(', ')[:2])
                                name1 = ', '.join(name.split(', ')[2:])
                                string2 = font.render(name2, 1, pygame.Color('black'))
                                string1 = font.render(name1, 1, pygame.Color('black'))
                                screen.blit(string1, (100, 530))
                                screen.blit(string2, (100, 510))
                            else:
                                screen.blit(string, (100, 510))
                    else:
                        font = pygame.font.Font(None, 24)
                        pygame.draw.rect(screen, pygame.Color('Green'), [(561, 12), (26, 26)])
                        string = font.render('P', 1, pygame.Color('black'))
                        screen.blit(string, (567, 16))
                        post_adress = True
                        post_adress_have = False
                elif event.pos[0] > 0 and event.pos[1] > 515 and \
                        event.pos[0] < 100 and event.pos[1] < 550:  # кнопка Reset
                    params = {"spn": params['spn'],
                              "l": params['l'],
                              'll': params['ll']}
                    pygame.draw.rect(screen, pygame.Color('White'), [(100, 510), (500, 50)])
                elif event.pos[0] > 5 and event.pos[1] > 5 and \
                        event.pos[0] < 450 and event.pos[1] < 35:  # Lineedit
                    Start_input = True
                elif event.pos[0] >= 470 and event.pos[1] > 10 and \
                        event.pos[0] < 550 and event.pos[1] < 40:  # Кнопка поиска
                    font = pygame.font.Font(None, 20)
                    Start_input = False
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={search_text}&format=json"
                    response = requests.get(geocoder_request)
                    if response:
                        try:
                            json_response = response.json()
                            try:
                                post_code = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                            except BaseException:
                                post_code = ''
                                print('У данного объекта не имеется почтовый код')
                            name = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']  # полный адрес
                            string = font.render(name, 1, pygame.Color('black'))
                            if string.get_rect()[2] > 475:
                                name2 = ', '.join(name.split(', ')[:2])
                                name1 = ', '.join(name.split(', ')[2:])
                                string2 = font.render(name2, 1, pygame.Color('black'))
                                string1 = font.render(name1, 1, pygame.Color('black'))
                                screen.blit(string1, (100, 530))
                                screen.blit(string2, (100, 510))
                            else:
                                screen.blit(string, (100, 510))
                            pos = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
                            params['ll'] = ','.join(pos)
                            params['pt'] = ','.join(pos) + ',org'

                            Start = True
                        except:
                            print('Возможно произошла ошибка, попробуйте \
                            изменить ведённое название')

        elif event.type == pygame.KEYDOWN:
            if event.unicode and Start_input:
                try:
                    search_text += sl[event.key]
                    font_search = pygame.font.Font(None, 35)
                    string = font_search.render(search_text, 1, pygame.Color('black'))
                    pygame.draw.rect(screen, pygame.Color('White'), [(100, 510), (500, 50)])
                    a = string.get_rect()
                    b = 9
                    if a[2] > 450:
                        b = 450 - a[2]
                    pygame.draw.rect(screen, pygame.Color('White'), [(0, 5), (455, 35)])
                    screen.blit(string, (b, 12))
                    pygame.draw.rect(screen, pygame.Color('White'), [(0, 5), (5, 35)])
                    pygame.draw.rect(screen, pygame.Color('Yellow'), [(5, 5), (450, 35)], 2)
                except BaseException as ve:
                    pass
            elif event.key == 1073741915:
                if float(delta) < 60:
                    delta = str(float(delta) * 1.5)
                    lon1 = params['spn'].split(',')
                    lon1 = [float(i) for i in lon1]
                    lon1[1] = delta
                    lon1[0] = delta
                    lon1 = [str(i) for i in lon1]
                    params['spn'] = ','.join(lon1)
            elif event.key == 1073741921:
                delta = str(float(delta) / 1.5)
                lon1 = params['spn'].split(',')
                lon1 = [float(i) for i in lon1]
                lon1[1] = delta
                lon1[0] = delta
                lon1 = [str(i) for i in lon1]
                params['spn'] = ','.join(lon1)
            elif event.key == pygame.K_BACKSPACE:
                search_text = search_text[:-1]
                font = pygame.font.Font(None, 35)
                string = font.render(search_text, 1, pygame.Color('black'))
                a = string.get_rect()
                b = 9
                if a[2] > 450:
                    b = 450 - a[2]
                pygame.draw.rect(screen, pygame.Color('White'), [(0, 5), (460, 35)])
                screen.blit(string, (b, 12))
                pygame.draw.rect(screen, pygame.Color('White'), [(0, 5), (5, 35)])
                pygame.draw.rect(screen, pygame.Color('Yellow'), [(5, 5), (450, 35)], 2)
            elif event.key == pygame.K_RIGHT:
                lon1 = params['ll'].split(',')
                lon1 = [float(i) for i in lon1]
                lon1[0] += 0.4 * float(delta)
                lon1 = if_ll(lon1)
                lon1 = [str(i) for i in lon1]
                params['ll'] = ','.join(lon1)
            elif event.key == pygame.K_LEFT:
                lon1 = params['ll'].split(',')
                lon1 = [float(i) for i in lon1]
                lon1[0] -= 0.4 * float(delta)
                lon1 = if_ll(lon1)
                lon1 = [str(i) for i in lon1]
                params['ll'] = ','.join(lon1)
            elif event.key == pygame.K_UP:
                lon1 = params['ll'].split(',')
                lon1 = [float(i) for i in lon1]
                lon1[1] += 0.4 * float(delta)
                lon1 = if_ll(lon1)
                lon1 = [str(i) for i in lon1]
                params['ll'] = ','.join(lon1)
            elif event.key == pygame.K_DOWN:
                lon1 = params['ll'].split(',')
                lon1 = [float(i) for i in lon1]
                lon1[1] -= 0.4 * float(delta)
                lon1 = if_ll(lon1)
                lon1 = [str(i) for i in lon1]
                params['ll'] = ','.join(lon1)
    map_file = "map.png"
    pygame.draw.rect(screen, pygame.Color('White'), [(0, 50), (600, 450)])
    if post_adress and not post_adress_have and name != '':
        font = pygame.font.Font(None, 20)
        post_adress_have = True
        pygame.draw.rect(screen, pygame.Color('White'), [(100, 510), (500, 50)])
        name_postcode = name + ', ' + post_code
        string = font.render(name_postcode, 1, pygame.Color('black'))
        if string.get_rect()[2] > 475:
            name2 = ', '.join(name_postcode.split(', ')[:2])
            name1 = ', '.join(name_postcode.split(', ')[2:])
            string2 = font.render(name2, 1, pygame.Color('black'))
            string1 = font.render(name1, 1, pygame.Color('black'))
            screen.blit(string1, (100, 530))
            screen.blit(string2, (100, 510))
        else:
            screen.blit(string, (100, 510))
    if Start:
        response = requests.get(api_server, params=params)
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 50))
    pygame.display.flip()
pygame.quit()
try:
    os.remove(map_file)
except BaseException as ve:
    pass
