# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print('system loading...wait...')
SUMRESOURCES = 0
driver_detail = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])#据说windows不用加参数
driver_item = webdriver.Chrome()
url = 'https://movie.douban.com/explore#!type=movie'
#等待页面加载
wait = ui.WebDriverWait(driver_item,15)
wait1 = ui.WebDriverWait(driver_detail,15)

#获取url和文章标题
def getUrl_Title():
    global SUMRESOURCES

    #需要输入想要获取的信息。比如排序方式，种类，内容。
    print('please select:')
    kind = input("1-Hot\n2-Newest\n3-Classics\n4-Playable\n5-High Scores\n6-Wonderful but not popular\n7-Chinese film\n8-Hollywood\n9-Korea\n10-Japan\n11-Action movies\n12-Comedy\n13-Love story\n14-Science fiction\n15-Thriller\n16-Horror film\n17-Cartoon\nplease select:")
    print "--------------------------------------------------------------------------"
    sort = input("1-Sort by hot\n2-Sort by time\n3-Sort by score\nplease select:")
    print "--------------------------------------------------------------------------"
    number = input("TOP ?:")
    print "--------------------------------------------------------------------------"
    # ask_long = input("don't need long-comments,enter 0,i like long-comments enter 1:")
    # print "--------------------------------------------------------------------------"
    global save_name
    save_name = raw_input("save_name (xx.txt):")
    print "---------------------crawling...---------------------"

    driver_item.get(url)
    # 进行网页get后，先进行电影种类选择的模拟点击操作，然后再是排序方式的选择
    # 最后等待一会，元素都加载完了，才能开始爬电影，不然元素隐藏起来，不能被获取
    # wait.until是等待元素加载完成！

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
        print '------------------' + 'NO.' + str(SUMRESOURCES) + '------------------'
        print u'电影名: ' + list_title.text
        print u'链接: ' + list_title.get_attribute('href')
        # print unicode码自动转换为utf-8的

        #写入txt部分１
        list_title_wr = list_title.text.encode('utf-8')#unicode码，需要重新编码再写入txt
        list_title_url_wr = list_title.get_attribute('href')    #href
        Write_txt('\n----------------------------------'+'NO.' + str(SUMRESOURCES)+'-----------------------------------','',save_name)
        Write_txt(list_title_wr,list_title_url_wr,save_name)

        # try:  # 获取具体内容和评论。href是每个超链接也就是资源单独的url
        #     getDetails(str(list_title.get_attribute('href')))
        # except:
        #     print 'can not get the details!'
        ##############################################################################
        # 当选择一部电影后，进入这部电影的超链接，然后才能获取
        # 同时别忽视元素加载的问题
        # 在加载长评论的时候，注意模拟点击一次小三角，不然可能会使内容隐藏
        ##############################################################################
        driver_detail.get(list_title_url_wr)
        wait1.until(lambda driver: driver.find_element_by_xpath("//div[@id='link-report']/span"))
        introduction = driver_detail.find_element_by_xpath("//div[@id='link-report']/span").text
        print u"简介：" + introduction
        introduction_wr = introduction.encode('utf-8')
        Write_txt(introduction_wr, '', save_name)
        for i in range(1, 5):
            try:
                comments_hot = driver_detail.find_element_by_xpath("//div[@id='hot-comments']/div[%d]/div/p" % i)
                print u'最新热评：' + comments_hot.text
                comments_hot_wr = 'Hot comments '+str(i)+' : '+comments_hot.text.encode('utf-8')
                # Write_txt("----------------------Hot comments TOP%d--------------------" % i, '', save_name)
                Write_txt(comments_hot_wr, '', save_name)
            except:
                print 'can not caught the comments.'

    # 1. webDriver.Close() - Close the browser window that the driver has focus of // 关闭当前焦点所在的窗口
    # 2. webDriver.Quit() - Calls dispose // 调用dispose方法
    # 3. webDriver.Dispose() Closes all browser windows and safely ends the session 关闭所有窗口，并且安全关闭session


# def getDetails(url):
#     driver_detail.get(url)
#     wait1.until(lambda driver:driver.find_element_by_xpath("//div[@id='link-report']/span"))
#     introduction = driver_detail.find_element_by_xpath("//div[@id='link-report']/span").text
#     print u"简介："+introduction
#     introduction_wr = introduction.encode('utf-8')
#     Write_txt(introduction_wr,'',save_name)
#     for i in range(1,5):
#         try:
#             comments_hot = driver_detail.find_element_by_xpath("//div[@class='hot-comments'/div[%d]/div/p]"%i)
#             print u'最新热评：'+comments_hot.text
#             comments_hot_wr = comments_hot.text.encode('utf-8')
#             Write_txt("----------------------Hot comments TOP%d--------------------" % i,'', save_name)
#             Write_txt(comments_hot_wr, '', save_name)
#
#         except:
#             print 'can not caught the comments.'
    # if long == 1:
    #     try:
    #         driver_detail.find_element_by_xpath("//img[@class='bn-arrow']").click()
    #         # wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='review-bd']/div[2]/div/div"))
    #         time.sleep(1)
    #         # 解决加载长评会提示剧透问题导致无法加载
    #         comments_get = driver_detail.find_element_by_xpath("//div[@class='review-bd']/div[2]/div")
    #         if comments_get.text.encode('utf-8') == '提示: 这篇影评可能有剧透':
    #             comments_deep = driver_detail.find_element_by_xpath("//div[@class='review-bd']/div[2]/div[2]")
    #         else:
    #             comments_deep = comments_get
    #         print "--------------------------------------------long-comments---------------------------------------------"
    #         print u"深度长评：" + comments_deep.text
    #         comments_deep_wr = comments_deep.text.encode('utf-8')
    #         Write_txt(
    #             "--------------------------------------------long-comments---------------------------------------------\n",
    #             '', save_name)
    #         Write_txt(comments_deep_wr, '', save_name)
    #     except:
    #         print 'can not caught the deep_comments!'


def Write_txt(text1='',text2='',title='douban.txt'):
    with open(title,"a") as f:
        # for i in text1:
        f.write(str(text1)) #str()不可少
        f.write("\n")
        # for j in text2:
        f.write(str(text2))
        f.write("\n")

if __name__ == '__main__':
    getUrl_Title()
    driver_item.quit()