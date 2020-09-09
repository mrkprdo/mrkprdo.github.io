"""
CLI Python App that will generate contents for my github page
"""

import os
import json
import requests
import shutil
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import * 

today = date.today()

class ImageDownloader:
    def __init__(self,post_id=None,l=None,w=None,src=None,ext='jpg'):
        req = requests.get(src, stream = True)
        filename = '{}_{}x{}.{}'.format(post_id,l,w,ext)
        if req.status_code == 200:
            req.raw.decode_content = True
            images_folder = os.path.join(os.getcwd(),'images')
            with open(os.path.join(images_folder,filename),'wb') as f:
                shutil.copyfileobj(req.raw, f)
        else:
            raise Exception('Error in requesting image...')
        self.img_src = 'https://mrkprdo.github.io/images/{}'.format(filename)
    def get_image_src(self):
        return self.img_src

class MetaTagGen:
    def __init__(self,post_dict=None):
        metapages = os.path.join(os.getcwd(),'metapages')
        meta_filename = 'shared_post_{}.html'.format(post_dict['id'])
        html_contents = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
    <!-- Primary Meta Tags -->
    <title>MRKPRDO </title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="title" content="MRKPRDO - {post_dict['title']}">
    <meta name="description" content="{post_dict['content']}... [Click to read more]">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://mrkprdo.github.io/view.html?post={post_dict['id']}">
    <meta property="og:title" content="{post_dict['title']}">
    <meta property="og:description" content="{post_dict['content'][0:50]}... [Click to read more]">
    <meta property="og:image" content="{post_dict['meta_image']}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://mrkprdo.github.io/view.html?post=`+postId+`">
    <meta property="twitter:title" content="{post_dict['title']}">
    <meta property="twitter:description" content="{post_dict['content'][0:104]}-[Click to read more]">
    <meta property="twitter:image" content="{post_dict['meta_image']}">
    </head>
    <body>
        <script>
            window.location.href = "https://mrkprdo.github.io/view.html?post={post_dict['id']}";
        </script>
    </body>
</html>
        """
        with open(os.path.join(metapages,meta_filename),'w+') as f:
            f.write(html_contents)

class CMS:
    def __init__(self):
        self.post = {
            "id":"",
            "image":"",
            "title":"",
            "date":"",
            "tags":"",
            "content":""
            "meta_image"
        }

    def write(self,title=None,tags=None,date=None,content=None):
        self.post['title'] = title
        self.post['tags'] = tags
        self.post['date'] = date if bool(date) else today.strftime("%B %d, %Y")
        self.post['content'] = content

    def save(self):
        post_folder = os.path.join(os.getcwd(),'posts')
        posts = os.listdir(post_folder)
        self.post['id'] = len(posts)
        self.post['image'] = 'https://picsum.photos/id/{}/1285/300'.format(self.post['id'])

        img_dl = ImageDownloader(post_id=self.post['id'],l=300,w=300,src='https://picsum.photos/id/{}/300/300'.format(self.post['id']))
        self.post['meta_image'] = img_dl.get_image_src()

        with open(os.path.join(post_folder,'{}.json'.format(self.post['id'])),'w+') as new_post:
            json.dump(self.post,new_post,indent=4)

        metapages = MetaTagGen(self.post)


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
