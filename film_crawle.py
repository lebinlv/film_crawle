# coding utf-8

import os
from urllib import request
from bs4 import BeautifulSoup as bs


output_file_path = os.getcwd()+'\\film.txt'
try:
    output_file = open(output_file_path,'w',encoding='utf-8')
except:
    raise

'''
爬取BT天堂首页，获取热映电影列表
'''

'''  测试时使用的代码
page_obj = request.urlopen('http://www.bttiantangs.com/')
page_data = page_obj.read().decode('utf-8')
page = bs(page_data,'lxml')
page_file = open('E:\lvleb\Desktop\crawle\film_demo.html','w',encoding='utf-8')
page_file.write(page.prettify())
page_file.close()
'''

try:
    film_page_obj = request.urlopen('http://www.bttiantangs.com/')
except:
    print('Error!')
    raise

film_page_data = film_page_obj.read().decode('utf-8')
page = bs(film_page_data, 'lxml')

# film list
film_link = []
film_title = []

film_info_raw = page.find_all('h2')

for link in film_info_raw[:-8]:
    film_link.append('http://www.bttiantangs.com' + link.find('a').get('href'))

    title_raw = link.find('a').get('title')
    idx = title_raw.find('迅雷')
    film_title.append(title_raw[:idx])

film_num = len(film_title)
print('网站首页热映电影列表已爬取完毕！共获得%d部电影。'%film_num)
print('...请等待电影信息爬取完毕...\n')
#print(film_title)
'''
逐个爬取上一过程中获得的热映电影的详情页面，获取电影详情及BT种子
'''

''' 测试时使用的代码
detail_obj = request.urlopen('http://www.bttiantangs.com/movie/38145.html')
detail_data = detail_obj.read().decode('utf-8')
detail = bs(detail_data,'lxml')
detail_file = open('E:\lvleb\Desktop\crawle\detail_demo.html','w',encoding='utf-8')
detail_file.write(detail.prettify())
detail_file.close()
'''

#print(film_num)

sub = []             # 字幕
torrent_link = []    # bt torrent link
torrent_title = []   # bt torrent title
torrent_grade = []   # 电影清晰度分级
torrent_grade_allowed = ['BluRay-1080P','蓝光原盘','超清4K','WEB-1080P']

for i in range(film_num):
    output_file.write(film_title[i])

    #torrent_grade_temp = []
    #torrent_link_temp = []
    #torrent_title_temp = []
    try:
        film_detail_obj = request.urlopen(film_link[i],timeout=10)
    except:
        print(film_title[i]+'爬取失败')
        output_file.write('\n\nError')

    else:
        film_detail_data = film_detail_obj.read().decode('utf-8')
        detail = bs(film_detail_data,'lxml')
        douban = detail.find('div',id='post_content').find('strong').get_text()
        output_file.write('    '+douban)

        download_block = detail.find('div',id='download')  # 找出网页中包含下载信息的块

        #sub.append(download_block.find('a').get('href'))   # 写入字幕下载链接
        output_file.write('\n字幕： '+download_block.find('a').get('href'))

        torrent_block = download_block.find_all('li')      # 找到下载信息块中包含BT种子下载链接的块

        for torrent_info in torrent_block:
            grade_raw = torrent_info.find('em')
            if grade_raw:
                grade = grade_raw.get_text()

                if grade in torrent_grade_allowed:
                    #output_file.write(grade.encode())
                    
                    #torrent_grade_temp.append(grade)
                    #torrent_raw = torrent_info.a.next_sibling
                    #torrent_title_temp.append(torrent_raw.get_text())
                    #torrent_link_temp.append(torrent_raw.get('href'))
                    torrent_raw = torrent_info.a.next_sibling
                    torrent_title_temp = torrent_raw.get_text()
                    torrent_link_temp = torrent_raw.get('href')
                    output_file.write('\n'+grade+'    '+torrent_title_temp+'    '+torrent_link_temp)
    output_file.write('\n\n\n')
    print('电影《'+film_title[i]+'》已爬取完毕！')

'''
    print(torrent_grade_temp)
    print(torrent_link_temp)
    print(torrent_title_temp)


    torrent_grade.append(torrent_grade_temp)
    torrent_link.append(torrent_link_temp)
    torrent_title.append(torrent_title_temp)
'''


'''
将爬取到的信息输出
'''

'''
for i in range(film_num):
    now_torrent_link = torrent_link[i]    # bt torrent link
    now_torrent_title = torrent_title[i]   # bt torrent title
    now_torrent_grade = torrent_grade[i]   # 电影清晰度分级
    torrent_num = len(now_torrent_grade)
    print('\n\n'+film_title[i]+'    '+sub[i])
    output_file.write(('\n\n'+film_title[i]).encode())
    output_file.write(sub[i].encode())

    for j in torrent_num:
        print(now_torrent_grade[j]+now_torrent_title[j]+now_torrent_link[j])
        output_file.write((now_torrent_grade[j]+now_torrent_title[j]+now_torrent_link[j]).encode())
'''

output_file.close()
print('\n爬取结束！！')
print('电影信息已写入 '+output_file_path+'\n')
