# -*-coding:utf-8-*-
from werobot import WeRoBot

robot = WeRoBot(token="ye980226")



def grade(account, passwd):
    try:
        Session = requests.session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        r = Session.post("http://newjw.lixin.edu.cn/sso/login", data={"username": account, "password": passwd},
                         timeout=4, headers=headers)
        r.encoding = "utf-8"
        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/grade/course.action?_=1516950321254", headers=headers,
                        timeout=4)
        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/grade/course!innerIndex.action?projectId=5",
                        timeout=4, headers=headers)
        bsObj = BeautifulSoup(r.text, "lxml")
        average_grade = bsObj.findAll("table")[1].findAll("tbody")[
            0].findAll("tr")[-3]
        average = u"平均分:" + u" " + average_grade.findAll("td")[-2].text + "        " + u"平均绩点" + ": " + \
                  average_grade.findAll("td")[-1].text
        bsObj = bsObj.findAll("table")[2].findAll("tbody")[0].findAll("tr")
        result = ""
        for trs in bsObj:
            course = trs.findAll("td")[2].text
            result += course + " "
            score = trs.findAll("td")[-2].text
            result += score + "\n"
        result += average + "\n"
        return result
    except requests.Timeout:
        return "连接超时"
    except Exception as e:
        return e


def get_notification():
    Session = requests.session()
    r = Session.get("http://www.lixin.edu.cn/")
    r.encoding = "utf-8"
    bsObj = BeautifulSoup(r.text, "lxml")
    bsObj = bsObj.findAll("div", {"class": "xwlb_list xwlb_list1"})[0]
    bsObjs = bsObj.findAll("a")
    result = ""
    for bsObj in bsObjs:
        href = "http://www.lixin.edu.cn/" + bsObj["href"]
        result += bsObj["title"] + " " + href + "\n"
    return result


def get_news():
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': APIKEY,
        'info': u"我想看新闻",
        'userid': 'wechat_account',
    }
    r = requests.post(apiUrl, data=data).json()
    # print  r
    rs = r.get(u"list")
    result = u""
    for r in rs:
        result += r.get(u"article") + " "
        result += u""
        result += r.get(u"detailurl")
        result += "\n"
    # result=""
    # for content in contents:
    #     result+=(content["article"]+" "+content["detailurl"]+"\n")
    return result


def card_balance(account, passwd):
    pass


