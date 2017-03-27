# coding: utf-8
"""View module."""
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.db.models import F, Sum, Q
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from account.models import Account
from product.models import (
    Product, Using, Stat, Share, Give, Category
)
from stock.models import Stock, Stocking

from .utils import sendemail

from uuid import uuid4 as uuid

from collections import namedtuple

CatPropValues = namedtuple('CatPropValues', ('name', 'propvalues'))


def basecontext(request, page='home', tableofcontents=False):
    """Get base context.

    :rtype: dict
    """
    productcount = Product.objects.count()
    stockcount = Stock.objects.count()
    accountcount = Account.objects.count()
    categories = Category.objects.all()

    catpropvalues = []

    for category in Category.objects.filter(parent=None):
        propvalues = category.allpropertieswvalues
        catpropvalues.append(CatPropValues(category.name, propvalues))

    result = {
        'productcount': productcount, 'stockcount': stockcount,
        'accountcount': accountcount, 'catpropvalues': catpropvalues,
        'page': page,
        'tableofcontents': tableofcontents,
        'next': request.GET.get('next', page),
        'host': settings.HOST, 'api': settings.API,
        'categories': list(categories),
        'topcategories': list(Category.objects.filter(parent=None))
    }

    return result


def rendernextpage(request, context):
    """Redirect to the nextage."""
    nextpage = context.pop('next', 'home') or 'home'
    return render(request, '{0}.html'.format(nextpage), context=context)


def loginview(request):
    """Login view."""
    username = email = request.POST.get('email')

    context = basecontext(request, 'login')

    result, user = None, None

    if email is not None:
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            try:
                user = User.objects.get(email=email, username=username)

            except User.DoesNotExist:
                user = User(email=email, username=username)
                user.set_password(password)
                user.save()
                account = Account(user=user)
                account.save()

            else:
                context['errors'] = ['Mauvais mot de passe !']
                context['csrf_token'] = request.POST['csrfmiddlewaretoken']
                context['username'] = username
                context['email'] = email
                user = None

    if user is None:
        result = render(request, 'login.html', context)

    else:
        login(request, user, 'django.contrib.auth.backends.ModelBackend')
        result = redirect('/{0}'.format(request.GET.get('next', '')))

    return result


def logoutview(request):
    """Login view."""
    logout(request)
    context = basecontext(request)
    context['successes'] = ['Vous êtes déconnecté !']
    return redirect('/{0}'.format(request.GET.get('next', '')))


def resetpwdview(request):
    """Reset password view."""
    result = None

    lost_key = request.GET.get('lost_key', request.POST.get('lost_key'))

    context = basecontext(request, 'resetpwd')

    if lost_key is None:
        result = render(request, 'resetpwd.html', context=context)

    else:
        context['lost_key'] = lost_key

        email = request.GET.get('email', request.POST.get('email'))
        if email is None:
            context['errors'] = ['Email manquant !']
            context['page'] = 'home'
            result = render(request, 'home.html', context=context)

        else:
            context['email'] = email

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                context['errors'] = [
                    'Email {0} non enregistré !'.format(email)
                ]
                context['page'] = 'home'
                result = render(request, 'home.html', context=context)

            else:
                account = user.account
                password = request.POST.get('password')

                if 'email' in request.GET:
                    result = render(request, 'resetpwd.html', context=context)

                elif password is None:
                    lost_key = str(uuid())
                    account.lost_key = lost_key
                    account.save()

                    url = '{0}/resetpwd?lost_key={1}&email={2}'.format(
                        settings.HOST, lost_key, email
                    )
                    subject = 'Réinitialiser le mot de passe de lechangement'
                    msg = 'Réinitialiser le mot de passe de : {0}'.format(url)
                    html = '<a href="{0}">Changer mot de passe !</a>'.format(
                        url
                    )
                    sendemail(subject, msg, html, email)

                    context['successes'] = [
                        'Changement de mot de passe envoyé !'.format(email)
                    ]
                    result = render(request, 'resetpwd.html', context=context)

                else:
                    context['lost_key'] = lost_key

                    if 'lost_key' in request.POST:  # reset password
                        password = request.POST['password']

                        account.user.set_password(password)
                        account.lost_key = None
                        account.save()
                        account.user.save()
                        login(
                            request, user,
                            'django.contrib.auth.backends.ModelBackend'
                        )

                        context['successes'] = ['Mot de passe changé !']
                        context['page'] = 'home'
                        result = rendernextpage(request, context=context)

                    elif 'lost_key' in request.GET:  # reset form
                        result = render(
                            request, 'resetpwd.html', context=context
                        )

    return result


