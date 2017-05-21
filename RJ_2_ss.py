#!/home/nimasane/bin/python3.4
#
#This script is written in Python3 by Nimasajedi[at]gmail.com on 20th May 2017 to exctract direct download links for musics/video clips 
#(3 different video quality)/podcasts and albums on Radiojavan.com. Moreover, it generates file size and depicts cover photos alongside 
#showing artist/art name. This is the same copy running on http://mynext.pro/RJ
#
import re
from datetime import datetime
import requests
import cgi, cgitb 
cgitb.enable(display=1, logdir="./tmp/", context=5, format="html")
form = cgi.FieldStorage()

url = form.getvalue('url')
if url is not None:
    url=url.lower()
else:
    url=""
    
l_mp3= "https://rjmediamusic.com/media/mp3/"
l_vid="https://rjmediamusic.com/media/music_video/"
l_pod="https://rjmediamusic.com/media/podcast/"

##########################################################
#          Functions are listed below                    #
##########################################################

def Image(html):
    a1=html.find('<link rel="image_src" href="')
    a2=html.find('<meta property="og:')
    a3=html[a1+len('<link rel="image_src" href="'):a2-2]
    a4=re.match(r'(.*)"/>', a3, re.M|re.I)
    try:
        i_big=a4.group(1)
    except AttributeError:
        i_big='Have you pasted the RJ link correctly?\nMake sure that the link could be opened in your browser. If so, select it throughly and paste again'
    else:
        image_big_dl=requests.get(i_big, stream=True)
        with open('../RJ/tmp/%s_b_image.jpg'%artist_song(html)[1], 'wb') as f:
            f.write(image_big_dl.content)
    image_big='http://mynext.pro/RJ/tmp/%s_b_image.jpg'%artist_song(html)[1]
    A=[]
    A.append(image_big)
    
    try:
        i_small=a4.group(1)[:len(a4.group(1))-4]+'-thumb.jpg'
    except AttributeError:
        i_small='Have you pasted the RJ link correctly?\nMake sure that the link could be opened in your browser. If so, select it throughly and paste again'
    else:
        image_small_dl=requests.get(i_small, stream=True)
        with open('../RJ/tmp/%s_s_image.jpg'%artist_song(html)[1], 'wb') as f:
            f.write(image_small_dl.content)
    image_small='http://mynext.pro/RJ/tmp/%s_s_image.jpg'%artist_song(html)[1]
    A.append(image_small)
    return (A)
    
def artist_song(Html):
    a1=Html.find('<meta property="og:title" content=')
    a2=Html.find('<meta property="og:type" content=')
    if (a2<0 or a2<a1):
        a2=Html.find('<meta name="twitter:title" content')
    a3=Html[a1+1+len('<meta name="twitter:title" content'):a2-5]
    if (a3.find('"')>0):
        a4_fck=a3[:a3.find('"')]
    else:
        a4_fck=a3
    a5=re.match(r'(.*) - (.*)', a4_fck, re.M|re.I)
    a6=re.match('(.*)\((.*)\)', a4_fck)
    try:
        song=(' %s'%(a5.group(2)))
    except AttributeError:
        song=(' %s'%(a6.group(1)))
    A=[]
    A.append(song)
    try:
        ar1=a5.group(1)
    except AttributeError:
        ar1=a6.group(2)
    if ('&amp' in ar1):
        ar2=re.match(r'(.*)amp;(.*)',ar1, re.M|re.I)
        artist=ar2.group(1)+ar2.group(2)
    else:
        artist=ar1
    A.append(artist)
    return (A)


def file_size(dl_link):
    file_size=requests.get(dl_link, stream=True)
    file_size2=file_size.headers['content-length']
    file_size3=int(file_size2)/1048576
    file_size4='%3.1f MB'%file_size3
    return (file_size4)
    
def mp3(url):
    a1=url.find('/mp3/')
    a2=url.find('?start')
    if a2<0:
        a2=len(url);
    a3=url[a1+5:a2]
    if z1>0:
        dl_link=z3
    else:
        dl_link=l_mp3+a3+'.mp3'
    return(dl_link)
        
def video(URL):
    a1=URL.find('/video/')
    a2=URL.find('?start')
    if a2<0:
        a2=len(url);
    a3=URL[a1+7:a2]
    vid_list=[]
    q1=l_vid+'lq/'+a3+'.mp4'
    vid_list.append(q1)
    q2=l_vid+'hq/'+a3+'.mp4'
    vid_list.append(q2)
    q3=l_vid+'hd/'+a3+'.mp4'
    vid_list.append(q3)
    return(vid_list)

