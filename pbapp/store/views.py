from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout


from .forms import Register, ParagraphErrorList, SearchProduct, LogIn
from .request_.offs_req import AllRequests
from .models import ProductsNutriTypeA, Favorite

# Create your views here.


def index(request):
    """Display index page"""
    form = SearchProduct()
    context = {'form':form}
    print('ici index')
    return render(request, 'store/index.html', context)


def login_(request):
    """display register or login"""
    form = SearchProduct()
    if request.method == 'POST':
        form = Register(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            emailUser = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            user = User.objects.create_user(username=name, email=emailUser, password=passwd)
            user.save()
            return HttpResponseRedirect('store/index.html')
    elif not request.user.id:
        forml = Register()
        formlg = LogIn()
        context = {

            'forml': forml,
            'register': False,
            'formlg': formlg,
            'form': form,
            'logEr': False
        }
        return render(request, 'store/login.html', context)
    else:
        user = request.user.id
        detUser = get_object_or_404(User, pk=user)
        name = detUser.username
        mail = detUser.email
        context = { 'user': name,
                    'mail': mail,
                    'register': True,
                    'form': form
                    }
        return render(request, 'store/login.html', context)


def connect_user(request):
    if request.method == 'POST':
        form = LogIn(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            passwd = form.cleaned_data['passwd']
            user = authenticate(username=name, password=passwd)
            if user is None:
                print('invalid')
                forml = Register()
                formlg = LogIn()
                form = SearchProduct()
                context = {
                    'logEr': True,
                    'forml': forml,
                    'formlg': formlg,
                    'form': form
                }
                return render(request, 'store/login.html', context)
            else:
                print('valid')
                login(request, user)
                return HttpResponseRedirect('store/index.html')


def search(request):
    """Display the results for the request"""
    form = SearchProduct(request.POST, error_class=ParagraphErrorList)
    if form.is_valid():
        item = form.cleaned_data['search']
        req = AllRequests()
        prd = req.search_product_item(item)
        product = prd.json()
        product = product['products'][0]
        category_ = product['pnns_groups_2']
        picture = product['image_front_url']
        name = product['product_name']
        aProducts = ProductsNutriTypeA.objects.filter(category=category_)[:33]
        formi = SearchProduct()
        context = {'product': aProducts,
                   'picture': picture,
                   'name': name,
                   'form': formi
                   }
        print('ici search')
        return render(request, 'store/result.html', context)


@login_required
def display_my_products(request):
    """display the favorite"""
    form = SearchProduct
    id_user = request.user.id
    user = get_object_or_404(User, pk=id_user)
    products = get_list_or_404(Favorite, id_user=user)
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        pProducts = paginator.get_page(page)
    except PageNotAnInteger:
        pProducts = paginator.get_page(1)
    except EmptyPage:
        pProducts = paginator.get_page(paginator.num_pages)
    for p in products:
        print(p.name)
    context = {'products': pProducts,
               'form': form
               }
    return render(request, 'store/show_products.html', context)


@login_required
def add_product_to_favorite(request, id):
    """Add product to favorite"""
    product = get_object_or_404(ProductsNutriTypeA, pk=id)
    id_user = request.user.id
    user = get_object_or_404(User, pk=id_user)
    name = product.product_name
    category = product.category
    picture = product.picture
    with transaction.atomic():
        prd = Favorite(name=name, generic_name=name, categorie=category, nutriscore='a', picture=picture,
                       id_user=user)
        prd.save()
    return render(request, 'store/index.html')


def detail(request, id):
    """Display the product detail"""
    form = SearchProduct
    product = get_object_or_404(ProductsNutriTypeA, pk=id)
    code = product.code
    req = AllRequests()
    prod = req.code_request(code)
    product = prod.json()
    filtProduct = product['product']
    try:
        pictureFicheNutri = filtProduct['selected_images']['nutrition']['display']['fr']
    except KeyError:
        pictureFicheNutri = None
    filtProduct = product['product']
    try:
        picturePrd = filtProduct['image_front_url']
    except KeyError:
        picturePrd = None
    picture_nutri_score = 'https://static.openfoodfacts.org/images/misc/nutriscore-a.svg'
    name = filtProduct['product_name']
    context = {
        'nutri_score': picture_nutri_score,
        'nutri_pic': pictureFicheNutri,
        'code': code,
        'name': name,
        'form': form,
        'picture': picturePrd
    }
    print('ok tonton')
    return render(request, 'store/detail.html', context)


def log_out(request):
    """Disconnect user"""
    logout(request)
    return HttpResponseRedirect('store/index.html')



