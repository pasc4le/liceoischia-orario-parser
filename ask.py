import json

if __name__ == "__main__":
    schedules = json.load(open('parsedSchedules.json', 'r'))

    className = input('Insert your class: (eg. 5AO) ').strip().upper()

    if className in list(schedules.keys()):
        print(schedules[className])