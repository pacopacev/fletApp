import flet as ft
import math
import time
import random
import asyncio


class EQ(ft.Container):
    def __init__(self, page: ft.Page, *, width: int = 400, height: int = 300, num_bars: int = 10, levels: int = 13, block_height: int = 15, spacing: int = 2, update_interval: float = 0.15):
        """Equalizer visual control.

        Parameters:
          - page: ft.Page
          - width, height: control size
          - num_bars: number of vertical bars
          - levels: vertical resolution (rows)
          - block_height: pixel height of each block row
          - spacing: spacing between rows
          - update_interval: seconds between animation frames
        """
        self.page = page
        self.num_bars = num_bars
        self.levels = levels
        self.block_height = block_height
        self.spacing = spacing
        self.update_interval = update_interval

        # Colors
        self.red = ft.Colors.RED
        self.green = ft.Colors.GREEN
        self.yellow = ft.Colors.YELLOW
        self.blue = ft.Colors.BLUE
        self.purple = ft.Colors.PURPLE
        self.cyan = ft.Colors.CYAN
        self.white = ft.Colors.WHITE

        self.is_running = False
        self.animation_task = None

        # Colors for bars (cycled)
        self.colors = [self.red, self.yellow, self.green, self.cyan, self.blue, self.purple]

        # Start animation (will schedule on event loop)
        # Note: start_animation will try to create an asyncio task; if the page's loop
        # isn't running yet the implementation will fallback gracefully.
        # Keep width/height passed to super so they are available as attributes.
        super().__init__(
            content=ft.Text("Initializing Equalizer..."),
            width=width,
            height=height,
            bgcolor=ft.Colors.BLACK,
            padding=4,
            border=None,
            border_radius=6,
        )

        # Kick off animation
        self.start_animation()

    def update_equalizer_display(self, bar_heights):
        """Update the visual display of the equalizer"""
        bars_display = ft.Row(spacing=6, alignment=ft.MainAxisAlignment.CENTER)

        # Create vertical bars left-to-right
        for i, bar_height in enumerate(bar_heights[: self.num_bars]):
            col = ft.Column(spacing=self.spacing, alignment=ft.MainAxisAlignment.END)
            color = self.colors[i % len(self.colors)]
            # compute block width based on control width
            try:
                block_w = max(6, int(self.width / (self.num_bars + 2)))
            except Exception:
                block_w = 10
            for level in range(self.levels, 0, -1):
                if bar_height >= level:
                    block = ft.Container(
                        width=block_w,
                        height=self.block_height,
                        bgcolor=color,
                        border_radius=ft.border_radius.all(2),
                    )
                else:
                    block = ft.Container(
                        width=block_w,
                        height=self.block_height,
                        bgcolor=ft.Colors.BLACK,
                        border_radius=ft.border_radius.all(2),
                    )
                col.controls.append(block)
            bars_display.controls.append(col)

        self.content = bars_display
        # Update this control only (safer than calling page.update() from elsewhere)
        try:
            self.update()
        except Exception:
            # Fallback to page.update() if control update fails for any reason
            try:
                self.page.update()
            except Exception:
                pass

    async def equalizer_animation(self):
        """The main equalizer animation loop (runs on asyncio loop)."""
        while self.is_running:
            bar_heights = []
            for i in range(self.num_bars):
                base_height = 1 + abs(math.sin(time.time() * 2 + i * 0.5)) * (self.levels - 1)
                noise = random.uniform(-1, 1)
                height_val = int(base_height + noise)
                bar_heights.append(max(1, min(self.levels, height_val)))

            # Update the display on the main event loop
            self.update_equalizer_display(bar_heights)
            await asyncio.sleep(self.update_interval)

    def start_animation(self):
        """Start the equalizer animation"""
        if not self.is_running:
            self.is_running = True
            # Create an asyncio task so animation runs on the main event loop
            try:
                self.animation_task = asyncio.create_task(self.equalizer_animation())
            except RuntimeError:
                # If there's no running loop, schedule the task via the page
                try:
                    self.page.session.run_sync(lambda: asyncio.create_task(self.equalizer_animation()))
                except Exception:
                    # If scheduling fails, leave is_running True and let
                    # the caller try again once the loop is active.
                    pass

    def stop_animation(self):
        """Stop the equalizer animation"""
        self.is_running = False
        # Cancel asyncio task if running
        try:
            if self.animation_task and not self.animation_task.done():
                self.animation_task.cancel()
        except Exception:
            pass
        