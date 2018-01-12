import cv2
import os
import numpy as np
import pickle
import shutil
import math
from PIL import Image
from PIL import ImageDraw



def detectFaces(image_name):
	img = cv2.imread(image_name)
	face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
	if(img.ndim == 3):
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	else:
		gray = img
	faces = face_cascade.detectMultiScale(gray,1.2,5)
	result = []
	for (x,y,width,height) in faces:
		result.append((x,y,x+width,y+height))
	return result

def saveFaces(image_name):
	faces = detectFaces(image_name)
	file_name = ""
	if(faces):
		save_dir = image_name.split('.')[0]+"_faces"
		os.mkdir(save_dir)
		count = 0
		for (x1,y1,x2,y2) in faces:
			file_name = os.path.join(save_dir,str(count)+".jpg")
			Image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
			count += 1
        img = cv2.imread(file_name)
        shutil.rmtree(os.getcwd() + '/' + image_name.split('.')[0]+"_faces")
        return img


def img_to_vp(img):
    return get_vp(change_p(get_p(img,4,4)))


def get_data(img):
    H = len(img)
    W = len(img[0])
    data = np.zeros((H,W,3))
    for i in range(H):
        for j in range(W):
            data[i,j][0] = img[i,j][0]
            data[i,j][1] = img[i,j][1]
            data[i,j][2] = img[i,j][2]
    return data,H,W

def get_bgr(image_data,x1,y1,x2,y2):
    b = 0
    g = 0
    r = 0
    for i in range(x1,x2):
        for j in range(y1,y2):
            b += image_data[i,j][0]
            g += image_data[i,j][1]
            r += image_data[i,j][2]
    total = float(b + g + r)
    bgr = [b/total,g/total,r/total]
    return bgr

def get_p(img,nx = 2, ny = 2):
    p = []
    data, H, W = get_data(img)
    h = float(H)/nx
    w = float(W)/ny
    for i in range(nx):
        for j in range(ny):
            p.append(get_bgr(data,int(i*h),int(j*w),int((i+1)*h),int((j+1)*w)))
    return p

def change_p(p, d = 48, x1 = 0.31973228, x2 = 0.34527915):
    global find_bound_set
    new_p = []
    for i in range(d/3):
        for j in range(3):         
            if(p[i][j] < x1):
                new_p.append(0)
            elif(p[i][j] >= x1 and p[i][j] < x2):
                new_p.append(1)
            else:
                new_p.append(2)
    return new_p

def get_vp(p,d = 48):
    vp = ''
    for i in range(d):
        if(p[i] == 0):
            vp += '00'
        elif(p[i] == 1):
            vp += '10'
        else:
            vp += '11' 
    return vp


def my_hash(vp,I = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,70,71,73,75,77,79,81,83,85,87,89,91,93,95]):
    result = ''
    for i in I:
        result += vp[int(i) - 1]
    return result

def get_hash_dic(hash_vp_set):
    hash_dic = {}
    for index,hash_vp in enumerate(hash_vp_set):
        if(hash_vp not in hash_dic):
            hash_dic[hash_vp] = [index]
        else:
            hash_dic[hash_vp].append(index)

    return hash_dic
              
def find_box(tgt_hash_vp,dic):
    return dic[tgt_hash_vp]

def NN_find():
    target_img = cv2.imread('target.jpg')
    tgt_vp = img_to_vp(target_img)


    dataset = []
    for i in range(1,41):
        im = os.path.join('dataset',str(i) + '.jpg')
        dataset.append(im)

    vpset = []
    for im in dataset:

        cd_im = cv2.imread(im)
        cd_vp = img_to_vp(cd_im)
        vpset.append(cd_vp)

    for vp in vpset:
        if(vp == tgt_vp):
            name =  str(index+1)+'.jpg'
            im = os.path.join('dataset',name)
            img = cv2.imread(im)

def path_to_name(path):
    pic = path.split('/')[-1]
    name = pic.split('_faces')[0]
    temp = name.split('_')
    result = ' '.join(temp)
    if(result[-1] == '0' or result[-1] == '1' or result[-1] == '2' or result[-1] == '3'):
        return result[0:-1]
    return result



def my_equ(tgt_p,p):
    for i in range(15):
        for j in range(3):
            tmp = abs(tgt_p[i][j] - p[i][j])
            if(tmp > 0.01):
                return False
    return True

def dic_pickle():
    dataset = []
    data_path = os.path.join(os.getcwd(),'finaldataset')
    for pic in os.listdir(data_path):
        temp = os.path.join(data_path,pic)
        dataset.append(temp)
    f0 = file('dataset.pkl','wb')
    pickle.dump(dataset,f0,True)
    f0.close()

    vpset = []
    npic = 0
    for im in dataset:
        #print im
        cd_im = cv2.imread(im)
        cd_vp = img_to_vp(cd_im)
        vpset.append(cd_vp)
        print npic
        npic += 1
    #print vpset
    hash_vp_set = []
    for vp in vpset:
        hash_vp = my_hash(vp)
        hash_vp_set.append(hash_vp)
    dic = get_hash_dic(hash_vp_set)

    f1 = file('hash_dic.pkl', 'wb')
    pickle.dump(dic, f1, True)
    f1.close()
    
    f2 = file('vp_set.pkl','wb')
    pickle.dump(vpset,f2,True)
    f2.close()





def person_detect(img_name):
    #dataset = []
    #data_path = os.path.join(os.getcwd(),'finaldataset')
    #for pic in os.listdir(data_path):
     #   temp = os.path.join(data_path,pic)
      #  dataset.append(temp)

    target_img = saveFaces(img_name)
    
    
    tgt_p = get_p(target_img,4,4)
    
    tgt_vp = get_vp(change_p(tgt_p))
    
    tgt_hash_vp = my_hash(tgt_vp)

    fp = file('pset.pkl', 'rb')
    pset = pickle.load(fp)
    fp.close()

    f01 = file('dataset.pkl','rb')
    dataset = pickle.load(f01)
    f01.close()

    f11 = file('hash_dic.pkl','rb')
    dic = pickle.load(f11)
    f11.close()

    f21 = file('vp_set.pkl','rb')
    vpset = pickle.load(f21)
    f21.close()  

    box = find_box(tgt_hash_vp,dic)

    for index in box:
        if(vpset[index] == tgt_vp):
            if(len(box) == 1 or my_equ(tgt_p,pset[index])):
                im =  dataset[index]
                return path_to_name(im)



def my_remove():
    path = os.getcwd()
    path = os.path.join(path,'dataset')
    i = 0
    x = 0
    for pic in os.listdir(path):
        print pic
        img_name = os.path.join('dataset',pic)
        try:
            tmp =  person_detect(img_name)
            print tmp
            if(tmp == None):
                
                print x
                x += 1
            else:
                shutil.copy(os.path.join(path,pic),os.path.join(os.getcwd(),'rightset'))
        except:
             
             print x
             x += 1
        os.remove(os.path.join(path,pic))

           
        
    

