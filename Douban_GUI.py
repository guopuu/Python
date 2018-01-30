# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from Tkinter import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def Write_txt(text1='',text2='',title='douban.txt'):
    with open(title,"a") as f:
        # for i in text1:
        f.write(str(text1)) #str()不可少
        f.write("\n")
        # for j in text2:
        f.write(str(text2))
        f.write("\n")

def getMV():
    Kind_Dict = {'Hot': 1, 'Newest': 2, 'Classics': 3, 'Playable': 4, 'High Scores': 5,
                 'Wonderful but not popular': 6, 'Chinese film': 7, 'Hollywood': 8,
                 'Korea': 9, 'Japan': 10, 'Action movies': 11, 'Comedy': 12, 'Love story': 13,
                 'Science fiction': 14, 'Thriller': 15, 'Horror film': 16, 'Whatever': 17}
    Sort_Dict = {'Sort by hot': 1, 'Sort by time': 2, 'Sort by score': 3}
    kind_in = Kind_Dict[kind.get(kind.curselection())]
    sort_in = Sort_Dict[sort.get(sort.curselection())]
    number_in = int(top_count.get())
    save_in = file_to.get()
    getUrl_Title(kind_in,sort_in,number_in,save_in)

def clean():
    input_top.delete(0,END)
    input_file.delete(0,END)
    result_out.delete(0,END)

root = Tk()
root.title('豆瓣电影获取')
root.geometry('600x400+100+100')
root_label = Label(root,text='豆瓣电影获取-GUOPUU',font=('宋体',15))
root_label.pack(side=TOP)

frame3 = Frame(root)
frame3.pack(side=TOP)
label4 = Label(frame3,text='**'*45)
label4.pack(side=TOP)

choose_frame = Frame(root)
choose_frame.pack(side=TOP)
kind = Listbox(choose_frame,exportselection=False,height=5)
kind_item = ['Hot','Newest','Classics','Playable','High Scores','Wonderful but not popular','Chinese film',
             'Hollywood','Korea','Japan','Action movies','Comedy','Love story',
             'Science fiction','Thriller','Horror film','Cartoon']
for i in kind_item:
    kind.insert(END,i)
kind.pack(side=LEFT)
#滑动Scrollbar
scr1 = Scrollbar(choose_frame)
kind.configure(yscrollcommand=scr1.set)
scr1['command']=kind.yview()
scr1.pack(side=LEFT,fill=Y)

sort = Listbox(choose_frame,exportselection=False,height=5)
sort_item = ['Sort by hot','Sort by time','Sort by score']
for i in sort_item:
    sort.insert(END,i)
sort.pack(side=LEFT)
#滑动Scrollbar
scr2 = Scrollbar(choose_frame)
sort.configure(yscrollcommand=scr2.set)
scr2['command']=sort.yview()
scr2.pack(side=LEFT,fill=Y)

label2 = Label(choose_frame,text=' Top ？:',font=('宋体',15))
label2.pack(side=LEFT)
top_count = StringVar()
input_top = Entry(choose_frame,width=10,textvariable=top_count)
input_top.pack(side=LEFT)

frame1 = Frame(root)
frame1.pack(side=TOP)
label4 = Label(frame1,text='导出文件名(**.txt)：',font=('宋体',15))
label4.pack(side=LEFT)
file_to = StringVar()
input_file = Entry(frame1,width=30,textvariable=file_to)
input_file.pack(side=LEFT)

frame5 = Frame(root)
frame5.pack(side=TOP)
label51 = Label(frame5,text='*'*40)
label51.pack(side=TOP)

job_frame = Frame(root)
job_frame.pack(side=TOP)
label1 = Label(job_frame,text='爬取数据：',font=('宋体',15))
label1.pack(side=LEFT)
button = Button(job_frame,text='爬取',command=getMV)
button.pack(side=LEFT)
button_c = Button(job_frame,text='清空',command=clean)
button_c.pack(side=RIGHT)

frame2 = Frame(root)
frame2.pack(side=TOP)
label4 = Label(frame2,text='*'*40)
label4.pack(side=TOP)

