import sys, pygame, time, random, os
from spritesheet import Spritesheet

os.chdir(rf"{os.path.realpath(os.path.dirname(__file__))}")

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

icon = pygame.image.load("./icon.ico")                    # Memuat gambar untuk dijadikan icon
res_w, res_h = 1366, 768                                # Menentukan resolusi lebar (width/w) dan panjang (height/h)
screen = pygame.Surface((res_w, res_h))                 # Membuat surface untuk menempatkan gambar
window = pygame.display.set_mode((res_w, res_h))        # Mendefinisikan layar (display) dengan ukuran resolusi yang sudah ditentukan
caption = pygame.display.set_caption("Snake & Ladder")  # Mendefinisikan nama (Caption) pada window yang dibuat
pygame.display.set_icon(icon)

def mainmusic_play():                                   # Membuat module untuk memutar background musik utama
    pygame.mixer.music.load("data/sounds/Theme Song.wav")           # Memuat file audio
    return pygame.mixer.music.play(-1)                  # Memutar file audio

def mainmusic_pause():                                  # Membuat module untuk memberhentikan background musik utama
    pygame.mixer.music.load("data/sounds/Theme Song.wav")           # Memuat file audio
    return pygame.mixer.music.pause()                   # Memberhentikan file audio

def winmusic_play():                                    # Membuat module untuk memutar background musik saat Player 1 / Player 2 menang
    pygame.mixer.music.load("data/sounds/Level Complete.wav")       # Memuat file audio
    return pygame.mixer.music.play(-1)                  # Memutar file audio

def winmusic_pause():                                   # Membuat module untuk memberhentikan background musik saat Player 1 / Player 2 menang
    pygame.mixer.music.load("data/sounds/Level Complete.wav")       # Memuat file audio
    return pygame.mixer.music.pause()                   # Memberhentikan file audio

def losemusic_play():                                   # Membuat module untuk memutar background musik saat CPU menang
    pygame.mixer.music.load("data/sounds/gotcha.wav")               # Memuat file audio
    return pygame.mixer.music.play(-1)                  # Memutar file audio

def losemusic_pause():                                  # Membuat module untuk memberhentikan background musik saat CPU menang
    pygame.mixer.music.load("data/sounds/gotcha.wav")               # Memuat file audio
    return pygame.mixer.music.pause()

gameClock = pygame.time.Clock()                         # Mendefinisikan waktu game

p1 = pygame.image.load("data/images/Mario.png")                             # Memuat file gambar untuk Player 1
p2 = pygame.image.load("data/images/Luigi.png")                             # Memuat file gambar untuk Player 2
cpu = pygame.image.load("data/images/Yoshi.png")                            # Memuat file gambar untuk CPU
p1_p2 = pygame.image.load("data/images/Mario & Luigi.png")                  # Memuat file gambar saat Player 1 & Player 2 di posisi yang sama
p1_cpu = pygame.image.load("data/images/Mario & Yoshi.png")                 # Memuat file gambar saat Player 1 & CPU di posisi yang sama
mainmenu = pygame.image.load("data/images/Ladder & Snake (Menu).png")       # Memuat file gambar untuk tampilan menu
board = pygame.image.load("data/images/Ladder & Snake (Gameplay).png")      # Memuat file gambar untuk tampilan papan permainan
p1_win = pygame.image.load("data/images/Player 1 Win-1.png")                # Memuat file gambar saat Player 1 menang
p2_win = pygame.image.load("data/images/Player 2 Win-2.png")                # Memuat file gambar saat Player 2 menang
lose = pygame.image.load("data/images/You Lose.png")                        # Memuat file gambar saat CPU menang

