import pygame
from moviepy.editor import *
import numpy as np
import random


# Inicialização do Pygame
pygame.init()

# Configuração da janela
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo com GIF Animado")

# Carregar o arquivo GIF animado
video = VideoFileClip("./assets/img/animation.gif")
video.set_duration(1)  # Defina a duração do GIF (em segundos)
frames = []

for t in range(int(video.duration * video.fps)):
    frame = video.get_frame(t / video.fps)
    frame = np.rot90(frame, 1)  # Gira a imagem em 90 graus
    surface = pygame.surfarray.make_surface(frame)
    surface = pygame.transform.scale(surface, (screen_width, screen_height))  # Redimensiona a imagem
    frames.append(surface)

# Variáveis do personagem
character_image = pygame.image.load("./assets/img/waitress.png")

# Função para redimensionar a imagem
def resize_image(image, width, height):
    return pygame.transform.scale(image, (width, height))

# Dimensões do personagem
character_width = 600
character_height = 600

# Redimensionar a imagem do personagem
character_image = resize_image(character_image, character_width, character_height)

# Posição inicial do personagem
character_x = screen_width // 2 - character_width // 2  # Posição inicial no centro horizontal da tela
character_y = screen_height // 2  - character_height // 2  # Posição inicial no lado inferior da tela

# Configuração da barra de diálogo
dialogue_width = screen_width
dialogue_height = 150
dialogue_surface = pygame.Surface((dialogue_width, dialogue_height))
dialogue_surface.fill((0, 0, 0))  # Cor de fundo da barra de diálogo

dialogue_font = pygame.font.Font(None, 24)  
dialogue_texts = [
    "Bem-vindo, aventureiro! Está pronto para participar do nosso desafio da Lojinha Mediavel?",
    "Nós temos uma seleção de barris com diferentes bebidas deliciosas.",
    "Cada barril tem um peso e um valor associados.",
    "Seu objetivo é distribuir esses barris entre duas carroças de carga",
    "de forma que a soma dos valores seja maximizada",
    "e o peso em cada carroça seja igual ou o mais próximo possível.",
    "Ah, sim! Além da diversão de participar, há recompensas em jogo.",
    "Se conseguir distribuir os barris de forma eficiente, receberá moedas de ouro como prêmio.",
    "E, é claro, a satisfação de se tornar o melhor estrategista da taverna!",
    "Eai, Está Pronto Para começar?",
]
current_dialogue_index = 0  # Índice inicial do texto do diálogo

# Barris
barrels = [
    {"name": "Barril 1", "weight": 4, "value": 8},
    {"name": "Barril 2", "weight": 3, "value": 5},
    {"name": "Barril 3", "weight": 2, "value": 3},
    {"name": "Barril 4", "weight": 5, "value": 10},
    {"name": "Barril 5", "weight": 1, "value": 2},
]

# Função para calcular a distribuição eficiente dos barris
def knapsack(barrels, max_weight):
    n = len(barrels)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, max_weight + 1):
            if barrels[i - 1]["weight"] <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - barrels[i - 1]["weight"]] + barrels[i - 1]["value"])
            else:
                dp[i][j] = dp[i - 1][j]

    selected_barrels = []
    i = n
    j = max_weight
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_barrels.append(barrels[i - 1])
            j -= barrels[i - 1]["weight"]
        i -= 1

    return selected_barrels

# Distribuição eficiente dos barris
max_weight_per_cart = 7
selected_barrels = knapsack(barrels, max_weight_per_cart)
selected_barrels_names = [barrel["name"] for barrel in selected_barrels]