def search(question):
    i = 0
    while i < 5:
        try:
            i = i + 1
            url = "https://www.baidu.com/s?wd=%s" % (question)
            headers = {"Host": "sp0.baidu.com",
                       "Cookie": "BDUSS=sxfjBQZ2RDbjFjQ25NYU5VajVjc35QR21WVjhSSlc5RS1reXNBUkljSnoxM1phQVFBQUFBJCQAAAAAAAAAAAEAAAD5cRGevsbX7cjLsrvX1NftAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHNKT1pzSk9aQW; BAIDUID=3F50035AAA689B4F646729842B13E216:FG=1; BIDUPSID=9F12AB144CF4A5003F269F5A2545A028; PSTM=1515328250; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1430_21126_17001_20719; PSINO=7",
                       "Cache-Control": "no-cache", "Accept": "*/*",
                       "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                       "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
                       "Pragma": "no-cache", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
            r = requests.get(url, headers=headers)
            r.encoding = "utf-8"
            bsObj = BeautifulSoup(r.text, "lxml")
            bsObjs = bsObj.findAll("div", {"id": "content_left"})[
                0].findAll("a")
            i = 0
            result = ""
            for bsObj in bsObjs:
                try:
                    if question.encode("utf-8") in bsObj.text.encode("utf-8"):
                        result += bsObj.text + " " + bsObj["href"] + "\n"
                        i = i + 1
                    if i >= 10:
                        break
                except Exception as e:
                    continue
            return result
        except Exception as e:
            continue
    else:
        return "服务器繁忙"


def qryPower(room):
    floor = room[-6:-4]
    floor = floor.lstrip("0")
    if floor == "1":
        floor = "111"
    r = requests.get("http://192.168.134.%s/find.cgi?textfield=%s&Submit=%s" %
                     (floor, room, "%CC%E1%BD%BB"))
    r.encoding = "gb2312"
    result = ""
    for content in r.text.split("\n")[1:3]:
        result += content + "\n"
    return result


def get_exam_arrangement(account, password, semester_id):
    try:
        Session = requests.session()
        cookies = {}
        r = Session.post("http://newjw.lixin.edu.cn/sso/login", data={"username": account, "password": password},
                         allow_redirects=False, timeout=3)
        cookies["URP_SID"] = r.headers['set-cookie'].split(";")[
            0].split("=")[1]
        r = Session.get(
            "http://newjw.lixin.edu.cn/sso/login/success", cookies=cookies, timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/home/",
                        cookies=cookies, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/exam/", cookies=cookies, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/sso/login?service=http://newjw.lixin.edu.cn/webapp/std/edu/exam/home.action",
            cookies=cookies, allow_redirects=False, timeout=3)
        url = r.headers["location"]
        r = Session.get(url, cookies=cookies)
        headers = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Accept": "text/html, */*; q=0.01",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Host": "newjw.lixin.edu.cn", "Pragma": "no-cache", "Cache-Control": "no-cache",
                   "X-Requested-With": "XMLHttpRequest"}
        cookies["JESSIONID"] = r.cookies["JSESSIONID"]
        cookies["URP_EDU"] = "{\"projectId\":5,\"semesterId\":%s}" % semester_id
        shijianchuo = int(time.time() * 1000)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/exam/home!submenus.action?menu.id=39&menu.title=我的考试",
            cookies=cookies, headers=headers, timeout=3)
        headers = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Accept": "text/html, */*; q=0.01",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Host": "newjw.lixin.edu.cn", "Pragma": "no-cache", "Cache-Control": "no-cache",
                   "Upgrade-Insecure-Requests": "1"}
        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/exam/home!welcome.action?_=%d" % (shijianchuo + 1),
                        cookies=cookies, headers=headers, timeout=3)

        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/exam/static/scripts/my97/My97DatePicker.htm",
                        cookies=cookies, timeout=3)

        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/exam/home!childmenus.action?menu.id=441&_=%d" % (
                shijianchuo + 2),
            cookies=cookies, timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/exam/stdExamTable.action?_=%d" % (shijianchuo + 3),
                        cookies=cookies, allow_redirects=False, timeout=3)

        url = r.headers["location"]
        r = Session.get("http://newjw.lixin.edu.cn" +
                        url, cookies=cookies, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/exam/stdExamTable!examTable.action?semester.id=%s&examType.id=1&_=%d" % (
                semester_id, shijianchuo + 4), cookies=cookies, timeout=3)
        bsObj = BeautifulSoup(r.text, "lxml")
        bsObj = bsObj.findAll("table")[-1]
        trs = bsObj.findAll("tr")[1:]
        result = ""

        def transpose(x):
            x = re.sub("&nbsp", "", x.text.strip())
            return x + " "

        for tr in trs:
            temp = ""
            temp += " ".join(map(transpose, tr.findAll("td")[1:]))
            if "[考试情况尚未发布]" in temp:
                continue
            result += temp + '\n'
    except requests.Timeout:
        return "timeout"
    if result == "":
        return "目前还没有考试安排"
    return result


