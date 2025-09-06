import pygame  # Game library
import sys     # System functions

pygame.init()

# Setup
colors = list(pygame.color.THECOLORS.items())  # List of (name, RGB)

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h  # Screen size

background_color = (255, 255, 255)  # White background
font_size = 50
padding = 20
rect_height = 60

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Fullscreen window
pygame.display.set_caption('Pygame Color Names')

font = pygame.font.Font(None, font_size)  # Font setup

scroll_y = 0  # Vertical scroll position
clock = pygame.time.Clock()
is_dragging = False  # Dragging flag
is_scrollbar_dragging = False  # Scrollbar dragging flag
start_y = 0  # Drag start position

content_height = len(colors) * (rect_height + padding)  # Total content height
max_scroll = max(0, content_height - screen_height)  # Max scroll limit

scrollbar_width = 75
scrollbar_color = (150, 150, 150)
scrollbar_drag_color = (100, 100, 100)

rendered_rows = {}  # Cache for rendered rows

def render_row(i):  # Render a color row
    if i in rendered_rows:
        return rendered_rows[i]

    name, rgb = colors[i]
    brightness = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]  # Calculate brightness
    text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)  # Choose text color

    row_surface = pygame.Surface((screen_width - 2 * padding, rect_height))
    row_surface.fill(rgb)  # Fill row with color

    text_surface = font.render(name, True, text_color)
    text_rect = text_surface.get_rect(midleft=(20, rect_height // 2))
    row_surface.blit(text_surface, text_rect)  # Draw color name

    rgb_text = f"{rgb}"
    rgb_surface = font.render(rgb_text, True, text_color)
    rgb_rect = rgb_surface.get_rect(midright=(row_surface.get_width() - 20, rect_height // 2))
    row_surface.blit(rgb_surface, rgb_rect)  # Draw RGB value

    rendered_rows[i] = row_surface  # Cache the row
    return row_surface

while True:
    screen.fill(background_color)  # Clear screen

    start_index = max(0, int(-scroll_y // (rect_height + padding)))  # First visible row
    end_index = min(len(colors), int((-scroll_y + screen_height) // (rect_height + padding)) + 2)  # Last visible row

    for i in range(start_index, end_index):  # Draw visible rows
        row_surface = render_row(i)
        rect_y = scroll_y + i * (rect_height + padding)
        screen.blit(row_surface, (padding, rect_y))

    if content_height > screen_height:  # Draw scrollbar if needed
        scrollbar_height = max((screen_height / content_height) * screen_height, 50)
        scrollbar_pos = (-scroll_y / max_scroll) * (screen_height - scrollbar_height)
        scrollbar_rect = pygame.Rect(screen_width - scrollbar_width, scrollbar_pos, scrollbar_width, scrollbar_height)
        pygame.draw.rect(screen, scrollbar_drag_color if is_scrollbar_dragging else scrollbar_color, scrollbar_rect)
    else:
        scrollbar_rect = None  # No scrollbar if content fits

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if scrollbar_rect and scrollbar_rect.collidepoint(event.pos):  # Start dragging scrollbar
                is_scrollbar_dragging = True
                drag_offset = event.pos[1] - scrollbar_rect.y
            else:  # Start dragging screen
                is_dragging = True
                start_y = event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:  # Stop dragging
            is_dragging = False
            is_scrollbar_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:  # Drag screen
                dy = event.pos[1] - start_y
                scroll_y += dy
                start_y = event.pos[1]
                scroll_y = max(-max_scroll, min(0, scroll_y))  # Limit scroll

            elif is_scrollbar_dragging:  # Drag scrollbar
                new_scrollbar_y = event.pos[1] - drag_offset
                new_scrollbar_y = max(0, min(new_scrollbar_y, screen_height - scrollbar_height))
                scroll_y = - (new_scrollbar_y / (screen_height - scrollbar_height)) * max_scroll

    pygame.display.flip()  # Update screen
    clock.tick(60)  # 60 FPS