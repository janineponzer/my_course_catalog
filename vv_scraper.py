import requests
from bs4 import BeautifulSoup
from operator import itemgetter

weekdays = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","semesterbegleitend"]

def get_title():
    title = soup.find("div", class_="modules_container").find("h1").get_text()
    return title

def get_programme_name():
    programme_name = soup.find("div", class_="modules_container").find("h2").get_text()
    return programme_name

def get_all_module_ids():
    module_ids = []
    for module in soup.select("li .module_name h3"):
        id = module.get("id")
        module_ids.append(id)
    return module_ids

def get_module_name(module_id):
    module_name = soup.find("h3", id=module_id).get_text()
    return module_name

def get_course_items(module_id):
    list_element = soup.find("h3", id=module_id).parent.parent.ul
    course_items = list_element.find_all("li")
    return course_items

def get_course_name(course_item):
    course_name = course_item.span.a.span.text
    return course_name

def get_course_number(course_item):
    module_number = course_item.span.b.text
    return module_number

def get_course_category(course_item):
    module_category = course_item.find("span", class_="category").text.strip()
    return module_category

def get_course_instructor(course_item):
    course_instructor = course_item.find("span", class_="course_instructor").text
    course_instructor = course_instructor.strip().lstrip("(").rstrip(")")
    return course_instructor

def get_course_time(course_item):
    course_time = course_item.find("span", class_="course_time").text
    course_time = course_time.lstrip().rstrip(", zusätzliche Termine siehe LV-Details")
    course_time = course_time.lstrip("Zeit: ")
    if get_course_name(course_item) == "Biochemie I - Grundlagen der Biochemie":
        course_time = "Mi 12:00-14:00"
    return course_time.split(", ")

def isWeekday(weekday):
    isWeekday = False
    if weekday in weekdays:
        isWeekday = True
    return isWeekday

def get_timetable_of(weekday):
    ids = get_all_module_ids()
    presorted_data = []
    if isWeekday(weekday):
        for id in ids:
            for item in get_course_items(id):
                dates = get_course_time(item)
                for date in dates:
                    if date[:2] == weekday[:2]
                        presorted_data.append((get_course_name(item), get_course_category(item), get_course_instructor(item), dates))
                
    sorted_data = sorted(presorted_data, key=itemgetter(3,0))

    print("\n" + weekday + ":")
    print("---\n")

    prev_course = ""
    for data in sorted_data:
        course = data[0]
        if course != prev_course:
            print(course)
            print(data[1])
            print(data[2])
            for elem in data[3]:
                if elem[:2] == weekday[:2]:
                    print(elem)
                # prev_day = day
            print("\n")
            prev_course = course

""" Add url of your programme's webpage in the course catalog here """
url = requests.get("https://www.fu-berlin.de/vv/de/modul?id=75011&sm=580670")
# url = requests.get("https://www.fu-berlin.de/vv/de/modul?id=75011&sm=528624")

soup = BeautifulSoup(url.content, 'html.parser')

for day in weekdays:
    get_timetable_of(day)
