from django.shortcuts import render, HttpResponse, redirect

from app import models


# Create your views here.
def index(req):
    return render(req, "index.html")


def list(req):
    # 获取所有的出版社信息
    publisher_res = models.Publisher.objects.all().order_by("id")
    return render(req, "list.html", {'list': publisher_res})


def add(req):
    if req.method == "POST":
        name = req.POST.get('name')

        if not name:
            return render(req, "add.html", {"error": "出版社名称不能为空"})

        # 检查是否存在
        have_name = models.Publisher.objects.filter(name=name)
        if have_name:
            return render(req, "add.html", {"error": "出版社名称已存在"})

        # 添加数据到数据库
        models.Publisher.objects.create(name=name)
        return redirect("/list")

    return render(req, "add.html")


def delete(req):
    id = req.GET.get("id")
    models.Publisher.objects.filter(id=id).delete()
    return redirect("/list")


def edit(req):
    id = req.GET.get("id")
    name = req.GET.get("name")

    if req.method == "GET":
        return render(req, "edit.html", {"name": name})
    else:
        valueName = req.POST.get('name')

        dataName = models.Publisher.objects.filter(name=name)

        if dataName:
            template = {}
            template["error"] = "名称重复"
            template["name"] = name
            return render(req, "edit.html", template)
        else:
            models.Publisher.objects.filter(id=id).update(name=valueName)
            return redirect("/list")


def book(req):
    req_id = req.GET.get("id")

    if req_id:
        books = models.Book.objects.filter(publisher_id=req_id)
    else:
        books = models.Book.objects.all()

    return render(req, "book.html", {"data": books})


def book_add(req):
    # 获取传过来的参数
    name = req.POST.get("name")
    # 查询所有出版社信息
    publisher_list = models.Publisher.objects.all()
    if name:
        data = {
            "publisher": publisher_list,
            "name": name
        }
    else:
        data = {
            "publisher": publisher_list
        }

    if req.method == "POST" and not models.Book.objects.filter(name=name):
        publisher_id = req.POST.get("publisher")
        models.Book.objects.create(name=name, publisher_id=publisher_id)
        return redirect("/book")

    return render(req, "book_add.html", {"data": data})


def book_delete(req):
    id = req.GET.get("id")
    models.Book.objects.filter(id=id).delete()
    return redirect("/book")


def book_edit(req):
    id = req.GET.get("id")

    book_obj = models.Book.objects.filter(id=id)

    publisher = models.Publisher.objects.all()

    if req.method == "POST":
        book_name = req.POST.get("name")
        book_publisher = req.POST.get("publisher")
        models.Book.objects.filter(id=id).update(name=book_name, publisher=book_publisher)
        return redirect("/book")

    return render(req, "book_edit.html", {"book_obj": book_obj[0], "publisher": publisher})


def author(req):
    author = models.Author.objects.all()

    return render(req, "author.html", {"data": author})


def author_add(req):
    # 查询所有书籍数据
    book = models.Book.objects.all()

    if req.method == "POST":
        name = req.POST.get("name")
        books = req.POST.getlist("books")
        # print(req.POST)
        author_obj = models.Author.objects.create(name=name)
        author_obj.book.set(books)
        return redirect("/author")

    return render(req, "author_add.html", {"data": book})


def author_del(req):
    id = req.GET.get("id")
    models.Author.objects.filter(id=id).delete()
    return redirect("/author")


def author_edit(req):
    id = req.GET.get("id")

    author = models.Author.objects.get(id=id)

    all_books = models.Book.objects.all()

    if req.method == "POST":
        # 获取传过来的参数
        name = req.POST.get("name")
        books = req.POST.getlist("book")
        author.name = name
        author.save()

        # 修改多对多关系
        author.book.set(books)

        return redirect("/author")

    return render(req, "author_edit.html", {"author": author, "books": all_books})
