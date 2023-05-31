import pygame
from moviepy.editor import *
import numpy as np
import random
from settings import *


# Inicialização do Pygame
pygame.init()

# Configuração da janela
window = pygame.display.set_mode((RES))
pygame.display.set_caption("Bar do Gordo")

# Carregar o arquivo GIF animado
video = VideoFileClip("./assets/img/animation.gif")
video.set_duration(1)  # duração do GIF (em segundos)
frames = []

for t in range(int(video.duration * video.fps)):
    frame = video.get_frame(t / video.fps)
    frame = np.rot90(frame, 1)  # Gira a imagem em 90 graus
    surface = pygame.surfarray.make_surface(frame)
    surface = pygame.transform.scale(surface, (RES))  # Redimensiona a imagem
    frames.append(surface)

# Função para redimensionar a imagem


def resize_image(image, width, height):
    return pygame.transform.scale(image, (width, height))


# Ajudante
waitress = pygame.image.load("./assets/img/waitress.png")
waitress = resize_image(waitress, waitress_width, waitress_height)
waitress_x = WIDTH // 2 - waitress_width // 2
waitress_y = HEIGHT // 2 - waitress_height // 2

# Configuração da barra de diálogo
dialogue_width = WIDTH
dialogue_height = 150
dialogue_surface = pygame.Surface((dialogue_width, dialogue_height))
dialogue_surface.fill((0, 0, 0))  # Cor de fundo da barra de diálogo

dialogue_font = pygame.font.Font(None, 24)
dialogue_texts = [
    "Bem vindo de volta Sir Gordo!",
    "Já preparei 100 litros da melhor cerveja do reino de Camaroes",
    "...",
    "Toc Toc",
    "Que barulho é esse tão cedo",
    "Olha! parece que chegaram 5 clientes querendo comprar cerveja",
    "Parece que já vamos vender tudo",
    "'Eles estão loucos por uma biritinha. risos!'",
    "Entre as ofertas, ache a melhor distribuição para que possa lucrar o máximo possível",
    "Caso erre você perderá e entraremos em falencia ç-ç",
    "De o seu melhor."
]


def message_res(player_res, knap_res):
    return f"Voce encontrou um caminho melhor que o knapsack 😮! Voce {player_res :.2f} Knapsack {knap_res :.2f}" if player_res > knap_res else (
        f"Parabéns você lucro o máximo que podia! {player_res :.2f}" if player_res == knap_res else f"Voce errou! Lucrou { player_res :.2f} e poderia ter lucrado {knap_res :.2f}")


current_dialogue_index = 0  # Índice inicial do texto do diálogo

# Carregar a música de fundo
pygame.mixer.music.load("./assets/sound/background_music.mp3")
pygame.mixer.music.set_volume(0.1)  # Definir o volume do áudio

# Reproduzir a música de fundo em um loop infinito
pygame.mixer.music.play(-1)

# Carregar a imagem de fundo da tela inicial
background_image = pygame.image.load("./assets/img/start_background_image.png")
background_image = resize_image(background_image, WIDTH, HEIGHT)

# Variável para controlar se o jogador clicou na tela inicial
clicked_on_screen = False

# Loop principal do jogo
running = True
frame_index = 0
clock = pygame.time.Clock()


# dados do player
player_capacity = 100
player_profit = 0


def knapsack(capacity, items):
    items.sort(key=lambda x: x[1] / x[0], reverse=True)

    total_value = 0
    included_items = []

    for weight, value in items:
        if weight <= capacity:
            included_items.append(weight)
            total_value += value
            capacity -= weight
        else:
            fraction = capacity / weight
            included_items.append(fraction * weight)
            total_value += fraction * value
            break

    return total_value, included_items

# Função para o loop do novo módulo


def show_beer_details(num, beer, x, y, beer_width, beer_height):
    beer_qnt = beer[0]
    beer_price = beer[1]
    beer_number = dialogue_font.render(f"Cerveja {num}", True, (255, 255, 255))
    details_x = x + (beer_width - beer_number.get_width()) // 2
    details_y = y + beer_height + (beer_number.get_height() + 5)
    window.blit(beer_number, (details_x, details_y))

    # Black rectangle dimensions
    rect_width = beer_width
    rect_height = 4 * beer_number.get_height() + 4 * 5
    rect_x = x
    rect_y = details_y - beer_number.get_height() - 5
    # Draw the black rectangle
    pygame.draw.rect(window, (0, 0, 0),
                     (rect_x, rect_y, rect_width, rect_height))

    window.blit(beer_number, (details_x, details_y))

    beer_qnt_surface = dialogue_font.render(
        f"Qnt: {beer_qnt}", True, (255, 255, 255))
    qnt_x = x + (beer_width - beer_qnt_surface.get_width()) // 2
    qnt_y = details_y + beer_qnt_surface.get_height() + 5
    window.blit(beer_qnt_surface, (qnt_x, qnt_y))

    beer_price_surface = dialogue_font.render(
        f"R$ {beer_price :.2f}", True, (255, 255, 255))
    price_x = x + (beer_width - beer_price_surface.get_width()) // 2
    price_y = qnt_y + beer_qnt_surface.get_height() + 5
    window.blit(beer_price_surface, (price_x, price_y))


def get_items():
    qnt = 150
    items = []
    for i in range(0, 4):
        num = random.randint(20, 32)
        items.append((num, random.randint(20, 500)))
        qnt -= num
    items.append((qnt, random.randint(20, 500)))
    return items


