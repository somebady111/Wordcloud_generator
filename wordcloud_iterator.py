#!/usr/bin/python3
#_*_coding:utf-8_*_
'''
此例用于生成云词,并赋予他一个用户端界面窗口
'''
# 导入响应需求库
import wordcloud
import jieba
import wx
import os
# 说明文件的依赖库
from tkinter import filedialog
from scipy.misc import imread

class Word(wx.Frame):
    def __init__(self):
        # 设置主窗口
        wx.Frame.__init__(self,parent=None,title = "云词生成器",size=(925,510))
        # 设置拉伸窗口
        panel = wx.Panel(self)
        panel.SetBackgroundColour((143,193,254))

        # 设置断言,是否选择文件,或编辑了文字
        self.isChoosedFile = False
        self.isText = False

        # 用户输入的生成图片大小和文件名
        self.width = None
        self.height = None
        self.name = ""

        # 事先声明文本框输入的值为空
        self.message = ""

        # 设置窗口布局

        # 选择图片,选择文本文件
        self.pichoose = wx.Button(parent = panel,pos=(20,25),size = (130,50),label="图片选择")
        self.filechoose = wx.Button(parent = panel,pos=(245,25),size = (130,50),label="文本文件选择")
        self.pichoose.SetBackgroundColour((255,234,166))
        self.filechoose.SetBackgroundColour((255,234,166))
        # 文本输入框,滚动方式
        self.inputext = wx.TextCtrl(panel,pos=(20,80),size=(370,230),value="请在这里输入文本",style = wx.TE_MULTILINE | wx.HSCROLL)
        separatin2 = wx.TextCtrl(parent = panel,pos=(20,100),size=(370,2))
        separatin2.SetBackgroundColour((0,0,0))
        self.inputext.SetBackgroundColour((255,255,255))
        # 设置文本颜色
        self.inputext.SetForegroundColour((234,62,18))
        # 按钮,使用说明,生成云图
        self.button = wx.Button(parent = panel,pos=(20,350),size=(130,50),label = "使用说明")
        self.make = wx.Button(parent = panel,pos=(198,350),size=(130,50),label = "生成云图")

        # 分割线
        separatin = wx.TextCtrl(parent = panel,pos=(420,10),size=(5,450))
        separatin.SetBackgroundColour((224, 255, 255))
        # 接收图片框
        text_picture = wx.TextCtrl(parent = panel,pos=(450,10),size=(450,450),value = "图片显示",style=wx.TE_READONLY)
        separatin1 = wx.TextCtrl(parent = panel,pos=(450,40),size=(450,2))
        separatin1.SetBackgroundColour((0,0,0))

        # 绑定按钮事件
        self.Bind(wx.EVT_BUTTON,self.OpenPic,self.pichoose)
        self.Bind(wx.EVT_BUTTON,self.OpenFile,self.filechoose)
        self.Bind(wx.EVT_BUTTON,self.ClickButton,self.button)
        self.Bind(wx.EVT_BUTTON,self.ClickMake,self.make)
    # 处理打开图片事件,这里打开的图片要交给云词程序处理
    def OpenPic(self,event):
        # 如果没打开了选择文件
        if self.isChoosedFile == True:
            wx.MessageDialog(self,u'''必须选择一张图片进行生成云图''',u"警告",wx.OK).ShowModal()
        else:
            # 如果打开文件选择
            file = filedialog.askopenfilename(title="请选择生成的的图片")
            return self.word(file)

    # 处理打开文件事件
    def OpenFile(self,event):
        # 进行输入判断,如果输入的是文字,则读取文字,如果选择的是文本文件,则读取文本文件
        # 如果是文字
        message = self.message = self.inputext.Value
        if self.isText == True:
            if message == "":
                wx.MessageDialog(self,u'''必须输入文本或者选择文本文件''',u"警告",wx.OK).ShowModal()
            else:
                return self.word(message)
        # 如果是文本文件
        else:
            textfile = filedialog.askopenfilename(title="请选择文本文件")
            return self.word(textfile)

    # 点击说明按钮事件
    def ClickButton(self,event):
        wx.MessageDialog(self, u'''1、必须选择一张带有轮廓的图片才更明显\n\r2、文本文件和输入文本不能同时进行''', u"警告",
                         wx.OK).ShowModal()

    # 点击生成云图按钮事件,实际是读取本地文件的内容
    def ClickMake(self):
        pass

    # 先生成指定的图片大小,后边在修改,可以根据用户设置的尺寸,和文件名进行制定
    def word(file,textfile,message):
        # 如果接收到的是文件则,按文件打开处理
        if textfile:
            textfile = textfile
            mask = imread(file)
            with open(textfile,'r',encoding='utf-8') as f:
                text = f.read()
                ls = jieba.lcut(text)
                txt = '\n'.join(ls)
                w = wordcloud.WordCloud(font_path='msyh.ttc',mask=mask,width=1193,height=800,background_color='white')
                w.generate(txt)
                return w.to_file('picture.png')
        # 如果接受到的是文字,则以字符串方式读取
        else:
            mask = imread(file)
            ls = jieba.lcut(message)
            txt = '\n'.join(ls)
            w = wordcloud.WordCloud(font_path='msyh.ttc', mask=mask, width=1193, height=800,
                                    background_color='white')
            w.generate(txt)
            return w.to_file('picture.png')


if __name__ =="__main__":
    app = wx.App()
    frame = Word()
    frame.Show()
    app.MainLoop()
