from django.utils import timezone
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Project, Category, Todo, UserPortfolio, Tag, User, Team

from .forms import ProjectForm, TodoForm, UserPortfolioForm

import operator

# E-MAIL SMTP
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

# Create your views here.
def index_redirect(request):
    return redirect('/app/login/')

def index(request):
    project_list = Project.objects.order_by('-end_date').all()

    context = {'project_list':project_list}

    return render(request, 'project_app/index.html', context)

def mng_login(request):
    if request.user.is_authenticated:
        print("Registered User!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return redirect('/app/')

    return render(request, 'project_app/login.html')

def mng_personal(request):

    project_list_all = Project.objects.all()

    participation_team = []
    for project in project_list_all:
        if project.participation is not None:
            team = project.participation
            for participation in team.participation.all():
                if participation == request.user:
                    participation_team.append(team)

    participation_team = list(set(participation_team))

    project_list = Project.objects.filter(author=request.user, status=False)
    for team in participation_team:
        project_list |= Project.objects.filter(participation=team, status=False)


    todo_list = Todo.objects.filter(author=request.user)

    project_todo_list = {}

    # for project in project_list:
    #     project_todo_list_finished = []
    #     project_todo_list_not_finished = []
    #     for todo in project.todo_set.all():
    #         if todo.status==False:
    #             project_todo_list_not_finished.append(todo)
    #         else:
    #             project_todo_list_finished.append(todo)
    #
    #     if len(project_todo_list_finished) != 0 and len(project_todo_list_not_finished) != 0:
    #         project_todo_list[project] = {}
    #     if len(project_todo_list_finished) != 0:
    #         project_todo_list[project]["finished"] = project_todo_list_finished
    #     if len(project_todo_list_not_finished) != 0:
    #         project_todo_list[project]["not_finished"] = project_todo_list_not_finished


    # project's todolist counting
    finishedCountValue = 0
    for project in project_list:
        finishedCount = 0;
        notFinishedCount = 0;
        countList = []
        for todo in project.todo_set.all():
            if todo.status == True:
                finishedCount += 1
            else:
                notFinishedCount += 1
        countList.append(notFinishedCount)
        countList.append(finishedCount)
        finishedCountValue += finishedCount
        project_todo_list[project] = countList

    todo_list_dday = {}
    now = timezone.localdate()
    for todo in todo_list:
        temp = todo.end_date - now
        temp = str(temp)
        todo_list_dday[todo] = int(temp.split(',')[0].split(' ')[0])

    # for todo_key, todo_value in todo_list_dday.items():
    #     print("{}:{}".format(todo_key,todo_value))

    context = {'project_list': project_list, 'todo_list': todo_list, 'project_todo_list': project_todo_list, 'todo_list_dday': todo_list_dday, "finishedCountValue": finishedCountValue}

    return render(request, 'project_app/mng_personal.html', context)

def mng_project(request, pk):
    project_list_all = Project.objects.all()

    participation_team = []
    for project in project_list_all:
        if project.participation is not None:
            team = project.participation
            for participation in team.participation.all():
                if participation == request.user:
                    participation_team.append(team)

    participation_team = list(set(participation_team))

    project_list = Project.objects.filter(author=request.user, status=False)
    for team in participation_team:
        project_list |= Project.objects.filter(participation=team, status=False)

    pk_project = Project.objects.get(pk=pk)

    "Showing Group members - way 1"
    user_list = []
    user_list.append(request.user)
    if pk_project.participation is not None:
        team = pk_project.participation
        for participation in team.participation.all():
            user_list.append(participation)
    user_list = list(set(user_list))

    for user in user_list:
        print(user)

    category_list = pk_project.category.all()

    now = timezone.localdate()
    project_dday = pk_project.end_date - now
    project_dday = str(project_dday)
    project_dday = project_dday.split(',')[0]
    project_dday = project_dday.split('d')[0]   # Ndays

    context = {'project_list': project_list, 'pk_project': pk_project, 'category_list': category_list, 'project_dday':project_dday, 'user_list':user_list}
    return render(request, 'project_app/mng_project.html', context)

def mng_part(request,pk,category_title):
    project_list_all = Project.objects.all()

    participation_team = []
    for project in project_list_all:
        if project.participation is not None:
            team = project.participation
            for participation in team.participation.all():
                if participation == request.user:
                    participation_team.append(team)

    participation_team = list(set(participation_team))

    project_list = Project.objects.filter(author=request.user, status=False)
    for team in participation_team:
        project_list |= Project.objects.filter(participation=team, status=False)

    pk_project = Project.objects.get(pk=pk)
    pk_category = Category.objects.get(title=category_title)

    # edit - for user todo_list, author = request.user
    todo_list = Todo.objects.filter(project=pk_project, category=pk_category)

    countList = []
    notFinishedCount = 0
    finishedCount = 0
    for todo in todo_list:
        if todo.status == False:
            notFinishedCount += 1
        else:
            finishedCount += 1
    countList.append(notFinishedCount)
    countList.append(finishedCount)

    print("CountList = {}".format(countList))

    todo_list_dday = {}
    now = timezone.localdate()
    for todo in todo_list:
        temp = todo.end_date - now
        temp = str(temp)
        todo_list_dday[todo] = int(temp.split(',')[0].split(' ')[0])

    for todo_key, todo_value in todo_list_dday.items():
        print("{}:{}".format(todo_key,todo_value))

    "Showing Group members - way 2"
    # html file - direct edit

    context = {'project_list': project_list, 'pk_project': pk_project, 'pk_category': pk_category, 'todo_list': todo_list, 'todo_list_dday':todo_list_dday, "countList": countList}
    return render(request, 'project_app/mng_part.html', context)

# portfolio_1.html1
def user_portfolio(request):
    project_list_all = Project.objects.all()

    participation_team = []
    for project in project_list_all:
        if project.participation is not None:
            team = project.participation
            for participation in team.participation.all():
                if participation == request.user:
                    participation_team.append(team)

    participation_team = list(set(participation_team))

    project_list = Project.objects.filter(author=request.user)
    for team in participation_team:
        project_list |= Project.objects.filter(participation=team)

    try:
        userPortfolio = UserPortfolio.objects.get(author = request.user)
    except UserPortfolio.DoesNotExist:
        userPortfolio = None

    if userPortfolio is None:
        content = request.user.username + "입니다."
        userPortfolio = UserPortfolio(author=request.user, content = content)
        userPortfolio.save()

    context = {'project_list':project_list, 'userPortfolio':userPortfolio}
    return render(request, 'project_app/portfolio_1.html', context)

# portfolio_1.html2
def user_portfolio_detail(request, pk):
    pk_project = Project.objects.get(pk=pk)
    score = 5
    todo_list = Todo.objects.filter(project = pk_project, author = request.user)
    todo_list_count = Todo.objects.filter(project = pk_project, author = request.user).count()

    # if Todo_list's count is 0
    if todo_list_count == 0:
        redirectAddr = '/app/portfolio/'
        return redirect(redirectAddr)

    todo_dict = {}
    for todo in todo_list:
        if todo.category.__str__() not in todo_dict.keys():
            print(todo.category.__str__())
            todo_dict[todo.category.__str__()] = 0
        todo_dict[todo.category.__str__()] += 1

    # {'기획' : 4, '디자인' : 2}
    Sort = sorted(todo_dict.items(), key=operator.itemgetter(1), reverse=True)

    category_title = Sort[0][0] # 기획
    category = Category.objects.get(title = category_title)

    tag_list = Tag.objects.filter(project = pk_project, category = category, user = request.user)
    tag_dict = {}   #{'#HTML' : 5, '#CSS' : 3}
    for tag in tag_list:
        if tag.score == 0:
            continue
        tag_dict[tag.title.__str__()] = tag.score

    todo_dict = dict(Sort)

    context = {'pk_project':pk_project, 'score':score, "todo_dict":todo_dict, "tag_dict":tag_dict}
    return render(request, 'project_app/portfolio_2.html', context)


# project_edit.html
def edit_project_form(request,pk):
    pk_project = Project.objects.get(pk=pk)
    context={'pk_project':pk_project}
    return render(request, 'project_app/project_edit.html', context)

# portfolio_edit.html
def edit_userportfolio_form(request):
    userPortfolioForm = UserPortfolioForm()
    context = {'userPortfolioForm':userPortfolioForm}

    return render(request, 'project_app/portfolio_edit.html', context)

def edit_userportfolio(request):
    print("edit_userportfolio!!!")
    userPortfolio = UserPortfolio.objects.get(author=request.user)

    if (request.method == 'POST'):
        userPortfolioForm = UserPortfolioForm(request.POST)
        if userPortfolioForm.is_valid():
            userPortfolio.content = userPortfolioForm.cleaned_data['content']
            userPortfolio.save()

    redirectAddr = '/app/portfolio/'
    return redirect(redirectAddr)

# mng_personal.html 에서 complete btn 적용
def finish_todo(request, todo_pk):
    done_todo = Todo.objects.get(pk=todo_pk)
    done_todo.status = True
    done_todo.save()

    project = done_todo.project
    category = done_todo.category

    tag_title = done_todo.tag
    try:
        tag = Tag.objects.get(title=tag_title, user=request.user, project=project, category=category)
    except Tag.DoesNotExist:
        tag = None

    if tag is not None:
        tag.score += 1
        tag.save()
    else:
        print("else")

    redirectAddr = '/app/' + '#card-finished-' + str(todo_pk)
    return redirect(redirectAddr)


# mng_part.html 에서 complete btn 적용
def finish_todo_part(request,pk,category_title, todo_pk):
    done_todo = Todo.objects.get(pk=todo_pk)
    done_todo.status = True
    done_todo.save()

    project = done_todo.project
    category = done_todo.category

    tag_title = done_todo.tag
    try:
        tag = Tag.objects.get(title=tag_title, user=request.user, project=project, category=category)
    except Tag.DoesNotExist:
        tag = None

    if tag is not None:
        tag.score+=1
        tag.save()

    redirectAddr = '/app/' + str(pk) + "/" + category_title + "/" + "#card-finished-" + str(todo_pk)
    return redirect(redirectAddr)

# mng_project.html 에서 project complete btn 적용
def finish_project(request, pk):
    project = Project.objects.get(pk = pk)
    project.status = True
    project.save()
    redirectAddr = '/app/'
    return redirect(redirectAddr)

def create_project_form(request):
    project_form = ProjectForm()
    context = {"project_form": project_form}
    return render(request, 'project_app/create_project.html', context)

def create_todo_form(request, pk, category_title):
    project = Project.objects.get(pk=pk)
    category = Category.objects.get(title=category_title)
    todo_form = TodoForm(initial={'project':project, 'category':category})
    context = {"todo_form": todo_form, 'pk':pk, 'category_title':category_title}
    return render(request, 'project_app/create_todo.html', context)

def create_project(request):
    print("========================def:create_project========================")
    if request.method == "POST":
        project_form = ProjectForm(request.POST)    # Instance
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.author = request.user
            project.save()
            project_form.save_m2m() # for ManyToMany save (category)
            return redirect('/app/')
    else:
        print("else")
        return redirect('/app/')

def create_todo(request, pk, category_title):
    print("========================def:create_todo========================")
    start_date = timezone.localdate()
    project = Project.objects.get(pk=pk)
    category = Category.objects.get(title=category_title)

    if request.method =="POST":
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            todo = todo_form.save(commit=False)

            # create Tag - if Tag is exist then no create
            # if blank then todo.tag = None
            if todo.tag!="":
                tag_title = todo.tag
                try:
                    tag = Tag.objects.get(title=tag_title, project=project, category=category, user=request.user)
                except Tag.DoesNotExist:
                    tag = None
                if tag is None:
                    tag = Tag(title=tag_title, project=project, category=category, user=request.user)
                    tag.save()
            else:
                todo.tag = None

            todo.author = request.user
            todo.start_date = start_date
            todo.save()
            return redirect('/app/' + str(pk) + '/' + category_title + '/')
        else:
            print("todo_form.is_not_valid")
    else:
        print("else")
        return redirect('/app/')

# E-MAIL SMTP
def email_test(request, pk):
    pk_project = Project.objects.get(pk=pk)
    print(request.user)
    print(pk_project)

    context = {'pk_project':pk_project}
    return render(request, 'project_app/email_test_page.html', context=context)

def email_send(request, pk):

    print("========================def:email_send========================")
    pk_project = Project.objects.get(pk=pk)
    print(pk_project)

    from_user = request.user
    from_user_email = from_user.email
    print(from_user)
    print(from_user_email)


    if request.method == "POST":
        print("request.method!!!")
        email_address = request.POST['emailaddress']
        print(email_address)
        target_user = None
        try:
            target_user = User.objects.get(email=email_address)
        except User.DoesNotExist:
            print("User.DoesNotExist")
            return redirect('/app/{{pk}}/edit_project/edit_project_form/')

        current_site = get_current_site(request)
        print(current_site) # 127.0.0.1:8000

        print("target_user = {}".format(target_user))
        print("current_site.domain = {}".format(current_site.domain))
        print("urlsafe_base64_encode(force_bytes(target_user.pk)) = {}".format(urlsafe_base64_encode(force_bytes(target_user.pk))))    # Mg
        print("account_activation_token.make_token(target_user) = {}".format(account_activation_token.make_token(target_user)))  # 56l-dcdec8b0e14ff14333cf

        # send to email
        email_titleText = "Invitation Profol Project!!"
        email_bodyText = render_to_string('project_app/acc_active_email.html',{
            'user':target_user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(target_user.pk)),
            'token':account_activation_token.make_token(target_user),
            'from_user':from_user,
            'from_user_email':from_user_email,
            'pk':pk,
        })
        to_email = email_address

        email = EmailMessage(email_titleText, email_bodyText, to=[to_email])
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
    else:
        return HttpResponse('request.method is not POST')


    # email_titleText = "Invitation Profol Project!!"
    # email_bodyText = "Hello, This is invitation for joining Profol's project." \
    #                  "if you want to permit to join this project, you can click  JOIN PROJECT button." \
    #                  "Thank you."
    # email = EmailMessage(email_titleText, email_bodyText, to=['hj2_0468@naver.com'])
    # result = email.send()
    # print("result")
    # print(result)
    print("========================def:email_send:finish========================")
    return redirect('/app/{{pk}}/edit_project/edit_project_form/')

