from django.shortcuts import render
from onlinetutorial.forms import UserForm,CourseForm,QuestionForm
from onlinetutorial.forms import StudentForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from onlinetutorial.models import StudentProfile,CourseDetails,Question
from django.contrib.auth.models import User


def index(request):

    return render(request, 'onlinetutorial/index.html',)

def register(request):

       
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
    

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
       

    # Render the template depending on the context.
    return render(request,
            'onlinetutorial/register.html',
            {'user_form': user_form,'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        category = request.POST.get('dropdown')
        



        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                
                    if(category=='student'):

                # If the account is valid and active, we can log the user in.
                # We'll send the user to the dashboard.
                     login(request, user)
                     return HttpResponseRedirect('/onlinetutorial/dashboard1')
                    else:
                      login(request, user)
                      return HttpResponseRedirect('/onlinetutorial/tutordashboard')
                

            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/index.html', {})

def dashboard(request):

    completed=False

    #try:
    user=User.objects.get(username=request.user.username)
    userid=user.id
    print(userid)
    #student_ob = StudentProfile.objects.get(user__username=request.user.username)
    #student_ob = StudentProfile(user=user)
    #student_ob = StudentProfile.objects.get(user__username=request.user.username)


        #ob=User.objects.get(username=request.user.username)
    #except:return HttpResponseRedirect('/logout/')
  # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
       
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        student_form = StudentForm(data=request.POST)
        print "Inside11"
    

        # If the two forms are valid...
        if student_form.is_valid():
            print "Inside12"
            # Save the user's form data to the database.
            student=student_form.save(commit=False)
            student.user=User.objects.get(id=userid)

            if 'picture' in request.FILES:
                student.picture = request.FILES['picture']
            
            student.save()

            completed=True

            return HttpResponseRedirect('/onlinetutorial/dashboard2')



        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print student_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        
        student_form = StudentForm()
        print "Outside"
       
       
 
    return render(request,'onlinetutorial/dashboard.html',{'student_form': student_form,'completed':completed})

    print "Dashboard"
    student_form = StudentForm()
    return render(request, 'onlinetutorial/dashboard.html',)

def tutordashboard(request):

    
    return render(request, 'onlinetutorial/tutordashboard.html',)


def admindashboard(request):

    
    return render(request, 'onlinetutorial/admindashboard.html',)

def createcourse(request):

    completed=False

    if request.method == 'POST':
     course_form = CourseForm(data=request.POST)
     if course_form.is_valid():
        course=course_form.save(commit=False)

        if 'syllabus' in request.FILES:
                course.syllabus = request.FILES['syllabus']
        course.save()

        completed=True


        

       # title = request.POST.get('title')
        #category = request.POST.get('category')
        #description = request.POST.get('description')
        #course=CourseDetails(title =title ,category=category,description=description)

        #course.save()


     else:
            print course_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        
        course_form = CourseForm()

    
    
    return render(request, 'onlinetutorial/createcourse.html',{'course_form':course_form,'completed':completed})


def courseview(request):

    obj=CourseDetails.objects.all()

    
    return render(request, 'onlinetutorial/courseview.html',{'obj':obj})

def dashboard1(request):

    
   # try:
    #    ob = StudentProfile.objects.get(user__username=request.user.username)
    #except:return HttpResponseRedirect('/onlinetutorial/logout/')
    #ob=StudentProfile.objects.get(user__username = request.user.username)

    
    return render(request, 'onlinetutorial/dashboard1.html')

def dashboard2(request):


    
    try:

        ob = StudentProfile.objects.get(user__username=request.user.username)
    except:return HttpResponseRedirect('/onlinetutorial/logout/')
    #ob=StudentProfile.objects.get(user__username = request.user.username)

    
    return render(request, 'onlinetutorial/dashboard2.html',{'student_ob':ob})


def quiz(request):

    
    return render(request, 'onlinetutorial/quiz.html',)


def managequiz(request):



    completed=False

    if request.method == 'POST':

    #ob=CourseDetails.objects.get()
     question_form = QuestionForm(data=request.POST)
     if question_form.is_valid():
        question=question_form.save(commit=False)
        print question.course.id


        question.save()


        completed=True

     else:
            print question_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        
        question_form = QuestionForm()


    
    return render(request, 'onlinetutorial/managequiz.html',{'question_form':question_form,'completed':completed})



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/onlinetutorial/')


