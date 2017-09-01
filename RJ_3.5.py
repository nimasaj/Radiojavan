#!/home/<user>/bin/python3

"""This script is first written on 20th May 2017 in Python3 by Nimasajedi[at]gmail.com to get direct download links for musics, video clips 
(including 3 different video qualities), podcasts and albums on Radiojavan.com. Also, it generates file size beside depicting cover photos and 
showing artist/art name. A copy of this script is running on http://mynext.pro/RJ."""

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
    

l_mp3= 'mp3/mp3-256/'
l_vid=("music_video/lq","music_video/hq","music_video/hd","music_video/4k")
l_pod="podcast/"
l_host=("https://host1.rjmediamusic.com/media/","https://host2.rjmediamusic.com/media/")
font_size=2
Artist='<font color="gray" size="%d">Artist:</font>'%font_size
Album='<font color="gray" size="%d">Album:</font>'%font_size
Track='<font color="gray" size="%d">Track:</font>'%font_size
Song='<font color="gray" size="%d">Song:</font>'%font_size

DL_track='Download track'
ask='<font color="gray">You asked for</font>'
color='<font color="gray">'
header='Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title>\n</head>\n<body>'
difficulties='</br><h4>Having difficulties in downloading? Paste generated link <a href="/RFT">here</a>.</h4>'
url0='https://www.radiojavan.com'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

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
        image_big_dl=s.get(i_big, stream=True)
        with open('../RJ/tmp/%s_b_image.jpg'%artist_song(html)[1], 'wb') as f:
            f.write(image_big_dl.content)
    image_big='http://mynext.pro/RJ/tmp/%s_b_image.jpg'%artist_song(html)[1]
    A=[]
    A.append(image_big)
    
    i_small=a4.group(1)[:len(a4.group(1))-4]+'-thumb.jpg'
    if float(file_size(i_small)[0])!=0:
        image_small_dl=s.get(i_small, stream=True)
        with open('../RJ/tmp/%s_s_image.jpg'%artist_song(html)[1], 'wb') as f:
            f.write(image_small_dl.content)
        image_small='http://mynext.pro/RJ/tmp/%s_s_image.jpg'%artist_song(html)[1]
    else:
        image_small=image_big
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
        try:
            song=(' %s'%(a6.group(1)))
        except AttributeError:
            song=a4_fck
    A=[]
    A.append(song)
    try:
        ar1=a5.group(1)
    except AttributeError:
        try:
            ar1=a6.group(2)
        except AttributeError:
            #ar1=a4_fck
            ar1=''
    if ('&amp' in ar1):
        ar2=re.match(r'(.*)amp;(.*)',ar1, re.M|re.I)
        artist=ar2.group(1)+ar2.group(2)
    else:
        artist=ar1
    A.append(artist)
    return (A)
    
    
def file_size(dl_link):
    fs=[]
    try:
        file_size=s.get(dl_link, verify=True, stream=True, headers=headers)
        file_size2=file_size.headers['content-length']
    except KeyError:
        file_size2=0
    file_size3=int(file_size2)/1048576
    fs.append('%.3f'%file_size3)
    fs.append('%.1f MB'%file_size3)
    return (fs)
    
    
def check_host(cat,last_part):
    x,i=0,0
    ch=[]
    dl_link=l_host[x]+cat+last_part
    for i in range(0,len(l_host)):
        if float(file_size(dl_link)[0])>0:
            dl_link=l_host[x]+cat+last_part
            ch.append(dl_link)
            ch.append(l_host[x])
            break
        else:
            if x==len(l_host)-1:
                break
            else:
                x+=1
                dl_link=l_host[x]+cat+last_part
    return(ch)
    
    
def mp3(url):
    a1=url.find('/mp3/')
    a2=url.find('?start')
    if a2<0:
        a2=len(url);
    a3=url[a1+5:a2]+'.mp3'
    if z1>0:
        dl_link=z3
    else:
        dl_link=check_host(l_mp3,a3)[0]
    return(dl_link)


def video(URL):
    vid_list=[]
    x=0
    a1=URL.find('/video/')
    a2=URL.find('?start')
    if a2<0:
        a2=len(url);
    a3='/'+URL[a1+7:a2]+'.mp4'
    first_part=check_host(l_vid[0],a3)[1]
    for i in range(0,len(l_vid)):
        if x==len(l_vid):
            break
        else:
            try:
                vid_list.append(check_host(l_vid[x],a3)[0])
            except IndexError:
                break
            x+=1
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
        current_track_no='null'
        ID=a1[a1.find('/album/')+len('/album/'):]
        track_list.append('%s'%current_track_no)
    i=0
    b=html[html.find('<span class="song_name">'):html.rfind('<span class="song_name">')]
    b_len=len('<span class="song_name">')
    iter=re.finditer(r'<span class="song_name">', b)
    indices=[m.start(0) for m in iter]
    while i<all_track_nr:
        track_list.append('%s?index=%d'%(a1,i))
        d=(b[indices[i]:].find('</span>'))
        track_name=b[indices[i]+b_len:indices[i]+d]
        track_list.append(track_name)
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
        dl_link=check_host(l_pod,ID+'.mp3')
    return(dl_link)


def list_DL(List):
    List=List[1:]
    List2,ID_list,List_dl=[],[],[]
    k,j,p=0,0,0    
    while p*2<len(List):
        List2.append(List[p*2])
        p+=1
        
    for i in List2:
        url_list=s.get(List2[j], headers=headers)
        html=url_list.text
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
            a4=a4[:a4.find("'")]
            ID_list.append(a4+'.mp3')
            while k < len(ID_list):
                List_dl.append(check_host(l_mp3[:4],ID_list[k])[0])
                k+=1
        else:
            List_dl.append(a4)
        j+=1
    return(List_dl)
    

