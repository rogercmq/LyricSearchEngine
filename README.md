# Lyric Search Engine
Team project for course EE208，
基于虾米音乐的歌词+图片搜索引擎

### 团队分工

  * 曹梦奇：组长，scrapy爬虫/网页UI优化
  
  * 丁雨晨：网页逻辑搭建，webpy前端基础
  
  * 柳旭东：数据库处理
  
  * 罗英哲：图像哈希检索

### 环境搭建

 
  - Ubuntu14.04 
  
  - scrapy python3.6  
  
  - pylucene python2.7 miniconda
  
  - webpy
  
  - PIL for pics
  
  - cv2/opencv

### 项目简介

  - Scrapy爬取虾米音乐2w歌曲的歌词、音乐流派；爬取虾米音乐歌手图片
  - 歌词文本搜索，实现对搜索结果进行排序与筛选
  - 将歌曲设置ID，根据ID搭建简单的歌曲详细信息网页
  - 相似歌曲推荐
  - 图像哈希检索，搜索图片库中歌手图片，返回该歌手的歌曲


 ### 若配置完毕，打开webserver里的server3.py进入localhost服务器，可以在网页上操作；</br>
 ### PicSpider和SongInfoSpider文件夹中是两个scrapy project；
