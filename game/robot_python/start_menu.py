import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("robot_switch")

def draw_start_screen():
    # 1. 填充背景色
    screen.fill((30, 30, 30))  # 深灰色背景

    # 2. 绘制标题
    font_title = pygame.font.Font(None, 74)
    title_surface = font_title.render("robot_switch", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    screen.blit(title_surface, title_rect)

    # 3. 绘制“开始游戏”按钮
    button_rect = pygame.Rect(SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2, 150, 50)
    pygame.draw.rect(screen, (0, 200, 0), button_rect) # 绿色按钮
    font_button = pygame.font.Font(None, 36)
    button_surface = font_button.render("开始游戏", True, (0, 0, 0))
    button_text_rect = button_surface.get_rect(center=button_rect.center)
    screen.blit(button_surface, button_text_rect)

    # 返回按钮的矩形区域，以便后续检测点击
    return button_rect

# --- 在游戏主循环之前定义状态 ---
MENU, PLAYING = 0, 1
game_state = MENU

# --- 主循环 ---
running = True
clock = pygame.time.Clock() # 用于控制帧率

while running:
    # 1. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 如果当前是菜单状态
        if game_state == MENU:
            # 检测鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 假设 draw_start_screen 返回了按钮的 rect
                if start_button_rect.collidepoint(mouse_pos):
                    print("开始游戏！")
                    game_state = PLAYING # 切换到游戏状态
        # 如果当前是游戏状态
        elif game_state == PLAYING:
            # 这里处理游戏中的事件，例如按ESC返回菜单
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = MENU

    # 2. 更新与绘制
    if game_state == MENU:
        # 重新绘制开始界面，并获取按钮位置用于检测
        start_button_rect = draw_start_screen()
    elif game_state == PLAYING:
        # 这里调用你游戏的主逻辑函数
        # run_game()
        screen.fill((0, 0, 0)) # 临时用黑色填充表示游戏画面
        pass

    # 3. 刷新屏幕
    pygame.display.flip()
    clock.tick(60) # 设置帧率为60FPS

pygame.quit()
sys.exit()