# Carregar a música de fundo
pygame.mixer.music.load("./assets/sound/background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Definir o volume do áudio

# Reproduzir a música de fundo em um loop infinito
pygame.mixer.music.play(-1)

# Carregar a imagem de fundo da tela inicial
background_image = pygame.image.load("./assets/img/start_background_image.png")
background_image = resize_image(background_image, screen_width, screen_height)

# Variável para controlar se o jogador clicou na tela inicial
clicked_on_screen = False

# Loop principal do jogo
running = True
frame_index = 0
frame_rate = 30  # Taxa de atualização dos quadros (frames por segundo)
clock = pygame.time.Clock()


# Variáveis do novo módulo
new_module_running = False  # Variável para controlar o novo módulo
new_module_music_path = ""  # Caminho da nova música de fundo

# Função para o loop do novo módulo

def new_module_loop():

    # Load the new module background
    new_module_background_image_path = "./assets/img/new_background_image.png"
    new_module_background_image = pygame.image.load(new_module_background_image_path)
    new_module_background_image = pygame.transform.scale(new_module_background_image, (screen_width, screen_height))

    # Load the new module music
    new_module_music_path = "./assets/sound/ingame_music.mp3"
    pygame.mixer.music.load(new_module_music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load the image to be displayed
    image_path = "./assets/img/beer.png"
    image_width = 100
    image_height = 100
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (image_width, image_height))

    # Calculate the horizontal spacing between images
    num_images = 5
    total_spacing = screen_width - (image_width * num_images)
    spacing = total_spacing // (num_images + 1)

    # Calculate the initial x-coordinate for the first image
    start_x = (screen_width - (image_width * num_images) - (spacing * (num_images - 1))) // 2

    # Define the color for the glowing effect
    glow_color = (255, 255, 0)  # Yellow

    # Store the visibility status of each image
    image_visible = [True] * num_images

    # Loop of the new module
    new_module_running = True
    while new_module_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_module_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the mouse clicked on any visible image
                    for i in range(num_images):
                        if image_visible[i]:
                            x = start_x + (i * (image_width + spacing))
                            y = (screen_height - image_height) // 2
                            image_rect = pygame.Rect(x, y, image_width, image_height)
                            if image_rect.collidepoint(event.pos):
                                image_visible[i] = False
                                break

        window.blit(new_module_background_image, (0, 0))

        # Display the images equally spaced in the middle of the screen
        for i in range(num_images):
            if image_visible[i]:
                x = start_x + (i * (image_width + spacing))
                y = (screen_height - image_height) // 2

                image_rect = pygame.Rect(x, y, image_width, image_height)
                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    # Apply the color tint effect (glowing effect)
                    tinted_image = image.copy()
                    tinted_image.fill(glow_color, special_flags=pygame.BLEND_RGB_ADD)
                    window.blit(tinted_image, (x, y))
                else:
                    window.blit(image, (x, y))

        pygame.display.update()
        pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS

    # Stop the music when the new module ends
    pygame.mixer.music.stop()

    pygame.quit()
    
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
        window.blit(background_image, (0, 0))  # Exibe a imagem de fundo da tela inicial
    else:
        window.blit(frames[frame_index % len(frames)], (0, 0))  # Exibe o quadro atual do GIF
        window.blit(character_image, (character_x, character_y))  # Exibe o personagem na tela

        dialogue_x = 0
        dialogue_y = screen_height - dialogue_height
        window.blit(dialogue_surface, (dialogue_x, dialogue_y))

        # Limpa o texto anterior
        dialogue_surface.fill((0, 0, 0))

        if current_dialogue_index < len(dialogue_texts):
            dialogue_text = dialogue_texts[current_dialogue_index]
            text_surface = dialogue_font.render(dialogue_text, True, (255, 255, 255))
            text_x = (dialogue_width - text_surface.get_width()) // 2
            text_y = (dialogue_height - text_surface.get_height()) // 2
            dialogue_surface.blit(text_surface, (text_x, text_y))
            
            dialogue_text = "Clique em espaço para continuar..."
            text_surface = dialogue_font.render(dialogue_text, True, (255, 255, 255))
            text_x = (dialogue_width - text_surface.get_width()) // 1.8
            text_y = (dialogue_height - text_surface.get_height()) // 1.2
            dialogue_surface.blit(text_surface, (text_x, text_y))

        
        elif current_dialogue_index == len(dialogue_texts):
            dialogue_text = "Barris selecionados: " + ", ".join(selected_barrels_names)
            text_surface = dialogue_font.render(dialogue_text, True, (255, 255, 255))
            text_x = (dialogue_width - text_surface.get_width()) // 2
            text_y = (dialogue_height - text_surface.get_height()) // 2
            dialogue_surface.blit(text_surface, (text_x, text_y))
            pygame.mixer.music.stop()

            new_module_loop()

            
    pygame.display.update()

    if clicked_on_screen:
        frame_index += 1

    clock.tick(frame_rate)

pygame.quit()
