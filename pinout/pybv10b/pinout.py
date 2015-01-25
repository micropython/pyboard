"""
Generate pinout for PYBv1.0.

This file is part of the Micro Python project, http://micropython.org/
Licensed under the The MIT License
Copyright (c) 2013, 2014 Damien P. George
"""

import argparse
import math
import re
import cairo

board_unit_x = 0
board_unit_y = 0

class Pin:
    def __init__(self, name, label, pos, cpu):
        self.name = name
        self.label = label
        self.pos = pos
        self.cpu = cpu
        self.tim = [None, None, None]

# pos is from top left, which is (1,1)
pin_info = [
    Pin('X1', 'X1', (12, 16), 'A0'),
    Pin('X2', 'X2', (12, 15), 'A1'),
    Pin('X3', 'X3', (12, 14), 'A2'),
    Pin('X4', 'X4', (12, 13), 'A3'),
    Pin('X5', 'X5', (12, 12), 'A4'),
    Pin('X6', 'X6', (12, 11), 'A5'),
    Pin('X7', 'X7', (12, 10), 'A6'),
    Pin('X8', 'X8', (12, 9), 'A7'),

    Pin('X9', 'X9', (1, 9), 'B6'),
    Pin('X10', 'X10', (1, 10), 'B7'),
    Pin('X11', 'X11', (1, 11), 'C4'),
    Pin('X12', 'X12', (1, 12), 'C5'),
    Pin('X13', 'RST', (1, 13), None),
    Pin('X14', 'GND', (1, 14), None),
    Pin('X15', '3V3', (1, 15), None),
    Pin('X16', 'VIN', (1, 16), None),

    Pin('X17', 'X17', (2, 16), 'B3'),
    Pin('X18', 'X18', (3, 16), 'C13'),
    Pin('X19', 'X19', (4, 16), 'C0'),
    Pin('X20', 'X20', (5, 16), 'C1'),
    Pin('X21', 'X21', (6, 16), 'C2'),
    Pin('X22', 'X22', (7, 16), 'C3'),
    Pin('X23', 'A3V3', (8, 16), None),
    Pin('X24', 'AGND', (9, 16), None),

    Pin('P1', 'BOOT0', (2, 15), None),
    Pin('P2', 'P2', (3, 15), 'B4'),
    Pin('P3', 'P3', (4, 15), 'A15'),
    Pin('P4', 'P4', (5, 15), 'A14'),
    Pin('P5', 'P5', (6, 15), 'A13'),
    Pin('P6', 'VBAT', (7, 15), None),
    Pin('P7', 'VIN', (8, 15), None),
    Pin('P8', 'GND', (9, 15), None),

    Pin('Y1', 'Y1', (1, 1), 'C6'),
    Pin('Y2', 'Y2', (1, 2), 'C7'),
    Pin('Y3', 'Y3', (1, 3), 'B8'),
    Pin('Y4', 'Y4', (1, 4), 'B9'),
    Pin('Y5', 'Y5', (1, 5), 'B12'),
    Pin('Y6', 'Y6', (1, 6), 'B13'),
    Pin('Y7', 'Y7', (1, 7), 'B14'),
    Pin('Y8', 'Y8', (1, 8), 'B15'),

    Pin('Y9', 'Y9', (12, 8), 'B10'),
    Pin('Y10', 'Y10', (12, 7), 'B11'),
    Pin('Y11', 'Y11', (12, 6), 'B0'),
    Pin('Y12', 'Y12', (12, 5), 'B1'),
    Pin('Y13', 'RST', (12, 4), None),
    Pin('Y14', 'GND', (12, 3), None),
    Pin('Y15', '3V3', (12, 2), None),
    Pin('Y16', 'VIN', (12, 1), None),
]

