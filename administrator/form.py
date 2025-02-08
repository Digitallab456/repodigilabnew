from django.forms import ModelForm

from administrator.models import *

class StudentForm(ModelForm):
    class Meta:
        model = StudentTable
        fields = ['LOGINID','studentname','department','phoneno','dob','address','semester','email','regno']


class StudentForm_edit(ModelForm):
    class Meta:
        model = StudentTable
        fields = ['studentname','department','phoneno','dob','address','semester','regno']


class facultyform(ModelForm):
    class Meta:
        model=facultyTable
        fields=['name','department','subject','qualification','phoneno']

# class complaintform(ModelForm):
#     class Meta:
#         model=complaintTable
#         fields= ['complaint','date','reply'] 

class Notification_form(ModelForm):
    class Meta:
        model = notificationTable
        fields = ['post']
# class registrationform(ModelForm):
#     class Meta:
#         model = fac_registrationTable
#         fields=['FirstName','LastName','Email','PhoneNumber','Department','BriefBiography','LOGINID']
class marklistForm(ModelForm):
    class Meta:
        model = markupTable
        fields = ['FACULTY', 'STUDENT', 'mark']


class TaskForm(ModelForm):
    class Meta:
        model = taskTable
        fields = ['facultyid', 'task']

class cForm(ModelForm):
    class Meta:
        model = complaintTable
        fields = ['complaint', 'LOGIN']

class Uploaded(ModelForm):
    class Meta:
        model = UploadedCode
        fields = ['code', 'output']