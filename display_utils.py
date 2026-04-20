# display_utils.py
import pygame
import logging

def _try_sdl2_monitor_index():
    try:
        from pygame._sdl2 import Window
        win = Window.from_display_module()
        return getattr(win, "displayindex", None)
    except Exception as ex:
        logging.warning(f"Failed to get SDL2 display index: {ex}")
        return None

def _try_screeninfo_center_monitor():
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if not monitors:
            return None
        try:
            from pygame._sdl2 import Window
            win = Window.from_display_module()
            wx, wy = win.position
            ww, wh = pygame.display.get_window_size()
            cx, cy = wx + ww // 2, wy + wh // 2
            for m in monitors:
                if m.x <= cx < m.x + m.width and m.y <= cy < m.y + m.height:
                    return (m.width, m.height)
        except Exception:
            # fallback to primary monitor
            m = monitors[0]
            return (m.width, m.height)
    except Exception as ex:
        return None

def get_current_monitor_size():
    # 1) SDL2 display index -> pygame.desktop sizes
    try:
        logging.info("Attempting to get monitor size via SDL2 display index...")
        idx = _try_sdl2_monitor_index()
        logging.info(f"SDL2 display index: {idx}")
        if idx is not None:
            sizes = pygame.display.get_desktop_sizes()
            if 0 <= idx < len(sizes):
                return sizes[idx]
    except Exception as ex:
        logging.warning(f"Failed to get SDL2 monitor size: {ex}")

    # 2) screeninfo fallback (cross-platform)
    si = _try_screeninfo_center_monitor()
    logging.info(f"Screeninfo center monitor size: {si}")
    if si:
        return si

    # 3) last resort: pygame Info
    info = pygame.display.Info()
    return (info.current_w, info.current_h)


def compute_cell_and_offsets(screen, grid_w, grid_h, monitor_size=None):
    if monitor_size is None:
        monitor_size = get_current_monitor_size()
    mon_w, mon_h = monitor_size
    cell = max(1, min(mon_w // grid_w, mon_h // grid_h))
    field_w, field_h = cell * grid_w, cell * grid_h
    screen_w, screen_h = screen.get_size()
    x_offset = (screen_w - field_w) // 2
    y_offset = (screen_h - field_h) // 2
    return cell, x_offset, y_offset


class DisplayManager:
    """
    Usage:
      dm = DisplayManager(screen, GRID_WIDTH, GRID_HEIGHT)
      # in event loop: new_screen = dm.handle_event(event); if new_screen: screen = new_screen
      # when drawing: use dm.cell_size, dm.x_offset, dm.y_offset
      # call dm.update_for_window() if you want to re-query monitor (e.g. on WINDOW_MOVED)
    """
    def __init__(self, screen, grid_w, grid_h):
        self.screen = screen
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.cell_size = 1
        self.x_offset = 0
        self.y_offset = 0
        self.update_for_window()

    def update_for_window(self):
        mon = get_current_monitor_size()
        self.cell_size, self.x_offset, self.y_offset = compute_cell_and_offsets(
            self.screen, self.grid_w, self.grid_h, mon
        )

    def handle_event(self, event):
        # returns new screen if we changed the display mode on resize
        if event.type == pygame.VIDEORESIZE:
            # recreate window in resizable mode and update metrics
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.update_for_window()
            return self.screen
        # pygame 2: WINDOWEVENT with event.event == WINDOWEVENT_MOVED
        if event.type == pygame.WINDOWEVENT and getattr(event, "event", None) == pygame.WINDOWEVENT_MOVED:
            # window moved -> monitor may have changed
            self.update_for_window()
        return None