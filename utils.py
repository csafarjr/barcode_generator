'''
        Add this class after SVGWriter in:
        [python-path]/Lib/site-packages/barcode/writer.py
'''

class PNGWriter(BaseWriter):

        def __init__(self):
            BaseWriter.__init__(self, self._init, self._paint_module,
                                self._paint_text, self._finish)
            self.format = 'PNG'
            self.font_size = 15
            self.custom_font = os.path.join(PATH, 'OpenSans-Bold.ttf')
            self.dpi = 300
            self._image = None
            self._draw = None

        def _init(self, code):
            size = self.calculate_size(len(code[0]), len(code), self.dpi)
            self._image = Image.new('RGB', size, self.background)
            self._draw = ImageDraw.Draw(self._image)

        def _paint_module(self, xpos, ypos, width, color):
            size = [(mm2px(xpos, self.dpi), mm2px(ypos, self.dpi)),
                    (mm2px(xpos + width, self.dpi),
                     mm2px(ypos + self.module_height, self.dpi))]
            self._draw.rectangle(size, outline=color, fill=color)

        def _paint_text(self, xpos, ypos):
            font = ImageFont.truetype(self.custom_font, self.font_size * 5)
            width, height = font.getsize(self.text)
            pos = (mm2px(xpos, self.dpi) - width // 2,
                   mm2px(ypos, self.dpi) - height // 2)
            self._draw.text(pos, self.text, font=font, fill=self.foreground)

        def _finish(self):
            return self._image

        def save(self, filename, output):
            filename = '{0}.{1}'.format(filename, self.format.lower())
            output.save(filename, self.format.upper())
            return filename
