"""
Generate pinout.
"""

import argparse
import math
import cairo

board_pin_sep_x = 0
board_pin_sep_y = 0

def do_work():
    global board_pin_sep_x, board_pin_sep_y

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1600, 1150)

    cr = cairo.Context(surface)

    # clear background
    cr.set_source_rgb(0, 0, 0)
    cr.paint()

    # draw the logo!
    img = cairo.ImageSurface.create_from_png('trans-logo-sml.png')
    cr.identity_matrix()
    cr.translate(0.01 * surface.get_width(), 0.01 * surface.get_height())
    cr.move_to(100, 40)
    cr.set_source_rgb(1, 1, 1)
    cr.set_font_size(40)
    cr.show_text('PYBv3')
    cr.scale(1, 1)
    cr.set_source_surface(img, 0, 0)
    cr.paint()

    # draw the board image
    img = cairo.ImageSurface.create_from_png('pybv3.png')
    board_scale = 0.963
    cr.identity_matrix()
    cr.translate(surface.get_width() / 2, surface.get_height() / 2)
    cr.scale(board_scale, board_scale)
    cr.set_source_surface(img, -img.get_width() / 2, -img.get_height() / 2 - 130)
    cr.paint()

    # coordinates for drawing labels
    cr.identity_matrix()
    cr.translate(surface.get_width() / 2, surface.get_height() / 2)

    board_left = board_scale * (-img.get_width() / 2) - 10
    board_top = board_scale * (-img.get_height() / 2) - 120
    board_right = -board_left
    board_bottom = board_scale * (img.get_height() / 2) - 120 + 10

    board_scale = 0.4
    board_left_pin_x = board_left + board_scale * 168
    board_top_pin_y = board_top + board_scale * 156
    line_left = -0.45 * surface.get_width()
    line_right = 0.45 * surface.get_width()
    board_pin_sep_x = board_scale * 114
    board_pin_sep_y = board_scale * 114
    end_point_radius = 6

    # draw left and right lines
    cr.set_source_rgb(1, 1, 1)
    for i in range(15):
        cr.move_to(line_left, board_top_pin_y + i * board_pin_sep_y)
        cr.line_to(board_left, board_top_pin_y + i * board_pin_sep_y)
        cr.move_to(line_right, board_top_pin_y + i * board_pin_sep_y)
        cr.line_to(board_right, board_top_pin_y + i * board_pin_sep_y)
    cr.stroke()
        
    # draw left- and right-line end points
    for i in range(15):
        cr.move_to(board_left, board_top_pin_y + i * board_pin_sep_y)
        cr.arc(board_left, board_top_pin_y + i * board_pin_sep_y, end_point_radius, 0, 2 * math.pi)
        cr.move_to(board_right, board_top_pin_y + i * board_pin_sep_y)
        cr.arc(board_right, board_top_pin_y + i * board_pin_sep_y, end_point_radius, 0, 2 * math.pi)
    cr.fill()

    # draw bottom left lines
    for i in range(4):
        cr.move_to(line_left, board_top_pin_y + (i + 16) * board_pin_sep_y)
        cr.line_to(board_left_pin_x + (i + 1) * board_pin_sep_x, board_top_pin_y + (i + 16) * board_pin_sep_y)
        cr.line_to(board_left_pin_x + (i + 1) * board_pin_sep_x, board_bottom)
    cr.stroke()

    # draw bottom right lines
    for i in range(6):
        cr.move_to(line_right, board_top_pin_y + (21 - i) * board_pin_sep_y)
        cr.line_to(board_left_pin_x + (i + 5) * board_pin_sep_x, board_top_pin_y + (21 - i) * board_pin_sep_y)
        cr.line_to(board_left_pin_x + (i + 5) * board_pin_sep_x, board_bottom)
    cr.stroke()

    # draw bottom end points
    for i in range(10):
        x, y = board_left_pin_x + (i + 1) * board_pin_sep_x, board_bottom
        cr.move_to(x, y)
        cr.arc(x, y, end_point_radius, 0, 2 * math.pi)
    cr.fill()

    def make_box_pos(pin_from, pin_to, xslot):
        slot_w = (board_left - line_left) / 4
        w = 0.9 * slot_w
        h = (0.9 + abs(pin_from - pin_to)) * board_pin_sep_y 
        if 1 <= pin_to <= 15:
            # left
            pin_from -= 1
            pin_to -= 1
            x = line_left + xslot * slot_w
            y = board_top_pin_y + 0.5 * (pin_from + pin_to) * board_pin_sep_y
        elif 26 <= pin_to <= 40:
            # right
            pin_from -= 26
            pin_to -= 26
            x = line_right - xslot * slot_w
            y = board_top_pin_y + (14 - 0.5 * (pin_from + pin_to)) * board_pin_sep_y
        elif 16 <= pin_to <= 19:
            # bottom left
            pin_from -= 16
            pin_to -= 16
            x = line_left + xslot * slot_w
            y = board_top_pin_y + (16 + 0.5 * (pin_from + pin_to)) * board_pin_sep_y
        elif 20 <= pin_to <= 25:
            # bottom right
            pin_from -= 20
            pin_to -= 20
            x = line_right - xslot * slot_w
            y = board_top_pin_y + (21 - 0.5 * (pin_from + pin_to)) * board_pin_sep_y
        return (x, y, w, h)

    #cr.set_font_face()
    cr.set_font_size(20)

    port_rgb = (0.8, 0.8, 0.8)
    gnd_rgb = (0.2, 0.2, 0.2)
    timer_rgb = (0.9, 0.4, 0.7)
    adc_rgb = (0.6, 0.6, 0.6)

    # top ports
    draw_text_box(cr, "micro SD slot", (), (board_left_pin_x + 3.1 * board_pin_sep_x, board_top_pin_y - 2.2 * board_pin_sep_y, 4 * board_pin_sep_x, 1 * board_pin_sep_y), port_rgb)
    draw_text_box(cr, "USB micro-AB", (), (board_left_pin_x + 8.25 * board_pin_sep_x, board_top_pin_y - 2.2 * board_pin_sep_y, 4 * board_pin_sep_x, 1 * board_pin_sep_y), port_rgb)

    draw_text_box(cr, "3.3v", (), make_box_pos(1, 1, 0), (1.0, 0.1, 0.1))
    draw_text_box(cr, "GND", (), make_box_pos(2, 2, 0), gnd_rgb)
    port_names = (None, None, 'PB13', 'PB14', 'PB15', 'PC6', 'PC7', 'PA13', 'PA14', 'PA15', 'PB3', 'PB4', 'PB6', 'PB7', None)
    for i in range(1, 16):
        pname = port_names[i - 1]
        if pname:
            draw_text_box(cr, pname, (), make_box_pos(i, i, 0), port_rgb, triangle=(None if pname in ['PA13', 'PA14'] else timer_rgb))
    draw_text_box(cr, "3.3v", (), make_box_pos(15, 15, 0), (1.0, 0.1, 0.1))

    draw_text_box(cr, "CAN2 tx", (), make_box_pos(3, 3, 2), (0.9, 0.9, 0.4))
    draw_text_box(cr, "SPI2", (), make_box_pos(3, 5, 1), (0.4, 0.9, 0.4))
    draw_text_box(cr, "USART6", (), make_box_pos(6, 7, 2), (0.9, 0.4, 0.4))
    draw_text_box(cr, "I2C1", (), make_box_pos(13, 14, 1), (0.4, 0.4, 0.9))
    draw_text_box(cr, "USART1", (), make_box_pos(13, 14, 2), (0.9, 0.4, 0.4))

    draw_text_box(cr, "BOOT0", (), make_box_pos(16, 16, 0), (0.4, 0.4, 0.4))
    draw_text_box(cr, "RST", (), make_box_pos(17, 17, 0), (0.4, 0.4, 0.4))
    draw_text_box(cr, "PB8", (), make_box_pos(18, 18, 0), port_rgb, triangle=timer_rgb)
    draw_text_box(cr, "PB9", (), make_box_pos(19, 19, 0), port_rgb, triangle=timer_rgb)

    draw_text_box(cr, "I2C1", (), make_box_pos(18, 19, 1), (0.4, 0.4, 0.9))
    draw_text_box(cr, "CAN1", (), make_box_pos(18, 19, 2), (0.9, 0.9, 0.4))

    draw_text_box(cr, "PC0", (), make_box_pos(20, 20, 0), port_rgb)
    draw_text_box(cr, "PC1", (), make_box_pos(21, 21, 0), port_rgb)
    draw_text_box(cr, "PC2", (), make_box_pos(22, 22, 0), port_rgb)
    draw_text_box(cr, "PC3", (), make_box_pos(23, 23, 0), port_rgb)
    draw_text_box(cr, "GND", (), make_box_pos(24, 24, 0), gnd_rgb)
    draw_text_box(cr, "VIN", (), make_box_pos(25, 25, 0), (1.0, 0.1, 0.1))
    
    # bottom right special function
    draw_text_box(cr, "ADC", (), make_box_pos(20, 23, 3), adc_rgb)

    port_names = ('PA0', 'PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7', 'PB0', 'PB1', 'PB10', 'PB11', 'PB12', None, None)
    for i in range(26, 41):
        pname = port_names[i - 26]
        if pname:
            draw_text_box(cr, pname, (), make_box_pos(i, i, 0), port_rgb, triangle=(None if pname in ['PB12', 'PA4'] else timer_rgb))
    draw_text_box(cr, "GND", (), make_box_pos(39, 39, 0), gnd_rgb)
    draw_text_box(cr, "VIN", (), make_box_pos(40, 40, 0), (1.0, 0.1, 0.1))

    # right special function
    draw_text_box(cr, "ADC", (), make_box_pos(26, 35, 3), adc_rgb)
    draw_text_box(cr, "USART4", (), make_box_pos(26, 27, 2), (0.9, 0.4, 0.4))
    draw_text_box(cr, "USART2", (), make_box_pos(28, 29, 2), (0.9, 0.4, 0.4))
    draw_text_box(cr, "DAC", (), make_box_pos(30, 31, 2), (0.4, 0.4, 0.4))
    #draw_text_box(cr, "SPI1", ('ck', 'miso', 'mosi'), make_box_pos(31, 33, 1), (0.4, 0.9, 0.4))
    draw_text_box(cr, "SPI1", (), make_box_pos(31, 33, 1), (0.4, 0.9, 0.4))
    draw_text_box(cr, "I2C2", (), make_box_pos(36, 37, 1), (0.4, 0.4, 0.9))
    draw_text_box(cr, "USART3", (), make_box_pos(36, 37, 2), (0.9, 0.4, 0.4))
    draw_text_box(cr, "rx CAN2", (), make_box_pos(38, 38, 2), (0.9, 0.9, 0.4))

    text_scale = 2
    # draw labels
    cr.identity_matrix()
    #cr.translate(surface.get_width() / 2 + x, surface.get_height() / 2 + y)
    cr.set_font_size(16)
    for kw in ["test", "again"]:
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(text_scale * 10, text_scale * 4)
        cr.show_text(kw)
        cr.fill()

    surface.write_to_png('pinout.png')
    surface.finish()

