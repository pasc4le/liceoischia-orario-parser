import camelot
import os
import json
import re

if __name__ == "__main__":
    cwd = os.getcwd()
    tmp_dir_name = 'tmp'
    classes = []
    classesSchedules = {}
    parsedClassesSchedules = {}
    days_of_the_week = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"]
    n_hour_to_string = ["8.30-9.30", "9.30-10.30", "10.30-11.30", "11.30-12.30", "12.30-13.30", "13.30-14.30"]
    n_of_hours_per_day = 6

    if not os.path.exists(tmp_dir_name):
        os.mkdir(tmp_dir_name)

    gen = input('Do you want to parse the pdf? (Y/n) ').strip().lower() == "y"
    if gen:
        document = camelot.read_pdf('orario.pdf', pages='all')
        document.export(f'./{tmp_dir_name}/orario.json', f='json')

        for filename in os.listdir(tmp_dir_name):
            teachersSchedule = json.load(open(os.path.join(cwd, tmp_dir_name, filename), 'r'))
            for teacher in teachersSchedule:
                teacherSchedule = list(teacher.values())
                if teacherSchedule[0] == "Docente" or teacherSchedule[0] == "": continue
                for i in range(0, len(teacherSchedule)):
                    if re.match(r"^\d+[A-Za-z]+", teacherSchedule[i]) and teacherSchedule[i] not in classes:
                        classes.append(re.search(r"(^\d+[A-Za-z]+)", teacherSchedule[i]).group(0))
        
        json.dump(classes, open('classes.json', 'w'))
    else:
        classes = json.load(open('classes.json', 'r'))

    for schoolClass in classes:
        classesSchedules[schoolClass] = {}
        for day in days_of_the_week:
            classesSchedules[schoolClass][day] = {}
    
    
    for filename in os.listdir(tmp_dir_name):
        teachersSchedule = json.load(open(os.path.join(cwd, tmp_dir_name, filename), 'r'))
        for teacher in teachersSchedule:
            teacherSchedule = list(teacher.values())
            teacherName = teacherSchedule[0]
            if teacherName == "Docente" or teacherName == "": continue
            for i in range(1, len(teacherSchedule)):
                if not teacherSchedule[i] or re.match(r"(D|t|ischia)",teacherSchedule[i]): continue
                parsedClass = re.search(r"(^\d+[A-Za-z]+)", teacherSchedule[i]).group(0)
                classesSchedules[parsedClass][days_of_the_week[(i - 1)//n_of_hours_per_day]][i] = teacherName
    
    for schoolClass in classes:
        classSchedule = classesSchedules[schoolClass]
        tmpString = f"ORARIO CLASSE {schoolClass}"
        
        for day in days_of_the_week:
            tmpString += f"\n*{day}*\n"
            lessons = list(classSchedule[day].values())
            for i in range(0, len(lessons)):
                tmpString += f"{n_hour_to_string[i]} {lessons[i]}\n"

        parsedClassesSchedules[schoolClass] = tmpString
    
    json.dump(parsedClassesSchedules, open('parsedSchedules.json', 'w'))