@robot.text
def echo(message):
    semester_id = "1640420182"
    if datetime.datetime.now() > datetime.datetime.strptime("2019-07-09", "%Y-%m-%d"):
        semester_id = "1640420191"
    compile1 = re.compile(
        "bind.*?(2016[0-9]{3}[0-9A-Z][0-9]{2}|17[0-9]{7}|15[0-9]{8}|14[0-9]{8}|18[0-9]{7}).*?([0-9a-zA-Z]{6,20})")
    m = compile1.match(message.content)
    wechat_id = message.source
    compile2 = re.compile("search(.*)")
    seek = compile2.match(message.content)
    if seek:
        question = seek.group(1).strip()
        return search(question)
    if message.content==u"重启":
        os.system('start /b python "C:\\Users\\Administrator\\Desktop\\wechat_connector\\lixinvpn\\lixinvpn.py" &exit')
    if message.content == u"绑定":
        return "请输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"
    if m:
        if not os.path.exists("stu_info.json"):
            stu_info = {"basic": {"account": "basic", "passwd": "basic"}}
            fp = open("stu_info.json", "w")
            json.dump(stu_info, fp)
        with open("stu_info.json", "r") as f:
            stu_info = json.load(f)
            account = m.group(1)
            passwd = m.group(2)
            stu_info[wechat_id] = {"account": account, "passwd": passwd}
        with open("stu_info.json", "w") as f:
            json.dump(stu_info, f)
        return "绑定成功"
        # try:
        # gevent.joinall([
        #     gevent.spawn(grade, (account,passwd)),
        # ])
        # if  os.path.exists("1.txt"):
        #     with open("1.txt") as f:
        #         result=f.read()
    if message.content == u"搜索":
        return "请输入search+空格+关键字"
    if re.search("[r|R]oom(.*?)", message.content):
        if re.search("[r|R]oom(.*?)(\d{5,6})", message.content):
            room = re.search(
                "[r|R]oom(.*?)(\d{5,6})", message.content).group(2)
            return qryPower(room)
        else:
            return "请输入room+楼号+房号,中间没有空格"
    if "成绩" in message.content:
        try:
            with open("stu_info.json", "r") as f:
                stu_info = json.load(f)
                info = stu_info[wechat_id]
                account = info.get(u'account')
                passwd = info.get(u'passwd')
            return grade(account, passwd)
        except Exception as e:
            return "请绑定正确的账号密码，输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"
    if message.content == u"通知":
        result = get_notification()
        return result
    if message.content == u"帮助":
        return "输入以下关键字:\n    绑定、成绩、搜索、通知、考试安排、课表、查电费"
    if "电费" in message.content or "电量" in message.content:
        return "输入room+楼号+房号,例如:room 011001"
    if message.content == u"全部课表":
        try:
            with open("stu_info.json", "r") as f:
                stu_info = json.load(f)
                info = stu_info[wechat_id]
                account = info.get(u'account')
                passwd = info.get(u'passwd')
            return whole_course(account, passwd, semester_id)
        except Exception as e:
            return "请绑定正确的账号密码，输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"
    if message.content == u"课表":
        try:
            with open("stu_info.json", "r") as f:
                stu_info = json.load(f)
                info = stu_info[wechat_id]
                account = info.get(u'account')
                passwd = info.get(u'passwd')
            return get_nextCourse(account, passwd, semester_id)
        except Exception as e:
            return "请绑定正确的账号密码，输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"

    if message.content == u"考试安排":
        try:
            with open("stu_info.json", "r") as f:
                stu_info = json.load(f)
                info = stu_info[wechat_id]
                account = info.get(u'account')
                passwd = info.get(u'passwd')
            return get_exam_arrangement(account, passwd, semester_id)
        except Exception as e:
            return "请绑定正确的账号密码，输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"
    if message.content == u"空教室":
        try:
            with open("stu_info.json", "r") as f:
                stu_info = json.load(f)
                info = stu_info[wechat_id]
                account = info.get(u'account')
                passwd = info.get(u'passwd')
            return get_free_list(account, passwd, semester_id)
        except Exception as e:
            return "请绑定正确的账号密码，输入'bind'+账号密码（例：bind：201612xxxx xxxxxx）"

    # if message.content==u"一开通余额":
    #     with open("stu_info.json", "r") as f:
    #         stu_info = json.load(f, "ascii")
    #         info = stu_info[wechat_id]
    #         account = info.get(u'account')
    #         passwd = info.get(u'passwd')
    #         result=card_balance(account,passwd)
    #     return result
    return get_response(message.content)


@robot.subscribe
def account_subcribe():
    return """欢迎关注立信2016级会计9班的公众号♪٩(´ω`)و♪    

世界这么大，我们相遇在九班。属于大学的这段路，让我们一起走。

在接下来的日子里，公众号将会努力成为大家在大学生活中的小帮手。这里将定期分享属于9班的点点滴滴，提供学习上的各种干货，链接学校多个网址…力求做一个贴心的班级公众号~

可以通过输入“帮助”获取关键字信息，每个关键字都有相应的功能，当然，还有很多功能有待开发哦！欢迎每一个关注者在后台留言，小编会努力做到更好！让我们一起期待9班的成长哟~"""


url = "http://www.tuling123.com/openapi/api"
APIKEY = "dbafb0a6c63f42c88440842716fb9d69"


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': APIKEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


def merge_week(strs):
    results = ""
    length = len(strs)
    if length == 1:
        return strs[0]
    else:
        i = 1
        while i < length:
            start = strs[0]
            d0 = float(strs[1]) - float(start)
            end = strs[i]
            d = (int(end) - int(start)) / float(i)
            if d == d0:
                result = strs[0] + "-" + strs[i]
                i += 1
            else:
                results += result + " "
                strs = strs[i:]
                i = 1
                length = len(strs)
                if length <= 1:
                    results += strs[0]
    if results == "":
        return result
    return results


