from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View

from .form import *
from.models import *

# Create your views here.

 
# ///////////////////////////////////// admin////////////////////////////


# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View

class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'admin/forgot_password.html')

    def post(self, request, *args, **kwargs):


            email = request.POST.get('email')
            
            try:
                user = logintable.objects.get(username=email)  # Fetch user based on email
                user_password = user.password  # Get the password hash (you won't send plain password)
                
                # You should ideally send a password reset link instead of the plain password
                subject = "Password Reset"
                message = f"Your password is: {user_password}"  # This is just an example; sending the plain password is not recommended
                from_email = "no-reply@yourdomain.com"
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Your password has been sent to your email.")
                return HttpResponse('''<script>alert("password sent to your email");window.location="/"</script>''')
 # Redirect to the login page

            except logintable.DoesNotExist:
                return HttpResponse('''<script>alert("email doesnt exist");window.location="/"</script>''')


class LoginPage(View):
    def get(self, request):
        return render(request, "admin/login_page.html")
    def post(self, request):
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            obj=logintable.objects.get(username=username,password=password)
            request.session['user_id']=obj.id
            if obj.type=='admin':
                return HttpResponse('''<script>alert("welcome to home");window.location="adminhome_page"</script>''')
            elif obj.type=='faculty':
                return HttpResponse('''<script>alert("welcome to home");window.location="homepage"</script>''')
            elif obj.type=='student':
                return HttpResponse('''<script>alert("welcome to home");window.location="studenthomepage"</script>''')
        except:
            return HttpResponse('''<script>alert("invalid username or password");window.location="/"</script>''')


      
        #         return render(request,'userdashboard.html')
        #         else:
        #         return HttpResponse("User type not recognized")
        #         except logintable.DoesNotExit:
        #         messages.error(request,"invalid username or password")
                #    return redirect('login')
class logout(View):
    def get(self, request):
        return HttpResponse('''<script>alert("logout successfully");window.location="/"</script>''')
        
class StudentPage(View):
    def get(self, request):
        return render(request, "faculty/addstudent.html")

    def post(self, request):
        form1 = StudentForm(request.POST)
        print(request.POST['regno'])
        
        if form1.is_valid():
            # Create a new logintable entry
            c = logintable.objects.create(
                username=request.POST.get('email'),
                password=request.POST.get('regno'),
                type='student'
            )
            print(c)  # Log the created entry for debugging
            c.save()  # Save the logintable entry
            
            # Now, associate the created logintable entry with the StudentTable record
            student = form1.save(commit=False)  # Don't save to DB yet
            student.LOGINID = c  # Assign the logintable entry as LOGINID for the student
            
            # Save the student record
            student.save()

        return HttpResponse('''<script>alert("Done"); window.location="/student"</script>''')

class StudentEdit(View):
    def get(self,request,id):
        obj=StudentTable.objects.get(id=id)
        return render(request,"admin/edit student.html",{'val':obj})
    def post(self,request,id):
        obj=StudentTable.objects.get(id=id)
        form=StudentForm_edit(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("Done"); window.location="/student"</script>''')
        
class StudentRemove(View):
    def get(self, request, id):
        obj=StudentTable.objects.get(id=id)
        obj.delete()
        return HttpResponse('''<script>alert("Done"); window.location="/student"</script>''')


class FacultyPage(View):
    def get(self, request):
        return render(request,"admin/add faculty.html")
    def post(self,request):
        form=facultyform(request.POST)
        if form.is_valid():
            C = form.save(commit=False)
            d = logintable.objects.create(
                username=request.POST.get('email'),
                password=request.POST.get('password'),
                type='faculty'
                )
            d.save()
            C.LOGIN = d
            C.save()
            return HttpResponse('''<script>alert("Done"); window.location="/faculty"</script>''')

class facultyEdit(View):
    def get(self, request,id):
        obj=facultyTable.objects.get(id=id)
        return render(request,"admin/edit faculty.html",{'val':obj})
    def post(self,request,id):
        obj=facultyTable.objects.get(id=id)
        form=facultyform(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("Done"); window.location="/faculty"</script>''')
               
