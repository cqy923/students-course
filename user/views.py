from django.shortcuts import render

# usr/bin/env python3
# -*- coding:utf-8- -*-
import random
#
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, UpdateView

from constants import INVALID_KIND
from user.cbvs import CreateStudentView, CreateTeacherView
from user.forms import StuLoginForm, TeaLoginForm, StuRegisterForm, TeaRegisterForm, StuUpdateForm
from user.models import Student, Teacher


def home(request):
    return render(request, "user/login_home.html")


# def login(request, kind)
def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["teacher", "student","manager"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error("uid", "账号长度必须为10")
            else:
                if kind == "teacher":
                    department_no = uid[:3]
                    number = uid[3:]
                    object_set = Teacher.objects.filter(department_no=department_no, number=number)
                else:
                    grade = uid[:4]
                    number = uid[4:]
                    object_set = Student.objects.filter(grade=grade, number=number)

                if object_set.count() == 0:
                    form.add_error("uid", "该账号不存在.")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id
                        # successful login
                        # to_url = reverse("course", kwargs={'kind': kind})
                        return redirect("course", kind=kind)
            context['form'] = form
            return render(request, 'user/login_detail.html', context)
        else:
            context['form'] = form
    elif request.method == 'GET':
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            data = {"uid": uid, 'password': '12345678'}
            if kind == "teacher":
                form = TeaLoginForm(data)
            else:
                form = StuLoginForm(data)
        else:
            if kind == "teacher":
                form = TeaLoginForm()
            else:
                form = StuLoginForm()

        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

    return render(request, 'user/login_detail.html', context)

    # context = {'kind': kind}
    # if request.GET.get('uid'):
    #     uid = request.GET.get('uid')
    #     context['uid'] = uid
    #     if kind == "teacher":
    #         form = TeaLoginForm({"uid": uid, 'password': '12345678'})
    #     else:
    #         form = StuLoginForm({"uid": uid, 'password': '12345678'})
    # else:
    #     if kind == "teacher":
    #         form = TeaLoginForm()
    #     else:
    #         form = StuLoginForm()
    # context['form'] = form
    # if request.GET.get('from_url'):
    #     context['from_url'] = request.GET.get('from_url')

    # return render(request, 'user/login_detail.html', context)


def logout(request):
    for sv in ["kind", "user", "id"]:
        if request.session.get(sv):
            del request.session[sv]
    return redirect("login")
    # if request.session.get("kind", ""):
    #     del request.session["kind"]
    # if request.session.get("user", ""):
    #     del request.session["user"]
    # if request.session.get("id", ""):
    #     del request.session["id"]
    # return redirect(reverse("login"))


def register(request, kind):
    func = None
    if kind == "student":
        func = CreateStudentView.as_view()
    elif kind == "teacher":
        func = CreateTeacherView.as_view()

    if func:
        context = {
            "kind": kind
        }
        return func(request, context=context)
    else:
        return HttpResponse(INVALID_KIND)


def update(request, kind):
    func = None
    if kind == "student":
        func = UpdateStudentView.as_view()
    elif kind == "teacher":
        func = UpdateTeacherView.as_view()

    # if func:
    #     pk = request.session.get("id", "")
    #     if pk:
    #         context = {
    #             "name": request.session.get("name", ""),
    #             "kind": request.session.get("kind", ""),
    #         }
    #         return func(request, pk=pk, context=context)
    #     else:
    #         return redirect(reverse("login"))
    else:
        return HttpResponse(INVALID_KIND)
    pk = request.session.get("id", "")
    if pk:
        context = {
            "name": request.session.get("name", ""),
            "kind": request.session.get("kind", ""),
        }
        return func(request, pk=pk, context=context)
    return redirect("login")




class UpdateStudentView(UpdateView):
    model = Student
    form_class = StuUpdateForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "student"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "student"})


class UpdateTeacherView(UpdateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "teacher"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "teacher"})

