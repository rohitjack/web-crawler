import requests
import re
import csv
from bs4 import BeautifulSoup
import json
import time
PYTHONIOENCODING="UTF-8"
def removeSpaces(string): 
    string = string.replace(' ','') 
    return string  
f1 = csv.writer(open('preffix1.csv','w+'))
f1.writerow(['Affix', 'Root Word', 'Full Word'])
url=[r'https://en.wiktionary.org/wiki/Category:English_prefixes']
g={}
count=0
f=0
affix_count=0
for u in url:
    if u != r'https://en.wiktionary.org/wiki/Category:English_adverb-forming_suffixes' and u != r'https://en.wiktionary.org/wiki/Category:English_prefixes':
        
        r=requests.get(u)
        soup=BeautifulSoup(r.text, 'html.parser')
        price_box=soup.find('div', attrs={'class':'mw-category'})
        l=re.findall('<a href="([^"]+)" title="[^"]+">.*?</a>', str(price_box))
        print(l)
    elif u==r'https://en.wiktionary.org/wiki/Category:English_prefixes':
        r=requests.get(u)
        f=1
        l=[]
        u8=u
        while(1):
            count=count+1
            r=requests.get(u8)
            soup=BeautifulSoup(r.text, 'html.parser')
            price_box=soup.find('div', attrs={'id':'mw-pages'})
            print(price_box)
            l2=re.findall('<a href="([^"]+)" title="[^"]+">.*?</a>', str(price_box))
            if(l2):
                l.extend(l2)
            print(count)
            #price_box2=soup.find('div', attrs={'class':'mw-pages'})
            #print(price_box2)
            match1=re.findall('<a href="([^"]+)" title="[^"]+">next page</a>', str(price_box))
            #print(match1[0])
            #break
            if match1:
                u3='https://en.wiktionary.org'+match1[0]
                u8=u3.replace('amp;','')
                #rm=requests.get(u)

            else:
                break
        print(l)

    else:
        r=requests.get(u)
        soup=BeautifulSoup(r.text, 'html.parser')
        price_box=soup.find('div', attrs={'id':'mw-pages'})
        l=re.findall('<a href="([^"]+)" title="[^"]+">.*?</a>', str(price_box))
        q=u[u.find('_')+1:]
        print("adverb")
        g[q]={}
        
    for u2 in l: #affix
        count1 = 0
        count2 = 0
        try:
            
            if(u!=r'https://en.wiktionary.org/wiki/Category:English_prefixes'):

                u3='https://en.wiktionary.org'+u2
                print("u3="+u3)
                rm1=requests.get(u3)
                time.sleep(0.01)
                soup1=BeautifulSoup(rm1.text, 'html.parser')
                price_box7=soup1.find('div', attrs={'class':'CategoryTreeItem'})
                #print(price_box7)
                l7=re.findall('href="([^"]+)">English words suffixed with', str(price_box7))
                if(l7==[]):
                    continue
                print(l7)
                u4='https://en.wiktionary.org'+l7[0]
                print(u4)

                while(1):

                    rm=requests.get(u4)
                    soup1=BeautifulSoup(rm.text, 'html.parser')
                    price_box2=soup1.find('div', attrs={'class':'mw-category-generated'})
                    l2=re.findall('<a href="([^"]+)" title="[^"]+">.*?</a>', str(price_box2))
                    if(l2==[]):
                        break
                    for u4 in l2:

                        try:
                            k=u2.rfind('-')
                            str3=u2[k+1:]
                            a=u4.find('/')
                            b=u4.find('#')
                            str2=u4[a+1:b]

                            u5='https://en.wiktionary.org'+u4
                            print(u5)
                            k2=u5.rfind('/')
                            str7=u5[k2+1:]
                            rx=requests.get(u5)
                            soup2=BeautifulSoup(rx.text,'html.parser')
                            price_box3=soup2.p
                            #print(price_box3)
                            l3=re.findall('<a.*?href="[^"]+" title="([^"]+)">.*?</a>',str(price_box3))
                            if(l3==[]):
                                print("hola")
                                continue
                            #str2,l3[0],l3[1],extract the brackets out of root words and affixes
                           # if l3 :
                                #print("yes")
                            #    print(l3[0])
                             #   print(str3)
                           # else :
                           #     print("no")
                            #x=l3[0].find('(')
                            #y=l3[1].find('(')
                            #print(str1)
                            else:
                                root_word=" "
                                #print("str3="+str3)
                                str11='-'+str3
                                #print("str11="+str11)
                                print("hola1")
                                for a in range(len(l3)):
                                    
                                    x=l3[a].find('(')
                                    if(x!=-1):
                                        temp_word=l3[a][:x]
                                    else:
                                        temp_word=l3[a]
                                    lx=len(temp_word)
                                    if(temp_word[0]=='-'):
                                        temp_word=temp_word[1:]
                                    lx=len(temp_word)
                                    if(temp_word[lx-1]=='-'):
                                        temp_word=temp_word[:lx-1]
                                    print("temp_word="+temp_word)
                                    temp_word=removeSpaces(temp_word)
                                    if(temp_word.isalpha()==False):
                                        print("continuing")
                                        continue
                                    if(temp_word==str3):
                                        print("breaking")
                                        break
                                    if(root_word==" "):
                                        root_word=temp_word
                                        print("root_word"+root_word)
                                    else:
                                        root_word=root_word+"+"+temp_word
                                        print("root_word"+root_word)
                                #print(root_word)    
                            if(root_word.isalpha() and str7.isalpha()):
                                print("final=")
                                affix=str3
                                final_word=str7
                                print(affix+" "+root_word)
                                #print(str7)
                                f1.writerow([affix, root_word, final_word])
                                count1+=1
                                time.sleep(0.001)
                            else: 
                                print("error")
                                count2+=1
                                continue
            
                        except:
                            print("error")
                            count2+=1
                            continue


                    price_box3=soup1.find('div', attrs={'id':'mw-pages'})
                    #print(price_box3)
                    match=re.findall('<a href="([^"]+)" title="[^"]+">next page</a>', str(price_box3))
                    print(type(match))
                    if match:

                        u3='https://en.wiktionary.org'+match[0]
                        u4=u3.replace('amp;','')
                        print(u4)
                    else:
                        break
                f1.writerow([str(count1), str(count2)])
                print(" ")
                print(" ")
                print(count1 + " " + count2)
                print(" ")
                print(" ")


            else: 
                
                print(u2)
                u3='https://en.wiktionary.org'+u2
                print(u3)
                rm1=requests.get(u3)
                time.sleep(0.01)
                soup1=BeautifulSoup(rm1.text, 'html.parser')
                price_box6=soup1.find_all('div', attrs={'class':'CategoryTreeItem'})
                #print(price_box7)
                flag=0
                for price_box7 in price_box6:
                    l7=re.findall('href="([^"]+)">English words prefixed with', str(price_box7))
                    if(l7==[]):
                        flag=0
                        continue
                    else:    
                        print(l7)
                        u4='https://en.wiktionary.org'+l7[0]
                        print("u4="+u4)
                    
                

                while(1):

                    rm=requests.get(u4)
                    soup1=BeautifulSoup(rm.text, 'html.parser')
                    price_box2=soup1.find('div', attrs={'class':'mw-category-generated'})
                    l2=re.findall('<a href="([^"]+)" title="[^"]+">.*?</a>', str(price_box2))

                    if(l2==[]):
                        break

                    for u4 in l2:

                        try:
                            k=u2.rfind('/')
                            m=u2.rfind('-')
                            str3=u2[k+1:m]
                            u5='https://en.wiktionary.org'+u4
                            print(u5)
                            k2=u5.rfind('/')
                            str7=u5[k2+1:]
                            rx=requests.get(u5)
                            soup2=BeautifulSoup(rx.text,'html.parser')
                            price_box3=soup2.p
                            #print(price_box3)
                            l3=re.findall('<a.*?href="[^"]+" title="([^"]+)">.*?</a>',str(price_box3))
                            if(l3==[]):
                                print("hola")
                                continue
                            #str2,l3[0],l3[1],extract the brackets out of root words and affixes
                           # if l3 :
                                #print("yes")
                            #    print(l3[0])
                             #   print(str3)
                           # else :
                           #     print("no")
                            #x=l3[0].find('(')
                            #y=l3[1].find('(')
                            #print(str1)
                            else:
                                root_word=" "
                                #print("str3="+str3)
                                str11='-'+str3
                                #print("str11="+str11)
                                print("hola1")
                                for a in range(len(l3)):
                                    
                                    x=l3[a].find('(')
                                    if(x!=-1):
                                        temp_word=l3[a][:x]
                                    else:
                                        temp_word=l3[a]
                                    lx=len(temp_word)
                                    if(temp_word[0]=='-'):
                                        temp_word=temp_word[1:]
                                    lx=len(temp_word)
                                    if(temp_word[lx-1]=='-'):
                                        temp_word=temp_word[:lx-1]
                                    print("temp_word="+temp_word)
                                    temp_word=removeSpaces(temp_word)
                                    if(temp_word.isalpha()==False):
                                        print("continuing")
                                        continue
                                    if(temp_word==str3):
                                        print("skipping prefix")
                                        continue
                                    if(root_word==" "):
                                        root_word=temp_word
                                        print("root_word"+root_word)
                                    else:
                                        root_word=root_word+"+"+temp_word
                                        print("root_word"+root_word)
                                #print(root_word)
                            if(root_word.isalpha() and str7.isalpha()):    
                                affix=str3
                                final_word=str7
                                print(root_word)
                                #print(str7)
                                f1.writerow([affix, root_word, final_word])
                                count1+=1
                                time.sleep(0.001)
                            else:
                                print("error")
                                count2+=1
                                continue 
                        except:
                                print("error")
                                count2+=1
                                continue
                    price_box3=soup1.find('div', attrs={'id':'mw-pages'})
                    #print(price_box3)
                    match=re.findall('<a href="([^"]+)" title="[^"]+">next page</a>', str(price_box3))
                    print(type(match))
                    if match:

                        u3='https://en.wiktionary.org'+match[0]
                        u4=u3.replace('amp;','')
                        print(u4)
                    else:
                        break
                f1.writerow([str(count1), str(count2)])
                print(" ")
                print(" ")
                print(count1 + " " + count2)
                print(" ")
                print(" ")
        except:
                    print("error in affix")
                    continue