class facultyRemove(View):
    def get(self, request, id):
        obj=logintable.objects.get(id=id)
        obj.delete()
        return HttpResponse('''<script>alert("Done"); window.location="/faculty"</script>''')


class ComplaintPage(View):
    def get(self, request, id):
        return render(request,"admin/complaint.html")

    def post(self,request,id):
        reply=request.POST['reply']
        obj=complaintTable.objects.get(id=id)
        obj.reply=reply
        obj.save()
        return HttpResponse('''<script>alert("Done");window.location="/reply"</script>''')

class Adminp(View):
    def get(self, request):
        return render(request,"admin/admin_homepage.html")

class stdp(View):
    def get(self,request):
        obj=StudentTable.objects.all()
        print(obj)
        return render(request,"admin/student.html",{'val':obj})
class Reply(View):
    def get(self,request):
        obj=complaintTable.objects.all()
        return render(request,"admin/complaint reply.html",{'val':obj})
    

class Facpage(View):
    def get(self,request):
        obj=facultyTable.objects.all()
        return render(request,"admin/faculty.html",{'val':obj})
    
    
class notificationp(View):
    def get(self,request):
        return render(request,"admin/post notification.html")
    def post(self,request):
        c= Notification_form(request.POST)
        if c.is_valid():
            c.save()
        return HttpResponse('''<script>alert("Done");window.location="/notification"</script>''')

            
class select_class(View):
    def get(self, request):
        obj = Class.objects.all()
        return render(request, "admin/select_class.html", {'obj': obj})
                  
class manage_timetable(View):
    def post(self, request):
        class_id=request.POST['class_id']
        request.session['class_id']=class_id
        class_obj = Class.objects.get(id=class_id)
        subjects = Subject.objects.all()
        existing_days = Timetable.objects.filter(CLASS_id=class_obj).values_list('day', flat=True)
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        available_days = [day for day in all_days if day not in existing_days]
        return render(request, 'admin/manage_timetable.html', {'subjects': subjects,'available_days': available_days})

class add_timetable_action(View):
    def post(self, request):
        day = request.POST['day']
        slot_9_10 = request.POST['slot_9_10']
        slot_10_11 = request.POST['slot_10_11']
        slot_11_12 = request.POST['slot_11_12']
        slot_1_2 = request.POST['slot_1_2']
        slot_2_3 = request.POST['slot_2_3']
        slot_3_4 = request.POST['slot_3_4']
        obj = Timetable()
        obj.CLASS=Class.objects.get(id=request.session['class_id'])
        obj.day =day
        obj.slot_9_10=Subject.objects.get(id=slot_9_10)
        obj.slot_10_11=Subject.objects.get(id=slot_10_11)
        obj.slot_11_12=Subject.objects.get(id=slot_11_12)
        obj.slot_1_2=Subject.objects.get(id=slot_1_2)
        obj.slot_2_3=Subject.objects.get(id=slot_2_3)
        obj.slot_3_4=Subject.objects.get(id=slot_3_4)
        obj.save()
        return HttpResponse('''<script>alert("successfully added");window.location="/select_class#about"</script>''')
        
    
class select_class1(View):
    def get(self, request):
        obj = Class.objects.all()
        return render(request, "admin/select_class1.html", {'obj': obj})
class stselect_class1(View):
    def get(self, request):
        obj = Class.objects.all()
        return render(request, "student/select_class1.html", {'obj': obj})
                                   
class view_timetable(View):
    def post(self, request):
        class_id=request.POST['class_id']
        # Query all timetable entries from the database
        timetable_entries = Timetable.objects.filter(CLASS_id=class_id).order_by('day')
        # Render the timetable in a template
        return render(request, 'admin/timetable.html', {'timetable_entries': timetable_entries})  
      #////////////////////////// faculty///////////////////////////