def track_name(List):
    List2=[]
    p=0

    while p*2<len(List):
        List2.append(List[p*2])
        p+=1
    List2=List2[1:]
    return(List2)
    
    
def list_pr(list_pr,trackname):
    print (header)
    print ('<table>')
    print('<tr><td>%s %s%s</font></br></br></td></tr>'%(ask,color,url)+'<tr><th>%s %s</br>%s %s</br></br></th></tr>'%(Artist,artist_song(html)[1],Album,artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr>'%Image(html)[1]+'</table>')
    if ((album(url)[0]).isdigit() == True):
        print('<table><tr><td>'+'</br><a href="%(1)s">Download track %(2)s</a> - %(4)s (%(3)s) %(5)s at: %(1)s'%{'1':list_pr[int(album(url)[0])],'2':(int(album(url)[0]))+1,'3':file_size(list_pr[int(album(url)[0])])[1],'4':trackname[int(album(url)[0])],'5':color}+'</font></br></br></br>All album tracks are:'+'</td></tr>')
        
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> - %s (%s) %s at: '%(i,list_pr.index(i)+1,trackname[list_pr.index(i)],file_size(i)[1],color)+i+'</font></td></tr>')
        
    else:
        print('<table></br>')
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> - %s (%s) %s at: '%(i,list_pr.index(i)+1,trackname[list_pr.index(i)],file_size(i)[1],color)+i+'</font></td></tr>')
            
    print('</table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");


def single_pr(dl):
    print (header)
    print ('<table>')
    #print ('<div align="center" style="border:1px solid red">')
    print ('<tr><td>'+'%s %s%s</font></br></br></td></tr>'%(ask,color,url)+'<tr><th>%s %s</br>%s %s</br></br></th></tr>'%(Artist,artist_song(html)[1],Song,artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) %s at: %s'%(dl,file_size(dl)[1],color,dl)+'</font></td></tr></table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p')) 
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");


def vid_pr(dl):
    print (header)
    print ('<table>')
    j=0
    titles=['Download &nbsp; 480p','Download &nbsp; 720p','Download 1080p','Download &nbsp;&nbsp;4K&nbsp;&nbsp;&nbsp;']
    print ('<tr><td>'+'%s %s%s</font></br></br></td></tr>'%(ask,color,url)+'<tr><th>%s %s</br>%s %s</br></br></th></tr>'%(Artist,artist_song(html)[1],Track,artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[0])
    print('<table><tr><td></br>')
    while j<len(dl):
        print('<tr><td>'+'%s %s %s'%('<a href="%s"><b>%s</b></a>'%(dl[j],titles[j]),' (%s)'%file_size(dl[j])[1],'%s at: %s'%(color,dl[j]))+'</font></br></td></tr>')
        j+=1
    print('</td></tr></table>')
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");


def pod_pr(dl):
    p,q=0,0
    a1=html.find('<div class="mp3_description">')
    a2=html.find('<div style="margin-top: 10px">')
    if a2<0:
        a2=a1+html[a1:].find('</div>')
    a3=html[a1+len('<div class="mp3_description">'):a2]
    a4=a3
    A=['Listen and download the latest episode of ','the special episode of ','Listen and enjoy ','the second episode of ',',','/',',','RJ presents ','Radio Javan presents ','Radio Javan present ','exclusively','on RJ','sponsored','on Radio Javan','Listen to ','!']
    B=['Cover photo: ','Photographer: ', 'Cover by ','Cover: ']
    while p<len(A):
        if a4.lower().find(A[p].lower())>=0:
            rev1=a4[:(a4.lower().find(A[p].lower()))]
            rev2=a4[(a4.lower().find(A[p].lower()))+len(A[p].lower()):]
            a4='%s%s'%(rev1,rev2)
        p+=1
    while q<len(B):
        if a4.lower().find(B[q].lower())>=0:
            a4='%s'%(a4[:(a4.lower().find(B[q].lower()))])
        q+=1
    print (header)
    print ('<table>')
    #print ('<div align="center" style="border:1px solid red">')
    print ('<tr><td>'+'%s %s%s</font></br></br></td></tr>'%(ask,color,url)+'<tr><th>%s %s</br> %s</br> %s</br></br></th></tr>'%(Artist,a4,artist_song(html)[0],artist_song(html)[1])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) %s at: %s'%(dl,file_size(dl)[1],color,dl)+'</font></td></tr></table>')
    #print('<tr><td>'+'a3 is %s'%a3+'</td></tr>')
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");
    
##########################################################
#          Functions are listed above                    #
##########################################################

if (url.find('radiojavan.com'))>=0:
    s=requests.Session()
    s.get(url0)
    url2=s.get(url, headers=headers)
    html=url2.text
    z1=html.find('<a href="javascript:void(0)" link="')
    z2=html.find('" target="_blank" class="mp3_download_link">')
    z3=html[z1+len('<a href="javascript:void(0)" link="'):z2]
    if (url.find('/mp3/'))>0:
        a='%s'%single_pr(mp3(url))
    
    elif (url.find('/video/'))>0:
        a='%s'%vid_pr(video(url))
        
    elif (url.find('/album/'))>0:
        a='%s'%(list_pr(list_DL(album(url)),track_name(album(url)))) 
        
    elif (url.find('/podcast/'))>0:
        a='%s'%pod_pr(podcast(url))
        
    else:
        print (header)
        print ("<p><b>Paste a Radiojavan link. </br></br><a href='/RJ'>Try again</a></b></p>")
        print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
        print ("</body></html>");
else:
    print (header)
    print ("<p><b>Paste a Radiojavan link. </br></br><a href='/RJ'>Try again</a></b></p>")
    print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
    print ("</body></html>");
    
