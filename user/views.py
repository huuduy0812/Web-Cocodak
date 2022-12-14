import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView
from cart.models import Cart
from .models import User, Favorite
from django.core.mail import EmailMessage
from django.contrib import messages, auth


# Create your views here.

rf = ''

def CheckPassword(password):
    if len(password) < 6 or password[0].islower():
        return [0, 'Password must be greater than 6 characters with first uppercase letter.']
    else:
        return [1]


def register_access(request):
    return render(request, 'registration/register_access.html')


def forgotPassword_access(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'registration/forgotPassword_access.html')


def SiteLoginView(request):
    global rf
    mess = rf
    rf = ''
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            my_user = authenticate(username=username, password=password)
            if my_user is None:
                mess = "Your username and password didn't match. Please try again."
                return render(request, 'registration/login.html', dict(rf=mess))
            login(request, my_user)
            return redirect('index')
        return render(request, 'registration/login.html', dict(rf=mess))


class SiteProfilesView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'


class SiteLogoutView(LogoutView, TemplateView):
    #next_page = '/'
    extra_context = None
    template_name = 'index.html'


def SiteRegisterView(request):
    global rf
    mess = rf
    rf = ''
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            address = request.POST['address']
            password = request.POST['password']
            phone = request.POST['phone']
            make_password = request.POST['make_password']
            gender = request.POST['gender']

            if username == '':
                mess = 'Invalid username'
                return render(request, 'registration/register.html', dict(rf=mess))
            elif re.search(r'^\+$ ', username):
                mess = 'Username with special characters'
                return render(request, 'registration/register.html', dict(rf=mess))
            else:
                for item in User.objects.all():
                    if item.username == username:
                        mess = 'Account already exists'
                        return render(request, 'registration/register.html', dict(rf=mess))
                    elif item.email == email:
                        mess = 'Email already exists'
                        return render(request, 'registration/register.html', dict(rf=mess))
                test_account = 1
            check = CheckPassword(password)
            if check[0] == 0:
                mess = check[1]
                return render(request, 'registration/register.html', dict(rf=mess))

            if password == '' or make_password == '' or password != make_password:
                mess = 'Invalid password'
                return render(request, 'registration/register.html', dict(rf=mess))

            if password == make_password and test_account == 1:
                user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                address=address,
                                                password=password,
                                                phone=phone,
                                                gender=gender
                                                )
                user.save()
                print('user created')
                cart = Cart.objects.create(
                    user_id=user
                )
                cart.save()
                current_site = "cocodak.site"
                mail_subject = 'Activate your account.'
                rf = 'Your account has been created. Please check your email for account verification!'
                message = render_to_string('registration/active_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                send_email = EmailMessage(mail_subject, message, to=[email])
                send_email.content_subtype = "html"
                send_email.send()
                return redirect('login')

        else:
            return render(request, 'registration/register.html', dict(rf=rf))


def ChangePasswordSite(request):
    global rf
    mess =rf
    rf = ''
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            password = request.POST['password']
            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']
            username = request.user
            password_user = authenticate(username=username, password=password)

            if password_user is None:
                mess = "Your password wrong. Please try again."
                return render(request, 'registration/change_password.html', dict(rf=rf))

            check = CheckPassword(new_password)

            if check[0] == 0:
                mess = check[1]
                return render(request, 'registration/change_password.html', dict(rf=mess))

            if new_password == confirm_password:
                mess = "Congratulations! Your password changed successfully."
                u = User.objects.get(username__exact=request.user)
                u.set_password(new_password)
                u.save()
                return render(request, 'registration/change_password.html', dict(rf=mess))
        else:
            return render(request, 'registration/change_password.html', dict(rf=mess))


def activate(request, uidb64, token):
    global rf
    mess = rf
    rf =''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_active = True
        user.save()
        print('\n\n\n true \n\n\n')
        rf = 'Your account is activated, please login!'
        return render(request, "registration/register_access.html", dict(rf=''))
    else:
        print('\n\n\n false \n\n\n')
        mess = "Activation link is invalid!"
        return render(request, "registration/register_access.html", dict(rf=mess))


def forgotPassword(request):
    global rf
    if request.user.is_authenticated:
        return redirect('profile')
    else:

        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                user = User.objects.get(email__exact=email)

                current_site = "cocodak.site"
                mail_subject = 'Reset your password'
                message = render_to_string('registration/reset_password_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                send_email = EmailMessage(mail_subject, message, to=[email])
                send_email.content_subtype = 'html'
                send_email.send()

                rf = "Password reset email has been sent to your email address"
                return redirect('login')
            except Exception:
                rf = 'Email does not exist!'
                return render(request, 'registration/forgotPassword.html', dict(rf=rf))
        else:
            rf = ''
            return render(request, 'registration/forgotPassword.html', dict(rf=rf))


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('reset_password')
    else:
        return redirect('index')


def reset_password(request):
    global rf
    rf = ''
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        check = CheckPassword(password)

        if check[0] == 0:
            rf = check[1]
            return render(request, 'registration/reset_password.html', dict(rf=rf))

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            rf = "Password reset successful!"
            return redirect('login')
    return render(request, 'registration/reset_password.html', dict(rf=rf))
