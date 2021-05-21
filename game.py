
import pygame

class Game:
    pygame.init()

    pygame.display.set_caption('Tic-Tac-Toe')
    pygame.display.set_icon(pygame.image.load("Stuff/Other/tic-tac-toe.png"))

    def __init__(self):
        self.running = True
        self.playing = True

        self.clock = pygame.time.Clock()
        self.fps = 66

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.eeeeee = (238, 238, 238)
        self.dim_gray = (105, 105, 105)
        self.red = (218, 44, 73)
        self.green = (101, 208, 15)

        self.width = 500
        self.height = 500

        self.window = pygame.display.set_mode((self.width, self.height))

        self.canvas = pygame.Surface((self.width, self.height))
        self.canvas.fill(self.eeeeee)

        self.faded = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA, 32)
        self.faded = self.faded.convert_alpha()
        self.faded.fill((0, 0, 0, 175))

        self.end_text = ''
        self.game_over = False
        self.hid = False

        self.squares = 3

        self.board = [['_' for i in range(self.squares)]
                      for j in range(self.squares)]

        self.square_len = (self.height-100*2)//self.squares

        self.ai_turn = False

    def loop(self):

        self.if_ai()
        self.events()
        self.window.blit(self.canvas, (0, 0))
        self.blit_board()
        self.if_over()

        pygame.display.update()
        self.clock.tick(self.fps)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_r:
                    self.restart()
                if event.key == pygame.K_h:
                    self.hid = not self.hid
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.make_move(x, y)

    def blit_board(self):
        sl = self.square_len

        for i in range(self.squares):
            for j in range(self.squares):
                x = 100 + sl * j
                y = 100 + sl * i
                self.blit_rect(self.canvas, x, y, sl-5, sl -
                               5, self.eeeeee, self.black)

                v = self.board[i][j]
                if v != '_':
                    self.blit_text(v, x+(sl-5)*23//100, y+(sl-5)//9, self.canvas, sl*3//4)

    def blit_rect(self, surf, x, y, w, h, color, border_color):
        
        pygame.draw.rect(surf, border_color,
                         pygame.Rect(x-5, y-5, w+10, h+10))

        pygame.draw.rect(surf, color,
                         pygame.Rect(x, y, w, h))

    def blit_text(self, text, x, y, surf, size, color=(0, 0, 0)):
        f = pygame.font.Font('Stuff/Font/Qdbettercomicsans.ttf', size)
        t = f.render(text, True, color)
        surf.blit(t, (x, y))

    def make_move(self, x, y):
        if not self.ai_turn and not self.game_over:
            s = self.squares
            x = (x-100)//self.square_len
            y = (y-100)//self.square_len
            if 0 <= x < s and 0 <= y < s:
                if self.board[y][x] == '_':
                    self.board[y][x] = 'X'
                    self.ai_turn = not self.ai_turn
                    self.is_over()

    def moveable(self):
        l = self.squares
        for i in range(l):
            for j in range(l):
                if self.board[i][j] == '_':
                    return True
        return False

    def winnable(self):

        b = self.board
        l = len(b)

        for row in range(l):
            r = b[row]
            if all(e == r[0] for e in r):
                if r[0] == 'X':
                    return 10
                elif r[0] == 'O':
                    return -10

        for col in range(l):
            c = [row[col] for row in b]
            if all(e == c[0] for e in c):
                if c[0] == 'X':
                    return 10
                elif c[0] == 'O':
                    return -10

        diag = [b[d][d] for d in range(l)]
        if all(e == diag[0] for e in diag):
            if diag[0] == 'X':
                return 10
            elif diag[0] == 'O':
                return -10

        anti = [b[-a-1][a] for a in range(l)]
        if all(e == anti[0] for e in anti):
            if anti[0] == 'X':
                return 10
            elif anti[0] == 'O':
                return -10
        return 0

    def minimax(self, depth, isMax):

        b = self.board
        l = self.squares

        score = self.winnable()

        if score != 0:
            return score

        if not self.moveable():
            return 0

        if isMax:
            best = float('-inf')
            for i in range(l):
                for j in range(l):
                    if b[i][j] == '_':
                        b[i][j] = 'X'
                        best = max(best, self.minimax(depth + 1, not isMax))
                        b[i][j] = '_'
            return best
        else:
            best = float('inf')
            for i in range(l):
                for j in range(l):
                    if b[i][j] == '_':
                        b[i][j] = 'O'
                        best = min(best, self.minimax(depth + 1, not isMax))
                        b[i][j] = '_'
            return best

    def ai_move(self):

        r = -1
        c = -1
        b = self.board
        l = self.squares

        best = float('inf')

        for i in range(l):
            for j in range(l):
                if b[i][j] == '_':
                    b[i][j] = 'O'

                    m = self.minimax(0, True)

                    b[i][j] = '_'

                    if m < best:
                        best = m
                        r = i
                        c = j
        if r != -1 and c != -1:
            b[r][c] = 'O'

    def if_ai(self):
        if self.ai_turn:
            self.ai_move()
            self.ai_turn = not self.ai_turn
            self.is_over()

    def is_over(self):
        w = self.winnable()
        if w != 0:
            if w == 10:
                self.end_text = 'X Win'
            else:
                self.end_text = 'O Win'
            self.game_over = True
        elif not self.moveable():
            self.end_text = ' Draw'
            self.game_over = True

    def blit_over(self):
        self.window.blit(self.faded, (0, 0))

        s = self.height - 125*2
        x = 125
        y = 125 + 125//2

        self.blit_rect(self.faded, x, y, s-5,
                       s//2-5, self.eeeeee, self.black)
        self.blit_text(self.end_text, x+x//3,
                       y+10, self.faded, x//2)
        r = "Press 'R' to restart"
        self.blit_text(r, x+x*3//10, y+x*2//3, self.faded, 20)

    def if_over(self):
        if self.game_over:
            if not self.hid:
                self.blit_over()

    def restart(self):
        self.board = [['_' for i in range(self.squares)]
                      for j in range(self.squares)]
        self.game_over = False
