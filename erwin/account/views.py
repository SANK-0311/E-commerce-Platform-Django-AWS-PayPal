from django.shortcuts import render, redirect
from django.http import HttpResponse

from . forms import CreateUserForm, LoginForm,UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order , OrderItem
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import auth

from django.contrib.auth import login, logout,authenticate
from django.contrib import messages  # For error messages
from django.contrib.auth.decorators import login_required




# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            #Email verification setup
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })
            user.email_user(subject = subject, message = message)

            return redirect('email-verification-sent')
    context = {'form': form}
    return render(request, 'account/registration/register.html', context = context)






def email_verification(request, uidb64, token):
    #Unique ID
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    #Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    #Failed
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm as LoginForm

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Your account is inactive. Please verify your email.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form input.")
    
    context = {'form': form}
    return render(request, 'account/my-login.html', context)


@login_required(login_url='login')
def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    #auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('store')

@login_required(login_url='login')
def profile(request):
    #updating user profile
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Profile updated successfully.")
            return redirect('dashboard')
    context = {'user_form': user_form}
    return render(request, 'account/profile-management.html',context=context)

@login_required(login_url='login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.warning(request, "Your account has been deleted successfully.")
        return redirect('store')
    # Render the delete account confirmation page
    context = {'user': user}
    return render(request, 'account/delete-account.html',context=context)

@login_required(login_url='login')
def manage_shipping(request):
    try:
        #Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:
        #Account user with no shipment information
        shipping = None
    form = ShippingForm(instance = shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            
            #Assign the user FK on the object
            shipping_user = form.save(commit=False)

            #Adding the FK itself
            shipping_user.user = request.user
            #Save the object
            shipping_user.save()
            return redirect('dashboard')
    context = {'form': form, 'shipping': shipping}
    return render(request, 'account/manage-shipping.html', context=context)

@login_required(login_url='login')
def track_orders(request):

    try:
        orders = OrderItem.objects.filter(user= request.user)
        context = {'orders':orders}
        return render(request,'account/track-orders.html',context = context)

    except:
        return render(request,'account/track-orders.html',context = context)
        
    return render(request,'account/track-orders.html')