def get_recent_weekday(current_day=datetime.datetime.now().strftime("%Y-%m-%d"), start_time="2018-03-05"):
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    end_time = start_time + datetime.timedelta(days=7 * 18)
    current_day = datetime.datetime.strptime(current_day, "%Y-%m-%d")
    if current_day < start_time:
        current_day = start_time
    elif current_day >= start_time and current_day <= end_time:
        while current_day.weekday() + 1 in [6, 7]:
            current_day = current_day + datetime.timedelta(days=1)
    else:
        return u"联系管理员修改信息", u""
    start_time = start_time.strftime("%Y-%m-%d")
    current_day = current_day.strftime("%Y-%m-%d")
    week, weekday = current_week(start_time, current_day)
    return week, weekday


def get_nextCourse(account, password, semester_id):
    try:
        Session = requests.session()
        r = Session.post("http://newjw.lixin.edu.cn/sso/login", data={"username": account, "password": password},
                         timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/home/", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/home.action", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!innerIndex.action?x-requested-with=1&projectId=5",
            timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/static/scripts/semesterCalendar.js?s2j=3.6.1",
            timeout=3)
        headers = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Host": "newjw.lixin.edu.cn", "Accept-Encoding": "gzip, deflate",
                   "Referer": "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!courseTable.action",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
                   "Accept": "*/*", "X-Requested-With": "XMLHttpRequest",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {"setting.kind": "std", "weekSpan": "1-18",
                "semester.id": semester_id, "ids": "319284"}
        r = Session.post("http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!courseTable.action", data=data,
                         headers=headers, timeout=3)

        r.encoding = "utf-8"
        bsObj = BeautifulSoup(r.text, "lxml")

        compiler = re.compile(
            "activity = table0\.newActivity\(\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",(.*?)\)(.|\n)*?([0-9]),([0-9]{3,4}),([0-9]{4})\)\;")
        bsObj = str(bsObj)
        informations = compiler.findall(bsObj)
        end = re.search(
            "CourseTable\('([0-9]{4}-[0-9]{2}-[0-9]{2})'.*?", bsObj).group(1)
        start_time = end
        current_day = datetime.datetime.now().strftime("%Y-%m-%d")
        week, recent_weekday = get_recent_weekday(
            start_time=start_time, current_day=current_day)

        if week + recent_weekday == u"联系管理员修改信息":
            return week + recent_weekday
        weekdays = []
        courses = []
        times = []
        locations = []
        end_times = []
        # occupy_weeks=[]
        bool_occupy_weeks = []
        for information in informations:
            start_time = information[-2]
            start_time = start_time.rjust(4, "0")
            # print(start_time)
            end_time = information[-1]
            start_time = start_time[:2] + ":" + start_time[2:]
            end_time = end_time[:2] + ":" + end_time[2:]
            course = information[1] + " " + information[3]
            location = information[5]
            begin = information[6]
            weekstate = int(information[7])
            weekday = information[9]
            occupy_week, _, _ = get_weeks(begin, end, weekstate)
            bool_occupy_weeks.append(week in occupy_week)
            end_times.append(end_time)
            times.append(start_time + "-" + end_time)
            courses.append(course)
            locations.append(location)
            weekdays.append(weekday)

        result = ""
        infos = []

        while result == "":
            for i in range(len(bool_occupy_weeks)):
                if bool_occupy_weeks[i]:
                    if weekdays[i] == recent_weekday:
                        infos.append([courses[i], locations[i],
                                      times[i], end_times[i]])
            infos.sort(key=lambda x: x[-1])

            for course, location, time, _ in infos:
                result += course + " " + location + " " + time + "\n"
            recent_weekday = str(int(recent_weekday) + 1)
            if recent_weekday >= "7":
                return "本周无课"
        result = "第%s周 %s\n" % (week, int_to_weekday[
            str(int(recent_weekday)-1)])+result
        return result
    except requests.Timeout:
        return "连接超时"
    except Exception as e:
        return e



