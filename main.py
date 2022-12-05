import math
import random
import pygame


class Weasel:
    pos = (0, 0)
    path = ""

    def __init__(self, pos, path):
        self.pos = pos
        self.path = path


def generate():
    path = ""
    for i in range(12):
        turn = random.randint(0, 3)
        if turn == 0:
            path += "U"
        elif turn == 1:
            path += "D"
        elif turn == 2:
            path += "R"
        elif turn == 3:
            path += "L"
    return path


def mutate(path, origin):
    weasels = []
    for i in range(10):
        new = list(path)
        for s in range(len(new)):
            if random.randint(1, 100) < 5:
                turn = random.randint(0, 3)
                if turn == 0:
                    new[s] = 'U'
                elif turn == 1:
                    new[s] = 'D'
                elif turn == 2:
                    new[s] = 'R'
                elif turn == 3:
                    new[s] = 'L'
        new = "".join(new)
        weasels.append(Weasel(origin, new))
    return weasels


def distance(a, b):
    return math.sqrt(math.pow(b[0]-a[0], 2)+math.pow(b[1]-a[1], 2))


pygame.font.init()
window = pygame.display.set_mode((1200, 600), pygame.SCALED)
font = pygame.font.SysFont("monospace", 50)
consolefont = pygame.font.SysFont("monospace", 15)
pygame.display.set_caption("EvoWeasl")
weasl = pygame.image.load("weasl.png")
winsl = pygame.image.load("winner.png")
maus = pygame.image.load("maus.png")
grass = pygame.image.load("grass.png")
square = pygame.image.load("select.png")

display = True
console = []
select = 0
start = (0, 0)
finish = (0, 0)
step = 0
winner = generate()
specimen = []
generation = 0
finalWin = False
finalWinner = ""
while display:
    pygame.time.delay(50)
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if select == 0:
                    start = (math.ceil(mx / 100.0) * 100 - 100, math.ceil(my / 100.0) * 100 - 100)
                    if start[0] > 700 or start[1] > 600:
                        break
                    specimen = mutate(winner, start)
                    select = 1
                if select == 1:
                    if (math.ceil(mx / 100.0) * 100 - 100, math.ceil(my / 100.0) * 100 - 100) != start:
                        finish = (math.ceil(mx / 100.0) * 100 - 100, math.ceil(my / 100.0) * 100 - 100)
                        if finish[0] > 700 or finish[1] > 600:
                            break
                        current = start
                        console.append("Geração " + str(generation))
                        select = 2
    window.blit(grass, (0, 0))
    pygame.draw.polygon(window, (0, 0, 0), ((800, 0), (1200, 0), (1200, 600), (800, 600)))
    if finalWin:
        text = font.render("VENCEDOR! Geração " + str(generation), True, (0, 0, 0))
        window.blit(winsl, finish)
        window.blit(text, (100, 500))
    elif select == 0:
        draw = (math.ceil(mx / 100.0) * 100 - 100, math.ceil(my / 100.0) * 100 - 100)
        if not draw[0] > 700 and not draw[1] > 600:
            window.blit(square, draw)
            window.blit(weasl, draw)
    elif select == 1:
        draw = (math.ceil(mx / 100.0) * 100 - 100, math.ceil(my / 100.0) * 100 - 100)
        if not draw[0] > 700 and not draw[1] > 600:
            window.blit(square, draw)
            if not(start == draw):
                window.blit(maus, draw)
            window.blit(weasl, start)
    else:
        c = 0
        for weasel in specimen:
            c += 1
            if weasel.pos == finish:
                finalWin = True
                finalWinner = weasel.path
                console.append("VENCEDOR! Geração " + str(generation))
                console.append("Caminho Final: " + finalWinner)
                break
            text = font.render(str(c), True, (0, 0, 0))
            move = (0, 0)
            w = weasel.path
            if step < len(w):
                if w[step] == 'U':
                    move = (0, -100)
                elif w[step] == 'D':
                    move = (0, 100)
                elif w[step] == 'R':
                    move = (100, 0)
                else:
                    move = (-100, 0)
                if 0 <= weasel.pos[0]+move[0] <= 700 and 0 <= weasel.pos[1]+move[1] <= 500:
                    window.blit(weasl, weasel.pos)
                    window.blit(text, weasel.pos)
                    weasel.pos = (weasel.pos[0]+move[0], (weasel.pos[1]+move[1]))
                    window.blit(square, weasel.pos)
                    pygame.time.delay(50)
                else:
                    window.blit(square, weasel.pos)
                    window.blit(weasl, weasel.pos)
                    window.blit(text, weasel.pos)
            else:
                pygame.time.delay(100)
                window.blit(square, weasel.pos)
                window.blit(weasl, weasel.pos)
                window.blit(text, weasel.pos)
        window.blit(maus, finish)
        if step < 12:
            step += 1
        else:
            closest = specimen[0]
            for weasel in specimen:
                if distance(weasel.pos, finish) < distance(closest.pos, finish):
                    closest = weasel
            console.append("Mais próximo: " + str(closest.pos))
            console.append("Melhor caminho: " + str(closest.path))
            winner = closest.path
            specimen = mutate(winner, start)
            generation += 1
            step = 0
            console.append("Geração " + str(generation))

    c = 0
    for line in console:
        text = consolefont.render(line, True, (100, 255, 100))
        window.blit(text, (810, c*12))
        c += 1
    pygame.display.update()
pygame.quit()
