from django.shortcuts import render,redirect
from .models import Post,Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Post,Team,About
from django.contrib import messages
from django.views import generic
# Create your views here.
from django.template import RequestContext

def home(request):
    blogs = Post.objects.all()[:3]
    team = Team.objects.all()
    context = {'blogs': blogs , 'team': team  }

    return render(request, "index.html",{'blogs': blogs})

def signup(request):    
    if request.method == 'POST':
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        if password==password2:
            if request.POST.get('username') and request.POST.get('password'):
                user=User.objects.create_user(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    username=request.POST.get('username'),
                    password=request.POST.get('password'),
                )
                
                gender = request.POST['gender']
                date_of_birth = request.POST['date_of_birth']
                profile_image = request.FILES['profile_image']
                
                profile = Profile.objects.create(
                    user_id=user.pk,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    profile_image=profile_image
                )
                profile.save()

                messages.success(request, 'User created successfully!!')
                return render(request, "user/signup.html")

            else:
                messages.error(request, 'Something went wrong')
                return render(request, "user/signup.html")
        else:
            messages.error(request, 'User doesnt match ')
            return render(request, "user/signup.html")
    else:
        return render(request, "user/signup.html") 
    # if request.method == 'POST':
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     gender = request.POST['gender']
    #     date_of_birth = request.POST['date_of_birth']
    #     profile_image = request.FILES['profile_image']
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     if User.objects.filter(username=username).exists():
    #         messages.info(request, "Username taken. choose other")
    #         return redirect('/signup')
    #     try:
    #         user = User.objects.create(first_name=first_name,last_name=last_name,username=username,password=password,gender=gender,date_of_birth=date_of_birth,profile_image=profile_image)
    #         user.save()
    #         request.session['is_loggedin'] = True
    #         request.session['user_id'] = user.id
    #         request.session['first_name'] = user.first_name
    #         request.session['last_name'] = user.last_name
    #         request.session['profile_image'] = user.profile_image.url
    #         return redirect('/')
    #     except:
    #         messages.info(request, "Can't signup right now")
    #         return redirect('/signup')
    # else:
    #     return render(request, 'user/signup.html')

def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_password_hashed = make_password(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            
            profile = Profile.objects.get(user_id=user.id)
            request.session['profile_image'] = profile.profile_image.url
            return redirect('../dashboard')
        else:
            messages.error(request, 'Incorrect credentials ')
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')

def logout(request):
    try:
        if request.session['is_loggedin'] != True:
            return redirect('/login')
        del request.session['is_loggedin']
        del request.session['user_id']
        del request.session['first_name']
        del request.session['last_name']
        del request.session['profile_image']
        return redirect('/login')
    except:
        return redirect('/login')


@login_required(login_url='/login')
def dashboard(request):
    blogs = Post.objects.filter(author=request.user)
    total_blogs = Post.objects.filter(author=request.user).count()
    total_members = Team.objects.all().count()

    context = {'profile_image': request.session['profile_image'], 'blogs': blogs, 'total_blogs': total_blogs, 'total_members': total_members}

    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/login')
def new_blog(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('tags') and request.POST.get('content') and request.FILES['thumbnail']:

            blog_author = request.user
            status = 1
            blog = Post.objects.create(
                title=request.POST.get('title'),
                tags=request.POST.get('tags'),
                content=request.POST.get('content'),
                thumbnail=request.FILES['thumbnail'],
                status=status,
                author=blog_author,
            )
            messages.success(request, 'successfully created the movie!')
            return redirect('create-blog')
        else:
            messages.error(request, 'Something went wrong ,Please try again later!')
            return redirect('create-blog')
    else:
        return render(request, 'dashboard/create-blog.html',{'profile_image': request.session['profile_image']})

@login_required(login_url='/login')
def new_team(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('title') and request.POST.get('description')  and request.FILES['profile']:

            new_member = Team.objects.create(
                name=request.POST.get('name'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                profile=request.FILES['profile'],
            )
            messages.success(request, 'You Have successfully Joined Team!')
            return redirect('new-team')
        else:
            messages.error(request, 'Something went wrong. Please try again !')
            return redirect('new-team')
    else:
        return render(request, 'dashboard/new-team.html')

@login_required(login_url='/login')

@login_required(login_url='/login')

def blogs(request):
    blog_list = Post.objects.all()
    return render(request, "blogs.html",{'blog_list': blog_list})

def blog_details(request,by):
    blogs = Post.objects.get(id=by)
    related_blogs= Post.objects.filter(tags =blogs.tags).exclude(id=blogs.id)

    context = {'blogs':blogs , 'related_blogs':related_blogs}

    return render(request,"blog_details.html",context)

def edit_blog(request,by):
    blogs = Post.objects.get(id=by)
    context = {'blogs':blogs }

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('tags') and request.POST.get('content') and request.FILES['thumbnail']:

            blog = Post.objects.filter(pk=by).update(
                title=request.POST.get('title'),
                tags=request.POST.get('tags'),
                content=request.POST.get('content'),
                thumbnail=request.FILES['thumbnail'],
            )
            messages.success(request, 'Blog Updated successfully ')
            return render(request, "dashboard/edit-blog.html", context)
        else:
            messages.error(request, 'Something went wrong ,Please try again later!')
            return render(request,"dashboard/edit-blog.html",context)
    else:
        return render(request,"dashboard/edit-blog.html",context)

def delete_blog(request,by):
    blog_to_delete = Post.objects.get(id=by)
    blog_to_delete.delete()
    messages.success(request, 'Blog Deleted successfully!')
    return redirect('dashboard')

def search_post(request):
    if request.method == 'POST':

        title = request.POST['title']
        blog_list = Post.objects.filter(title__icontains=title)
        return render(request, "blog_results.html",{'blog_list': blog_list})
    else:
        return redirect(request, 'blogs/blog_results.html')