# print(merge_week(["1","2","3","4","5","6","7",'8','9','10','11','12','13','15']))
def get_weeks(begin, end, week_number):
    begin2 = datetime.datetime.strptime(begin, "%Y-%m-%d")
    end2 = datetime.datetime.strptime(end, "%Y-%m-%d")
    while (begin2.weekday() + 1 != 1):
        begin2 = begin2 - datetime.timedelta(days=1)
    while (end2.weekday() + 1 != 1):
        end2 = end2 - datetime.timedelta(days=1)
    weekstate1 = datetime.datetime.strptime(
        begin, "%Y-%m-%d") - datetime.datetime.strptime(end, "%Y-%m-%d")
    weekstate2 = begin2 - end2
    weeks = education.convertWeekstate2ReverseString(
        week_number, weekstate2.days // 7)
    w = ""
    for k, i in enumerate(weeks):
        if i == "1":
            w += str(k) + " "
    x = w.split()
    # 第一个参数是该门课包含的周数，第二个参数是类似1-15，上课的weekday
    return x, x[0] + "-" + x[-1], (-weekstate1.days) % 7 + 1


# 返回当前的周数和weekday
def current_week(begin="2018-03-05", end=datetime.datetime.now().strftime("%Y-%m-%d")):
    begin2 = datetime.datetime.strptime(begin, "%Y-%m-%d")
    end2 = datetime.datetime.strptime(end, "%Y-%m-%d")
    while (end2.weekday() + 1 != 1):
        end2 = end2 - datetime.timedelta(days=1)
    while (begin2.weekday() + 1 != 1):
        begin2 = begin2 - datetime.timedelta(days=1)
    week = (end2 - begin2).days // 7 + 1
    if week <= 0:
        return str(1), str(datetime.datetime.strptime(begin, "%Y-%m-%d").weekday() + 1)
    else:
        return str(week), str(datetime.datetime.strptime(end, "%Y-%m-%d").weekday() + 1)


# 下个学期需要改一下semester.id1640420172，改成1640420181
def whole_course(account, password, semester_id):
    try:
        Session = requests.session()
        r = Session.post("http://newjw.lixin.edu.cn/sso/login", data={"username": account, "password": password},
                         timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/home/", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/home.action", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!innerIndex.action?x-requested-with=1&projectId=5",
            timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/webapp/std/edu/lesson/static/scripts/semesterCalendar.js?s2j=3.6.1",
                        timeout=3)
        headers = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Host": "newjw.lixin.edu.cn", "Accept-Encoding": "gzip, deflate",
                   "Referer": "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!courseTable.action",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
                   "Accept": "*/*", "X-Requested-With": "XMLHttpRequest",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {"setting.kind": "std", "weekSpan": "1-18",
                "semester.id": semester_id, "ids": "319284"}
        r = Session.post("http://newjw.lixin.edu.cn/webapp/std/edu/lesson/timetable!courseTable.action", data=data,
                         headers=headers, timeout=3)

        r.encoding = "utf-8"
        bsObj = BeautifulSoup(r.text, "lxml")

        compiler = re.compile(
            "activity = table0\.newActivity\(\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",(.*?)\)(.|\n)*?([0-9]),([0-9]{3,4}),([0-9]{4})\)\;")
        bsObj = str(bsObj)
        informations = compiler.findall(bsObj)
        end = re.search(
            "CourseTable\('([0-9]{4}-[0-9]{2}-[0-9]{2})'.*?", bsObj).group(1)
        begins = []
        weekstates = []
        weekdays = []
        courses = []
        times = []
        locations_OccupyWeeks = []
        weeks = []
        start_times = []
        for information in informations:
            start_time = information[-2]
            start_time = start_time.rjust(4, "0")
            # print(start_time)
            end_time = information[-1]
            start_time = start_time[:2] + ":" + start_time[2:]
            end_time = end_time[:2] + ":" + end_time[2:]
            course = information[1] + " " + information[3]
            location = information[5]
            begin = information[6]
            weekstate = int(information[7])
            weekday = information[9]
            occupy_week, week, _ = get_weeks(begin, end, weekstate)
            occupy_weeks = merge_week(occupy_week)
            # print(occupy_weeks)
            if start_time in start_times and course in courses:
                if weekday == weekdays[courses.index(course)]:
                    locations_OccupyWeeks[courses.index(
                        course)] += "\n" + location + " " + occupy_weeks
                    continue
            # occupy_weeks.append(occupy_week)
            weeks.append(week)
            start_times.append(start_time)
            times.append((start_time, end_time))
            courses.append(course)
            locations_OccupyWeeks.append(location + " " + occupy_weeks)
            begins.append(begin)
            weekstates.append(weekstate)
            weekdays.append(weekday)
        # 上面是拿到所有信息
        courses_info = {}
        i = 0
        for begin, location_OccupyWeek, weekday, time in zip(begins, locations_OccupyWeeks, weekdays, times):
            # print(begin,location_OccupyWeek,weekday,time)
            weekday = int_to_weekday[weekday]
            if weekday not in courses_info:
                courses_info[weekday] = {}
                courses_info[weekday][time[0]] = ""
            courses_info[weekday][time[0]] = (
                courses[i], location_OccupyWeek, time[0] + "-" + time[1])
            # print (courses_info)
            # print(courses_info)
            i += 1
            # for week in weeks:
            # print(weeks,weekday)

        result = ""
        courses_info = list(courses_info.items())
        # print(courses_info)
        courses_info.sort(key=lambda x: week_to_int[x[0]])
        result = ""
        course_info = []
        for weekday, info in courses_info:
            course_info.append((weekday, list(info.items())))
        # weekday,course_info=courses_info[0]
        # print(course_info)
        # course_info=[]
        # course_info=list(course_info)
        for info in course_info:
            info[1].sort(key=lambda x: x[0])
        # print(course_info)
        # course_info.sort(key=lambda x:x[1].keys())
        for infos in course_info:
            weekday, info = infos
            result += weekday + "\n"
            for i in info:
                for j in i[1]:
                    result += j + " "
                result += "\n"
            result += '\n'
        return result
    except requests.Timeout:
        return "connection error"
    except Exception as e:
        return e