dice_1 = Spritesheet("data/images/Roll Dice Sprite Sheet 1.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 1
dice_2 = Spritesheet("data/images/Roll Dice Sprite Sheet 2.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 2
dice_3 = Spritesheet("data/images/Roll Dice Sprite Sheet 3.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 3
dice_4 = Spritesheet("data/images/Roll Dice Sprite Sheet 4.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 4
dice_5 = Spritesheet("data/images/Roll Dice Sprite Sheet 5.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 5
dice_6 = Spritesheet("data/images/Roll Dice Sprite Sheet 6.png")            # Memuat file gambar untuk dimasukkan kedalam module Spritesheet saat dadu keluar 6

dice_1_list = []    # Membuat list sequences gambar untuk dadu keluar 1
dice_2_list = []    # Membuat list sequences gambar untuk dadu keluar 2
dice_3_list = []    # Membuat list sequences gambar untuk dadu keluar 3
dice_4_list = []    # Membuat list sequences gambar untuk dadu keluar 4
dice_5_list = []    # Membuat list sequences gambar untuk dadu keluar 5
dice_6_list = []    # Membuat list sequences gambar untuk dadu keluar 6

for i in range(1,53):       # Total sequences gambar sebanyak 52 frame gambar
    dice_1_list.append(dice_1.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 1
    dice_2_list.append(dice_2.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 2
    dice_3_list.append(dice_3.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 3
    dice_4_list.append(dice_4.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 4
    dice_5_list.append(dice_5.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 5
    dice_6_list.append(dice_6.parse_sprite("Roll_Dice 1_Artboard {}.png".format(i)))    # Memasukkan sequence gambar dengan indexing pada file JSON kedalam list sequences gambar dadu 6

menu_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)         # Memuat file font style dengan font size 20 untuk menu utama
player_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 40)       # Memuat file font style dengan font size 40 untuk tombol pilihan jumlah pemain
dice_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 45)         # Memuat file font style dengan font size 45 untuk tombol acak dadu
p1_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)           # Memuat file font style dengan font size 20 untuk giliran Player 1
p2_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)           # Memuat file font style dengan font size 20 untuk giliran Player 2
cpu_font = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)          # Memuat file font style dengan font size 20 untuk giliran CPU

pos = [(1200, 624), (1200,504), (1200, 384), (1200,264), (1080,384), (960,384), (840,384), (840,264), (840,144)]
list_p = []     # Membuat list jumlah pemain
turn = 2        # Mendefinisikan jumlah giliran
n = int(0)      # Mendefinisikan indeks posisi pemain pertama
m = int(0)      # Mendefinisikan indeks posisi pemain kedua
pos_change = 0  # Mendefinisikan perubahan posisi
xn = 0          # Mendefinisikan indeks untuk list random number
back = False    # Mendefinisikan keadaan maju

class Player():
    def __init__(self,image,overlapimage):  # Membuat parameter berupa gambar yang dimuat pada saat sendiri dan pada saat posisi pemain 1 dan 2 sama
        self.image = image                  # Membuat atribut berupa file gambar saat posisi berbeda
        self.overlapimage = overlapimage    # Membuat atribut berupa file gambar saat posisi sama
    
    def draw(self,position):                                                    # Membuat instance posisi
        self.position = position                                                # Membuat atribut posisi
        self.rect_image = self.image.get_rect(center = self.position)           # Membuat rectangle pada file gambar yg dimuat dengan pusat pada posisi
        self.rect_overlap = self.overlapimage.get_rect(center = self.position)  # Membuat rectangle pada file gambar saat posisi sama yang dimuat dengan pusat pada posisi
        if int(n) == int(m):                # Membuat pengondisian jika posisi pemain 1 dan 2 sama
            window.blit(self.overlapimage, self.rect_overlap)
        else:                               # Membuat pengondisian jika posisi pemain 1 dan 2 berbeda
            window.blit(self.image, self.rect_image)

class Button():
	def __init__(self,text,x,y,font):   # Membuat parameter berupa text yang akan ditampilkan, koordinat, dan font yg dipilih
		self.clicked = False            # Membuat kondisi saat tombol tidak di tekan
		self.text_surf = font.render(text,True,'#FFFFFF')           # Mencetak text pada tombol
		self.text_rect = self.text_surf.get_rect(center = (x,y))    # Membuat rectangle pada text yang dicetak
	def draw(self):                     # Membuat instance untuk menggambar tombolnya
		action = False                  # Membuat konsisi saat tombol tidak di klik
		mouse_pos = pygame.mouse.get_pos()              # Memanggil posisi dari mouse
		if self.text_rect.collidepoint(mouse_pos):      # Membuat pengondisian saat posisi mouse tumpang tindih dengan rectangle text yang sudah dibuat
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:    # Membuat pengondisian saat klik kiri pada mouse ditekan
				self.clicked = True     # Sepanjang klik kiri mouse ditekan maka akan True
				action = True           # Sepanjang klik kiri mouse ditekan maka akan True
		if pygame.mouse.get_pressed()[0] == 0:          # Membuat pengondisian saat klik kiri mouse berhenti ditekan
			self.clicked = False        # Sesaat klik kiri mouse berhenti ditekan maka akan False tetapi action tetap True
        
		window.blit(self.text_surf, self.text_rect)     # Menggambar tombol dengan text yang sudah dimasukkan
		return action

single_button = Button("Single Player",683,433,player_font)     # Menginisiasi tombol "Single Player"
multi_button = Button("Multiplayer",683,513,player_font)        # Menginisiasi tombol "Multiplayer"
dice_button = Button("Roll", 1165, 155, dice_font)              # Menginisiasi tombol acak dadu

def clock():    # Membuat modul untuk menghitung waktu sejak file di running
    current_time = pygame.time.get_ticks()
    return current_time

nextFrame = clock()     # Mendefinisikan waktu untuk frame dadu
diceFrame = clock()     # Mendefinisikan waktu untuk perpindahan posisi
dicestatic = 0          # Mendefinisikan waktu statis untuk membuat timer saat perpindahan posisi
statictime = 0          # Mendefinisikan waktu statis untuk membuat timer saat animasi dadu bergerak
frame = 0               # Mendefinisikan frame awal pada animasi dadu
frame_change = 0        # Mendefinisikan perubahan frame pada animasi dadu

def whichDice(Dicelist):    # Membuat module untuk mencetak dadu dengan parameter list sequences gambar dadu yang keluar
    window.blit(Dicelist[frame], (1020, 564))

def choose_player():        # Membuat module untuk memilih jumlah pemain
    # Memanggil variable global
    global pos, list_p, n, m, player_1_cpu, player_1_2, com, player_2
    while True:             # Melakukan looping while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if single_button.draw() == True:    # Pengondisian saat tombol "Single Player" ditekan
                player_1 = Player(p1,p1_cpu)    # Menginisiasi pemain pertama
                com = Player(cpu,p1_cpu)        # Menginisiasi pemain kedua berupa CPU
                list_p.append(player_1)
                list_p.append(com)
                gameloop1()                     # Menjalankan game untuk 1 pemain
            elif multi_button.draw() == True:   # Pengondisian saat tombol "Multiplayer" ditekan
                player_1 = Player(p1,p1_p2)     # Menginisiasi pemain pertama
                player_2 = Player(p2,p1_p2)     # Menginisiasi pemain kedua
                list_p.append(player_1)
                list_p.append(player_2)
                gameloop2()                     # Menjalankan game untuk 2 pemain
        window.blit(mainmenu, (0,0))            # Memuat tampilan menu
        single_button.draw()                    # Memuat tombol "Single Player"
        multi_button.draw()                     # Memuat tombol " Multiplayer"
        pygame.display.update()                 # Meng-update layar untuk setiap looping while
        gameClock.tick(50)                      # Men-set FPS sebesar 50 Frame Per Second

def menu():                 # Membuat module untuk tampilan menu
    losemusic_pause()       # Memberhentikan background musik saat kalah
    winmusic_pause()        # Memberhentikan background musik saat menang
    mainmusic_play()        # Memutar background musik utama
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:  # Pengondisian jika keyboard atau mouse ditekan makaakan menampilkan tampilan pemilihan jumlah pemain
                choose_player()
        menu_msg = menu_font.render("Press Any Button To Start", True, WHITE)
        menu_rect = menu_msg.get_rect(center = (683, 473))
        window.blit(mainmenu, (0,0))            # Memuat tampilan menu
        window.blit(menu_msg, menu_rect)        # Memuat text "Press Any Button"
        pygame.display.update()                 # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)                      # Men-set FPS sebesar 50 Frame Per Second

def p1win():            # Membuat module untuk tampilan Player 1 menang
    mainmusic_pause()   # Memberhentikan background musik utama
    winmusic_play()     # Memutar background musik saat menang
    # Memanggil variable global
    global nextFrame, frame, frame_change, statictime, list_p, pos, n, m, player_1_cpu, player_1_2, com, player_2, turn, pos_change, dicestatic, diceFrame, back, xn
    # Men-set ulang nilai awal
    list_p = []
    n = 0
    m = 0
    turn = 3
    dicestatic = 0
    statictime = 0
    frame = 0
    frame_change = 0
    back = False
    xn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:  # Pengondisian jika keyboard atau mouse ditekan makaakan menampilkan tampilan pemilihan jumlah pemain
                menu()
        window.blit(p1_win, (0,0))
        pygame.display.update()             # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)                  # Men-set FPS sebesar 50 Frame Per Second

def p2win():            # Membuat module untuk tampilan Player 2 menang
    mainmusic_pause()   # Memberhentikan background musik utama
    winmusic_play()     # Memutar background musik saat menang
    # Memanggil variable global
    global nextFrame, frame, frame_change, statictime, list_p, pos, n, m, player_1_cpu, player_1_2, com, player_2, turn, pos_change, dicestatic, diceFrame, back, xn
    # Men-set ulang nilai awal
    list_p = []
    n = 0
    m = 0
    turn = 3
    dicestatic = 0
    statictime = 0
    frame = 0
    frame_change = 0
    back = False
    xn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:  # Pengondisian jika keyboard atau mouse ditekan makaakan menampilkan tampilan pemilihan jumlah pemain
                menu()
        window.blit(p2_win, (0,0))
        pygame.display.update()             # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)                  # Men-set FPS sebesar 50 Frame Per Second

def youlose():          # Membuat module untuk tampilan CPU menang
    mainmusic_pause()   # Memberhentikan background musik utama
    losemusic_play()    # Memutar background musik saat menang
    # Memanggil variable global
    global nextFrame, frame, frame_change, statictime, list_p, pos, n, m, player_1_cpu, player_1_2, com, player_2, turn, pos_change, dicestatic, diceFrame, back, xn
    # Men-set ulang nilai awal
    list_p = []
    n = 0
    m = 0
    turn = 3
    dicestatic = 0
    statictime = 0
    frame = 0
    frame_change = 0
    back = False
    xn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:  # Pengondisian jika keyboard atau mouse ditekan makaakan menampilkan tampilan pemilihan jumlah pemain
                menu()
        window.blit(lose, (0,0))
        pygame.display.update()             # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)                  # Men-set FPS sebesar 50 Frame Per Second

def gameloop1():
    # Memanggil variable global
    global nextFrame, frame, frame_change, statictime, list_p, pos, n, m, player_1_cpu, player_1_2, com, player_2, turn, pos_change, dicestatic, diceFrame, back, xn, p1_font, p2_font, cpu_font
    number_of_dice = 0      # Mendefinisikan jumlah dadu
    while True:
        window.blit(board, (0,0))       # Menggambar papan permainan
        list_p[0].draw(pos[int(n)])     # Menggambar posisi pemain 1
        list_p[1].draw(pos[int(m)])     # Menggambar posisi pemain 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if dice_button.draw() == True and turn%2 == 0:  # Pengondisian saat tombol ditekan dan giliran Player 1
                statictime = nextFrame                      # Menginisiasi timer
                number_of_dice = random.randint(1,6)        # Mengacak dadu
                frame = 0                                   
                frame_change = 1                            # Mengubah nilai perubahan frame animasi dadu
                
        if clock() > nextFrame:             # Pengondisian untuk timer
            frame = (frame + frame_change)%52   # Frame akan bertambah hingga 52 Frame dan berulang
            if frame_change == 1:               # Saat pertambahan frame 1 maka frame akan terus bertambah
                nextFrame += 1
            if nextFrame - statictime > 50 and frame_change == 1: # Frame akan berhenti bertambah setelah mencapai frame terakhir
                frame_change = 0
                dicestatic = diceFrame
                pos_change = 1
                
        if clock() > diceFrame:             # Pengondisian timer untuk perpindahan posisi
            if pos_change == 1:                 # Posisi akan berubah jika perubahan posisi = 1
                diceFrame += 1
            if (diceFrame - dicestatic)%5 == 0 and pos_change == 1:     # Pengondisian step akan berubah setiap detik
                if turn%2 == 0 and back == False:       # Pengongisian saat giliran pemain 1 dan jalan maju
                    n += 1
                    if n >= 9:
                        back = True     # Pengondisian saat mencapai 9 dan belum menang maka jalan mundur
                if turn%2 == 0 and back == True and n == 9: # Pengondisian saat jalan mundur
                    n = 8
                if turn%2 == 0 and back == True:
                    n -= 1
                if turn%2 == 1 and back == False:       # Pengongisian saat giliran pemain 2 dan jalan maju
                    m += 1
                    if m >= 9:
                        back = True     # Pengondisian saat mencapai 9 dan belum menang maka jalan mundur
                if turn%2 == 1 and back == True and m == 9: # Pengondisian saat jalan mundur
                    m = 8
                if turn%2 == 1 and back == True:
                    m -= 1
            if diceFrame - dicestatic > 5*number_of_dice and pos_change == 1:
                if number_of_dice != 6:
                    turn += 1
                if n == 1:  # Pengondisian pemain 1 saat posisi 2 maka naik tangga
                    n += 4
                if m == 1:  # Pengondisian pemain 2 saat posisi 2 maka naik tangga
                    m += 4
                if n == 8:  # Pengondisian pemain 1 menang
                    p1win()
                if m == 8:  # Pengondisian pemain 2 menang
                    youlose()
                pos_change = 0
                back = False
                if turn%2 == 1:     # Pengondisian saat tombol ditekan dan giliran CPU
                    statictime = nextFrame
                    number_of_dice = random.randint(1,6)
                    frame = 0
                    frame_change = 1
                                
        # Pengondisian untuk memunculkan animasi dadu berdasarkan nilai dadu yang keluar
        if number_of_dice == 1:
            whichDice(dice_1_list)
        elif number_of_dice == 2:
            whichDice(dice_2_list)
        elif number_of_dice == 3:
            whichDice(dice_3_list)
        elif number_of_dice == 4:
            whichDice(dice_4_list)
        elif number_of_dice == 5:
            whichDice(dice_5_list)
        elif number_of_dice == 6:
            whichDice(dice_6_list)
        else:
            whichDice(dice_1_list)
        dice_button.draw()
        
        if turn%2 == 0:         # Pengondisian untuk giliran pemain 1 berupa text
            p1_msg = p1_font.render("Player 1 Turn", True, BLACK)
            p1_rect = p1_msg.get_rect(center = (1125, 97))
            window.blit(p1_msg, p1_rect)
        if turn%2 == 1:         # Pengondisian untuk giliran pemain 2 berupa text
            cpu_msg = cpu_font.render("CPU Turn", True, BLACK)
            cpu_rect = cpu_msg.get_rect(center = (1175, 97))
            window.blit(cpu_msg, cpu_rect)

        xn += 1                 # Memajukan index untuk random number

        pygame.display.update()     # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)          # Men-set FPS sebesar 50 Frame Per Second

def gameloop2():
    # Memanggil variable global
    global nextFrame, frame, frame_change, statictime, list_p, pos, n, m, player_1_cpu, player_1_2, com, player_2, turn, pos_change, dicestatic, diceFrame, back, xn, p1_font, p2_font, cpu_font
    number_of_dice = 0      # Mendefinisikan jumlah dadu
    while True:
        window.blit(board, (0,0))       # Menggambar papan permainan
        list_p[0].draw(pos[int(n)])     # Menggambar posisi pemain 1
        list_p[1].draw(pos[int(m)])     # Menggambar posisi pemain 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Pengondisian saat window ditutup maka akan keluar (quit) dari pygame
                pygame.quit()
                sys.exit()
            if dice_button.draw() == True:      # Pengondisian saat tombol acak dadu ditekan
                statictime = nextFrame                      # Menginisiasi timer
                number_of_dice = random.randint(1,6)    # Mengacak dadu
                frame = 0
                frame_change = 1                            # Mengubah nilai perubahan frame animasi dadu
                
        if clock() > nextFrame:             # Pengondisian untuk timer
            frame = (frame + frame_change)%52   # Frame akan bertambah hingga 52 Frame dan berulang
            if frame_change == 1:               # Saat pertambahan frame 1 maka frame akan terus bertambah
                nextFrame += 1
            if nextFrame - statictime > 50 and frame_change == 1: # Frame akan berhenti bertambah setelah mencapai frame terakhir
                frame_change = 0
                dicestatic = diceFrame
                pos_change = 1
                
        if clock() > diceFrame:             # Pengondisian timer untuk perpindahan posisi
            if pos_change == 1:                 # Posisi akan berubah jika perubahan posisi = 1
                diceFrame += 1
            if (diceFrame - dicestatic)%5 == 0 and pos_change == 1:     # Pengondisian step akan berubah setiap detik
                if turn%2 == 0 and back == False:       # Pengongisian saat giliran pemain 1 dan jalan maju
                    n += 1
                    if n >= 9:
                        back = True     # Pengondisian saat mencapai 9 dan belum menang maka jalan mundur
                if turn%2 == 0 and back == True and n == 9: # Pengondisian saat jalan mundur
                    n = 8
                if turn%2 == 0 and back == True:
                    n -= 1
                if turn%2 == 1 and back == False:       # Pengongisian saat giliran pemain 2 dan jalan maju
                    m += 1
                    if m >= 9:
                        back = True     # Pengondisian saat mencapai 9 dan belum menang maka jalan mundur
                if turn%2 == 1 and back == True and m == 9: # Pengondisian saat jalan mundur
                    m = 8
                if turn%2 == 1 and back == True:
                    m -= 1
            if diceFrame - dicestatic > 5*number_of_dice and pos_change == 1:
                if number_of_dice != 6:
                    turn += 1
                if n == 1:  # Pengondisian pemain 1 saat posisi 2 maka naik tangga
                    n += 4
                if m == 1:  # Pengondisian pemain 2 saat posisi 2 maka naik tangga
                    m += 4
                if n == 8:  # Pengondisian pemain 1 menang
                    p1win()
                if m == 8:  # Pengondisian pemain 2 menang
                    p2win()
                pos_change = 0
                back = False
                
                
        # Pengondisian untuk memunculkan animasi dadu berdasarkan nilai dadu yang keluar
        if number_of_dice == 1:
            whichDice(dice_1_list)
        elif number_of_dice == 2:
            whichDice(dice_2_list)
        elif number_of_dice == 3:
            whichDice(dice_3_list)
        elif number_of_dice == 4:
            whichDice(dice_4_list)
        elif number_of_dice == 5:
            whichDice(dice_5_list)
        elif number_of_dice == 6:
            whichDice(dice_6_list)
        else:
            whichDice(dice_1_list)
        dice_button.draw()
        
        if turn%2 == 0:         # Pengondisian untuk giliran pemain 1 berupa text
            p1_msg = p1_font.render("Player 1 Turn", True, BLACK)
            p1_rect = p1_msg.get_rect(center = (1125, 97))
            window.blit(p1_msg, p1_rect)
        if turn%2 == 1:         # Pengondisian untuk giliran pemain 2 berupa text
            p2_msg = p2_font.render("Player 2 Turn", True, BLACK)
            p2_rect = p2_msg.get_rect(center = (1125, 97))
            window.blit(p2_msg, p2_rect)
        
        xn += 1                 # Memajukan index untuk random number

        pygame.display.update()     # Meng-update layar untuk setiap looping whlie
        gameClock.tick(50)          # Men-set FPS sebesar 50 Frame Per Second
menu()      # Memanggil module menu