# parse af from csv
with open('stm32f4xx_af.csv') as f:
    tim_idx = {
        1:0, 2:0,
        4:1, 5:1, 6:1, 7:1, 8:1,
        9:2, 10:2, 11:2, 12:2, 13:2, 14:2
    }
    f.readline() # skip header
    for line in f:
        port, pin_name, *afs = line.strip().split(',')
        pin_name = pin_name[1:] # skip letter "P"
        pin = None
        for p in pin_info:
            if p.cpu == pin_name:
                pin = p
                break
        if pin is None:
            continue
        afs2 = []
        for af in afs:
            afs2.extend(af.split('/'))
        for af in afs2:
            m = re.match(r'TIM(\d{1,2})_CH\dN?', af)
            if m and int(m.group(1)) in tim_idx:
                pin.tim[tim_idx[int(m.group(1))]] = af

def make_pinout():
    global board_unit_x, board_unit_y

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2000, 1500)

    cr = cairo.Context(surface)

    # clear background
    cr.set_source_rgb(0.9, 0.9, 0.9)
    cr.paint()

    # draw the logo!
    img = cairo.ImageSurface.create_from_png('trans-logo-sml.png')
    cr.identity_matrix()
    cr.translate(0.01 * surface.get_width(), 0.01 * surface.get_height())
    cr.move_to(120, 1400)
    cr.set_source_rgb(0, 0, 0)
    cr.set_font_size(80)
    cr.show_text('PYBv1.0')
    cr.move_to(20, 1310)
    cr.set_font_size(38.5)
    cr.show_text('Micro Python pyboard')
    cr.move_to(1520, 1400)
    cr.set_font_size(50)
    cr.show_text('micropython.org')
    cr.scale(1, 1)
    cr.translate(20, 1330)
    cr.set_source_surface(img, 0, 0)
    cr.paint()

    # coordinates for drawing labels
    cr.identity_matrix()
    cr.translate(surface.get_width() / 2, 0.35 * surface.get_height())
    cr.translate(-238, -363)
    board_unit_x = 43.6
    board_unit_y = 43.4

    board_left = 0 * board_unit_x
    board_top = 0 * board_unit_y
    board_right = 11 * board_unit_x
    board_bottom = 15 * board_unit_y

    line_left = board_left - 15.5 * board_unit_x
    line_right = board_right + 15.5 * board_unit_x
    end_point_offset = 1.5 * board_unit_x
    end_point_radius = 8

    cr.set_font_size(20)

    v33_rgb = (1.0, 0.1, 0.1)
    vin_rgb = (1.0, 0.2, 0.2)
    vbat_rgb = (1.0, 0.5, 0.5)
    gnd_rgb = (0.2, 0.2, 0.2)
    port_rgb = (0.9, 0.8, 0.3)
    cpu_rgb = (1.0, 1.0, 1.0)
    tim_rgb = (0.8, 0.6, 1.0)
    adc_rgb = (0.6, 0.6, 0.6)
    dac_rgb = (0.4, 0.4, 0.4)
    boot0_rgb = (0.4, 0.4, 0.4)
    can_rgb = (0.9, 0.9, 0.6)
    i2c_rgb = (0.4, 0.4, 0.9)
    spi_rgb = (0.4, 0.9, 0.4)
    uart_rgb = (0.9, 0.4, 0.4)

    # Y skin shadow
    cr.set_source_rgba(0, 0.5, 0, 0.2)
    cr.move_to(board_right + 2.0 * board_unit_x, board_top - 1.5 * board_unit_y)
    cr.rel_line_to(0, 9.0 * board_unit_y)
    cr.rel_line_to(-15 * board_unit_x, 0)
    cr.rel_line_to(0, -9.0 * board_unit_y)
    cr.close_path()
    cr.fill()
    cr.set_source_rgb(0, 0.5, 0)
    draw_text(cr, "Y skin", board_left - 1.8 * board_unit_x, board_top - 1 * board_unit_y, "l")

    # X skin shadow
    cr.set_source_rgba(0, 0, 0.5, 0.2)
    cr.move_to(board_right + 2.0 * board_unit_x, board_top + 7.5 * board_unit_y)
    cr.rel_line_to(0, 10.5 * board_unit_y)
    cr.rel_line_to(-15 * board_unit_x, 0)
    cr.rel_line_to(0, -10.5 * board_unit_y)
    cr.fill()
    cr.set_source_rgb(0, 0, 0.5)
    draw_text(cr, "X skin", board_right + 1.8 * board_unit_x, board_bottom + 2.5 * board_unit_y, "r")

    # shadow for holes
    cr.set_source_rgb(0.8, 0.7, 0.3)
    cr.move_to(board_right + 0.5 * board_unit_x, board_top - 0.4 * board_unit_y)
    cr.rel_line_to(0, 16 * board_unit_y)
    cr.rel_line_to(-12 * board_unit_x, 0)
    cr.rel_line_to(0, -16 * board_unit_y)
    cr.fill()

    # draw the board image
    cr.save()
    img = cairo.ImageSurface.create_from_png('pybv10b-front-trans.png')
    board_scale = 0.28
    cr.identity_matrix()
    cr.translate(surface.get_width() / 2, 0.35 * surface.get_height())
    cr.scale(board_scale, board_scale)
    cr.set_source_surface(img, -img.get_width() / 2, -img.get_height() / 2 - 130)
    cr.paint()
    cr.restore()

    def make_box_pos(pin_from, pin_to, xslot):
        xslot += 3.38
        slot_w = 1.9 * board_unit_x
        w = 0.9 * slot_w
        h = (0.9 + abs(pin_from - pin_to)) * board_unit_y 
        if 1 <= pin_to <= 16:
            # left
            pin_from -= 1
            pin_to -= 1
            x = line_left + xslot * slot_w
            y = board_top + 0.5 * (pin_from + pin_to) * board_unit_y
        elif 26 <= pin_to <= 42:
            # right
            pin_from -= 26
            pin_to -= 26
            x = line_right - xslot * slot_w
            y = board_top + (15 - 0.5 * (pin_from + pin_to)) * board_unit_y
        else:
            assert False
        return (x, y, w, h)

    def make_box_pos_inner_row(x, y, w, h):
        return (board_left + (x - 1 + 0.5 * (w - 1)) * board_unit_x, board_bottom + (4 + 0.5 * (y + y + h - 1)) * board_unit_y, (0.9 + w - 1) * board_unit_x, (y + h - 1 - y + 0.9) * board_unit_y)

    # draw left and right lines
    cr.set_source_rgb(0, 0, 0)
    for i in range(16):
        cr.move_to(line_left, board_top + i * board_unit_y)
        cr.line_to(board_left - end_point_offset, board_top + i * board_unit_y)
        cr.move_to(line_right, board_top + i * board_unit_y)
        cr.line_to(board_right + end_point_offset, board_top + i * board_unit_y)
    cr.stroke()
        
    # draw left- and right-line end points
    for i in range(16):
        cr.move_to(board_left, board_top + i * board_unit_y)
        cr.arc(board_left - end_point_offset, board_top + i * board_unit_y, end_point_radius, 0, 2 * math.pi)
        cr.move_to(board_right, board_top + i * board_unit_y)
        cr.arc(board_right + end_point_offset, board_top + i * board_unit_y, end_point_radius, 0, 2 * math.pi)
    cr.fill()

    # draw bottom lines
    for i in range(8):
        # for inner
        cr.move_to(board_left + (i + 1) * board_unit_x, board_bottom + end_point_offset + 0.5 * board_unit_y)
        cr.rel_line_to(-0.3 * board_unit_x, 0.3 * board_unit_y)
        cr.rel_line_to(0, 4 * board_unit_y)
        # for outer
        cr.move_to(board_left + (i + 1) * board_unit_x, board_bottom + end_point_offset + board_unit_y)
        cr.rel_line_to(0, 10 * board_unit_y)
    for i in range(8, 10):
        # for servo power
        cr.move_to(board_left + (i + 1) * board_unit_x, board_bottom + end_point_offset)
        cr.rel_line_to(0, 8 * board_unit_y)
    cr.stroke()

    # draw bottom end points
    for i in range(8):
        x, y = board_left + (i + 1) * board_unit_x, board_bottom + end_point_offset + 0.5 * board_unit_y
        cr.move_to(x, y)
        cr.arc(x, y, end_point_radius, 0, 2 * math.pi)
        y += 0.5 * board_unit_y
        cr.move_to(x, y)
        cr.arc(x, y, end_point_radius, 0, 2 * math.pi)
    for i in range(8, 10):
        # for servo power
        x, y = board_left + (i + 1) * board_unit_x, board_bottom + end_point_offset
        for j in range(4):
            cr.move_to(x, y)
            cr.arc(x, y, end_point_radius, 0, 2 * math.pi)
            y += 0.3333 * board_unit_y
    cr.fill()

    # top ports
    draw_text_box(cr, "micro SD slot", (), (board_left + 3.1 * board_unit_x, board_top - 2.2 * board_unit_y, 4 * board_unit_x, 1 * board_unit_y), port_rgb)
    draw_text_box(cr, "USB micro-AB", (), (board_left + 8.25 * board_unit_x, board_top - 2.2 * board_unit_y, 4 * board_unit_x, 1 * board_unit_y), port_rgb)

    # left and right pins
    for pin in pin_info:
        pname = pin.label
        if pname == "GND":
            rgb = gnd_rgb
        elif pname == "3.3v" or pname == "3V3":
            rgb = v33_rgb
        elif pname == "VIN":
            rgb = vin_rgb
        elif pname == "RST":
            rgb = boot0_rgb
        else:
            rgb = port_rgb
        print(pin.name, pin.tim)
        if pin.pos[0] == 1:
            box_pos_x = line_left
            box_pos_x_delta = 1
        elif pin.pos[0] == 12:
            box_pos_x = line_right
            box_pos_x_delta = -1
        elif 2 <= pin.pos[0] <= 9:
            continue
        else:
            assert False

        # main port name
        box_pos_y = board_top + (pin.pos[1] - 1) * board_unit_y
        box_pos = (
            box_pos_x - box_pos_x_delta * 0 * board_unit_x, box_pos_y,
            1.6 * board_unit_x, 0.9 * board_unit_y
        )
        draw_text_box(cr, pin.label, (), box_pos, rgb)

        # pin cpu name
        if pin.cpu is not None:
            box_pos = (
                box_pos_x - box_pos_x_delta * (-1.8) * board_unit_x, box_pos_y,
                box_pos[2], box_pos[3]
            )
            draw_text_box(cr, pin.cpu, (), box_pos, cpu_rgb)

        # timers
        for i in range(3):
            if pin.tim[i] is None:
                continue
            box_pos = (
                box_pos_x - box_pos_x_delta * (-3.5 - 1.55 * i) * board_unit_x, box_pos_y,
                1.35 * board_unit_x, box_pos[3]
            )
            draw_text_box(cr, pin.tim[i].split('_'), (), box_pos, tim_rgb, font_size=18)

    draw_text_box(cr, "I2C(1)", ("l", "SCL", "SDA"), make_box_pos(9, 10, 1), i2c_rgb) # SCL,SDA=X9,X10
    draw_text_box(cr, "I2C(2)", ("r", "SDA", "SCL"), make_box_pos(34, 35, 1), i2c_rgb) # SCL,SDA=Y9,Y10

    draw_text_box(cr, "SPI(1)", ("r", "MOSI", "MISO", "SCK", "/SS"), make_box_pos(30, 33, 1), spi_rgb)
    draw_text_box(cr, "SPI(2)", ("l", "/SS", "SCK", "MISO", "MOSI"), make_box_pos(5, 8, 1), spi_rgb)

    draw_text_box(cr, "CAN(1)", ("l", "RX", "TX"), make_box_pos(3, 4, 2), can_rgb)
    draw_text_box(cr, "CAN(2)", ("l", "RX", "TX"), make_box_pos(5, 6, 2), can_rgb)

    draw_text_box(cr, "UART(1)", ("l", "TX", "RX"), make_box_pos(9, 10, 2), uart_rgb)
    draw_text_box(cr, "UART(2)", ("r", "RX", "TX"), make_box_pos(28, 29, 2), uart_rgb)
    draw_text_box(cr, "UART(3)", ("r", "RX", "TX"), make_box_pos(34, 35, 2), uart_rgb)
    draw_text_box(cr, "UART(4)", ("r", "RX", "TX"), make_box_pos(26, 27, 2), uart_rgb)
    draw_text_box(cr, "UART(6)", ("l", "TX", "RX"), make_box_pos(1, 2, 2), uart_rgb)

    draw_text_box(cr, "DAC", (), make_box_pos(30, 31, 2), dac_rgb)

    draw_text_box(cr, "ADC", (), make_box_pos(11, 12, 3), adc_rgb) # C4-C5
    draw_text_box(cr, "ADC", (), make_box_pos(26, 33, 3), adc_rgb) # A0-A7
    draw_text_box(cr, "ADC", (), make_box_pos(36, 37, 3), adc_rgb) # B0-B1

    # bottom rows
    for pin in pin_info:
        if not (2 <= pin.pos[0] <= 9):
            continue
        if pin.label == 'BOOT0':
            rgb = boot0_rgb
        elif pin.label == 'VBAT':
            rgb = vbat_rgb
        elif pin.label == 'VIN':
            rgb = vin_rgb
        elif pin.label == 'A3V3':
            rgb = v33_rgb
        elif pin.label in ('GND', 'AGND'):
            rgb = gnd_rgb
        else:
            rgb = port_rgb
        x = pin.pos[0] + 0.3 * (pin.pos[1] - 16)
        y = 2 + 6.5 * (pin.pos[1] - 15)
        draw_text_box(cr, pin.label, ("c90",), make_box_pos_inner_row(x, y, 1, 2.2), rgb)
        if pin.cpu is not None:
            y = 0.25 + 6.5 * (pin.pos[1] - 15)
            draw_text_box(cr, pin.cpu, ("c90",), make_box_pos_inner_row(x, y, 1, 1.6), cpu_rgb)

    draw_text_box(cr, "B3 (USR)", ("c90",), make_box_pos_inner_row(2, 5.4, 1, 2.95), cpu_rgb)
    draw_text_box(cr, "C13 (3mA)", ("c90",), make_box_pos_inner_row(3, 5.4, 1, 2.95), cpu_rgb, font_size=20)
    draw_text_box(cr, "shielded ADC", (), make_box_pos_inner_row(4, 5.4, 4, 1.2), adc_rgb)
    draw_text_box(cr, "GND", ("c90",), make_box_pos_inner_row(10, 0.25, 1, 10.45), gnd_rgb)
    draw_text_box(cr, "VIN", ("c90",), make_box_pos_inner_row(11, 0.25, 1, 10.45), vin_rgb)

    # extra text

    draw_text(cr, ["pin", "name"], line_left - 0.8 * board_unit_x, board_top - 1.25 * board_unit_y, "l")
    draw_text(cr, ["CPU", "name"], line_left + 1 * board_unit_x, board_top - 1.25 * board_unit_y, "l")
    draw_text(cr, "available timers", board_left - 10.25 * board_unit_x, board_top - 1.25 * board_unit_y, "c")
    draw_text(cr, "peripherals", board_left - 5.25 * board_unit_x, board_top - 1.25 * board_unit_y, "c")

    draw_text(cr, ["pin", "name"], line_right + 0.8 * board_unit_x, board_bottom + 1.25 * board_unit_y, "r")
    draw_text(cr, ["CPU", "name"], line_right - 1 * board_unit_x, board_bottom + 1.25 * board_unit_y, "r")
    draw_text(cr, "available timers", board_right + 10.25 * board_unit_x, board_bottom + 1.25 * board_unit_y, "c")
    draw_text(cr, "peripherals", board_right + 5.25 * board_unit_x, board_bottom + 1.25 * board_unit_y, "c")

    draw_text(cr, "inner row", board_left - 0.25 * board_unit_x, board_bottom + 6.5 * board_unit_y, "r")
    draw_text(cr, "outer row", board_left, board_bottom + 13 * board_unit_y, "r")

    text_pos_x = board_right + 1 * board_unit_x
    text_pos_y = board_bottom + 8 * board_unit_y
    text = [
        "VIN: 3.6v - 10v power input",
        "        (supplied by USB when USB connected)",
        "3V3: regulated 3.3v output only, max 300mA",
        "VBAT: battery backup input",
        "A3V3: analog reference connected to 3V3 via inductor",
        "",
        "X17 is pulled to GND via 4.7k resistor when USR pressed",
        "P2-P5 are connected to the 4 LEDs",
        "SD = A8 is used for SD card switch",
        "MMA_INT = B2 is used for accelerometer interrupts",
        "",
        "connect BOOT0 to 3V3 and press RST to enter DFU mode",
    ]
    draw_text(cr, text, text_pos_x, text_pos_y, "l")


    surface.write_to_png('pinout.png')
    surface.finish()

