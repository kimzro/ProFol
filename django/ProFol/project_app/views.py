from django.utils import timezone


from django.shortcuts import render, redirect
from .models import Project,Category, Todo, UserPortfolio

from .forms import ProjectForm
# Create your views here.

def index_redirect(request):
    return redirect('/app/')

def index(request):
    project_list = Project.objects.order_by('-end_date').all()

    context = {'project_list':project_list}

    return render(request, 'project_app/index.html', context)

def mng_login(request):
    return render(request, 'project_app/mng_login.html')

def mng_personal(request):
    project_list = Project.objects.all()
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
    project_list = Project.objects.filter(author=request.user)
    pk_project = Project.objects.get(pk=pk)
    category_list = pk_project.category.all()

    now = timezone.localdate()
    project_dday = pk_project.end_date - now
    project_dday = str(project_dday)
    project_dday = project_dday.split(',')[0]
    project_dday = project_dday.split('d')[0]   # Ndays

    context = {'project_list': project_list, 'pk_project': pk_project, 'category_list': category_list, 'project_dday':project_dday}
    return render(request, 'project_app/mng_project.html', context)

def mng_part(request,pk,category_title):
    project_list = Project.objects.all()
    pk_project = Project.objects.get(pk=pk)
    pk_category = Category.objects.get(title=category_title)
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

    context = {'project_list': project_list, 'pk_project': pk_project, 'pk_category': pk_category, 'todo_list': todo_list, 'todo_list_dday':todo_list_dday, "countList": countList}
    return render(request, 'project_app/mng_part.html', context)

# portfolio_1.html1
def user_portfolio(request):
    project_list = Project.objects.filter(author=request.user)
    userPortfolio = UserPortfolio.objects.get(author = request.user)
    print("TEST===============================================================")
    context = {'project_list':project_list, 'userPortfolio':userPortfolio}
    return render(request, 'project_app/portfolio_1.html', context)

# portfolio_1.html2
def user_portfolio_detail(request, pk):
    pk_project = Project.objects.get(pk=pk)
    score = 5
    todo_list = Todo.objects.filter(project = pk_project)

    todo_dict = {}
    for todo in todo_list:
        if todo.category.__str__() not in todo_dict.keys():
            print(todo.category.__str__())
            todo_dict[todo.category.__str__()] = 0
        todo_dict[todo.category.__str__()] += 1


    context = {'pk_project':pk_project, 'score':score, "todo_dict":todo_dict}
    return render(request, 'project_app/portfolio_2.html', context)


def finish_todo(request, pk):
    done_todo = Todo.objects.get(pk=pk)
    done_todo.status = True
    done_todo.save()

    redirectAddr = '/app/' + '#card-finished-' + str(pk)
    return redirect(redirectAddr)

def finish_todo_part(request,pk,category_title, todo_pk):
    done_todo = Todo.objects.get(pk=todo_pk)
    done_todo.status = True
    done_todo.save()

    redirectAddr = '/app/' + str(pk) + "/" + category_title + "/" + "#card-finished-" + str(todo_pk)
    return redirect(redirectAddr)

def create_project_form(request):
    project_form = ProjectForm()
    context = {"project_form": project_form}
    return render(request, 'project_app/create_project.html', context)

def create_project(request):

    if request.method == "POST":
        print("request.method==POST")
        project_form = ProjectForm(request.POST)    # Instance
        if project_form.is_valid():
            print("project_form.is_valid")
            project = project_form.save(commit=False)
            project.author = request.user
            project.save()
            project_form.save_m2m()
            return redirect('/app/')
    else:
        print("else")
        return redirect('/app/')