def album(URL):
    track_list=[]
    if (URL.find('?index=')>0):
        all_track_nr=((html.count('?index='))//2)-1
        a1=URL[:URL.find('?index=')]
        current_track_no=int(URL[len(a1)+len('?index='):])
        ID=a1[a1.find('/album/')+len('/album/'):]
        track_list.append('%s'%current_track_no)
    elif (URL.find('?start')>0):
        all_track_nr=((html.count('?index='))//2)-1
        a1=URL[:URL.find('?start')]
        current_track_no=int(URL[len(a1)+len('?start'):])
        ID=a1[a1.find('/album/')+len('/album/'):]
        track_list.append('%s'%current_track_no)
    else:
        all_track_nr=(html.count('?index='))//2
        a1=URL
        current_track_no=0
        ID=a1[a1.find('/album/')+len('/album/'):]
        track_list.append('%s'%current_track_no)
    if z1>0:
        dl_link=z3
    else:
        dl_link=l_mp3+ID+'.mp3'
    i=0   
    while i<all_track_nr:
        track_list.append('%s?index=%d'%(a1,i))
        i+=1
    return(track_list)
                
def podcast(URL):
    a1=URL.find('/podcast/')
    a2=URL.find('?start')
    if a2<0:
        a2=len(URL);
    a3=html.find('<span class="category">Podcast</span>')
    ID=URL[a1+len('/podcast/'):a2]
    if z1>0:
        dl_link=z3
    else:
        dl_link=l_pod+ID+'.mp3'
    return(dl_link)


def list_dl(List):
    track_list_dl=[]
    List2=List[1:]
    j=0
    for i in List2:
        a1=requests.get(List2[j])
        html=a1.text
        a2=html.find('<a href="javascript:void(0)" link="')
        a2_len=len('<a href="javascript:void(0)" link="')
        if a2<0:
            a2=html.find("RJ.currentMP3Url = 'mp3/")
            a2_len=len("RJ.currentMP3Url = 'mp3/")
        a3=html.find('" target="_blank" class="mp3_download_link">')
        if a3<0:
            a3=html.find("RJ.currentMP3 = '")
        a4=html[a2+a2_len:a3]
        if a4.find("'")>0:
            a41=a4[:a4.find("'")]
            a4=l_mp3+a41+'.mp3'
        track_list_dl.append(a4)
        j+=1
    return(track_list_dl)
    
    
    
def list_pr(list_pr):
    print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print ('<table>')
    print('<tr><td>You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Album: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr>'%Image(html)[1]+'</table>')
    if int(album(url)[0]) is not 0:
        print('<table><tr><td>'+'</br><a href="%(1)s">Download track %(2)s</a> (%(3)s) at: %(1)s'%{'1':list_dl(album(url))[(int(album(url)[0])-1)],'2':album(url)[0],'3':file_size(list_dl(album(url))[(int(album(url)[0])-1)])}+'</br></br></br>Other album tracks are:'+'</td></tr>')
        
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> (%s) at: '%(i,list_pr.index(i)+1,file_size(i))+i+'</td></tr>')
        
    else:
        print('<table></br>')
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> (%s) at: '%(i,list_pr.index(i)+1,file_size(i))+i+'</td></tr>')
            
    print('</table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");


    
def single_pr(dl):
    print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print ('<table>')
    #print ('<div align="center" style="border:1px solid red">')
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Song: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) at: %s'%(dl,file_size(dl),dl)+'</td></tr></table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p')) 
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");

def vid_pr(dl):
    print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print ('<table>')
    #print ('<tr>')
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Song: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[0]+'<table><tr><td></br><a href="%(q1)s">Download 480p</a> (%(fs1)s) at: %(q1)s</br></td></tr><tr><td><a href="%(q2)s">Download 720p</a> (%(fs2)s) at: %(q2)s</br></td></tr><tr><td><a href="%(q3)s">Download 1080p</a> (%(fs3)s) at: %(q3)s</br></td></tr>' %{'q1':video(url)[0], 'q2':video(url)[1], 'q3':video(url)[2], 'fs1':file_size(video(url)[0]),'fs2':file_size(video(url)[1]),'fs3':file_size(video(url)[2])}+'</table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p')) 
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");

def pod_pr(dl):
    a1=html.find('<div class="mp3_description">')
    a2=html.find('<div style="margin-top: 10px">')
    a3=html[a1+len('<div class="mp3_description">'):a2]
    A=[',','exclusively','on RJ',',','sponsored']
    for i in A:
        if a3.find(i)>0:
            a4=a3[a3.find('with')+len('with'):a3.find(i)]
        
    B=['Listen and download the latest episode of']
    for i in B:
        if a4.find(i)>0:
            a5=a4[a4.find(i)+len(i):]
        else:
            a5=a4
        
    
    print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print ('<table>')
    #print ('<div align="center" style="border:1px solid red">')
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist:%s</br> %s</br> %s</br></br></th></tr>'%(a5,artist_song(html)[0],artist_song(html)[1])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) at: %s'%(dl,file_size(dl),dl)+'</td></tr></table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p')) 
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");    

##########################################################
#          Functions are listed above                    #
##########################################################

if (url.find('radiojavan.com'))>=0:
    url2=requests.get(str(url))
    html=url2.text
    z1=html.find('<a href="javascript:void(0)" link="')
    z2=html.find('" target="_blank" class="mp3_download_link">')
    z3=html[z1+len('<a href="javascript:void(0)" link="'):z2]
    if (url.find('/mp3/'))>0:
        a='%s'%single_pr(mp3(url))
    
    elif (url.find('/video/'))>0:
        a='%s'%vid_pr(url)
        
    elif (url.find('/album/'))>0:
        a='%s'%list_pr(list_dl(album(url)))  
        
    elif (url.find('/podcast/'))>0:
        a='%s'%pod_pr(podcast(url))
        
    else:
        print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
        print ("<p><b>Paste a Radiojavan link. </br></br><a href='/RJ'>Try again</a></b></p>")
        print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
        print ("</body></html>");
else:
    print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print ("<p><b>Paste a Radiojavan link. </br></br><a href='/RJ'>Try again</a></b></p>")
    print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
    print ("</body></html>");
    

    
