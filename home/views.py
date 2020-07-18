from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# HTML pages.
def home(request):
    return render(request, 'home/home.html')



def ajay(request):
    return render(request, 'home/ajay.html')



def cont(request):
    if request.method=='POST':
         name = request.POST['name']
         email = request.POST['email']
         phone = request.POST['phone']
         content = request.POST['content']
         if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
             messages.error(request, "Please fill the form correctly")
         else:
             contact = Contact(name=name, email=email, phone=phone, content=content)
             contact.save()
             messages.success(request, "Your message has been successfully sent")
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)  #icontains is bydefualt package that work is fetch all the contains of title
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request,'No search results found. Please refine your query')
    params = {'allPosts':allPosts,'query':query}
    return render(request, 'home/search.html',params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        #GEt the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Check for errorneous inputs
        # username should be under 20 characters
        if len(username) > 20:
            messages.error(request,"Username must be under 20 characters")
            return redirect('home')

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('home')

        # Passswords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')



    

        # Create the  user      
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
      if request.method == 'POST':
        #GET the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged IN")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    
      return HttpResponse('404 - Not Found')

def handleLogout(request):
    
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
    
