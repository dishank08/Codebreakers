from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import generic
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import EmailMessage
from CodeBreakersapp.forms import * 
from CodeBreakersapp.models import Users,Question,Que,Rank,Feedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from sphere_engine import CompilersClientV3
from sphere_engine.exceptions import SphereEngineException
import time
import requests
from django.db.models import Sum


def index(request):
    c={}
    c.update(csrf(request))
    if request.session.has_key('username'):
        return render(request,'index.html',c)
    return render_to_response('index.html',c)

def google(request):
    c={}
    c.update(csrf(request))
    return render_to_response('google8e6a172d6bdd9071.html',c)

def sitemap(request):
    c={}
    c.update(csrf(request))
    return render_to_response('sitemap.xml',c)

def login(request):
    c={}
    c.update(csrf(request))
    if request.session.has_key('username'):
        return HttpResponseRedirect('/home/')
    else:    
        return render_to_response('login.html',c)

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect('/')

def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        request.session['username'] = username
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/login/?msg=Invalid_Username_or_Password')
    
def home(request):
    if request.session.has_key('username'):
        return render(request,'home.html')
    else:
        return HttpResponseRedirect('/')
    
def register(request):
    c = {}
    c.update(csrf(request))
    if request.session.has_key('username'):
        return render(request,'register.html')       
    
    return render_to_response('register.html', c)

def addstudentinfo(request):
    uname = request.POST.get('username', '')
    pwd = request.POST.get('password1', '')
    pwd2 = request.POST.get('password2', '')
    mail = request.POST.get('email', '')
    try:
    	ob = Users.objects.get(username=uname)
    except Users.DoesNotExist:
        ob = None

    if ob is None:
	    form = SignUpForm(request.POST)
	    if form.is_valid():
	        username= form.cleaned_data.get('username')
	        password= form.cleaned_data.get('password1')
	        s=Users(username=uname, mailid=mail , password1=pwd, password2=pwd2)
	        s.save()
	        current_site = get_current_site(request)
	        mail_subject = 'Welcome to CodeBreakers.'
	        message = render_to_string('welcomemail.html', {
	        	'user':username,
	        	'domain':'codebreakers08.herokuapp.com/login/'
	        	})
	        to_email = form.cleaned_data.get('email')
	        email = EmailMessage(
	        	mail_subject, message, to=[to_email],
	        	)
	        email.send()
	        form.save()
	        return HttpResponseRedirect('/register/?msg=Account_created_successfully.')
	    else:
    		return HttpResponseRedirect('/register/?msg=Invalid_Email_Or_Password.')
    return HttpResponseRedirect('/register/?msg=Username_already_exist.')

def forgotpass(request):
 	c={}
 	c.update(csrf(request))
 	return render(request,'forgotpass.html',c)
 	 

def passverification(request):
	c={}
	c.update(csrf(request))
	uname=request.POST.get('username')
	try:
		ob=Users.objects.get(username=uname)
	except Users.DoesNotExist:
		ob=None

	if ob is not None:
		pwd=ob.password1
		to_email=ob.mailid
		mail_subject="Forgot Password"
		current_site = get_current_site(request)
		message = render_to_string('passmail.html', {
		        'user':uname,
		        'domain':'codebreakers08.herokuapp.com/login/',
		        'pwd':pwd })
		email = EmailMessage(mail_subject, message, to=[to_email] )
		email.send()
		return HttpResponseRedirect('/forgotpass/?msg=Please_check,_Mail_sent_to_your_email_id')    
	return HttpResponseRedirect('/forgotpass/?msg=Invalid_Username')

#@login_required(login_url='/login/')        
def practice(request):
	if request.session.has_key('username'):
		data=Que.objects.all().order_by('max_marks')
		uname=request.session['username']
		info=Rank.objects.filter(username=uname)
		context={'data':data , 'info':info}
		return render(request,'practice.html',context)
	else:
		return HttpResponseRedirect('/login/')
    
