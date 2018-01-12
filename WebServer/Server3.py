#coding:utf-8
import web
from SearchFiles import *


urls = (
    '/', 'main_page',
    '/s', 'main_res',
    '/img', 'img_index',
    '/img_res', 'img_res',
    '/mus','music',
    '/ab','aboutus'
)

render = web.template.render('templates')

manifest=[]

class main_page:
    def GET(self):
        return render.default()

class aboutus:
    def GET(self):
        return render.about()

class main_res:
    def GET(self):     #search
        global manifest
        user_data = web.input()
        a = run_main(user_data.keyword)
        manifest=a
        #return render.main_result(a)
        return  render.LyricResult(a)

    def POST(self):     #reorder
        global manifest
        user_data = web.input()
        a = reorder(user_data.hot, user_data.label, manifest)
        manifest=a
        return render.LyricResult(a)

class img_index:
    def GET(self):
        return render.PicIndex()

class img_res:
    def GET(self):     #reorder
        global manifest
        user_data = web.input()
        a = reorder(user_data.hot, user_data.label, manifest)
        manifest=a
        return render.PicResult(a)
    
    def POST(self):    #detect and search
        global manifest
        x=web.input(img_input={})
        fout = open('img_input/input.jpg','wb') 
        fout.write(x.img_input.file.read()) 
        fout.close()
        ans=run_img()
        a = search_for_singer(ans)
        manifest=a
        return render.PicResult(a)
    
class music:            #search for songs
    def POST(self):
        ID = web.input().id
        song_inf = run_music(ID)
        return render.MusicResult(song_inf)
    

if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()
