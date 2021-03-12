#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import requests
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

DELIVERY_STATUS_URL = "http://localhost/delivery.json"

# Configuration for the matrix
options = RGBMatrixOptions()
options.scan_mode = 0
options.pwm_lsb_nanoseconds = 130
options.pwm_bits = 11
options.show_refresh_rate = 0
options.gpio_slowdown = 4
options.rows = 32
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = "adafruit-hat"
options.drop_privileges = False

text_speed = 0.02
refresh_rate = 50 * 300


def delivery_status():
    res = requests.get(DELIVERY_STATUS_URL).json()

    return res


def led_display():
    matrix = RGBMatrix(options=options)
    offscreen_canvas = matrix.CreateFrameCanvas()
    pos = offscreen_canvas.width
    font_path = "fonts/"
    count = 0

    # Kolonial
    delivery = delivery_status()

    clock_color = graphics.Color(255, 165, 20)
    clock_font = graphics.Font()
    clock_font.LoadFont(os.path.join(font_path, "6x9.bdf"))

    k_header = "Kolonial.no Delivery Tracker"
    k_header_color = graphics.Color(255, 165, 20)
    k_header_font = graphics.Font()
    k_header_font.LoadFont(os.path.join(font_path, "6x9.bdf"))

    d_title = delivery.get("title")
    d_title_color = graphics.Color(0, 255, 0)
    d_title_font = graphics.Font()
    d_title_font.LoadFont(os.path.join(font_path, "clR6x12.bdf"))

    d_status = delivery.get("status")
    d_status_color = graphics.Color(238, 238, 228)
    d_status_font = graphics.Font()
    d_status_font.LoadFont(os.path.join(font_path, "6x12.bdf"))

    while True:
        clock = str(datetime.now().strftime("%H:%M:%S"))
        count += 1
        if count == refresh_rate:
            count = 0
            print(f"{datetime.now()} - Refreshing data...")

            delivery = delivery_status()
            d_title = delivery.get("title")
            d_status = delivery.get("status")

        offscreen_canvas.Clear()

        graphics.DrawText(offscreen_canvas, k_header_font, 0, 6, k_header_color, k_header)
        graphics.DrawText(offscreen_canvas, clock_font, 207, 6, clock_color, clock)
        graphics.DrawText( offscreen_canvas, d_title_font, 12, 19, d_title_color, d_title)
        len = graphics.DrawText(offscreen_canvas, d_status_font, pos, 31, d_status_color, d_status)

        pos -= 1
        if pos + len < 0:
            pos = offscreen_canvas.width

        time.sleep(text_speed)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__":
    print("Starting...")
    led_display()
