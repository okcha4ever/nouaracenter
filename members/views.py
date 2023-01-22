from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from NawaraCenter import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token

# My views
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "! تم تسجيل دخولك بنجاح")
            return redirect('home')
        else:
            messages.success(request, '...حدث خطأ ما ! اعد المحاولة ')
            return redirect('login')

    else:
        return render(request, 'auth/login.html', {})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
                
        if User.objects.filter(username=username):
            messages.error(request, "! إسم المستخدم هذا مستعمل من قبل")
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "! تم إستعمال هذا البريد من قبل")
            return redirect('/')
        
        if len(username)>20:
            messages.error(request, "! يجب ان يكون إسم المستخدم أقل من 20 حرفاً")
            return redirect('/')
        
        if pass1 != pass2:
            messages.error(request, "! لم تتساوا كلمات السر")
            return redirect('/')
        
        if not username.isalnum():
            messages.error(request, "! يجب ان يكون إسم المستجدم متكون من أرقام او حروف فقط")
            return redirect('/')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "تم إنشاء حسابك, الرجاء تفعيله")
        
        # Welcome Email
        subject = "!!مرحباً بكم في موقع 'مركز نوارة'"
        message = "مرحباً " + myuser.first_name + "!! \n" + "أهلا وسهلا في موقع مركز نوارة!! \nنشكركم على زيارة موقعنا\nوأيضا لقد ارسلنا في هطا البريد رابط, الرجاء تفعيل الحساب \n\nشكراً لكم\nمركز موارة | Nawara Center"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        

        current_site = get_current_site(request)
        email_subject = "تفعيل البريد - مركز نوارة"
        message2 = render_to_string('auth/email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('login')
        
        
    return render(request, "auth/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "! تم تفعيل حسابك, بوسعك الأن تسجيل الدخول")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')
        
def signout(request):
    logout(request)
    messages.success(request, "! تم تسجيل خروجك بنجاح")
    return redirect('home')