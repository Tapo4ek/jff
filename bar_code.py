#! /usr/bin/python2.7

import Image
import ImageDraw
import ImageFont
import base64
import sys
import cStringIO
import os

TABLE = {'0':'00110', '1':'10001', '2':'01001', '3':'11000', '4':'00101', '5':'10100', '6':'01100', '7':'00011', '8':'10010', '9':'01010'}

class InterLeaved2of5:
    """
    Generates InterLeaved 2 of 5 Bar code as base64
    import bar_code
    bar_code_obj = bar_code.InterLeaved2of5('10987654321007412589630')
    im = bar_code_obj.get_image()
    """

    def __init__(self, data=sys.argv[1], width=2, height=50, first_color='#000000', second_color='#ffffff', font="ARIAL.TTF"):
        self.data = data
        self.width = width
        self.height = height
        self.first_color = first_color
        self.second_color = second_color
        self.font = font

    def _control_number(self):
        """
        Function counts control number
        and returns all data plus control number as string
        """
        if len(self.data) % 2 == 0:
            self.data = '0' + self.data
        even_array = []
        odd_array = []
        for even in self.data[1::2]:
            even_array += [eval(even)]
        for odd in self.data[::2]:
            odd_array += [eval(odd)]
        all_sum = sum(odd_array) * 3 + sum(even_array)
        control_number = 0
        while all_sum % 10 != 0:
            all_sum += 1
            control_number += 1
        self.data = self.data + str(control_number)
        self.value = ''
        for i in self.data:
            self.value += i

    def _encoding(self):
        """
        Function encoding all data to bits
        and returns string of bits
        """
        self._control_number()
        self.value = self.data[:]
        start = '0000'
        stop = '100'
        counter = 0
        encoding_numbers = ''
        while counter < len(self.data):
            for num1, num2 in zip(TABLE[self.data[counter]], TABLE[self.data[counter+1]]):
                encoding_numbers += ''.join(num1+num2)
            counter += 2
        self.data = start + encoding_numbers + stop

    def _image_size(self):
        """
        Count width of the image
        """
        self._encoding()
        bits = self.data
        all_width = 0
        for bit in bits:
            if bit == '0':
                all_width += self.width
            else:
                all_width += self.width *3
        self.image_width = self.width * 2 + all_width

    def _get_font_size(self):
        """
        Count font size for the image
        """
        image_height = self.height * 100 / 67
        good_size = False
        self.font_size = 1
        while not good_size:
            font = ImageFont.truetype(self.font, self.font_size)
            self.all_len = 0
            for i in self.value:
                length, height = font.getsize(i)
                self.all_len += length
            if ((self.image_width / 2) < self.all_len < self.image_width) and (height < image_height-self.height):
                good_size = True
            if self.all_len > self.image_width or height > (image_height - self.height):
                self.font_size -= 1
                good_size = True
            else:
                self.font_size += 1

    def get_image(self):
        """
        Function creats image
        then loading font and creating a number under image
        """
        self._image_size()
        all_bits = self.data
        image_height = self.height * 100 / 67
        numbers_height = image_height - self.height
        im = Image.new('RGB', (self.image_width, image_height), '#ffffff')
        draw = ImageDraw.Draw(im)
        counter = 0
        beginning_of_line = self.width
        for bit in all_bits:
            if counter % 2 == 0:
                if bit == '0':
                    end_of_line = beginning_of_line + self.width
                    draw.rectangle( ( (beginning_of_line ,0), (end_of_line, self.height) ) , self.first_color)
                else:
                    end_of_line = self.width * 3 + beginning_of_line
                    draw.rectangle( ( (beginning_of_line, 0), (end_of_line, self.height ) ), self.first_color )
            else:
                if bit == '0':
                    end_of_line = beginning_of_line + self.width
                    draw.rectangle( ( (beginning_of_line ,0), (end_of_line, self.height) ) , self.second_color)
                else:
                    end_of_line = self.width * 3 + beginning_of_line
                    draw.rectangle( ( (beginning_of_line ,0), (end_of_line, self.height) ) , self.second_color)
            beginning_of_line = end_of_line
            counter += 1
        self._get_font_size()
        font = ImageFont.truetype(self.font, self.font_size)
        space = (self.image_width - self.all_len) / len(self.value)
        x_place = space / 2
        y_place = image_height - font.getsize(self.value[0])[1]
        for i in self.value:
            draw.text((x_place, y_place), i, self.first_color, font=font)
            simbol_width, simbol_height = font.getsize(i)
            x_place += simbol_width + space
#        image_base64 = base64.encode(im, open("out.b64", "w"))
#        im.save("foo.png")


#        output = cStringIO.StringIO()
#        format = 'PNG' # or 'JPEG' or whatever you want
#        im.save(output, format)
#        contents = output.getvalue()
#        output.close()

        im.save(self.value, "PNG")

        with open('%s' % self.value) as f:
            data = f.read()
            f.close()
            os.system('rm %s' % self.value)
            return data.encode("base64")

#        im.save(self.value, "JPEG")


#        image_base64 = im.tostring()
#        image_base64 = base64.b64encode(im.tostring())
#        image_base64 = str(image_base64, encoding='utf8')
#       image_base64 = base64.encodebytes(im.tostring())
#        im_text = im.read()
#        image_base64 = base64.b64encode(im_text)
#        return image_base64
#        data = im.tostring()
#        file_like = cStringIO.StringIO(data)
#        return file_like.read().encode('base64')
bar_code_obj = InterLeaved2of5(sys.argv[1]).get_image()
print (bar_code_obj)