import pygame as pg
import math

pg.init()

# Criação da janela (altura e largura) e do título da janela.
WIDTH, HEIGHT = 800, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
background_image = pg.image.load("img/background.jpg")
background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))
pg.display.set_caption("Simulador de Sistema Planetário")

# Cores e Fonte:
BRANCO = (255, 255, 255)
VERMELHO = (188, 39, 50)
PRETO = (0, 0, 0)
CINZA = (80, 78, 81)
LARANJA = (255, 165, 0)
AMARELO = (255, 255, 0)
AZUL = (100, 149, 237)

FONTE = pg.font.SysFont("comicsans", 16)

# Criação da Classe de Planetas.
class Planeta:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    ESCALA = min(WIDTH, HEIGHT) / (3 * AU)
    PASSO_TEMPO = 3600 * 24  # 1 dia

    def __init__(self, nome, x, y, radius, cor, massa):
        self.nome = nome
        self.x = x
        self.y = y
        self.radius = radius
        self.cor = cor
        self.massa = massa

        self.orbita = []
        self.sol = False
        self.distancia_sol = 0

        self.x_vel = 0
        self.y_vel = 0

    # Função para o desenho do planeta.
    def desenho_planeta(self, win):
        x = int(self.x * self.ESCALA + WIDTH / 2)
        y = int(self.y * self.ESCALA + HEIGHT / 2)

        if len(self.orbita) > 2:
            upd_pontos = []
            for ponto in self.orbita:
                x, y = ponto
                x = int(x * self.ESCALA + WIDTH / 2)
                y = int(y * self.ESCALA + HEIGHT / 2)
                upd_pontos.append((x, y))

            pg.draw.lines(win, self.cor, False, upd_pontos, 2)

        pg.draw.circle(win, self.cor, (x, y), self.radius)

    # Função para desenhar o nome do planeta na tela.
    def desenho_nome(self, win):
        x = int(self.x * self.ESCALA + WIDTH / 2)
        y = int(self.y * self.ESCALA + HEIGHT / 2 - self.radius - 20)

        texto = FONTE.render(self.nome, True, self.cor)
        win.blit(texto, (x - self.radius, y))

    # Função para atração dos planetas.
    def atracao(self, other):
        x2, y2 = other.x, other.y
        distancia_x = x2 - self.x
        distancia_y = y2 - self.y
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

        if other.sol:
            self.distancia_sol = distancia

        forca = self.G * self.massa * other.massa / distancia**2
        const = math.atan2(distancia_y, distancia_x)
        forca_x = math.cos(const) * forca
        forca_y = math.sin(const) * forca
        return forca_x, forca_y

    # Função para atualização de posição dos planetas em meio à órbita.
    def posicao(self, planetas):
        total_fx = total_fy = 0
        for planeta in planetas:
            if self == planeta:
                continue

            fx, fy = self.atracao(planeta)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.massa * self.PASSO_TEMPO
        self.y_vel += total_fy / self.massa * self.PASSO_TEMPO

        self.x += self.x_vel * self.PASSO_TEMPO
        self.y += self.y_vel * self.PASSO_TEMPO
        self.orbita.append((self.x, self.y))

# Principal.
def main():
    run = True
    tempo = pg.time.Clock()

    Sol = Planeta("Sol", 0, 0, 30, AMARELO, 1.98892 * 10**30)
    Sol.sol = True

    Terra = Planeta("Terra", -1 * Planeta.AU, 0, 16, AZUL, 5.9742 * 10**24)
    Terra.y_vel = 29.783 * 1000

    Mercurio = Planeta("Mercúrio", 0.387 * Planeta.AU, 0, 8, CINZA, 3.30 * 10**23)
    Mercurio.y_vel = -47.4 * 1000

    Venus = Planeta("Vênus", 0.723 * Planeta.AU, 0, 14, BRANCO, 4.8685 * 10**24)
    Venus.y_vel = -35.02 * 1000

    Marte = Planeta("Marte", 1.524 * Planeta.AU, 0, 12, VERMELHO, 6.4171 * 10**23)
    Marte.y_vel = -24.007 * 1000

    planetas = [Sol, Terra, Mercurio, Venus, Marte]

    while run:
        tempo.tick(60)
        WIN.blit(background_image, (0, 0))

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                run = False

        for planeta in planetas:
            planeta.posicao(planetas)
            planeta.desenho_planeta(WIN)
            planeta.desenho_nome(WIN)

        pg.display.update()
    pg.quit()

main()
