import os, time, codecs, datetime
from selenium import webdriver

import selenium, pdfplumber, requests

from log.logger import logger as log
from utils.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver.settings')
import django
django.setup()
from ipoWatcher.models import Project, Watcher

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), "chromedriver.exe"))


def get_all_info():
    '''
    动态ajax, 用浏览器获取数据比较方便
    :return:
    '''

    current_project_title = "" if len(Project.objects.all()) == 0 else Project.objects.all().order_by('-id')[0].title
    browser.get("http://kcb.sse.com.cn/renewal/")
    work_flag = True
    while work_flag:
        time.sleep(5) # 等待页面加载
        hrefs = browser.find_elements_by_css_selector("#dataList1_container>tbody>tr:not(:first-child) td:nth-child(2)>a")
        for href in hrefs:
            title = href.text.replace("<br>","").replace("\n","")
            if title == current_project_title or len(Project.objects.filter(title=title)):
                work_flag = False
                break
            else:
                qs = Project(
                    title = title,
                    link = href.get_attribute("href")
                )
                qs.save()
        if work_flag:
            try:
                browser.find_element_by_css_selector("a.paging_next").click()
            except selenium.common.exceptions.NoSuchElementException:
                work_flag = False
                log.info("all data loaded!")
                break
        log.info("reading projects...")
    # browser.close()


def dowload_pdf_and_convert():
    projects = Project.objects.filter(downloaded__isnull=True)
    for project in projects:
        browser.get(project.link)
        time.sleep(5)
        href = browser.find_elements_by_css_selector("tr#tile30 td.vs1 a")
        if len(href) == 0:
            log.error("web format changed, cannot find downloadlink")
            break
        else:
            href = href[0]
            pdf_file = requests.get(href.get_attribute("href"), stream=True)
            with open("..\\data\\{}.pdf".format(project.title), "wb") as f:
                for chunk in pdf_file.iter_content(chunk_size=128):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            project.downloaded = datetime.date.today()
            log.info("{} has been downloaded.".format(project.title))

            try:
                with pdfplumber.open("..\\data\\{}.pdf".format(project.title)) as pdf:
                    txt_filename = project.title + ".txt"
                    with codecs.open("..\\data\\{}".format(txt_filename), "w", encoding="utf-8") as new_f:
                        page_cnt = 1
                        for page in pdf.pages:
                            new_f.write(page.extract_text())
                            log.debug("converting page: {} / {}".format(page_cnt, len(pdf.pages)))
                            page_cnt += 1

                log.info("{} had been converted.".format(project.title))
            except:
                log.error("{} had convert failed.".format(project.title))

            project.save()


def check_and_notify():
    projects = Project.objects.exclude(checked = True)
    mails = []
    watchers = Watcher.objects.filter(available=True)
    for project in projects:
        for watcher in watchers:
            keyword_cnt = {}
            keywords = watcher.keywords.split(",")
            with open("..\\data\\{}".format(project.get("title") + ".txt"),"r", encoding="utf-8") as f:
                content = f.read()
                for keyword in keywords:
                    keyword_cnt[keyword] = content.count(keyword)
            keyword_threshold_cnt = 0
            for k,v in keyword_cnt.items():
                keyword_threshold_cnt += v
            if keyword_threshold_cnt >= watcher.keyword_threshold:
                message = "{}:\n".format(time.strftime("%Y/%m/%d"))
                message = message + "-"*8 + "\n"
                message = message + project["title"] + "/" + project["link"] + "\n"
                for k,v in keyword_cnt.items():
                    message = message + k + " : " + str(v) + "\n"
                mails.append({
                    "message": message,
                    "to": watcher.email
                })
    for mail in mails:
        send_mail(
            "科创板新股材料自动监测",
            mail.get("message"),
            mail.get("to")
        )


if __name__ == "__main__":
    get_all_info()
    dowload_pdf_and_convert()
    check_and_notify()
    browser.quit()