def activate(request, uidb64, token, from_user_email, pk):
    print("========================def:activate========================")
    print("from_user = {}".format(from_user_email))

    from_user = User.objects.get(email=from_user_email)
    project = Project.objects.get(pk=pk)

    print(from_user)
    print(project)

    # decode for user.pk
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    httpResponseMessage = ""
    alreadyMemberFlag = 0
    # check user, token
    if user is not None and account_activation_token.check_token(user, token):
        # team already exist.
        if project.participation is not None:
            team = project.participation
            for participation in team.participation.all():
                if participation == user:
                    print("You are memeber already.")
                    httpResponseMessage = "You are memeber already."
                    alreadyMemberFlag = 1
                    break;
            if alreadyMemberFlag == 0:
                print("successful for adding user.")
                team.participation.add(user)
                team.save()

            # just for printing
            print("team member!!!")
            for participation in team.participation.all():
                print(participation)

        # need to create team!
        else:
            print("create team start!!!")
            team = Team(status=False)
            team.save()
            team.participation.add(from_user)
            team.participation.add(user)
            team.save()
            print("create team end!!!")
            for participation in team.participation.all():
                print(participation)

            project.participation=team
            project.save()

        print("success!!")
        print("project = {}".format(project))
        print("project.team = {}".format(project.participation))
        print("project.team.member")
        team = project.participation
        for participation in team.participation.all():
            print(participation)

        # user.is_active = True
        # user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