def addQuestion(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		if request.session['username']=="dishank1":
			return render(request,'addquestion.html',c)
		else:
			return render(request,'home.html',{'msg':"you are not admin so that you are not alloweded"})

def users(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		if request.session['username']=="dishank1":
			data=Users.objects.all()
			info=Feedback.objects.all()
			context={'data':data , 'info':info}
			return render(request,'users.html',context)
		else:
			return HttpResponseRedirect('/')
	
def leaderboard(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		username=request.session['username']
		data=Rank.objects.values('username').annotate(sum=Sum('marks')).order_by('-sum')
		context={'data':data}
		return render(request,'leaderboard.html',context)
	else:
		return HttpResponseRedirect('/login/')

def profile(request):
    if request.session.has_key('username'):
    	if request.GET.get('uname') is not None:
    		uname=request.GET.get('uname')
    		data=Users.objects.filter(username = uname)
    		info=Rank.objects.filter(username = uname)
    		qinfo=Que.objects.all()
    		context={'data':data ,'info':info ,'qinfo':qinfo }
    		return render(request,'profile.html',context)
    	else:
        	uname=request.session.get('username')
        	data=Users.objects.filter(username = uname)
        	info=Rank.objects.filter(username = uname)
        	qinfo=Que.objects.all()
        	context={'data':data ,'info':info ,'qinfo':qinfo }
        	return render(request,'profile.html',context)
    else:
        return HttpResponseRedirect('/login/')
    
def add(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		qname=request.POST.get('qname')
		qid=request.POST.get('qid')
		qlevel=request.POST.get('qlevel')
		marks=request.POST.get('marks')
		input=request.POST.get('input')
		output=request.POST.get('output')
		d=Que.objects.filter(question_Id=qid)
		if not d:
			data=Que(question_Id=qid,question_name=qname,q_level=qlevel,max_marks=marks)
			data.save()
			info=Users.objects.all()
			for i in info:
				to_email=i.mailid
				uname=i.username
				mail_subject="New Question Added"
				current_site = get_current_site(request)
				message = render_to_string('queadd.html', {
		        'user':uname,
		        'qname':qname,
		        'domain':'codebreakers08.herokuapp.com/practice/'})
				email = EmailMessage(mail_subject, message, to=[to_email] )
				email.send()

		data1=Question(question_Id=qid,question_name=qname,q_level=qlevel,cinput=input,Eoutput=output,max_marks=marks)
		data1.save()
		return render(request,'addquestion.html',c)
	else:
		return HttpResponseRedirect('/')

def deleteq(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		qname=request.GET.get('qname')
		Que.objects.filter(question_name=qname).delete()
		Question.objects.filter(question_name=qname).delete()
		return HttpResponseRedirect('/practice/')
	else:
		return HttpResponseRedirect('/')

def userdelete(request):
	if request.session.has_key('username'):
		uname=request.GET.get('uname')
		Users.objects.filter(username=uname).delete()
		User.objects.filter(username=uname).delete()
		Rank.objects.filter(username=uname).delete()
		Feedback.objects.filter(username=uname).delete()
		return HttpResponseRedirect('/users/')
	else:
		return HttpResponseRedirect('/')

def editprofile(request):
	if request.session.has_key('username') and request.session['username']!='dishank1':
		uname=request.session.get('username')
		data=Users.objects.filter(username = uname)
		return render(request,'editprofile.html',{'data':data})
	return HttpResponseRedirect('/')

def update(request):
    if request.session.has_key('username'):
        uname=request.session.get('username')
        data=Users.objects.filter(username = uname)
        firstname = request.POST.get('fname', '')
        middlename =request.POST.get('mname', '')
        lastname = request.POST.get('lname', '')
        mail = request.POST.get('mail', '')
        university = request.POST.get('uni', '')
        degree = request.POST.get('deg', '')
        country = request.POST.get('country', '')
        for i in data:
            i.firstName=firstname
            i.middleName=middlename
            i.lastName=lastname
            i.mailid=mail
            i.university=university
            i.degree=degree
            i.country=country
            i.save()
    return HttpResponseRedirect('/profile/')

def hcode(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		qname=request.GET.get('qname')
		data=Que.objects.filter(question_name=qname)
		for i in data:
                    request.session['pcode']=i.question_Id
                    request.session['max']=i.max_marks	
		return render(request,'practice/'+qname+'.html',c)
	else:
		return HttpResponseRedirect('/')
		
#@login_required(login_url='/login/')
def code(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username') and request.session['username']!='dishank1':
		return render(request,'code.html',{'msg':"xyz"})
	else:
		return HttpResponseRedirect('/')

def contact(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		return render(request,'contact.html',c)
	else:
		return HttpResponseRedirect('/')

def feedback(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		uname=request.session.get('username')
		feedback=request.POST.get('feedback')
		s=Feedback(username_id=uname , feedback=feedback)
		s.save()
		return render(request,'contact.html',{'msg':"Feedback Sent"})
	else:
		return HttpResponseRedirect('/')
		
#@login_required(login_url='/login/')	
def execute(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username') and request.session['username']!='dishank1':
	# define access parameters
		accessToken='635261e9572cfed16a140f349c08df82'
		# accessToken='8f7022c5db9a91c4fa8c699309094d9e'
		endpoint='e6a34d7a.compilers.sphere-engine.com'
		# initialization
		client = CompilersClientV3(accessToken, endpoint)
		# API usage
		source = request.POST.get('sourcecode')
		compiler = request.POST.get('language')
		y=0
		input1 = Question.objects.filter(question_Id=request.session['pcode'])
		for var in input1:
			input=var.cinput
			try:
				response = client.submissions.create(source, compiler, input)
				x=var.Eoutput
				id=response['id']
				
				time.sleep(5)
				response=client.submissions.get(id)
				if(response['result']==11):
					c['q']="Compilation error"
					return render(request,'code.html',c)
				elif(response['result']==15):
					if(response['time']<=1):
						url = "https://e6a34d7a.compilers.sphere-engine.com/api/v3/submissions/"+str(id)+"/output?access_token=635261e9572cfed16a140f349c08df82"
						response = requests.get(url)
						if(str(x)!=str(response.content.decode("utf-8"))):
							c['q']="Wrong Answer!!"
							c['q1']="You Got 0 marks."
							c['q2']=str(input)
							c['q3']=str(x)
							c['q4']=str(response.content.decode("utf-8"))
							return render(request,'code.html',c)
						else:
							y=1
							c['q2']=str(input)
							c['q3']=str(x)
					else:
						c['q']="Time limit exceeded"
						c['q1']="You Got 0 marks."
						c['q2']=str(input)
						c['q3']=str(x)
						return render(request,'code.html',c)
				elif(response['result']==12):
					c['q']="Runtime error"
					return render(request,'code.html',c)
				elif(response['result']==13):
					c['q']="Time limit exceeded"
					c['q1']="You Got 0 marks."
					return render(request,'code.html',c)
			except SphereEngineException as e:
				print(e)
				if e.code == 401:
					print('Invalid access token')
		if(y==1):
				
			marks=(str)(request.session['max'])
			username=request.session['username']
			user= Users.objects.get(username=username)
			que= Que.objects.get(question_Id=request.session['pcode'])
			c['q']="Code Running Successfully!!"
			c['q1']="You Got "+marks+" marks."
			c['q4']=str(response.content.decode("utf-8"))
			check=Rank.objects.filter(username=user,question_Id=que)
			if not check:
				r=Rank(username=user,marks=marks,question_Id=que)
				r.save()
		else:
			c['q']="Source code is empty."
			
		return render_to_response('code.html',c)
	else:
		return HttpResponseRedirect('/')
