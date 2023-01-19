import imp
from puzzle import Puzzle
import pygame
import pygame_gui
import time
import colors


SCREEN_SIZE = (1000, 700)

pygame.init()
BASICFONT = pygame.font.Font('FiraCode-Retina.ttf',50)

pygame.display.set_caption('Sliding 8 Puzzle')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(colors.BABY_BLUE))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')

pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8-Puzzle")

def display_elements():
    #Elements
    ### Title Label
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8-Puzzle Game",
                                        relative_rect=pygame.Rect((350, 10), (300, 70)),
                                        object_id="#title_box"
                                        )
    
display_elements()
### solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 450), (250, 50)),
                                             text='Solve Puzzle',
                                             manager=manager,
                                             object_id="#solve_btn")

### algorithmOptions DropDown
dropdown_layout_rect = pygame.Rect((650, 370), (280, 50))
algorithmOptions = ["A* (Manhatan Distance)","Breadth-First"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

### shuffle button
button_layout_rect = pygame.Rect((650, 290), (250, 50))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)

### info button
info_html = "<b>Click Here<b>To see developers info!!!"
button_layout_rect = pygame.Rect((50, 690), (30, 30))
info_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='?',
                                             manager=manager,
                                             tool_tip_text=info_html)
### alert label
alert_label = pygame_gui.elements.ui_label.UILabel(
                                     manager=manager,
                                     text="",
                                     relative_rect=pygame.Rect((920, 320), (250, 30)),
                                     object_id="#accept_label")


def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, colors.BLUE_GROTTO, block['rect'])
            textSurf = BASICFONT.render(str(block['block']), True, colors.NAVY_BLUE)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left+50,block['rect'].top+50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, colors.ROYAL_BLUE, block['rect'])

def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matrix.searchBlock(0)
        if mv == "right":
            puzzle.matrix.moveright(zero)
        elif mv == "left":
            puzzle.matrix.moveleft(zero)  
        elif mv == "up":
            puzzle.matrix.moveup(zero)
        elif mv == "down":
            puzzle.matrix.movedown(zero)
        puzzle.setBlocksMatrix()
        draw_blocks(puzzle.blocks)
        pygame.display.update()
        time.sleep(0.2)
        
window_surface.blit(background, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.initialize()
algorithm = "Breadth-First"
fstate="1,2,3,4,5,6,7,8,0"
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.randomBlocks()

                
                elif event.ui_element == solve_button:
                    
                    if algorithm == "Breadth-First":
                        moves = puzzle.breadthFirst()
                        solveAnimation(moves)
                        
                    elif algorithm == "A* (Manhatan Distance)":
                        moves = puzzle.a_star()
                        solveAnimation(moves)
                        
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
                print("")
        manager.process_events(event)
        
        
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocks)
    pygame.display.update()
