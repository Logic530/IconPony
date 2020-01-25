"""
IconPony 
A simple python gui tool for making avartar outof ponytown exported image

This program needs pillow library

Version: 0.2
Author: Logic_530
Date: 2020-1-24
"""

import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageTk


class app(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self['padx'] = 8
        self['pady'] = 8
        self.pack()
        self.set_up_vars()
        self.create_widgets()
        self.init_widgets()

    def set_up_vars(self):

        # 输出大小控制变量
        self.export_size = tk.IntVar()
        self.export_size.set(64)

        # 背景颜色变量
        self._export_color = '#90ee90'

    def create_widgets(self):

        # 预览框
        self.preview_frame = tk.LabelFrame(self)
        self.preview_frame['text'] = 'preview'
        self.preview_frame['height'] = 160
        self.preview_frame['width'] = 160
        self.preview_frame.grid_propagate(0)
        self.preview_frame.grid(row=0, column=0)

        # 预览图片
        self.previewer = tk.Label(self.preview_frame)
        self.previewer['image'] = ImageTk.PhotoImage(
            image=Image.new('RGBA', (128, 128)))
        self.previewer.pack()

        # 导入按钮
        self.import_button = tk.Button(self)
        self.import_button['text'] = 'import file'
        self.import_button['command'] = self.import_image
        self.import_button.grid(row=1, column=0,
                                sticky=tk.N + tk.S + tk.W + tk.E)

        # 导出按钮
        self.export_button = tk.Button(self)
        self.export_button['text'] = 'export'
        self.export_button['command'] = self.export_image
        self.export_button.grid(row=1, column=1,
                                sticky=tk.N + tk.S + tk.W + tk.E)

        # 选项框
        self.option_box = tk.LabelFrame(self)
        self.option_box['text'] = 'options'
        self.option_box['padx'] = 4
        self.option_box['pady'] = 4
        self.option_box.grid(row=0, column=1,
                             sticky=tk.N + tk.S + tk.W + tk.E)

        # 颜色选择按钮
        self.color_selector = tk.Button(self.option_box)
        self.color_selector['text'] = 'bg color'
        self.color_selector['command'] = self.select_color
        self.color_selector['bg'] = self._export_color
        self.color_selector.pack(side='top')

        # 输出大小选择框和单选按钮
        self.size_button_frame = tk.Frame(self.option_box)
        self.size_button_frame.pack(side='top')
        self.size_button_64 = tk.Radiobutton(self.size_button_frame,
                                             text='64', value=64, variable=self.export_size)
        self.size_button_256 = tk.Radiobutton(self.size_button_frame,
                                              text='256', value=256, variable=self.export_size)
        self.size_button_512 = tk.Radiobutton(self.size_button_frame,
                                              text='512', value=512, variable=self.export_size)
        self.size_button_64.pack()
        self.size_button_256.pack()
        self.size_button_512.pack()

        pass

    def init_widgets(self):
        self.color_selector['state'] = 'disable'
        self.size_button_64['state'] = 'disable'
        self.size_button_256['state'] = 'disable'
        self.size_button_512['state'] = 'disable'
        self.export_button['state'] = 'disable'

    def import_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[('pony image', '*.png')])
        if self.image_path:
            print('import image:', self.image_path)
            self.image = self.pony_image(self.image_path)
            self.update_preview()
            print('active option widgets')
            self.color_selector['state'] = 'normal'
            self.size_button_64['state'] = 'normal'
            self.size_button_256['state'] = 'normal'
            self.size_button_512['state'] = 'normal'
            self.export_button['state'] = 'normal'
        else:
            print('user canceled open file')

    def export_image(self):
        self._save_file_path = filedialog.asksaveasfilename(
            filetypes=[('PNG', '*.png')])
        if self._save_file_path:
            self.image.export(self.export_size.get(),
                              self._export_color).save(self._save_file_path)
            print('export image:', self._save_file_path)
        else:
            print('user canceled save file')
        pass

    def radio_button_clicked(self, event):
        print('export size selected')
        self.update_preview()

    def select_color(self):
        color = colorchooser.askcolor()
        color = color[1]
        print('choosed color', color)
        self._export_color = color
        self.color_selector['bg'] = color
        self.update_preview()
        pass

    def update_preview(self):
        self._preview_image = ImageTk.PhotoImage(
            image=self.image.export(128, self._export_color))
        self.previewer['image'] = self._preview_image
        print('update preview')
        pass

    class pony_image(object):

        def __init__(self, image_path):
            self._image_path = image_path
            self._raw_image = Image.open(self._image_path)
            pass

        def export(self, size, bg_color):
            self.box = self._raw_image.getbbox()
            self.corped_image = self._raw_image.crop(self.box)
            self._x_size = self.box[2] - self.box[0]
            self._y_size = self.box[3] - self.box[1]
            self._x_offset = int((64 - self._x_size)/2)
            self._y_offset = int((64 - self._y_size)/2)
            self.background = Image.new('RGBA', (64, 64), bg_color)
            self.background.paste(self.corped_image,
                                  (self._x_offset,
                                   self._y_offset,
                                   self._x_offset + self._x_size,
                                   self._y_offset + self._y_size),
                                  self.corped_image)
            self.resized_image = self.background.resize(
                (size, size), resample=0)
            return self.resized_image


if __name__ == '__main__':
    root = tk.Tk()
    root.title('IconPony')
    root.resizable(False, False)
    icon_pony = app(root)
    root.mainloop()
    pass
