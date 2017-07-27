#!/home/<user>/bin/python3.4
#
#This script is written in Python3 by Nimasajedi[at]gmail.com on 20th May 2017 to exctract direct download links for musics/video clips 
#(3 different video quality)/podcasts and albums on Radiojavan.com. Moreover, it generates file size and depicts cover photos alongside 
#showing artist/art name. A copy of this script is running on http://mynext.pro/RJ
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
    
#l_mp3= "https://rjmediamusic.com/media/mp3/"
#l_vid="https://rjmediamusic.com/media/music_video/"
l_mp3= 'mp3/mp3-256/'
l_vid=["music_video/lq","music_video/hq","music_video/hd"]
l_pod="podcast/"
l_host=["https://host1.rjmediamusic.com/media/","https://host2.rjmediamusic.com/media/"]

#header='Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title>\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n</head>\n<body>'
header='Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title>\n</head>\n<body>'
#difficulties='</br><table><td><button type="button" data-toggle="collapse" data-target="#RFT">Difficulties in downloading?</button><div id="RFT" class="collapse">Paste generated link at the following box and submit</br><iframe src="/RFT" height="350" width="600"></iframe></div></td></table></br></br>'
difficulties='</br><h4>Having difficulties in downloading? Paste generated link <a href="/RFT">here</a>.</h4>'

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
        file_size=requests.get(dl_link, verify=True, stream=True)
        file_size2=file_size.headers['content-length']
    except KeyError:
        file_size2=0
    file_size3=int(file_size2)/1048576
    fs.append('%d'%file_size3)
    fs.append('%.1f MB'%file_size3)
    return (fs)   


def check_host(cat,last_part):
    x=0
    i=0
    ch=[]
    dl_link=l_host[x]+cat+last_part
    for i in range(0,len(l_host)):
        if int(file_size(dl_link)[0])>0:
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
    a1=URL.find('/video/')
    a2=URL.find('?start')
    if a2<0:
        a2=len(url);
    a3='/'+URL[a1+7:a2]+'.mp4'
    first_part=check_host(l_vid[0],a3)[1]
    vid_list=[]
    x=0
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


def list_DL(List):
    List=List[1:]
    ID_list=[]
    List_dl=[]
    k=0
    j=0
    for i in List:
        a1=requests.get(List[j])
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
            a4=a4[:a4.find("'")]
            ID_list.append(a4+'.mp3')
            while k < len(ID_list):
                List_dl.append(check_host(l_mp3[:4],ID_list[k])[0])
                k+=1
        else:
            List_dl.append(a4)
        j+=1
    return(List_dl)


def list_pr(list_pr):
    print (header)
    print ('<table>')
    print('<tr><td>You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Album: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr>'%Image(html)[1]+'</table>')
    if ((album(url)[0]).isdigit() == True):
        print('<table><tr><td>'+'</br><a href="%(1)s">Download track %(2)s</a> (%(3)s) at: %(1)s'%{'1':list_pr.index(int(album(url).index(0))),'2':(int(album(url).index(0)))+1,'3':file_size(list_pr[int(album(url).index(0))]).index(1)}+'</br></br></br>Other album tracks are:'+'</td></tr>')
        
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> (%s) at: '%(i,list_pr.index(i)+1,file_size(i)[1])+i+'</td></tr>')
    else:
        print('<table></br>')
        for i in list_pr:
            #print ('<tr><td>'+i[0]+'<tr><td>'+i[1]+'</td></th>')
            print ('<tr><td>'+'<a href="%s">Download track %s</a> (%s) at: '%(i,list_pr.index(i)+1,file_size(i)[1])+i+'</td></tr>')
            
    print('</table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p'))
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");

    
def single_pr(dl):
    #print ("Content-type:text/html\r\n\r\n<html><head><title>Radiojavan.com download link generator</title></head><body>");
    print (header)
    print ('<table>')
    #print ('<div align="center" style="border:1px solid red">')
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Song: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) at: %s'%(dl,file_size(dl)[1],dl)+'</td></tr></table>')
    #print(datetime.now().strftime('</br></br></br>%A, %d %b %Y, %I:%M:%S %p')) 
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");

    
def vid_pr(dl):
    print (header)
    print ('<table>')
    #print ('<tr>')
    j=0
    titles=['Download &nbsp; 480p','Download &nbsp; 720p','Download 1080p']
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist: %s</br>Track: %s</br></br></th></tr>'%(artist_song(html)[1],artist_song(html)[0])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[0])
    print('<table><tr><td></br>')
    while j<len(dl):
        print('<tr><td>'+'%s %s %s'%('<a href="%s"><b>%s</b></a>'%(dl[j],titles[j]),' (%s)'%file_size(dl[j])[1],'at: %s'%dl[j])+'</br></td></tr>')
        j+=1
    print('</td></tr></table>')
    print(difficulties)
    print ("<p><b><a href='/RJ'>Try again</a></b></p>")
    print ("</body></html>");

    
def pod_pr(dl):
    p=0
    q=0
    a1=html.find('<div class="mp3_description">')
    a2=html.find('<div style="margin-top: 10px">')
    a3=html[a1+len('<div class="mp3_description">'):a2]
    a4=a3
    A=['Listen and download the latest episode of ','the special episode of ','the second episode of ',',','/',',','RJ presents ','Radio Javan presents ','exclusively','on RJ','sponsored','on Radio Javan','Listen to ','!','Cover photo: Nisha Barahmand','/ Photographer: Mobin Hekmatshoar', 'Cover by Negin Armon']
    B=['Cover photo: ','Photographer: ', 'Cover by ']
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
    print ('<tr><td>'+'You asked for %s</br></br></td></tr>'%url+'<tr><th>Artist:%s</br> %s</br> %s</br></br></th></tr>'%(a4,artist_song(html)[0],artist_song(html)[1])+'<tr><th><img src="%s" /></th></tr></table>'%Image(html)[1]+'<table><tr><td></br><a href="%s">Download track</a> (%s) at: %s'%(dl,file_size(dl)[1],dl)+'</td></tr></table>')
    #print('<tr><td>'+'a3 is %s'%a3+'</td></tr>')
    print(difficulties)
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
        a='%s'%vid_pr(video(url))
        
    elif (url.find('/album/'))>0:
        a='%s'%(list_pr(list_DL(album(url)))) 
        
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
