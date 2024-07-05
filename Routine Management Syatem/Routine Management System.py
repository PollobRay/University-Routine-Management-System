import os

from fpdf import FPDF
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import csv


from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker, MDTimePicker

class Notification(MDDialog):
    pass
class FileManage:
    def saveToFile(self, ls, path):
        with open('File\\Routine\\' + path + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7]])
            writer.writerow([ls[8], ls[9], ls[10], ls[11], ls[12], ls[13], ls[14], ls[15]])
            writer.writerow([ls[16], ls[17], ls[18], ls[19], ls[20], ls[21], ls[22], ls[23]])
            writer.writerow([ls[24], ls[25], ls[26], ls[27], ls[28], ls[29], ls[30], ls[31]])
            writer.writerow([ls[32], ls[33], ls[34], ls[35], ls[36], ls[37], ls[38], ls[39]])

    def restoreFromFile(self,fileN, path):
        ls = []
        with open('File\\'+fileN+'\\' + path + ".csv", 'r') as file:
            reader = csv.reader(file, skipinitialspace=True)

            for row in reader:
                for cell in row:
                    ls.append(cell)

        return ls


# CourseCoordinator panel
class CourseCoordinator(Screen):
    pass


class SelectInformationStd(Screen):
    pass


class MakeRutineWindow(Screen):
    path = ''  # from where save
    numberOfLines = 0
    courseName = ''
    courseCode = ''
    Lab = False
    teacher1 = ''  # teacher
    period = 1  # if lab then more than 1
    room = ''  # room no
    isFilled = False

    # popup values
    roomList = []
    teacherList = []
    def getTeacherList(self):
        ls = os.listdir('File\\Teacher')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.teacherList:
                self.teacherList.append(tchr)

        return self.teacherList

    def getRoomList(self):
        ls = os.listdir('File\\Class Room')
        for l in ls:
            rm = l.split('.csv')[0]
            if not rm in self.roomList:
                self.roomList.append(rm)

        return self.roomList


    def set_class_window(self, iids, name,dayT,timeT):
        showp = self.get_content(self, iids, name,dayT,timeT)
        showp.open()

    def set_class(self, iids, name,dayT,timeT):

        self.numberOfLines = iids.text.count('\n') + 1  # count lines

        # set properties
        self.isFilled = False
        self.courseCode = ''  # getting course code
        self.courseName = ''  # getting course name
        self.teacher1 = ''  # course Teacher
        self.teacher2 = ''  # course Teacher 2
        self.room = ''  # room no
        self.lab = False

        if self.numberOfLines == 5:  ########
            self.isFilled = True
            lines = iids.text.splitlines()
            self.courseCode = lines[0]  # getting course code
            self.courseName = lines[1]  # getting course name
            self.teacher1 = lines[2]  # course Teacher
            self.teacher2 = lines[3]
            self.room = lines[4]  # room no

        elif self.numberOfLines == 6:
            self.isFilled = True
            lines = iids.text.splitlines()
            self.lab = True
            self.courseCode = lines[1]  # getting course code
            self.courseName = lines[2]  # getting course name
            self.teacher1 = lines[3]  # course Teacher
            self.teacher2 = lines[4]  # course Teacher
            self.room = lines[5]  # room no

        # opening popup window
        self.set_class_window(iids, name,dayT,timeT)

    def get_content(self, obj, iids, name,dayT,timeT):
        class PopWidget(Popup):

            # return properties of Base class or a input box
            def getCourseName(self):
                return obj.courseName

            def getCourseCode(self):
                return obj.courseCode

            def getTeacherName1(self):
                if obj.teacher1 == '':
                    return '<select>'
                return obj.teacher1

            def getTeacherName2(self):
                if obj.teacher2 == '':
                    return '<select>'
                return obj.teacher2

            def getRoomNo(self):
                if obj.room == '':
                    return '<select>'
                return obj.room

            def getRoomList(self):
                return obj.getRoomList()

            def getTeacherList(self):
                return obj.getTeacherList()

            def isLab(self):
                return obj.lab

            #start
            days = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4}  # indicate row number on csv file
            time = {"08:00 - 08:30 Am": 0, "08:30 - 09:30 Am": 1, "09:30 - 10:30 Am": 2, "10:45 - 11:45 Am": 3, "11:45 - 12:45 Pm": 4, "01:45 -02:45 Pm": 5, "02:45 - 03:45 Pm": 6, "03:45 - 04:30 Pm": 7}  # class time indicate column number on csv file
            # end

            ## selection Code
            def isAvailable(self,path, fileName, day, classTime): #path can be teacher or room folder name & fileName can be file name
                daySerialNo = int(self.days[day])  # row no
                classTimeNo = int(self.time[classTime])  # column no

                cellValue = ""
                if not os.path.exists("File\\"+path+'\\'+ fileName + ".csv"):
                    return False

                with open("File\\"+path+'\\'+ fileName + ".csv", 'r') as file:
                    reader = csv.reader(file)
                    i = 0
                    for row in reader:  # store a row
                        cellValue = row[classTimeNo]  # store a cell
                        if i == daySerialNo:
                            break
                        i = i + 1

                if cellValue == 'Free':
                    return True
                else:
                    return False
                # end function

            def select(self,path, fileN, day, classTime,dtl,course,room):
                if not os.path.exists("File\\"+path+'\\'+ fileN + ".csv"):
                    return False

                if not self.isAvailable(path,fileN, day, classTime):
                    return False

                else:
                    daySerialNo = int(self.days[day])  # row no
                    clsTime = int (self.time[classTime])

                    filename ="File\\"+path+'\\'+ fileN + ".csv"

                    # updating the column value/data
                    if path == 'Class Room':
                        value = 'CSE' + ' ' +dtl+'\n'+course+'\n'+fileN  # updating a cell, first is row no second is column name
                    else:
                        value  = 'CSE' + ' ' + dtl+'\n'+course+'\n'+room  # updating a cell, first is row no second is column name

                    data = []
                    inFile = open(filename,'r')
                    reader = csv.reader(inFile)

                    for row in reader:
                        data.append(row)
                    inFile.close()
                    data[daySerialNo][clsTime] = value

                    outFile = open(filename,'w', newline='')
                    writer = csv.writer(outFile)
                    for i in range(5):
                        writer.writerow(data[i])
                    outFile.close()

                    return True

                '''def freeSchedule(self,path, fileN, day, classTime):

                daySerialNo = int(self.days[day])  # row no
                clsTime = int(self.time[classTime])

                filename = "File\\" + path + '\\' + fileN + ".csv"
                data = []
                inFile = open(filename, 'r')
                reader = csv.reader(inFile)

                for row in reader:
                    data.append(row)
                inFile.close()
                data[daySerialNo][clsTime] = 'Free'

                outFile = open(filename, 'w',newline='')
                writer = csv.writer(outFile)
                for i in range(5):
                    writer.writerow(data[i])
                outFile.close()'''

            def spinnerEvent1(self):
                teacher1 = str(self.ids.teachers1.text)

                #if theacher changed
                #if (self.getTeacherName1() != '<select>' and self.getTeacherName1() != '') and self.getTeacherName1() != teacher1:
                 #   self.freeSchedule('Teacher',teacher1,dayT,timeT)
                    #teacher changed
                if not self.isAvailable('Teacher',teacher1,dayT,timeT):
                    note = Notification()
                    note.title = 'Alert'
                    note.text = teacher1 + ' is busy on that time'
                    note.open()
                    self.ids.sdlBtn.disabled = True
                else:
                    self.ids.sdlBtn.disabled = False

            def spinnerEvent2(self):
                teacher2 = self.ids.teachers2.text
                #if theacher changed

               # if (self.ids.Select.active and self.getTeacherName2()!='<select>' and self.getTeacherName2()!=' - ') and self.getTeacherName2()!=teacher2:
                  #  self.freeSchedule('Teacher', teacher2, dayT, timeT)
                    #teacher name

                if self.ids.Select.active:
                    if not self.isAvailable('Teacher',teacher2,dayT,timeT):
                        note = Notification()
                        note.title = 'Alert'
                        note.text = teacher2 + ' is busy on that time'
                        note.open()
                        self.ids.sdlBtn.disabled = True
                    else:
                        self.ids.sdlBtn.disabled = False

            def spinnerEvent3(self):
                room = self.ids.rooms.text
                #if theacher changed

                #if (self.getRoomNo()!='<select>' and self.getRoomNo()!='') and self.getRoomNo()!=room:
                  #  self.freeSchedule('Class Room', room, dayT, timeT)

                if not self.isAvailable('Class Room',room,dayT,timeT):
                    note = Notification()
                    note.title = 'Alert'
                    note.text = room + ' is busy on that time'
                    note.open()
                    self.ids.sdlBtn.disabled = True
                else:
                    self.ids.sdlBtn.disabled = False


            def press_btn(self): #schedule
                # print(self.ids.inputT.text)  # access class memeber
                # obj.ids.superlabel.text = self.ids.inputT.text  # access outerclass member

                if self.ids.Select.active:
                    teacher1 = self.ids.teachers1.text
                    teacher2 = self.ids.teachers2.text
                    room = self.ids.rooms.text
                    if self.ids.courseCode.text != '' or self.ids.courseName.text != '' or teacher1 != '<select>' or room != '<select>':
                        if teacher1 == '<select>':
                            teacher1 = ' '
                        if teacher2 == '<select>':
                            teacher2 = ' '
                        if room == '<select>':
                            room = ' '

                        txt = str('Lab' + '\n' + self.ids.courseCode.text + '\n' + self.ids.courseName.text + '\n' + teacher1 + '\n' + teacher2 + '\n' + room)
                        iids.text = txt
                    else: # fill detail
                        note = Notification()
                        note.title = "Fill information"
                        note.open()

                    self.select('Teacher', teacher2, dayT, timeT, obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                    # first lab
                    if name == 'sun1':  # diabled other with same lab
                        obj.ids.sun2.disabled = True
                        obj.ids.sun2.text = txt
                        obj.ids.sun3.disabled = True
                        obj.ids.sun3.text = txt

                        self.select('Teacher', teacher1, 'sunday','08:30 - 09:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday','08:30 - 09:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'sunday','09:30 - 10:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday','09:30 - 10:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '09:30 - 10:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'mon1':  # diabled other with same lab
                        obj.ids.mon2.disabled = True
                        obj.ids.mon3.disabled = True
                        obj.ids.mon2.text = txt
                        obj.ids.mon3.text = txt
                        self.select('Teacher', teacher1, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tue1':  # diabled other with same lab
                        obj.ids.tue2.disabled = True
                        obj.ids.tue3.disabled = True
                        obj.ids.tue2.text = txt
                        obj.ids.tue3.text = txt
                        self.select('Teacher', teacher1, 'tuesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '08:30 - 09:30 Am', obj.path,self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'wed1':  # diabled other with same lab
                        obj.ids.wed2.disabled = True
                        obj.ids.wed3.disabled = True
                        obj.ids.wed2.text = txt
                        obj.ids.wed3.text = txt
                        self.select('Teacher', teacher1, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tues1':  # diabled other with same lab
                        obj.ids.tues2.disabled = True
                        obj.ids.tues3.disabled = True
                        obj.ids.tues2.text = txt
                        obj.ids.tues3.text = txt
                        self.select('Teacher', teacher1, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    # after launch lab
                    if name == 'sun6':  # diabled other with same lab
                        obj.ids.sun7.disabled = True
                        obj.ids.sun8.disabled = True
                        obj.ids.sun7.text = txt
                        obj.ids.sun8.text = txt
                        self.select('Teacher', teacher1, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'mon6':  # diabled other with same lab
                        obj.ids.mon7.disabled = True
                        obj.ids.mon8.disabled = True
                        obj.ids.mon7.text = txt
                        obj.ids.mon8.text = txt
                        self.select('Teacher', teacher1, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tue6':  # diabled other with same lab
                        obj.ids.tue7.disabled = True
                        obj.ids.tue8.disabled = True
                        obj.ids.tue7.text = txt
                        obj.ids.tue8.text = txt
                        self.select('Teacher', teacher1, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'wed6':  # diabled other with same lab
                        obj.ids.wed7.disabled = True
                        obj.ids.wed8.disabled = True
                        obj.ids.wed7.text = txt
                        obj.ids.wed8.text = txt
                        self.select('Teacher', teacher1, 'wednesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tues6':  # diabled other with same lab
                        obj.ids.tues7.disabled = True
                        obj.ids.tues8.disabled = True
                        obj.ids.tues7.text = txt
                        obj.ids.tues8.text = txt
                        self.select('Teacher', teacher1, 'thursday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'thursday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)



                else:
                    # deselect
                    # first lab
                    if name == 'sun1':  # diabled other with same lab
                        obj.ids.sun2.disabled = False
                        obj.ids.sun3.disabled = False
                        obj.ids.sun2.text = ""
                        obj.ids.sun3.text = ""
                    if name == 'mon1':  # diabled other with same lab
                        obj.ids.mon2.disabled = False
                        obj.ids.mon3.disabled = False
                        obj.ids.mon2.text = ""
                        obj.ids.mon3.text = ""
                    if name == 'tue1':  # diabled other with same lab
                        obj.ids.tue2.disabled = False
                        obj.ids.tue3.disabled = False
                        obj.ids.tue2.text = ""
                        obj.ids.tue3.text = ""
                    if name == 'wed1':  # diabled other with same lab
                        obj.ids.wed2.disabled = False
                        obj.ids.wed3.disabled = False
                        obj.ids.wed2.text = ""
                        obj.ids.wed3.text = ""
                    if name == 'tues1':  # diabled other with same lab
                        obj.ids.tues2.disabled = False
                        obj.ids.tues3.disabled = False
                        obj.ids.tues2.text = ""
                        obj.ids.tues3.text = ""

                    # after launch lab
                    if name == 'sun6':  # diabled other with same lab
                        obj.ids.sun7.disabled = False
                        obj.ids.sun8.disabled = False
                        obj.ids.sun7.text = ""
                        obj.ids.sun8.text = ""
                    if name == 'mon6':  # diabled other with same lab
                        obj.ids.mon7.disabled = False
                        obj.ids.mon8.disabled = False
                        obj.ids.mon7.text = ""
                        obj.ids.mon8.text = ""
                    if name == 'tue6':  # diabled other with same lab
                        obj.ids.tue7.disabled = False
                        obj.ids.tue8.disabled = False
                        obj.ids.tue7.text = ""
                        obj.ids.tue8.text = ""
                    if name == 'wed6':  # diabled other with same lab
                        obj.ids.wed7.disabled = False
                        obj.ids.wed8.disabled = False
                        obj.ids.wed7.text = ""
                        obj.ids.wed8.text = ""
                    if name == 'tues6':  # diabled other with same lab
                        obj.ids.tues7.disabled = False
                        obj.ids.tues8.disabled = False
                        obj.ids.tues7.text = ""
                        obj.ids.tues8.text = ""

                    teacher1 = self.ids.teachers1.text
                    teacher2 = self.ids.teachers2.text
                    room = self.ids.rooms.text
                    if self.ids.courseCode.text != '' or self.ids.courseName.text != '' or teacher1 != '<select>' or room != '<select>':
                        if teacher1 == '<select>':
                            teacher1 = ' '
                        if teacher2 == '<select>':
                            teacher2 = ' - '
                        if room == '<select>':
                            room = ' '
                        iids.text = str(self.ids.courseCode.text + '\n' + self.ids.courseName.text + '\n' + teacher1 + '\n' + teacher2 + '\n' + room)

                ########## start

                    #room changed
                ########## end
                ### check teachers and room free or not
                if teacher1!='<select>' and teacher1!='':
                    self.select('Teacher',teacher1,dayT,timeT,obj.path,self.ids.courseCode.text+' '+self.ids.courseName.text,room)

                if self.ids.Select.active and teacher2 != '<select>' and teacher2 != ' - ':
                    self.select('Teacher',teacher2,dayT,timeT,obj.path,self.ids.courseCode.text+' '+self.ids.courseName.text,room)

                if room!='<select>' and room!='':
                    self.select('Class Room',room,dayT,timeT,obj.path,self.ids.courseCode.text+' '+self.ids.courseName.text,room)
                ### end

        return PopWidget()

    # save button
    cellValue = []
    file = FileManage()

    def saveButtonEvent(self):
        # sunday
        self.cellValue.append(self.ids.sun1.text)
        self.cellValue.append(self.ids.sun2.text)
        self.cellValue.append(self.ids.sun3.text)
        self.cellValue.append(self.ids.sun4.text)
        self.cellValue.append(self.ids.sun5.text)
        self.cellValue.append(self.ids.sun6.text)
        self.cellValue.append(self.ids.sun7.text)
        self.cellValue.append(self.ids.sun8.text)

        # monday
        self.cellValue.append(self.ids.mon1.text)
        self.cellValue.append(self.ids.mon2.text)
        self.cellValue.append(self.ids.mon3.text)
        self.cellValue.append(self.ids.mon4.text)
        self.cellValue.append(self.ids.mon5.text)
        self.cellValue.append(self.ids.mon6.text)
        self.cellValue.append(self.ids.mon7.text)
        self.cellValue.append(self.ids.mon8.text)

        # tuesday
        self.cellValue.append(self.ids.tue1.text)
        self.cellValue.append(self.ids.tue2.text)
        self.cellValue.append(self.ids.tue3.text)
        self.cellValue.append(self.ids.tue4.text)
        self.cellValue.append(self.ids.tue5.text)
        self.cellValue.append(self.ids.tue6.text)
        self.cellValue.append(self.ids.tue7.text)
        self.cellValue.append(self.ids.tue8.text)

        # wednesday
        self.cellValue.append(self.ids.wed1.text)
        self.cellValue.append(self.ids.wed2.text)
        self.cellValue.append(self.ids.wed3.text)
        self.cellValue.append(self.ids.wed4.text)
        self.cellValue.append(self.ids.wed5.text)
        self.cellValue.append(self.ids.wed6.text)
        self.cellValue.append(self.ids.wed7.text)
        self.cellValue.append(self.ids.wed8.text)

        # tuesday
        self.cellValue.append(self.ids.tues1.text)
        self.cellValue.append(self.ids.tues2.text)
        self.cellValue.append(self.ids.tues3.text)
        self.cellValue.append(self.ids.tues4.text)
        self.cellValue.append(self.ids.tues5.text)
        self.cellValue.append(self.ids.tues6.text)
        self.cellValue.append(self.ids.tues7.text)
        self.cellValue.append(self.ids.tues8.text)

        # save
        self.file.saveToFile(self.cellValue, self.path)

        note =Notification()
        note.title='Saved'
        note.open()

class SelectInformationStdView(Screen):
    pass


class ViewRutineWindow(Screen):
    cellValue = []
    file = FileManage()
    path = str('')

    # cellValue = file.restoreFromFile()

    def restoreValues(self, path):
        self.path = path
        if os.path.exists('File\\Routine\\' + path + '.csv'):
            self.cellValue = self.file.restoreFromFile('Routine',path)
            # sunday
            self.ids.sun11.text = self.cellValue[0]
            self.ids.sun21.text = self.cellValue[1]
            self.ids.sun31.text = self.cellValue[2]
            self.ids.sun41.text = self.cellValue[3]
            self.ids.sun51.text = self.cellValue[4]
            self.ids.sun61.text = self.cellValue[5]
            self.ids.sun71.text = self.cellValue[6]
            self.ids.sun81.text = self.cellValue[7]

            # monday
            self.ids.mon11.text = self.cellValue[8]
            self.ids.mon21.text = self.cellValue[9]
            self.ids.mon31.text = self.cellValue[10]
            self.ids.mon41.text = self.cellValue[11]
            self.ids.mon51.text = self.cellValue[12]
            self.ids.mon61.text = self.cellValue[13]
            self.ids.mon71.text = self.cellValue[14]
            self.ids.mon81.text = self.cellValue[15]

            # tuesday
            self.ids.tue11.text = self.cellValue[16]
            self.ids.tue21.text = self.cellValue[17]
            self.ids.tue31.text = self.cellValue[18]
            self.ids.tue41.text = self.cellValue[19]
            self.ids.tue51.text = self.cellValue[20]
            self.ids.tue61.text = self.cellValue[21]
            self.ids.tue71.text = self.cellValue[22]
            self.ids.tue81.text = self.cellValue[23]

            # wednesday
            self.ids.wed11.text = self.cellValue[24]
            self.ids.wed21.text = self.cellValue[25]
            self.ids.wed31.text = self.cellValue[26]
            self.ids.wed41.text = self.cellValue[27]
            self.ids.wed51.text = self.cellValue[28]
            self.ids.wed61.text = self.cellValue[29]
            self.ids.wed71.text = self.cellValue[30]
            self.ids.wed81.text = self.cellValue[31]

            # tuesday
            self.ids.tues11.text = self.cellValue[32]
            self.ids.tues21.text = self.cellValue[33]
            self.ids.tues31.text = self.cellValue[34]
            self.ids.tues41.text = self.cellValue[35]
            self.ids.tues51.text = self.cellValue[36]
            self.ids.tues61.text = self.cellValue[37]
            self.ids.tues71.text = self.cellValue[38]
            self.ids.tues81.text = self.cellValue[39]

        else:
            note = Notification()
            note.title = "The Class Routine Don't Exits"
            note.open()

    def download(self):
        detail = self.path
        day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

        pdf = FPDF('l', 'mm', 'A3')
        pdf.add_page()
        # header
        pdf.set_font('times', '', 20)
        pdf.cell(400, 16, 'DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING', 0, 0, 'C')
        pdf.ln(10)
        pdf.set_font('times', '', 20)
        pdf.cell(400, 16, 'Dhaka University of Engineering & Technology, Gazipur', 0, 0, 'C')
        pdf.ln(10)
        pdf.cell(400, 16, 'Gazipur-1707, Bangladesh', 0, 0, 'C')
        pdf.line(120, 48, 300, 48)
        pdf.image('File\\Image\\DUET.png', 80, 18, 20, 20)
        pdf.ln(20)
        pdf.set_font('times', '', 16)
        pdf.cell(400, 8, 'CLASS ROUTINE', 0, 0, 'C')
        pdf.ln(8)
        pdf.cell(400, 8, detail, 0, 0, 'C')
        pdf.ln(15)
        pdf.set_font('times', '', 10)

        # content
        # class Time
        pdf.cell(20, 10, 'Day / Time', 1, 0, 'C')  # width, height, text, broder, endline, 'align'
        pdf.cell(47, 10, '8.00 - 8.30', 1, 0, 'C')
        pdf.cell(47, 10, '8.30 - 9.30', 1, 0, 'C')
        pdf.cell(47, 10, '9.30 - 10.30', 1, 0, 'C')
        pdf.cell(2, 10, ' ', 1, 0, 'C')  # tea break
        pdf.cell(47, 10, '10.45 - 11.45', 1, 0, 'C')
        pdf.cell(47, 10, '11.45 - 12.45', 1, 0, 'C')
        pdf.cell(2, 10, ' ', 1, 0, 'C')  # launch break
        pdf.cell(47, 10, '1.45 - 2.45', 1, 0, 'C')
        pdf.cell(47, 10, '2.45 - 3.45', 1, 0, 'C')
        pdf.cell(47, 10, '3.45 - 4.30', 1, 0, 'C')
        pdf.cell(0, 10, '', 0, 1)  # dummy

        counter = 0
        for i in range(5):  # for day
            pdf.cell(20, 30, day[i], 1, 0, 'C')  # width, height, text, broder, endline, 'align'

            j = 0

            while j < 10:

                x = pdf.get_x()
                y = pdf.get_y()
                u = int(1)
                if j == 3 or j == 6:  # for tea and launch break
                    pdf.cell(2, 30, '', 1, 0, 'C')
                    j = j + 1
                    continue
                courseDtl = self.cellValue[counter].count('\n') + 1
                if courseDtl == 6:
                    pdf.multi_cell(47 * 3, 5, self.cellValue[counter], 1, 'C')
                    u = int(3)

                elif courseDtl == 5:
                    pdf.multi_cell(47, 6, self.cellValue[counter], 1, 'C')

                else:
                    pdf.cell(47, 30, ' - ', 1, 0, 'C')
                # move to position
                pdf.set_xy(x + 47 * u, y)  # 20 for day + 10 for left margin width
                j = j + u
                counter = counter + u

            pdf.cell(0, 30, '', 0, 1)  # for line break

        pdf.ln(29)

        # signature line of course coordinator sir & head sir
        pdf.set_font('times', '', 15)
        y = pdf.get_y()
        dotLine = '------------------------------'
        courseC = 'Course Coordinator'
        head = 'Head'
        CourseCoordinatorSir = 'Dr. Md. Jakirul Islam, Assistant Professor, Dept of CSE'
        HeadSir = 'Prof. Dr. Md. Obaidur Rahman, Dept of CSE'
        pdf.set_xy(80, y)
        pdf.cell(80, 4, dotLine, 0, 0, 'C')
        pdf.set_xy(260, y)
        pdf.cell(80, 4, dotLine, 0, 0, 'C')
        pdf.ln(3)
        pdf.set_font('times', 'B', 15)
        pdf.set_xy(80, y + 3)
        pdf.cell(80, 6, courseC, 0, 0, 'C')
        pdf.set_xy(260, y + 3)
        pdf.cell(80, 6, head, 0, 0, 'C')
        pdf.ln(5)
        pdf.set_font('times', '', 15)
        pdf.set_xy(70, y + 3 + 6)
        pdf.cell(100, 6, CourseCoordinatorSir, 0, 0, 'C')
        pdf.set_xy(238, y + 3 + 6)
        pdf.cell(120, 6, HeadSir, 0, 0, 'C')

        pdf.output('File\\Pdf\\' + detail + '.pdf')

        note = Notification()
        note.title = "Save to Pdf folder"
        note.open()


class SelectInformationStdUpd(Screen):  # to update
    pass


class UpdateRoutineWindow(Screen):
    path = ''

    cellValue = []
    numberOfLines = 0
    courseName = ''
    courseCode = ''
    Lab = False
    teacher1 = ''  # teacher
    period = 1  # if lab then more than 1
    room = ''  # room no
    isFilled = False

    # popup values
    roomList = []
    teacherList =[]

    file = FileManage()

    def getTeacherList(self):
        ls = os.listdir('File\\Teacher')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.teacherList:
                self.teacherList.append(tchr)

        return self.teacherList

    def getRoomList(self):
        ls = os.listdir('File\\Class Room')
        for l in ls:
            rm = l.split('.csv')[0]
            if not rm in self.roomList:
                self.roomList.append(rm)
        return self.roomList

    def restoreValues(self, path):
        if os.path.exists('File\\Routine\\' + path + '.csv'):
            self.cellValue = self.file.restoreFromFile('Routine',path)
            # sunday
            self.ids.sun1.text = self.cellValue[0]
            self.ids.sun2.text = self.cellValue[1]
            self.ids.sun3.text = self.cellValue[2]
            self.ids.sun4.text = self.cellValue[3]
            self.ids.sun5.text = self.cellValue[4]
            self.ids.sun6.text = self.cellValue[5]
            self.ids.sun7.text = self.cellValue[6]
            self.ids.sun8.text = self.cellValue[7]

            # monday
            self.ids.mon1.text = self.cellValue[8]
            self.ids.mon2.text = self.cellValue[9]
            self.ids.mon3.text = self.cellValue[10]
            self.ids.mon4.text = self.cellValue[11]
            self.ids.mon5.text = self.cellValue[12]
            self.ids.mon6.text = self.cellValue[13]
            self.ids.mon7.text = self.cellValue[14]
            self.ids.mon8.text = self.cellValue[15]

            # tuesday
            self.ids.tue1.text = self.cellValue[16]
            self.ids.tue2.text = self.cellValue[17]
            self.ids.tue3.text = self.cellValue[18]
            self.ids.tue4.text = self.cellValue[19]
            self.ids.tue5.text = self.cellValue[20]
            self.ids.tue6.text = self.cellValue[21]
            self.ids.tue7.text = self.cellValue[22]
            self.ids.tue8.text = self.cellValue[23]

            # wednesday
            self.ids.wed1.text = self.cellValue[24]
            self.ids.wed2.text = self.cellValue[25]
            self.ids.wed3.text = self.cellValue[26]
            self.ids.wed4.text = self.cellValue[27]
            self.ids.wed5.text = self.cellValue[28]
            self.ids.wed6.text = self.cellValue[29]
            self.ids.wed7.text = self.cellValue[30]
            self.ids.wed8.text = self.cellValue[31]

            # tuesday
            self.ids.tues1.text = self.cellValue[32]
            self.ids.tues2.text = self.cellValue[33]
            self.ids.tues3.text = self.cellValue[34]
            self.ids.tues4.text = self.cellValue[35]
            self.ids.tues5.text = self.cellValue[36]
            self.ids.tues6.text = self.cellValue[37]
            self.ids.tues7.text = self.cellValue[38]
            self.ids.tues8.text = self.cellValue[39]

        else:
            note = Notification()
            note.title = "Don't Exits"
            note.open()

    def set_class_window(self, iids, name,dayT,timeT):
        showp = self.get_content(self, iids, name,dayT,timeT)
        showp.open()

    def set_class(self, iids, name,dayT,timeT):

        self.numberOfLines = iids.text.count('\n') + 1  # count lines

        # set properties
        self.isFilled = False
        self.courseCode = ''  # getting course code
        self.courseName = ''  # getting course name
        self.teacher1 = ''  # course Teacher
        self.teacher2 = ''  # course Teacher 2
        self.room = ''  # room no
        self.lab = False

        if self.numberOfLines == 5:  #######
            self.isFilled = True
            lines = iids.text.splitlines()
            self.courseCode = lines[0]  # getting course code
            self.courseName = lines[1]  # getting course name
            self.teacher1 = lines[2]  # course Teacher
            self.teacher2 = lines[3]
            self.room = lines[4]  # room no

        elif self.numberOfLines == 6:
            self.isFilled = True
            lines = iids.text.splitlines()
            self.lab = True
            self.courseCode = lines[1]  # getting course code
            self.courseName = lines[2]  # getting course name
            self.teacher1 = lines[3]  # course Teacher
            self.teacher2 = lines[4]  # course Teacher
            self.room = lines[5]  # room no

        # opening popup window
        self.set_class_window(iids, name,dayT,timeT)

    def get_content(self, obj, iids, name,dayT,timeT):
        class PopWidget(Popup):

            # return properties of Base class or a input box
            def getCourseName(self):
                return obj.courseName

            def getCourseCode(self):
                return obj.courseCode

            def getTeacherName1(self):
                if obj.teacher1 == '':
                    return '<select>'
                return obj.teacher1

            def getTeacherName2(self):
                if obj.teacher2 == '':
                    return '<select>'
                return obj.teacher2

            def getRoomNo(self):
                if obj.room == '':
                    return '<select>'
                return obj.room

            def getRoomList(self):
                return obj.getRoomList()

            def getTeacherList(self):
                return obj.getTeacherList()

            def isLab(self):
                return obj.lab

            days = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3,
                    "thursday": 4}  # indicate row number on csv file
            time = {"08:00 - 08:30 Am": 0, "08:30 - 09:30 Am": 1, "09:30 - 10:30 Am": 2, "10:45 - 11:45 Am": 3,
                    "11:45 - 12:45 Pm": 4, "01:45 -02:45 Pm": 5, "02:45 - 03:45 Pm": 6,
                    "03:45 - 04:30 Pm": 7}  # class time indicate column number on csv file

            # end

            ## selection Code
            def isAvailable(self, path, fileName, day,
                            classTime):  # path can be teacher or room folder name & fileName can be file name
                daySerialNo = int(self.days[day])  # row no
                classTimeNo = int(self.time[classTime])  # column no

                cellValue = ""
                if not os.path.exists("File\\" + path + '\\' + fileName + ".csv"):
                    return False

                with open("File\\" + path + '\\' + fileName + ".csv", 'r') as file:
                    reader = csv.reader(file)
                    i = 0
                    for row in reader:  # store a row
                        cellValue = row[classTimeNo]  # store a cell
                        if i == daySerialNo:
                            break
                        i = i + 1

                if cellValue == 'Free':
                    return True
                else:
                    return False
                # end function

            def select(self, path, fileN, day, classTime, dtl, course, room):
                if not os.path.exists("File\\" + path + '\\' + fileN + ".csv"):
                    return False

                if not self.isAvailable(path, fileN, day, classTime):
                    return False

                else:
                    daySerialNo = int(self.days[day])  # row no
                    clsTime = int(self.time[classTime])

                    filename = "File\\" + path + '\\' + fileN + ".csv"

                    # updating the column value/data
                    if path == 'Class Room':
                        value = 'CSE' + ' ' + dtl + '\n' + course + '\n' + fileN  # updating a cell, first is row no second is column name
                    else:
                        value = 'CSE' + ' ' + dtl + '\n' + course + '\n' + room  # updating a cell, first is row no second is column name

                    data = []
                    inFile = open(filename, 'r')
                    reader = csv.reader(inFile)

                    for row in reader:
                        data.append(row)
                    inFile.close()
                    data[daySerialNo][clsTime] = value

                    outFile = open(filename, 'w', newline='')
                    writer = csv.writer(outFile)
                    for i in range(5):
                        writer.writerow(data[i])
                    outFile.close()

                    return True

            def spinnerEvent1(self):
                teacher1 = str(self.ids.teachers1.text)

                #if theacher changed
                #if (self.getTeacherName1() != '<select>' and self.getTeacherName1() != '') and self.getTeacherName1() != teacher1:
                 #   self.freeSchedule('Teacher',teacher1,dayT,timeT)
                    #teacher changed
                if not self.isAvailable('Teacher',teacher1,dayT,timeT):
                    note = Notification()
                    note.title = 'Alert'
                    note.text = teacher1 + ' is busy on that time'
                    note.open()
                    self.ids.sdlBtn.disabled = True
                else:
                    self.ids.sdlBtn.disabled = False

            def spinnerEvent2(self):
                teacher2 = self.ids.teachers2.text
                #if theacher changed

               # if (self.ids.Select.active and self.getTeacherName2()!='<select>' and self.getTeacherName2()!=' - ') and self.getTeacherName2()!=teacher2:
                  #  self.freeSchedule('Teacher', teacher2, dayT, timeT)
                    #teacher name

                if self.ids.Select.active:
                    if not self.isAvailable('Teacher',teacher2,dayT,timeT):
                        note = Notification()
                        note.title = 'Alert'
                        note.text = teacher2 + ' is busy on that time'
                        note.open()
                        self.ids.sdlBtn.disabled = True
                    else:
                        self.ids.sdlBtn.disabled = False

            def spinnerEvent3(self):
                room = self.ids.rooms.text
                #if theacher changed

                #if (self.getRoomNo()!='<select>' and self.getRoomNo()!='') and self.getRoomNo()!=room:
                  #  self.freeSchedule('Class Room', room, dayT, timeT)

                if not self.isAvailable('Class Room',room,dayT,timeT):
                    note = Notification()
                    note.title = 'Alert'
                    note.text = room + ' is busy on that time'
                    note.open()
                    self.ids.sdlBtn.disabled = True
                else:
                    self.ids.sdlBtn.disabled = False


            def press_btn(self):
                # print(self.ids.inputT.text)  # access class memeber
                # obj.ids.superlabel.text = self.ids.inputT.text  # access outerclass member

                if self.ids.Select.active:
                    teacher1 = self.ids.teachers1.text
                    teacher2 = self.ids.teachers2.text
                    room = self.ids.rooms.text
                    if self.ids.courseCode.text != '' or self.ids.courseName.text != '' or teacher1 != '<select>' or room != '<select>':
                        if teacher1 == '<select>':
                            teacher1 = ' '
                        if teacher2 == '<select>':
                            teacher2 = ' '
                        if room == '<select>':
                            room = ' '

                        txt = str('Lab' + '\n' + self.ids.courseCode.text + '\n' + self.ids.courseName.text + '\n' + teacher1 + '\n' + teacher2 + '\n' + room)
                        iids.text = txt
                    # first lab
                    if name == 'sun1':  # diabled other with same lab
                        obj.ids.sun2.disabled = True
                        obj.ids.sun2.text = txt
                        obj.ids.sun3.disabled = True
                        obj.ids.sun3.text = txt
                        self.select('Teacher', teacher1, 'sunday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'sunday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'mon1':  # diabled other with same lab
                        obj.ids.mon2.disabled = True
                        obj.ids.mon3.disabled = True
                        obj.ids.mon2.text = txt
                        obj.ids.mon3.text = txt
                        self.select('Teacher', teacher1, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tue1':  # diabled other with same lab
                        obj.ids.tue2.disabled = True
                        obj.ids.tue3.disabled = True
                        obj.ids.tue2.text = txt
                        obj.ids.tue3.text = txt
                        self.select('Teacher', teacher1, 'tuesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'wed1':  # diabled other with same lab
                        obj.ids.wed2.disabled = True
                        obj.ids.wed3.disabled = True
                        obj.ids.wed2.text = txt
                        obj.ids.wed3.text = txt
                        self.select('Teacher', teacher1, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tues1':  # diabled other with same lab
                        obj.ids.tues2.disabled = True
                        obj.ids.tues3.disabled = True
                        obj.ids.tues2.text = txt
                        obj.ids.tues3.text = txt
                        self.select('Teacher', teacher1, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '08:30 - 09:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '09:30 - 10:30 Am', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    # after launch lab
                    if name == 'sun6':  # diabled other with same lab
                        obj.ids.sun7.disabled = True
                        obj.ids.sun8.disabled = True
                        obj.ids.sun7.text = txt
                        obj.ids.sun8.text = txt
                        self.select('Teacher', teacher1, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'sunday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'mon6':  # diabled other with same lab
                        obj.ids.mon7.disabled = True
                        obj.ids.mon8.disabled = True
                        obj.ids.mon7.text = txt
                        obj.ids.mon8.text = txt
                        self.select('Teacher', teacher1, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'monday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tue6':  # diabled other with same lab
                        obj.ids.tue7.disabled = True
                        obj.ids.tue8.disabled = True
                        obj.ids.tue7.text = txt
                        obj.ids.tue8.text = txt
                        self.select('Teacher', teacher1, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'tuesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'wed6':  # diabled other with same lab
                        obj.ids.wed7.disabled = True
                        obj.ids.wed8.disabled = True
                        obj.ids.wed7.text = txt
                        obj.ids.wed8.text = txt
                        self.select('Teacher', teacher1, 'wednesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '02:45 - 03:45 Pm', obj.path,  self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'wednesday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                    if name == 'tues6':  # diabled other with same lab
                        obj.ids.tues7.disabled = True
                        obj.ids.tues8.disabled = True
                        obj.ids.tues7.text = txt
                        obj.ids.tues8.text = txt
                        self.select('Teacher', teacher1, 'thursday', '02:45 - 03:45 Pm', obj.path,  self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '02:45 - 03:45 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher1, 'thursday', '03:45 - 04:30 Pm', obj.path,  self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Teacher', teacher2, 'thursday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)
                        self.select('Class Room', room, 'thursday', '03:45 - 04:30 Pm', obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                else:
                    # deselect
                    # first lab
                    if name == 'sun1':  # diabled other with same lab
                        obj.ids.sun2.disabled = False
                        obj.ids.sun3.disabled = False
                        obj.ids.sun2.text = ""
                        obj.ids.sun3.text = ""
                    if name == 'mon1':  # diabled other with same lab
                        obj.ids.mon2.disabled = False
                        obj.ids.mon3.disabled = False
                        obj.ids.mon2.text = ""
                        obj.ids.mon3.text = ""
                    if name == 'tue1':  # diabled other with same lab
                        obj.ids.tue2.disabled = False
                        obj.ids.tue3.disabled = False
                        obj.ids.tue2.text = ""
                        obj.ids.tue3.text = ""
                    if name == 'wed1':  # diabled other with same lab
                        obj.ids.wed2.disabled = False
                        obj.ids.wed3.disabled = False
                        obj.ids.wed2.text = ""
                        obj.ids.wed3.text = ""
                    if name == 'tues1':  # diabled other with same lab
                        obj.ids.tues2.disabled = False
                        obj.ids.tues3.disabled = False
                        obj.ids.tues2.text = ""
                        obj.ids.tues3.text = ""

                    # after launch lab
                    if name == 'sun6':  # diabled other with same lab
                        obj.ids.sun7.disabled = False
                        obj.ids.sun8.disabled = False
                        obj.ids.sun7.text = ""
                        obj.ids.sun8.text = ""
                    if name == 'mon6':  # diabled other with same lab
                        obj.ids.mon7.disabled = False
                        obj.ids.mon8.disabled = False
                        obj.ids.mon7.text = ""
                        obj.ids.mon8.text = ""
                    if name == 'tue6':  # diabled other with same lab
                        obj.ids.tue7.disabled = False
                        obj.ids.tue8.disabled = False
                        obj.ids.tue7.text = ""
                        obj.ids.tue8.text = ""
                    if name == 'wed6':  # diabled other with same lab
                        obj.ids.wed7.disabled = False
                        obj.ids.wed8.disabled = False
                        obj.ids.wed7.text = ""
                        obj.ids.wed8.text = ""
                    if name == 'tues6':  # diabled other with same lab
                        obj.ids.tues7.disabled = False
                        obj.ids.tues8.disabled = False
                        obj.ids.tues7.text = ""
                        obj.ids.tues8.text = ""

                    teacher1 = self.ids.teachers1.text
                    teacher2 = '-'
                    room = self.ids.rooms.text
                    if self.ids.courseCode.text != '' or self.ids.courseName.text != '' or teacher1 != '<select>' or room != '<select>':
                        if teacher1 == '<select>':
                            teacher1 = ' '
                        if room == '<select>':
                            room = ' '
                        iids.text = str(self.ids.courseCode.text + '\n' + self.ids.courseName.text + '\n' + teacher1 + '\n' + teacher2 + '\n' + room)

                if teacher1 != '<select>' and teacher1 != '':
                    self.select('Teacher', teacher1, dayT, timeT, obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                if self.ids.Select.active and teacher2 != '<select>' and teacher2 != ' - ':
                    self.select('Teacher', teacher2, dayT, timeT, obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

                if room != '<select>' and room != '':
                    self.select('Class Room', room, dayT, timeT, obj.path, self.ids.courseCode.text + ' ' + self.ids.courseName.text, room)

        return PopWidget()

    def saveButtonEvent(self):
        self.cellValue.clear()
        # sunday
        self.cellValue.append(self.ids.sun1.text)
        self.cellValue.append(self.ids.sun2.text)
        self.cellValue.append(self.ids.sun3.text)
        self.cellValue.append(self.ids.sun4.text)
        self.cellValue.append(self.ids.sun5.text)
        self.cellValue.append(self.ids.sun6.text)
        self.cellValue.append(self.ids.sun7.text)
        self.cellValue.append(self.ids.sun8.text)

        # monday
        self.cellValue.append(self.ids.mon1.text)
        self.cellValue.append(self.ids.mon2.text)
        self.cellValue.append(self.ids.mon3.text)
        self.cellValue.append(self.ids.mon4.text)
        self.cellValue.append(self.ids.mon5.text)
        self.cellValue.append(self.ids.mon6.text)
        self.cellValue.append(self.ids.mon7.text)
        self.cellValue.append(self.ids.mon8.text)

        # tuesday
        self.cellValue.append(self.ids.tue1.text)
        self.cellValue.append(self.ids.tue2.text)
        self.cellValue.append(self.ids.tue3.text)
        self.cellValue.append(self.ids.tue4.text)
        self.cellValue.append(self.ids.tue5.text)
        self.cellValue.append(self.ids.tue6.text)
        self.cellValue.append(self.ids.tue7.text)
        self.cellValue.append(self.ids.tue8.text)

        # wednesday
        self.cellValue.append(self.ids.wed1.text)
        self.cellValue.append(self.ids.wed2.text)
        self.cellValue.append(self.ids.wed3.text)
        self.cellValue.append(self.ids.wed4.text)
        self.cellValue.append(self.ids.wed5.text)
        self.cellValue.append(self.ids.wed6.text)
        self.cellValue.append(self.ids.wed7.text)
        self.cellValue.append(self.ids.wed8.text)

        # tuesday
        self.cellValue.append(self.ids.tues1.text)
        self.cellValue.append(self.ids.tues2.text)
        self.cellValue.append(self.ids.tues3.text)
        self.cellValue.append(self.ids.tues4.text)
        self.cellValue.append(self.ids.tues5.text)
        self.cellValue.append(self.ids.tues6.text)
        self.cellValue.append(self.ids.tues7.text)
        self.cellValue.append(self.ids.tues8.text)

        # save
        self.file.saveToFile(self.cellValue, self.path)
        note = Notification()
        note.title = "Updated"
        note.open()


class DeleteRoutineWindow(Screen):
    def deleteRoutine(self, year, sem, sec):
        path = str(year + ' year ' + sem + ' semester ' + sec + ' section')
        if os.path.exists('File\\Routine\\' + path + '.csv'):
            os.remove('File\\Routine\\' + path + '.csv')
            note = Notification()
            note.title = "Deleted"
            note.open()

        else:
            note = Notification()
            note.title = "Don't Exits"
            note.open()


class AddTeacher(Screen):

    def isTeacherExists(self, teacher):  # start
        return bool(os.path.exists("File\\Teacher\\" + teacher + ".csv"))
    def addTeacher(self):
        teacherName = str(self.ids.teacherName.text)
        self.ids.teacherName.text = ''
        if teacherName == '':
            note = Notification()
            note.title = "Fill Name"
            note.open()
        else:
            if self.isTeacherExists(teacherName):
                note = Notification()
                note.title = "Already added"
                note.open()

            else:
                # create a new csv file and write into it for a class room
                with open("File\\Teacher\\" + teacherName + ".csv", 'w', newline='') as file:  # newline='' for no extra newline
                    writer = csv.writer(file)  # function is used to create a writer object
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  #for sunday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  #for monday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  #for Tuesday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  #for wednesday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  #for Thursday

                    note = Notification()
                    note.title = "Added"
                    note.open()
            # end

class AddClassRoom(Screen):

    def isRoomExists(self,roomNo):  # start
        return bool(os.path.exists("File\\Class Room\\" + roomNo+ ".csv"))

    def addRoom(self):
        room = str(self.ids.roomNo.text)
        self.ids.roomNo.text =''
        if room=='':
            note = Notification()
            note.title = "Fill information\n"
            note.open()
        else:
            if self.isRoomExists(room):
                note = Notification()
                note.title = "Already added\n"
                note.open()

            else:
                # create a new csv file and write into it for a class room
                with open("File\\Class Room\\" + room+ ".csv", 'w', newline='') as file:  # newline='' for no extra newline
                    writer = csv.writer(file)  # function is used to create a writer object
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  # for sunday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  # for monday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  # for Tuesday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  # for wednesday
                    writer.writerow(["Free", "Free", "Free", "Free", "Free", "Free", "Free", "Free"])  # for Thursday

                    note = Notification()
                    note.title = "Added"
                    note.open()
            # end

class ViewTeacherScedule(Screen):
    teachers =[]
    def loadTeacherList(self):
        ls = os.listdir('File\\Teacher')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.teachers:
                self.teachers.append(tchr)

    def teacherList(self):
        ls = os.listdir('File\\Teacher')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.teachers:
                self.teachers.append(tchr)

        return self.teachers

    def view(self):
        path = str(self.ids.teacher.text)
        cellValue = []
        if os.path.exists('File\\Teacher\\' + path + '.csv'):
            file = FileManage()
            self.cellValue = file.restoreFromFile('Teacher',path)
            # sunday
            self.ids.sun11.text = self.cellValue[0]
            self.ids.sun21.text = self.cellValue[1]
            self.ids.sun31.text = self.cellValue[2]
            self.ids.sun41.text = self.cellValue[3]
            self.ids.sun51.text = self.cellValue[4]
            self.ids.sun61.text = self.cellValue[5]
            self.ids.sun71.text = self.cellValue[6]
            self.ids.sun81.text = self.cellValue[7]

            # monday
            self.ids.mon11.text = self.cellValue[8]
            self.ids.mon21.text = self.cellValue[9]
            self.ids.mon31.text = self.cellValue[10]
            self.ids.mon41.text = self.cellValue[11]
            self.ids.mon51.text = self.cellValue[12]
            self.ids.mon61.text = self.cellValue[13]
            self.ids.mon71.text = self.cellValue[14]
            self.ids.mon81.text = self.cellValue[15]

            # tuesday
            self.ids.tue11.text = self.cellValue[16]
            self.ids.tue21.text = self.cellValue[17]
            self.ids.tue31.text = self.cellValue[18]
            self.ids.tue41.text = self.cellValue[19]
            self.ids.tue51.text = self.cellValue[20]
            self.ids.tue61.text = self.cellValue[21]
            self.ids.tue71.text = self.cellValue[22]
            self.ids.tue81.text = self.cellValue[23]

            # wednesday
            self.ids.wed11.text = self.cellValue[24]
            self.ids.wed21.text = self.cellValue[25]
            self.ids.wed31.text = self.cellValue[26]
            self.ids.wed41.text = self.cellValue[27]
            self.ids.wed51.text = self.cellValue[28]
            self.ids.wed61.text = self.cellValue[29]
            self.ids.wed71.text = self.cellValue[30]
            self.ids.wed81.text = self.cellValue[31]

            # tuesday
            self.ids.tues11.text = self.cellValue[32]
            self.ids.tues21.text = self.cellValue[33]
            self.ids.tues31.text = self.cellValue[34]
            self.ids.tues41.text = self.cellValue[35]
            self.ids.tues51.text = self.cellValue[36]
            self.ids.tues61.text = self.cellValue[37]
            self.ids.tues71.text = self.cellValue[38]
            self.ids.tues81.text = self.cellValue[39]


class ViewRoomStatus(Screen):
    rooms= []

    def loadRoomList(self):
        ls = os.listdir('File\\Class Room')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.rooms:
                self.rooms.append(tchr)

    def roomList(self):
        ls = os.listdir('File\\Class Room')
        for l in ls:
            tchr = l.split('.csv')[0]
            if not tchr in self.rooms:
                self.rooms.append(tchr)
        return self.rooms

    def view(self):
        path = str(self.ids.room.text)
        cellValue = []
        if os.path.exists('File\\Class Room\\' + path + '.csv'):
            file = FileManage()
            self.cellValue = file.restoreFromFile('Class Room', path)
            # sunday
            self.ids.sun11.text = self.cellValue[0]
            self.ids.sun21.text = self.cellValue[1]
            self.ids.sun31.text = self.cellValue[2]
            self.ids.sun41.text = self.cellValue[3]
            self.ids.sun51.text = self.cellValue[4]
            self.ids.sun61.text = self.cellValue[5]
            self.ids.sun71.text = self.cellValue[6]
            self.ids.sun81.text = self.cellValue[7]

            # monday
            self.ids.mon11.text = self.cellValue[8]
            self.ids.mon21.text = self.cellValue[9]
            self.ids.mon31.text = self.cellValue[10]
            self.ids.mon41.text = self.cellValue[11]
            self.ids.mon51.text = self.cellValue[12]
            self.ids.mon61.text = self.cellValue[13]
            self.ids.mon71.text = self.cellValue[14]
            self.ids.mon81.text = self.cellValue[15]

            # tuesday
            self.ids.tue11.text = self.cellValue[16]
            self.ids.tue21.text = self.cellValue[17]
            self.ids.tue31.text = self.cellValue[18]
            self.ids.tue41.text = self.cellValue[19]
            self.ids.tue51.text = self.cellValue[20]
            self.ids.tue61.text = self.cellValue[21]
            self.ids.tue71.text = self.cellValue[22]
            self.ids.tue81.text = self.cellValue[23]

            # wednesday
            self.ids.wed11.text = self.cellValue[24]
            self.ids.wed21.text = self.cellValue[25]
            self.ids.wed31.text = self.cellValue[26]
            self.ids.wed41.text = self.cellValue[27]
            self.ids.wed51.text = self.cellValue[28]
            self.ids.wed61.text = self.cellValue[29]
            self.ids.wed71.text = self.cellValue[30]
            self.ids.wed81.text = self.cellValue[31]

            # tuesday
            self.ids.tues11.text = self.cellValue[32]
            self.ids.tues21.text = self.cellValue[33]
            self.ids.tues31.text = self.cellValue[34]
            self.ids.tues41.text = self.cellValue[35]
            self.ids.tues51.text = self.cellValue[36]
            self.ids.tues61.text = self.cellValue[37]
            self.ids.tues71.text = self.cellValue[38]
            self.ids.tues81.text = self.cellValue[39]


class TeachersPanel(Screen):
    pass


class MakeCTSchedule(Screen):

    def timePicker(self):
        time_dialog = MDTimePicker()
        time_dialog.open()
        time_dialog.bind(on_save=self.on_save_time)

    def datePicker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()
        date_dialog.bind(on_save=self.on_save)

    def on_save_time(self, instance, value):
        self.ids.time.text = str(value)

    def on_save(self, instance, value, range):
        self.ids.date.text = str(value)

    def schedule(self):
        path = 'File\\CT\\' + self.ids.year.text + ' ' + self.ids.sem.text + ' ' + self.ids.sec.text + '.txt'

        if not os.path.exists(path):
            file = open(path, 'w')
            file.write('* ' + self.ids.date.text + '	- 	' + self.ids.time.text + '\n	' + self.ids.code.text + '\n	' + self.ids.title.text + '\n\n')

        else:
            file = open(path, 'a')
            file.write('* ' + self.ids.date.text + '	-	' + self.ids.time.text + '\n	' + self.ids.code.text + '\n	' + self.ids.title.text + '\n\n')

        note = Notification()
        note.title = "Added"
        note.open()

class ViewCTScheduled(Screen):
    path = ''

    def viewRoutine(self):
        self.path = 'File\\CT\\' + self.ids.year.text + ' ' + self.ids.sem.text + ' ' + self.ids.sec.text + '.txt'

        if os.path.exists(self.path):
            with open(self.path) as file:
                data = file.read()
                self.ids.ctroutine.text = str(data)


        else:
            self.ids.ctroutine.text=''
            note = Notification()
            note.title = "Not exits"
            note.open()


class StudentPanel(Screen):
    pass


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class RoutineManagementSystem(MDApp):
    page = ''
    path = ''

    def build(self):
        return Builder.load_file('design.kv')  # for MDLabel

    def loadRoutine(self, year, sem, sec, trans):
        path = str(year + ' year ' + sem + ' semester ' + sec + ' section')
        self.root.get_screen('vroutine').restoreValues(path)  # access window
        self.root.current = "vroutine"
        self.root.transition.direction = trans

    def loadMakeWindow(self, year, sem, sec, transitin):  # goto make window
        path = str(year + ' year ' + sem + ' semester ' + sec + ' section')
        self.path = path
        self.root.get_screen('mroutine').path = path
        self.root.current = "mroutine"
        self.root.transition.direction = transitin

    def updateRoutine(self, year, sem, sec, trans):
        path = str(year + ' year ' + sem + ' semester ' + sec + ' section')
        self.path = path
        self.root.get_screen('uproutine').path = path
        self.root.get_screen('uproutine').restoreValues(path)  # access window
        self.root.current = "uproutine"
        self.root.transition.direction = trans

    def loadTeacherClassSchedule(self):
        self.root.get_screen('vtroutine').loadTeacherList() # access window
        self.root.current = "vtroutine"
        self.root.transition.direction = "left"
    def loadClassRoomStatus(self):
        self.root.get_screen('vcroutine').loadRoomList() # access window
        self.root.current = "vcroutine"
        self.root.transition.direction = "left"


if __name__ == '__main__':
	Clock.max_iteration = 10  # for warning
	RoutineManagementSystem().run()