def draw_text(cr, text, x, y, alignment):
    if not isinstance(text, list):
        text = [text]
    ext_x_bear, ext_y_bear, ext_w, ext_h, _, _ = cr.text_extents(text[0])
    for i in range(1, len(text)):
        ext = cr.text_extents(text[i])
        ext_w = max(ext_w, ext[2])
    if alignment == "c":
        x = x - 0.5 * ext_w - ext_x_bear
        y = y - 0.5 * ext_h - ext_y_bear
    elif alignment == "c90":
        x = x - 0.5 * ext_h - ext_y_bear
        y = y + 0.5 * ext_w + ext_x_bear
    elif alignment == "l":
        x = x - ext_x_bear
        y = y - 0.5 * ext_h - ext_y_bear
    elif alignment == "r":
        x = x - ext_w - ext_x_bear
        y = y - 0.5 * ext_h - ext_y_bear
    else:
        assert False
    y -= 0.5 * (len(text) - 1) * 1.15 * ext_h
    cr.move_to(x, y)
    for t in text:
        if alignment == "c90":
            cr.save()
            cr.rotate(-1.570796)
        cr.show_text(t)
        if alignment == "c90":
            cr.restore()
        y += 1.15 * ext_h
        cr.move_to(x, y)

def draw_text_box(cr, text, detail, geom, rgb, font_size=24):
    x, y, w, h = geom
    cr.set_source_rgb(rgb[0], rgb[1], rgb[2])
    cr.rectangle(x - 0.5 * w, y - 0.5 * h, w, h)
    cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(x - 0.5 * w, y - 0.5 * h, w, h)
    cr.stroke()
    if rgb[0] + rgb[1] + rgb[2] < 0.7:
        cr.set_source_rgb(1, 1, 1)
    else:
        cr.set_source_rgb(0, 0, 0)
    if len(detail) == 0:
        cr.set_font_size(font_size)
        draw_text(cr, text, x, y, "c")
    elif len(detail) == 1:
        cr.set_font_size(font_size)
        draw_text(cr, text, x, y, detail[0])
    else:
        if detail[0] == "l":
            sign = 1
            align = "r"
        elif detail[0] == "r":
            sign = -1
            align = "l"
        else:
            assert False
        max_detail_label = max(len(d) for d in detail)
        cr.set_font_size(18)
        draw_text(cr, text, x - sign * (0.14 + 0.04 * max_detail_label) * w, y, "c90")
        x_detail = x + sign * 0.42 * w
        y_detail = y - ((0.5 * len(detail) - 2) + 2) * board_unit_y
        cr.set_font_size(17)
        for i in range(1, len(detail)):
            draw_text(cr, detail[i], x_detail, y_detail + i * board_unit_y, align)

def main():
    # command line arguments
    cmd_parser = argparse.ArgumentParser(description='Generate pyboard pinout.')
    args = cmd_parser.parse_args()

    # make the pinout
    make_pinout()

if __name__ == '__main__':
    main()
