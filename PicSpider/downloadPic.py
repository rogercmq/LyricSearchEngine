# -*- coding: utf-8 -*-
import urllib,sys
#import pandas as pd
reload(sys)
sys.setdefaultencoding('UTF-8')

def quchong(file):
    df = pd.read_csv(file,header=0)
    datalist = df.drop_duplicates()
    datalist.to_csv(file)

def downloadPic(singers_file):
    f = open(singers_file, "r")
    lines = f.readlines()
    f.close()

    # 这里line[:-1]的含义是每行末尾都是一个换行符，要去掉
    # 这里in lines[1:]的含义是csv第一行是字段名称，要去掉
    song_url_list = [line[:-1] for line in lines[2:]]

    for singer in song_url_list:
        detail = singer.split(',')
        info = []
        for i in detail:
            if i != '':
                info.append(i)

        try:
            name = '_'.join(info[0].split(' '))
        except:
            pass
        MainPicpath = './dataset/'+ name + '.jpg'
        try:
            urllib.urlretrieve(info[1], unicode(MainPicpath))
            print("%s MainPic done!" % (name))
        except:
            pass
        for i in range(2,len(info)):
            path = './dataset/'+ name + str(i-2) +'.jpg'
            try:
                urllib.urlretrieve(info[i], unicode(path))
            except:
                pass

singers_file = './singersPic.csv'
#quchong(singers_file)
downloadPic(singers_file)