class stview_timetable(View):
    def post(self, request):
        class_id=request.POST['class_id']
        # Query all timetable entries from the database
        timetable_entries = Timetable.objects.filter(CLASS_id=class_id).order_by('day')
        # Render the timetable in a template
        return render(request, 'student/timetable.html', {'timetable_entries': timetable_entries})  
class editpage(View):
    def get(self,request):
        
        return render(request,"faculty/edit _student.html")
    
class homepage(View):
    def get(self,request):
        return render(request,"faculty/faculty_homepage.html")
    

class markupp(View):
    def get(self,request, id):
        obj = StudentTable.objects.filter(id=id).first()
        print(obj)
        c = facultyTable.objects.get(LOGIN__id = request.session['user_id'])
        return render(request,"faculty/mark_upload.html",{'obj':obj, 'a':c})
    
    def post(self, request, id):
        k = marklistForm(request.POST)
        if k.is_valid():
            k.save()
            return HttpResponse('''<script>alert("mark added successfully");window.location="/marklist"</script>''')

    
class notificationpage(View):
    def get(self,request):
        c= notificationTable.objects.all()
        return render(request,"faculty/notification.html", {'a':c})

class studentListp(View):
    def get(self,request):
        c= StudentTable.objects.all() 
        return render(request,"faculty/student_ list.html",{'farhana':c})

class regpage(View):
    def get(self,request):
        return render(request,"faculty/registration.html")
    def post(self,request):
        form=facultyform(request.POST)
        if form.is_valid():
               login_instance=logintable.objects.create(
                   type='faculty',
                   username=request.POST['username'],
                   password=request.POST['password'],
               )
               reg_form=form.save(commit=False)
               reg_form.LOGIN=login_instance
               reg_form.save()
               return HttpResponse('''<script>alert("Registered successfully");window.location="/"</script>''')


class marklistPage(View):
    def get(self, request):
        students = StudentTable.objects.all()  # Fetch all students

        # Prepare data for the template
        student_data = []
        for student in students:
            marks = markupTable.objects.filter(STUDENT=student)  # Fetch marks for each student
            student_data.append({
                'student': student,
                'marks': marks if marks.exists() else None,  # Include marks if they exist
                'can_add_mark': not marks.exists(),  # True if no marks exist
            })
        
        # Move the return statement outside the loop
        return render(request, "faculty/marklist.html", {'student_data': student_data})

  
class logout(View):
    def get(self, request):
        return HttpResponse('''<script>alert("logout successfully");window.location="/"</script>''')
class viewcomplaint(View):
    def get(self,request):
        c= complaintTable.objects.all()
        return render(request,"faculty/f_reply.html",{'a':c})
    
class task(View):
   def get(self,request):
        c = facultyTable.objects.get(LOGIN__id = request.session['user_id'])
        return render(request,"faculty/task.html", {'s':c})
   def post(self, request):
       d = TaskForm(request.POST)
       if d.is_valid():
           d.save()
           return HttpResponse('''<script>alert("task added successfully");window.location="/task"</script>''')

class taskman(View):
    def get(self,request):
        c = taskTable.objects.filter(facultyid__LOGIN_id=request.session['user_id'])
        return render(request,"faculty/taskMan.html",{'a':c})
    
class taskedit(View):
    def get(self,request,id):
        c = taskTable.objects.get(id=id)
        return render(request,"faculty/taskedit.html",{'s':c})
    def post(self,request,id):
        print(request.POST['task'])
        c = taskTable.objects.get(id=id)
        form = TaskForm(request.POST,instance=c)
        if form.is_valid():
            print(request.POST['task'])
            form.save()
            return HttpResponse('''<script>alert("task updated successfully");window.location="/taskman"</script>''')

class taskcodestatusaccept(View):
    def get(self,request,id):
        c = taskTable.objects.get(id=id)
        c.status = 'accept'
        c.save()
        return HttpResponse('''<script>alert("task code status updated successfully");window.location="/taskman"</script>''')



