from reportlab.pdfgen.canvas import Canvas
from attendance.models import Attendance
from sales.models import Sale
from datetime import date
import calendar

def inch(num):
    return num * 72.0

def cm(num):
    return num * 28.346456692913385

def objectsThisMonth(_object, month, **kwargs):
    objects = []
    for obj in _object.objects.filter(**kwargs):
        if (obj.date.month == month):
            objects.append(obj)
    return objects

FONTS = {'normal':'Times-Roman', 'bold':'Times-Bold', 'bold-italic':'Times-BoldItalic', 'italic':'Times-Italic'}

class Report:
    def __init__(self, file_name:str, user:str, month:int):
        self.user = user
        self.month = month
        self.monthly_sales = objectsThisMonth(Sale, month)
        self.monthly_attendances = objectsThisMonth(Attendance, month)

        self.canvas = Canvas(file_name, pagesize=(inch(8.5), inch(11)))
        self.canvas.translate(0, inch(11))

        #header
        self.canvas.setFont(FONTS.get('bold'), 18)
        self.canvas.drawString(inch(1), -inch(1), f"Executive Summary ({calendar.month_name[month]})")
        self.canvas.setFont(FONTS.get('normal'), 14)
        self.canvas.drawString(inch(1), -inch(1.5), f"Gym Name: Triple-J Fitness (Malinta)")
        self.canvas.drawString(inch(1), -inch(1.8), f"Request by: {user}")
        self.canvas.drawString(inch(1), -inch(2.1), f"Date Generated: {date.today().isoformat()}")
        self.canvas.setStrokeColorRGB(0, 0, 0, 1)
        self.canvas.line(inch(1), -inch(2.3), inch(7.5), -inch(2.3))
        self.y = -inch(2.1)
    
    def check_new_page(self):
        if (self.y < -inch(10)):
            self.canvas.showPage()
            self.canvas.translate(0, inch(11))
            self.canvas.setFont(FONTS.get('normal'), 12)
            self.y = -inch(1)
    
    def create_sales(self):
        #Sales
        self.canvas.setFont(FONTS.get('bold'), 16)
        self.canvas.drawString(inch(1), self.y-inch(0.5), "Sales")
        self.canvas.setFont(FONTS.get('bold'), 12)
        self.canvas.drawCentredString(inch(1.8125), self.y-inch(0.9), "Date Recorded")
        self.canvas.drawCentredString(inch(3.4375), self.y-inch(0.9), "Amount")
        self.canvas.drawCentredString(inch(5.875), self.y-inch(0.9), "Receipt No.")
        self.canvas.line(inch(1.1), self.y-inch(1.03), inch(7.4), self.y-inch(1.03))
        self.canvas.setFont(FONTS.get('normal'), 12)
        self.y -= inch(0.9)
        sales = 0
        for i, sale in enumerate(self.monthly_sales):
            self.y -= inch(0.4)
            self.check_new_page()
            sale:Sale = sale
            self.canvas.drawCentredString(inch(1.8125), self.y, sale.date.isoformat())
            self.canvas.drawCentredString(inch(3.4375), self.y, f'P{str(sale.amount)}')
            self.canvas.drawCentredString(inch(5.875), self.y, sale.receipt_no)
            sales += sale.amount
        self.canvas.line(inch(1.1), self.y-inch(0.13), inch(7.4), self.y-inch(0.13))
        self.canvas.setFont(FONTS.get('bold'), 12)
        self.canvas.drawCentredString(inch(1.8125), self.y-inch(0.4), "Total Sales:")
        self.canvas.setFont(FONTS.get('normal'), 12)
        self.canvas.drawCentredString(inch(3.4375), self.y-inch(0.4), f'P{str(sales)}')
        self.y -= inch(0.5)
        self.check_new_page()
    
    def busiest_date(self):
        dates = {}
        for attendace in self.monthly_attendances:
            dates[attendace.date.isoformat()] = dates.get(attendace.date.isoformat(), 1) + 1
        busiest_date = max(dates.keys(), key=lambda x: dates[x])
        return busiest_date

    def ranked_days(self):
        days = {}
        for attendance in self.monthly_attendances:
            days[attendance.date.weekday()] = days.get(attendance.date.weekday(), 1) + 1
        return sorted(days.keys(), key=lambda x: days[x])[:3]

    def ranked_time_in(self):
        hours = {}
        for attendance in self.monthly_attendances:
            hours[attendance.timeIn.hour] = hours.get(attendance.timeIn.hour, 1) + 1
        return sorted(hours.keys(), key=lambda x: hours[x])[:3]
    
    def create_attendance(self):
        self.canvas.setFont(FONTS.get('bold'), 16)
        self.canvas.drawString(inch(1), self.y-inch(0.5), "Attendances")
        self.canvas.setFont(FONTS.get('bold'), 12)
        self.canvas.drawCentredString(inch(1.8125), self.y-inch(0.9), "Date Recorded")
        self.canvas.drawCentredString(inch(3.4375), self.y-inch(0.9), "Username")
        self.canvas.drawCentredString(inch(5.0625), self.y-inch(0.9), "Time In")
        self.canvas.drawCentredString(inch(6.6875), self.y-inch(0.9), "Time Out")
        self.canvas.line(inch(1.1), self.y-inch(1.03), inch(7.4), self.y-inch(1.03))
        self.canvas.setFont(FONTS.get('normal'), 12)
        self.y -= inch(0.9)
        for i, attendance in enumerate(self.monthly_attendances):
            self.y -= inch(0.4)
            self.check_new_page()
            attendance:Attendance = attendance
            self.canvas.drawCentredString(inch(1.8125), self.y, attendance.date.isoformat())
            self.canvas.drawCentredString(inch(3.4375), self.y, attendance.member.username)
            self.canvas.drawCentredString(inch(5.0625), self.y, str(attendance.timeIn))
            self.canvas.drawCentredString(inch(6.6875), self.y, str(attendance.timeOut))
        self.canvas.line(inch(1.1), self.y-inch(0.13), inch(7.4), self.y-inch(0.13))
        self.canvas.setFont(FONTS.get('bold'), 12)
        self.canvas.drawCentredString(inch(1.8125), self.y-inch(0.4), "Attendances:")
        self.canvas.setFont(FONTS.get('normal'), 12)
        self.canvas.drawCentredString(inch(3.4375), self.y-inch(0.4), str(len(self.monthly_attendances)))
        self.canvas.setFont(FONTS.get('bold'), 12)
        if (len(self.monthly_attendances) > 0):
            self.canvas.drawCentredString(inch(5.0625), self.y-inch(0.4), "Busiest:")
            self.canvas.setFont(FONTS.get('normal'), 12)
            self.canvas.drawCentredString(inch(6.6875), self.y-inch(0.4), self.busiest_date())
        self.y -= inch(0.5)
        self.check_new_page()
    
    def create_busy_activity(self):
        self.canvas.setFont(FONTS.get('bold'), 16)
        self.canvas.drawString(inch(1), self.y-inch(0.5), "Peak Days & Hours")
        self.canvas.setFont(FONTS.get('bold'), 12)
        self.canvas.drawCentredString(inch(2.625), self.y-inch(0.9), "Peak Days (Ranked)")
        self.canvas.drawCentredString(inch(5.875), self.y-inch(0.9), "Peak Time In (Ranked)")
        self.canvas.line(inch(1.1), self.y-inch(1.03), inch(7.4), self.y-inch(1.03))
        self.canvas.setFont(FONTS.get('normal'), 12)
        self.y -= inch(0.9)
        days = self.ranked_days()
        hours = self.ranked_time_in()
        for i in range(min(len(days), len(hours))):
            self.y -= inch(0.4)
            self.check_new_page()
            if (i < len(days)):
                self.canvas.drawCentredString(inch(2.625), self.y, calendar.day_name[days[i]])
            if (hours[i] == 0):
                hour = '12 AM'
            elif (0 < hours[i] < 12):
                hour = f'{hours[i]} AM'
            elif (hours[i] == 12):
                hour = f'12 PM'
            else:
                hour = f'{hours[i] - 12} PM'
            if (i < len(hours)):
                self.canvas.drawCentredString(inch(5.875), self.y, hour)
    
    def save(self):
        self.canvas.save()