def getuserid(request):
    """Get user id from input request.

    If user is authenticated, get user id. Otherwise, get
    request.COOKIES.get('userid', uuid()).
    """
    if request.user.is_authenticated():
        result = request.user.id

    else:
        result = request.COOKIES.get('userid', uuid())

    return result


def appcontext(request, page='home', tableofcontents=False):
    """Get app context.

    :rtype: dict
    """
    result = basecontext(request, page, tableofcontents)
    return result


def getproductsfromsupply(request, supplytype, query=None):
    """Get products by supply type."""
    simplename = supplytype.__name__.lower()
    return render(
        request,
        'search.html',
        context=appcontext(request, page=simplename)
    )
    basequery = Q(requests=None) | Q(requests__accepted=None)
    query = basequery if query is None else (basequery | query)

    supplyings = supplytype.objects.filter(
        query
    )
    try:
        product_ids = supplyings.distinct('supplied__id')[start: count]

    except:
        product_ids = []

        for supplying in supplyings:
            for product in supplying.supplied.all():

                if product.id not in product_ids:
                    product_ids.add(product.id)

                if len(product_ids) > (start + count):
                    break

            if len(product_ids) > (start + count):
                break

        product_ids = product_ids[start:]

    count = request.GET.get('count', 50)
    page = request.GET.get('page', 0)

    start = request.GET.get('start', 0)
    context = appcontext(request, simplename)

    total = 0
    page = start * count

    try:
        product_ids = supplyings.distinct('supplied__id')[start: count]

    except:
        product_ids = set()

        for supplying in supplyings:
            for product in supplying.supplied.all():

                if product.id not in product_ids:
                    product_ids.add(product.id)

                if len(product_ids) > (start + count):
                    break

            if len(product_ids) > (start + count):
                break

        product_ids = product_ids[start:]

    if settings.DEBUG:
        product_ids = []

        for supplying in supplyings:
            for product in supplying.supplied.all():

                if product.id not in product_ids:
                    product_ids.add(product.id)

                if len(product_ids) > (start + count):
                    break

            if len(product_ids) > (start + count):
                break

        product_ids = product_ids[start:]

    else:
        product_ids = supplyings.distinct('supplied__id')[start: count]

    query = Product.objects.filter(id__in=product_ids)

    context['pages'] = list(range(total / count))

    context['products'] = Product.objects.filter(
        id__in=product_ids
    )

    return render(request, 'search.html'.format(simplename), context=context)


def giveview(request):
    """Give view."""
    return getproductsfromsupply(request, Give)


def shareview(request):
    """Shared product view."""
    return getproductsfromsupply(request, Share)


def stockview(request):
    """Stock view."""
    return getproductsfromsupply(request, Stocking)
    context = basecontext(request, 'stock')
    context['stocks'] = Stock.objects.order_by('-datetime')
    return render(request, 'stock.html', context=context)


def accountview(request):
    """Supply locations view."""
    context = basecontext(request, 'account')
    return render(request, 'acount.html', context=context)


def homeview(request):
    """Home view."""
    context = basecontext(request, 'home', True)
    return render(request, 'home.html', context=context)


def editview(request):
    """Home view."""
    context = basecontext(request, 'edit', False)
    return render(request, 'edit.html', context=context)


def faqview(request):
    """Faq view."""
    context = basecontext(request, 'faq')
    return render(request, 'faq.html', context=context)


def aboutview(request):
    """About view."""
    context = basecontext(request, 'about', True)
    return render(request, 'about.html', context=context)


def searchview(request):
    """Search view."""
    context = basecontext(request, 'search', True)
    return render(request, 'search.html', context=context)


def statsview(request):
    """Stat view."""
    context = basecontext(request, 'stats', True)
    context['stats'] = Stat.objects.all()
    context['ownercount'] = Account.objects.filter(ownes=None).count()
    context['suppliercount'] = Account.objects.filter(supplies=None).count()
    context['usercount'] = Account.objects.filter(uses=None).count()
    context['duration'] = Using.objects.all().aggregate(
        duration=Sum(F('endts') - F('startts'))
    )['duration']
    return render(request, 'stats.html', context=context)