def in_game_loop(player_capacity, player_profit):
    beers_array = get_items()  # (weight, value) pairs
    # beers_array = [(11, 120), (21, 60), (31, 100), (41, 180), (51, 200)]
    qnt_beer = len(beers_array)
    max_value, included_items = knapsack(CAPACITY, beers_array)
    random.shuffle(beers_array)

    # Load the new module background
    in_game_background = pygame.image.load(
        "./assets/img/ingame_background.png")
    in_game_background = pygame.transform.scale(in_game_background, (RES))

    # Load the new module music
    pygame.mixer.music.load("./assets/sound/ingame_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Load the image to be displayed
    beer_width = 100
    beer_height = 100
    beer = pygame.image.load("./assets/img/beer.png")
    beer = pygame.transform.scale(beer, (beer_width, beer_height))

    # Calculate the horizontal spacing between images
    total_spacing = WIDTH - (beer_width * qnt_beer)
    spacing = total_spacing // (qnt_beer + 1)

    # Calculate the initial x-coordinate for the first image
    start_x = (WIDTH - (beer_width * qnt_beer) -
               (spacing * (qnt_beer - 1))) // 2

    # Define the color for the glowing effect
    glow_color = (255, 255, 0)  # Yellow

    # Store the visibility status of each image
    beer_visible = [True] * qnt_beer

    # Loop of the new module
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the mouse clicked on any visible image
                    for i in range(qnt_beer):
                        if beer_visible[i]:
                            x = start_x + (i * (beer_width + spacing))
                            y = (HEIGHT - beer_height) // 2
                            beer_rect = pygame.Rect(
                                x, y, beer_width, beer_height)
                            if beer_rect.collidepoint(event.pos):
                                beer_visible[i] = False
                                if not player_capacity - beers_array[i][0] < 0:
                                    player_capacity -= beers_array[i][0]
                                    player_profit += beers_array[i][1]
                                else:
                                    player_profit += (player_capacity *
                                                      (beers_array[i][1]/beers_array[i][0]))
                                    player_capacity = 0
                                    window.blit(in_game_background, (0, 0))
                                    return player_profit, max_value
                                break

        window.blit(in_game_background, (0, 0))

        # Display the images equally spaced in the middle of the screen
        for i in range(qnt_beer):
            if beer_visible[i]:
                x = start_x + (i * (beer_width + spacing))
                y = (HEIGHT - beer_height) // 2

                beer_rect = pygame.Rect(x, y, beer_width, beer_height)
                if beer_rect.collidepoint(pygame.mouse.get_pos()):
                    # Apply the color tint effect (glowing effect)
                    tinted_beer = beer.copy()
                    tinted_beer.fill(
                        glow_color, special_flags=pygame.BLEND_RGB_ADD)
                    window.blit(tinted_beer, (x, y))
                    show_beer_details(
                        i+1, beers_array[i], x, y, beer_width, beer_height)
                else:
                    window.blit(beer, (x, y))
                    # Display beer details (value and price) below the beer image
                    show_beer_details(
                        i+1, beers_array[i], x, y, beer_width, beer_height)

        capacity_text = f"Litros de cerveja: {player_capacity}"
        capacity_surface = dialogue_font.render(
            capacity_text, True, (255, 255, 255))
        capacity_x = 10
        capacity_y = 10
        window.blit(capacity_surface, (capacity_x, capacity_y))

        # Display profit marker
        profit_text = f"Lucro: {player_profit}"
        profit_surface = dialogue_font.render(
            profit_text, True, (255, 255, 255))
        profit_x = 10
        profit_y = 40
        window.blit(profit_surface, (profit_x, profit_y))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)  # Limit the frame rate to 60 FPS


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and clicked_on_screen:
                current_dialogue_index += 1

        if event.type == pygame.MOUSEBUTTONDOWN and not clicked_on_screen:
            clicked_on_screen = True

    window.fill((255, 255, 255))  # Preenche a tela com uma cor de fundo

    if not clicked_on_screen:
        # Exibe a imagem de fundo da tela inicial
        window.blit(background_image, (0, 0))
    else:
        window.blit(frames[frame_index % len(frames)],
                    (0, 0))  # Exibe o quadro atual do GIF
        # Exibe o personagem na tela
        window.blit(waitress, (waitress_x, waitress_y))

        dialogue_x = 0
        dialogue_y = HEIGHT - dialogue_height
        window.blit(dialogue_surface, (dialogue_x, dialogue_y))

        # Limpa o texto anterior
        dialogue_surface.fill((0, 0, 0))

        if current_dialogue_index < len(dialogue_texts):
            dialogue_text = dialogue_texts[current_dialogue_index]
            text_surface = dialogue_font.render(
                dialogue_text, True, (255, 255, 255))
            text_x = (dialogue_width - text_surface.get_width()) // 2
            text_y = (dialogue_height - text_surface.get_height()) // 2
            dialogue_surface.blit(text_surface, (text_x, text_y))

            dialogue_text = "Clique em espaço para continuar..."
            text_surface = dialogue_font.render(
                dialogue_text, True, (255, 255, 255))
            text_x = (dialogue_width - text_surface.get_width()) // 1.8
            text_y = (dialogue_height - text_surface.get_height()) // 1.2
            dialogue_surface.blit(text_surface, (text_x, text_y))

        # aqui eh o jogo em si
        elif current_dialogue_index == len(dialogue_texts):
            pygame.mixer.music.stop()
            player_res, knap_res = in_game_loop(player_capacity, player_profit)
            message = message_res(player_res, knap_res)
            message_surface = dialogue_font.render(
                message, True, (255, 255, 255))
            message_x = (dialogue_width - message_surface.get_width()) // 2
            message_y = (dialogue_height -
                         message_surface.get_height()) // 2
            window.blit(message_surface, (message_x, message_y))
            pygame.display.update()
            pygame.time.delay(5000)  # Delay for 2 seconds
    pygame.display.update()

    if clicked_on_screen:
        frame_index += 1
    clock.tick(FPS)

pygame.quit()