def text_centre(cr, text, x, y):
    ext = cr.text_extents(text)
    cr.move_to(x - 0.5 * ext[2] - ext[0], y - 0.5 * ext[3] - ext[1])
    cr.show_text(text)

def text_left(cr, text, x, y):
    ext = cr.text_extents(text)
    cr.move_to(x - ext[0], y - 0.5 * ext[3] - ext[1])
    cr.show_text(text)

def draw_text_box(cr, text, detail, geom, rgb, triangle=None):
    x, y, w, h = geom
    cr.set_source_rgb(rgb[0], rgb[1], rgb[2])
    cr.rectangle(x - 0.5 * w, y - 0.5 * h, w, h)
    cr.fill()
    if triangle is not None:
        cr.set_source_rgb(triangle[0], triangle[1], triangle[2])
        cr.move_to(x + 0.5 * w, y + 0.5 * h)
        cr.rel_line_to(0, -0.4 * h)
        cr.rel_line_to(-0.4 * h, 0.4 * h)
        cr.rel_line_to(0.4 * h, 0)
        cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(x - 0.5 * w, y - 0.5 * h, w, h)
    cr.stroke()
    if rgb[0] + rgb[1] + rgb[2] < 0.7:
        cr.set_source_rgb(1, 1, 1)
    else:
        cr.set_source_rgb(0, 0, 0)
    text_centre(cr, text, x, y)
    for i in range(len(detail)):
        text_left(cr, detail[i], x - 30, y - (0.5 * (len(detail) - 1) - i) * board_pin_sep_y)

def main():
    # command line arguments
    cmd_parser = argparse.ArgumentParser(description='Generate pyboard pinout.')
    args = cmd_parser.parse_args()

    # do the work
    do_work()

if __name__ == '__main__':
    main()