result_frame = Frame(root)
result_frame.pack(side=TOP)
label3 = Label(result_frame,text='结果:',font=('宋体',15))
label3.pack(side=LEFT)
result_out = Listbox(result_frame,height=7,width=70)
result_out.pack(side=LEFT)

#获取url和文章标题
def getUrl_Title(kind,sort,number,save_name):
    global SUMRESOURCES
    result_out.insert(END,'system loading...wait...')
    SUMRESOURCES = 0
    driver_detail = webdriver.PhantomJS(
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])  # 据说windows不用加参数
    driver_item = webdriver.Chrome()
    url = 'https://movie.douban.com/explore#!type=movie'
    # 等待页面加载
    wait = ui.WebDriverWait(driver_item, 15)
    wait1 = ui.WebDriverWait(driver_detail, 15)
    result_out.insert(END,"---------------------crawling...---------------------")
    driver_item.get(url)
    wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='fliter-wp']/div[@class='filter']/form/div[@class='tags']/div[@class='tag-list']/label[%s]"%kind))
    driver_item.find_element_by_xpath("//div[@class='fliter-wp']/div[@class='filter']/form/div[@class='tags']/div[@class='tag-list']/label[%s]"%kind).click()
    wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='fliter-wp']/div[@class='filter']/form/div[3]/div[1]/label[%s]"%sort))
    driver_item.find_element_by_xpath("//div[@class='fliter-wp']/div[@class='filter']/form/div[3]/div[1]/label[%s]"%sort).click()

    num = number + 1
    time.sleep(2)

    #点击几次“加载更多”
    num_time = num/20+1
    wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']"))
    for times in range(1,num_time):
        time.sleep(1)
        driver_item.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']").click()
        time.sleep(1)
        wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='list']/a[%d]"%num))

    # 使用wait.until使元素全部加载好能定位之后再操作，相当于try/except再套个while把

    for i in range(1,num):
        wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='list']/a[%d]"%num))
        list_title = driver_item.find_element_by_xpath("//div[@class='list']/a[%d]"%i)
        SUMRESOURCES += 1
        result_out.insert(END, '------------------' + 'NO.' + str(SUMRESOURCES) + '------------------')
        result_out.insert(END, u'电影名: ' + list_title.text)
        result_out.insert(END, u'链接: ' + list_title.get_attribute('href'))
        # print unicode码自动转换为utf-8的
        #写入txt部分１
        list_title_wr = list_title.text.encode('utf-8')#unicode码，需要重新编码再写入txt
        list_title_url_wr = list_title.get_attribute('href')    #href
        Write_txt('\n----------------------------------'+'NO.' + str(SUMRESOURCES)+'-----------------------------------','',save_name)
        Write_txt(list_title_wr,list_title_url_wr,save_name)

        ##############################################################################
        # 当选择一部电影后，进入这部电影的超链接，然后才能获取
        # 同时别忽视元素加载的问题
        # 在加载长评论的时候，注意模拟点击一次小三角，不然可能会使内容隐藏
        ##############################################################################
        driver_detail.get(list_title_url_wr)
        wait1.until(lambda driver: driver.find_element_by_xpath("//div[@id='link-report']/span"))
        introduction = driver_detail.find_element_by_xpath("//div[@id='link-report']/span").text
        result_out.insert(END, u"简介：" + introduction)
        introduction_wr = introduction.encode('utf-8')
        Write_txt(introduction_wr, '', save_name)
        for i in range(1, 5):
            try:
                comments_hot = driver_detail.find_element_by_xpath("//div[@id='hot-comments']/div[%d]/div/p" % i)
                result_out.insert(END, u'最新热评：' + comments_hot.text)
                comments_hot_wr = 'Hot comments '+str(i)+' : '+comments_hot.text.encode('utf-8')
                # Write_txt("----------------------Hot comments TOP%d--------------------" % i, '', save_name)
                Write_txt(comments_hot_wr, '', save_name)
            except:
                result_out.insert(END, 'can not caught the comments.')
    result_out.insert(END,'Get Success !!!')
    driver_item.quit()

if __name__ == '__main__':
    # getUrl_Title()
    # driver_item.quit()
    root.mainloop()