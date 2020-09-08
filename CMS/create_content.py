"""
CLI Python App that will generate contents for my github page
"""

import os
import json
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import * 

today = date.today()

class CMS:
    def __init__(self):
        self.post = {
            "id":"",
            "image":"https://picsum.photos/1285/300",
            "title":"",
            "date":"",
            "tags":"",
            "content":""
        }

    def write(self,title=None,tags=None,date=None,content=None):
        self.post['title'] = title
        self.post['tags'] = tags
        self.post['date'] = date if bool(date) else today.strftime("%B %d, %Y")
        self.post['content'] = content

    def save(self):
        post_folder = os.path.join(os.getcwd(),'posts')
        posts = os.listdir(post_folder)
        with open(os.path.join(post_folder,'{}.json'.format(len(posts))),'w+') as new_post:
            self.post['id'] = len(posts)
            json.dump(self.post,new_post,indent=4)

class GUI:
    def __init__(self):
        self.root = Tk()

        # This is the section of code which creates the main window
        self.root.geometry('640x500')
        self.root.configure(background='#F0F8FF')
        self.root.title('MRKPRDO - github pages CMS')


        # This is the section of code which creates a text input box
        self.title_input=Entry(self.root, width=50)
        self.title_input.place(x=126, y=2)
        

        date_input_val = StringVar()
        self.date_input = Entry(self.root, textvariable=date_input_val)
        self.date_input.place(x=126, y=30)
        date_input_val.set(today.strftime("%B %d, %Y"),)
        
        
        self.tag_input=Entry(self.root, width=50)
        self.tag_input.place(x=126, y=60)
 

        self.content_input = Text(self.root, height=22, width=50)
        self.content_input.place(x=126, y=90)
        scroll = Scrollbar(self.root, command=self.content_input.yview)
        self.content_input.configure(yscrollcommand=scroll.set)
        self.content_input.tag_configure('bold_italics', 
                        font=('Verdana', 12, 'bold', 'italic'))
        self.content_input.tag_configure('big', 
                        font=('Verdana', 24, 'bold'))
        self.content_input.tag_configure('color', 
                        foreground='blue', 
                        font=('Tempus Sans ITC', 14))
        self.content_input.tag_configure('groove', 
                        relief=GROOVE, 
                        borderwidth=2)
        self.content_input.tag_bind('bite', 
                    '<1>', 
                    lambda e, t=self.content_input: t.insert(END, "Text"))
        # self.content_input.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)

        

        # This is the section of code which creates the a label
        Label(self.root, text='Post Title:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=0, y=0)
        Label(self.root, text='Post Date:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=0, y=30)
        Label(self.root, text='Post Tags:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=0, y=60)
        Label(self.root, text='Post Content:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=0, y=90)

        # This is the section of code which creates a button
        # Button(self.root, text='Open Post', bg='#5bc0de', font=('arial', 12, 'normal'), command=btnClickFunction).place(x=5, y=170)
        Button(self.root, text='Save Post', bg='#5cb85c', font=('arial', 12, 'normal'), command=self.save_post).place(x=5, y=205)

        self.root.mainloop()

    def save_post(self):
        cms = CMS()
        cms.write(title=self.title_input.get(),
                date=self.date_input.get(),
                tags=self.tag_input.get(),
                content=str(self.content_input.get('1.0','end-1c')).replace('\n','<br/>')
                )
        cms.save()
        self.root.destroy()


if __name__ == '__main__':
    gui = GUI()