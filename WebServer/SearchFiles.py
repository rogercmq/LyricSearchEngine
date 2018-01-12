#coding: utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba
import re
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.highlight import *
from org.apache.lucene.util import Version
import detect

vm_env=lucene.initVM(vmargs=['-Djava.awt.headless=true'])   


def run_main(command):
    STORE_DIR = "index"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    
    result = []
    all_labels = []
    if command == '':
        return
    inf=[command]
    seg_list = jieba.cut(command)
    target = " ".join(seg_list)

    query = QueryParser(Version.LUCENE_CURRENT, "lyrics_index", analyzer).parse(target)
    scoreDocs = searcher.search(query, 20).scoreDocs
    simpleHTMLFormatter = SimpleHTMLFormatter('<span style = "color:purple">', '</span>')
    hlt = Highlighter(simpleHTMLFormatter, QueryScorer(query))
    #hlt=Highlighter(QueryScorer(query))
    hlt.setTextFragmenter(SimpleFragmenter(20))

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        text = doc.get("lyrics")
        context=hlt.getBestFragment(analyzer,"lyrics",doc.get("lyrics"))
        # if context:
        #     context=' '.join(context.split())
        #     context=context.replace('<B>','')
        #     context=context.replace('</B>','')

        if context == None:
            context = '...'
            
        item=[]
        item.append(doc.get('id'))
        item.append(doc.get("song_title").encode('utf-8'))
        item.append(context)
        item.append(doc.get("singer").encode('utf-8'))
        item.append(doc.get("album_pic"))

        album_genre = doc.get('album_genre').encode('utf-8')
        item.append(album_genre)

        label_lst = re.split('[,]', album_genre)
        item.append(label_lst)          # item[6]
        listen_num = int(doc.get('listen_num'))
        item.append(listen_num)         # item[7]

        result.append(item)

        for label in label_lst:
            if len(label) == 0:
                continue
            flag = 1
            for term in all_labels:
                if label == term:
                    flag = 0
                    break
            if flag == 1:
                all_labels.append(label)
    
    del searcher
    inf.append(result)
    inf.append(all_labels)
    
    return inf


def run_music(ID):
    STORE_DIR = "index"
    vm_env=lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "id", analyzer).parse(ID)
    scoreDocs = searcher.search(query, 1).scoreDocs

    try:
        scoreDoc = scoreDocs[0]
    except:
        return None
    doc = searcher.doc(scoreDoc.doc)
            
    item=[]
    item.append(doc.get("song_title").encode('utf-8'))
    item.append(doc.get('song_url'))
    item.append(doc.get("singer").encode('utf-8'))
    item.append(doc.get("album").encode('utf-8'))
    item.append(doc.get("album_pic"))
    item.append(doc.get("album_genre").encode('utf-8'))
    item.append(doc.get("lyrics").encode('utf-8'))
    
    sim_str=doc.get("similar").encode('utf-8')
    sim_list=sim_str.split('+')
    for i in range(3):
        sim_list[i]=sim_list[i].split('*')
    item.append(sim_list)

    del searcher
    
    return item


def search_for_singer(name):
    STORE_DIR = "index"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    
    result = []
    all_labels = []
    inf=[name]

    query = QueryParser(Version.LUCENE_CURRENT, "singer_index", analyzer).parse(name)
    scoreDocs = searcher.search(query, 20).scoreDocs
    hlt=Highlighter(QueryScorer(query))
    hlt.setTextFragmenter(SimpleFragmenter(20))

    
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        
        item=[]
        item.append(doc.get('id'))
        item.append(doc.get("song_title").encode('utf-8'))
        item.append(' ')
        item.append(doc.get("singer").encode('utf-8'))
        item.append(doc.get("album_pic"))

        album_genre = doc.get('album_genre').encode('utf-8')
        item.append(album_genre)

        label_lst = re.split('[,]', album_genre)
        item.append(label_lst)          
        listen_num = int(doc.get('listen_num'))
        item.append(listen_num) 

        result.append(item)

        for label in label_lst:
            if len(label) == 0:
                continue
            flag = 1
            for term in all_labels:
                if label == term:
                    flag = 0
                    break
            if flag == 1:
                all_labels.append(label)
    
    del searcher
    inf.append(result)
    inf.append(all_labels)
    
    return inf

def run_img():
    path='img_input/input.jpg'
    answer=detect.person_detect(path)
    return answer


def reorder(hot, label, manifest):
    label = label.encode('utf-8')
    command = manifest[0]
    all_labels = manifest[2]
    tmp = manifest[1]
    
    if hot == '1':
        for i in range(len(tmp)-1):
            for j in range(len(tmp)-1-i):
                if tmp[j][7] < tmp[j+1][7]:
                    tmp[j], tmp[j+1] = tmp[j+1], tmp[j]

    else:
        tmp1 = []
        new_labels = []
        for i in range(len(tmp)):
            if label in tmp[i][6]:
                tmp1.append(tmp[i])
                for term in tmp[i][6]:
                    if term not in new_labels:
                        new_labels.append(term)
        tmp = tmp1[:]
        all_labels = new_labels[:]
        

    inf = []
    inf.append(command)
    inf.append(tmp)
    inf.append(all_labels)

    return inf
        





