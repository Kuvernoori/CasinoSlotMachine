import pygame
import sys
import random
from pygame import mixer
import moviepy.editor as mp

pygame.init()
mixer.init()
sound = mixer.music.load('Subwoofer Lullaby.mp3') # основная музыка, используется всегда, меняется только когда случается особое условие ( оно ниже )
mixer.music.set_volume(0.6) # (громкость всего на 0.6 этого вполне хватает)
mixer.music.play()

window_size = (800, 600)
pygame.display.set_caption("Slot Machine")
screen = pygame.display.set_mode(window_size)
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, window_size)


symbols = ["bell.png", "cherry.png", "lemon.png", "7.png"] # все символы игры
static_image_paths = ["Start.png", "machine.png", "stop.png", "spin.png", "win.png", "square.png", "inst.png"] # статичные изображения по типу кнопки стоп, спин и так дале

static_images = []
for path in static_image_paths:
    try:
        image = pygame.image.load(path)
        static_images.append(image)
    except:
        sys.exit()
# ниже размеры всех изображений
start_image = pygame.transform.scale(static_images[0], (100, 100))
machine_image = pygame.transform.scale(static_images[1], (1200, 1400))
stop_image = pygame.transform.scale(static_images[2], (120, 120))
spin_image = pygame.transform.scale(static_images[3], (250, 250))
win_image = pygame.transform.scale(static_images[4], (150, 150))
square_image = pygame.transform.scale(static_images[5], (400, 320))
inst_image = pygame.transform.scale(static_images[6], (185, 180))

symbol_images = []
for symbol in symbols:
    try:
        image = pygame.transform.scale(pygame.image.load(symbol), (100, 100))
        symbol_images.append(image)
    except:
        sys.exit()
# позиции всех изображений по x y
start_position = (660, 450)
stop_position = (650, 300)
machine_position = (-200, -400)
spin_position = (287, 214)
win_position = (335, 0)
square_position = (200, 180)
inst_position = (0, 0)

reel_positions = [(machine_position[0] + 560, machine_position[1] + 690),
                  (machine_position[0] + 450, machine_position[1] + 690),
                  (machine_position[0] + 660, machine_position[1] + 690)]

animation_started = [False] * len(reel_positions)
spinning = False
stop_count = 0
random_symbols = [None] * len(reel_positions)

won = False
show_image = True

attempts = 3
victories = 0
bigw = 0

while attempts > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_position[0] <= event.pos[0] <= start_position[0] + start_image.get_width() and \
                    start_position[1] <= event.pos[1] <= start_position[1] + start_image.get_height():
                show_image = False
                spinning = True
                animation_started = [False] * len(reel_positions)
                stop_count = 0
                won = False

            elif stop_position[0] <= event.pos[0] <= stop_position[0] + stop_image.get_width() and \
                    stop_position[1] <= event.pos[1] <= stop_position[1] + stop_image.get_height():
                if spinning:
                    animation_started[stop_count % len(reel_positions)] = True
                    stop_count += 1
                    if stop_count == len(reel_positions):
                        won = all(symbol == random_symbols[0] for symbol in random_symbols)
                        attempts -= 1  # Уменьшение кол во попыток
                        if won:
                            victories += 1  # Увеличиваем счетчик побед
                            if won and all(symbol == symbol_images[3] for symbol in random_symbols):
                                bigw += 1 # прибавляем если биг вин
# отображение всего
    screen.blit(background_image, (0, 0))
    screen.blit(machine_image, machine_position)
    screen.blit(start_image, start_position)
    screen.blit(stop_image, stop_position)
    screen.blit(square_image, square_position)
    screen.blit(inst_image, inst_position)
# надпись spin в самом начале, как только нажимаем старт , пропадает и появляются смволы
    if show_image:
        screen.blit(spin_image, spin_position)

    font = pygame.font.SysFont('Arial Black', 23)
    text = font.render(f'Attempts: {attempts}', True, (255, 255, 255))
    screen.blit(text, (20, window_size[1] - 50))  # счетчик попытыков

    text_victories = font.render(f'Victories: {victories}', True, (255, 255, 255))
    screen.blit(text_victories, (20, window_size[1] - 100)) # текст с победами ( сюда записываются все победы)

    text_victories = font.render(f'Big win: {bigw}', True, (255, 255, 255))
    screen.blit(text_victories, (20, window_size[1] - 150)) # текст с большим выигрышем, только если совпадают три семерки

    for i, position in enumerate(reel_positions): # подсчет индексов символов
        if spinning and not animation_started[i]:
            random_symbols[i] = random.choice(symbol_images) # через функцию random.choice выбирается рандомный символ
            screen.blit(random_symbols[i], position)
        elif animation_started[i]:
            screen.blit(random_symbols[i], position)

    if won and all(symbol == symbol_images[3] for symbol in random_symbols): # условие на большой выигрыш, 7 имеет индекс 3
        # остановка текущей музыки
        mixer.music.stop()

        # новая музыка
        mixer.music.load('ljnn.mp3')
        mixer.music.play()

        video_path = "bart.mp4"
        video_clip = mp.VideoFileClip(video_path) # подгружаю видео через ссылку на видео

        # серия изобр в качестве видео
        frames = []
        for frame in video_clip.iter_frames():
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            frames.append(frame_surface)

        # Ограничение в 3 секунды у видео
        max_frames = 30 * 3

        clock = pygame.time.Clock()
        running = True
        frame_index = 0
        frames_played = 0

        while running and frames_played < max_frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(pygame.transform.scale(frames[frame_index], window_size), (0, 0))
            pygame.display.flip()

            frame_index += 1
            if frame_index >= len(frames):
                frame_index = 0

            frames_played += 1
            clock.tick(30)


            if not running:
                break

        mixer.music.stop()
        mixer.music.load('Subwoofer Lullaby.mp3')
        mixer.music.play(-1)

    pygame.display.flip()
    pygame.time.delay(500)

    if won:
        screen.blit(win_image, win_position)
        pygame.display.flip()
        pygame.time.delay(3000)
        won = False # в случае простой победы, аналогично вызывается при победе BIG WIN

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