class taskcodestatusreject(View):
    def get(self,request,id):
        c = taskTable.objects.get(id=id)
        c.status = 'reject'
        c.save()
        return HttpResponse('''<script>alert("task code status updated successfully");window.location="/taskman"</script>''')

class taskdelete(View):
    def get(self,request,id):
        c = taskTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert("task deleted successfully");window.location="/taskman"</script>''')
class viewtask(View):
    def get(self,request):
        c = taskTable.objects.filter(facultyid__LOGIN_id=request.session['user_id'])
        return render(request,"faculty/viewtask.html",{'a':c})
    
class postcomplaintpage(View):
    def get(self,request):
        c = logintable.objects.get(id=request.session['user_id'])
        return render(request,"faculty/post.html",{'z':c})
    def post(self, request):
       d = cForm(request.POST)
       if d.is_valid():
           d.save()
           return HttpResponse('''<script>alert("complaint added successfully");window.location="/"</script>''')
       
class viewcomplaintpage(View):
    def get(self,request):
        c = complaintTable.objects.filter(facultyid__LOGIN_id=request.session['user_id'])
        return render(request,"faculty/viewcomplaint.html",{'a':c})

    

#///////////////////////////////////student////////////////////////////////////////////

class studpage(View):
    def get(self,request):
        c = taskTable.objects.all()

        return render(request,"student/student_homage.html",{'b':c})
class insert_timetable(View):
    def get(self,request):
        subjects = Subject.objects.all()
        teachers = Teacher.objects.all()
        classrooms = Class.objects.all()

        return render(request, 'admin/insert_timetable.html', {
            'subjects': subjects,
            'teachers': teachers,
            'classrooms': classrooms
        })
    

    # def post(self,request):
    #     subject_id = request.POST.get('subject')
    #     teacher_id = request.POST.get('teacher')
    #     classroom_id = request.POST.get('classroom')
    #     day_of_week = request.POST.get('day_of_week')
    #     time_slot = request.POST.get('time_slot')

    #     # Create a new TimetableEntry
    #     timetable_entry = TimetableEntry(
    #         subject_id=subject_id,
    #         teacher_id=teacher_id,
    #         classroom_id=classroom_id,
    #         day_of_week=day_of_week,
    #         time_slot=time_slot
    #     )
    #     timetable_entry.save()

    #     return redirect("/timetable")


    def post(self,request):
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        classroom_id = request.POST.get('classroom')
        day_of_week = request.POST.get('day_of_week')
        time_slot = request.POST.get('time_slot')

        print(f"Subject: {subject_id}, Teacher: {teacher_id}, Classroom: {classroom_id}, Day: {day_of_week}, Time Slot: {time_slot}")


        # Create a new TimetableEntry
        timetable_entry = TimetableEntry(
            subject_id=subject_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            day_of_week=day_of_week,
            time_slot=time_slot
        )
        timetable_entry.save()

        return redirect("/timetable")
    



class Codeupload(View):
    def get(self,request,id):
        ta=taskTable.objects.filter(id=id).first()
        return render(request,"codeupload.html",{'ta':ta})
    def post(self, request,id):
        c = Uploaded(request.POST, request.FILES)
        if c.is_valid():
            c.save()
            return HttpResponse('''<script>alert('code added successfully');window.location='/studenthomepage'</script>''')
        

class view_code(View):
    def get(self,request):
        obj= UploadedCode.objects.filter(taskid__facultyid__LOGIN_id=request.session['user_id'])
        print(obj)
        return render(request,"faculty/view_code.html", {'obj':obj})
    


class ViewTaskCode(View):
    def get(self, request):
        task_id = request.GET.get('taskid')  # Get task ID from request
        task = get_object_or_404(taskTable, id=task_id)
        return JsonResponse({'taskcode': task.taskcode}) 

class StudentProfileView(View):
    template_name = 'student/student_profile.html'

    def get(self, request, student_id):
        student = get_object_or_404(StudentTable, LOGINID__id=student_id)
        return render(request, self.template_name, {'student': student})