def get_free_list(account, password, semester_id):
    try:
        Session = requests.session()
        cookies = {}
        r = Session.post("http://newjw.lixin.edu.cn/sso/login", data={"username": account, "password": password},
                         allow_redirects=False, timeout=3)
        cookies["URP_SID"] = r.headers['set-cookie'].split(";")[
            0].split("=")[1]
        r = Session.get(
            "http://newjw.lixin.edu.cn/sso/login/success", cookies=cookies, timeout=3)
        r = Session.get("http://newjw.lixin.edu.cn/home/",
                        cookies=cookies, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/edu/exam/", cookies=cookies, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/sso/login?service=http://newjw.lixin.edu.cn/webapp/std/edu/exam/home.action",
            cookies=cookies, allow_redirects=False, timeout=3)
        url = r.headers["location"]
        r = Session.get(url, cookies=cookies)

        cookies["JESSIONID"] = r.cookies["JSESSIONID"]
        cookies["URP_EDU"] = "{\"projectId\":5,\"semesterId\":%s}" % semester_id
        r = Session.get(
            "http://newjw.lixin.edu.cn/home/static/home/js/templates/toolbarTab-template.html", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/home.action", allow_redirects=False, timeout=3)
        url = r.headers["Location"]
        r = Session.get(url, allow_redirects=False, timeout=3)
        url = r.headers["Location"]
        r = Session.get(url, allow_redirects=False, timeout=3)
        cookies.update(dict(r.cookies))
        school_id = cookies["school_id"]
        build_id_base = school_id + "10"

        timestamp = int(time.time()*1000)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/home!submenus.action?menu.id=35&menu.title=学生教室申请和查询&_=%d" % timestamp, timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/home!welcome.action?_=%d" % (timestamp+1), timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/static/scripts/my97/My97DatePicker.htm", timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/home!childmenus.action?menu.id=413&_=%d" % (timestamp + 2), timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/apply/index.action?_=%d" % (timestamp + 3), timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/static/scripts/itemSelect.js?_=%d" % (timestamp + 4), timeout=3)
        r = Session.get(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/apply/index!search.action?_=%d" % (timestamp + 5), timeout=3)
        # print(r.text)
        #print(cookies)
        result = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0)",
                   "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {"beginAt": datetime.datetime.now().strftime("%H:%M"), "cycleTime.beginOn": datetime.datetime.now().strftime("%Y-%m-%d"), "cycleTime.cycleCount": "1", "cycleTime.cycleType": "1", "cycleTime.endOn": datetime.datetime.now(
        ).strftime("%Y-%m-%d"), "endAt": "23:00", "room.campus.id": "6", "room.name": "", "room.roomType.id": "111", "roomApplyTimeType": "1"}
        r = Session.post(
            "http://newjw.lixin.edu.cn/webapp/std/lg/room/apply/free!search.action", data=data, headers=headers, timeout=3)
        bsObj = BeautifulSoup(r.text, "lxml")
        nodes = bsObj.find_all("tbody")[0]
        trs = nodes.find_all("tr")
        result = ""
        for node in trs:
            tds = node.find_all("td")
            number = tds[0].text
            room_id = tds[1].text
            build_id = tds[2].text
            result += " ".join([number, room_id, build_id])+"\n"
        return result
    except requests.Timeout:
        return "connection error"
    except Exception as e:
        return e


robot.run("auto", port=8000)
