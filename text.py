import fonts


class Text(entity.Entity):

    def __init__(self, text, x, y, font=fonts.main_font):
        self.x = x
        self.y = y
        self.font = font
        self.img = font.render(text, False, (255, 255, 255))
        self.w = self.img.get_size()[0]
        self.h = self.img.get_size()[1]

    def set_text(self, text):
        self.img = self.font.render(text, False, (255, 255, 255))
