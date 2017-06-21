# coding: utf-8
"""View module."""
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.db.models import F, Sum, Q
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from account.models import Account
from common.models import (
    Product, Using, Stat, Category, Stock, Stocking, Giving, Sharing, Common,
    Currency, Condition, Providing, Service
)

from .utils import sendemail, getclientip

from uuid import uuid4 as uuid

from collections import namedtuple

import requests

_MODELSBYACTION = {
    'give': (Product, Giving),
    'share': (Product, Sharing),
    'stock': (Stock, Stocking),
    'provide': (Service, Providing)
}

CatPropValues = namedtuple(
    'CatPropValues', ('name', 'propvalues', 'display_name', 'children')
)


def getcategories(categories, types=None):
    """Get categories."""
    result = []

    for category in categories:
        propvalues = category.allpropertieswvalues

        if types is None:
            query = category.children.all()

        else:
            query = category.children.filter(types__contains=types)

        children = getcategories(categories=query, types=types)

        result.append(
            CatPropValues(
                category.name, propvalues, category.display_name, children
            )
        )

    return result


def requirelogin(func=None):
    """Decorator for requiring login."""
    page = func.__name__[:-len('view')]

    def _requirelogin(request, *args, **kwargs):
        """Local require login."""
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)

        else:
            nextpage = '/{0}'.format(page)
            if 'action' in kwargs:
                nextpage = '/{0}{1}'.format(kwargs['action'], nextpage)
            return redirect('/login?next={0}'.format(nextpage))

    return _requirelogin


def basecontext(request, page='home', action=None, tableofcontents=False):
    """Get base context.

    :rtype: dict
    """
    productcount = Product.objects.count()
    stockcount = Stock.objects.count()
    accountcount = Account.objects.count()

    categories = []

    commontype = 'stock' if action == 'stock' else 'product'

    query = Category.objects.filter(
        types__contains=commontype, parent__isnull=True
    )

    categories = getcategories(categories=query, types=commontype)
    currencies = Currency.objects.all()

    if 'next' in request.GET:
        nextpage = request.GET['next']

    else:
        nextpage = '/{0}'.format(page)
        if action:
            nextpage = '/{0}{1}'.format(action, nextpage)

    result = {
        'action': action, 'page': page, 'next': nextpage, 'api': settings.API,
        'commontype': commontype,
        'productcount': productcount, 'stockcount': stockcount,
        'accountcount': accountcount,
        'tableofcontents': tableofcontents, 'errors': [], 'successes': [],
        'categories': categories, 'currencies': currencies,
        'DEBUG': settings.DEBUG
    }

    return result


def rendernextpage(request, context):
    """Redirect to the nextpage."""
    nextpage = context.pop('next', 'home') or 'home'
    return render(request, '{0}.html'.format(nextpage), context=context)


def loginview(request):
    """Login view."""
    email = request.POST.get('email')

    context = basecontext(request, 'login')

    result, user = None, None

    if email is not None:
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is None:
            try:
                user = User.objects.get(Q(email=email) | Q(username=email))

            except User.DoesNotExist:
                user = User(email=email, username=email)
                user.set_password(password)
                user.save()
                account = Account(user=user)
                account.save()

            else:
                user = authenticate(username=user.username, password=password)

                if user is None:
                    context['errors'] += ['Mauvais mot de passe !']
                    context['csrf_token'] = request.POST['csrfmiddlewaretoken']
                    context['email'] = email
                    user = None

    if user is None:
        result = render(request, 'login.html', context)

    else:
        login(request, user, 'django.contrib.auth.backends.ModelBackend')
        result = redirect('{0}'.format(request.GET.get('next', '')))

    return result


def logoutview(request):
    """Login view."""
    logout(request)
    return redirect('{0}'.format(request.GET.get('next', '')))


def resetpwdview(request):
    """Reset password view."""
    result = None

    lost_key = request.GET.get('lost_key', request.POST.get('lost_key'))

    context = basecontext(request, page='resetpwd')

    if lost_key is None:
        result = render(request, 'resetpwd.html', context=context)

    else:
        context['lost_key'] = lost_key

        email = request.GET.get('email', request.POST.get('email'))
        if email is None:
            context['errors'] += ['Email manquant !']
            context['page'] = 'home'
            result = render(request, 'home.html', context=context)

        else:
            context['email'] = email

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                context['errors'] += [
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

                    context['successes'] += [
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

                        context['successes'] += ['Mot de passe changé !']
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


def appcontext(request, page='home', action=None, tableofcontents=False):
    """Get app context.

    :rtype: dict
    """
    result = basecontext(
        request, page=page, action=action, tableofcontents=tableofcontents
    )
    return result


@requirelogin
def accountview(request):
    """Account locations view."""
    context = appcontext(request, page='account', tableofcontents=True)
    return render(request, 'account.html', context=context)


def homeview(request):
    """Home view."""
    context = basecontext(request, page='home')
    return render(request, 'home.html', context=context)


def getcommontype(action):
    """Get common type from action."""
    return action if action == 'stock' else 'product'


@requirelogin
def editview(request, action=None):
    """Edit view."""
    context = appcontext(
        request, page='edit', action=action, tableofcontents=True
    )

    if request.method == 'POST':
        payload = {
            'secret': settings.reCAPTCHA_SECRET_KEY,
            'remoteip': getclientip(request),
            'response': request.POST['g-recaptcha-response']
        }
        response = requests.post(
            url='https://www.google.com/recaptcha/api/siteverify',
            data=payload
        )
        if response.json()['success']:

            commonmodel, actionmodel = _MODELSBYACTION[action]

            common = {}
            supplyings = {}

            for name in request.POST:
                value = request.POST[name]
                splittedname = name.split('-')

                splittednamelen = len(splittedname)

                if splittednamelen > 0 and splittedname[0] == 'supplying':
                    name = splittedname[0]

                    if name == 'common':
                        attr = splittedname[1]
                        common[attr] = splittedname[2]

                    elif name == 'supplying':
                        supplying = supplyings.setdefault(
                            splittedname[1], {
                                'id': splittedname[1],
                                'conditions': {}
                            }
                        )

                        if splittedname[2] == 'condition':
                            condition = supplying['conditions'].setdefault(
                                splittedname[3], {'id': splittedname[3]}
                            )
                            condition[splittedname[4]] = value

                        else:
                            supplying[splittedname[3]] = value

            commonmodel.update_or_create(id=common['id'], **common)

            for supplyid in supplyings:
                supply = supplyings[supplyid]
                conditions = supply.pop('conditions')

                actionmodel.update_or_create(id=supplyid, **supply)

                for conditionid in conditions:
                    condition = conditions[conditionid]

                    Condition.update_or_create(id=conditionid, **condition)

            commons = []

            if request.POST['addnew']:
                commonid = request.POST['common-id']

                model = globals()[getcommontype(action).title()]

                if commonid is None:
                    common = model()

                else:
                    common = model.objects.get(id=commonid)

                def setattrs(*attrs, **kwargs):
                    """Set attrs to the common."""
                    for attr in attrs:
                        value = request.POST['common-{0}'.format(attr)]
                        setattr(common, attr, value)

                    for kwarg in kwargs:
                        value = request.POST['common-{0}'.format(attr)]
                        try:
                            value = kwargs[kwarg](value)
                        except TypeError:
                            continue
                        else:
                            setattr(common, kwarg, value)

                setattrs(
                    'name', 'description', 'shortdescription', 'owners',
                    'suppliers', 'users', 'category', 'professional', 'medias',
                    'quantity', 'tostock', 'category'
                )
                if model is Stock:
                    setattr('pamount', 'pcategory')

                model.save()
                commons.append(model)

                # get common information
            selection = request.POST['selection'].split(',')

            commons += list(Common.objects.filter(id__in=selection))

            category = request.POST['category']
            name = request.POST['name']
            quantity = request.POST['quantity']

            common.category = category
            common.quantity = quantity

        else:
            context['errors'] += [
                'Veuillez ne pas utiliser de robot'
            ]

    return render(request, 'edit.html', context=context)


def faqview(request):
    """Faq view."""
    context = basecontext(request, page='faq')
    return render(request, 'faq.html', context=context)


def aboutview(request):
    """About view."""
    context = basecontext(request, page='about', tableofcontents=True)
    return render(request, 'about.html', context=context)


def searchview(request, action):
    """Search view."""
    model = _MODELSBYACTION[action]
    commons = model.objects.all()
    context = appcontext(
        request, page='search', action=action, tableofcontents=True
    )
    context['commons'] = commons
    return render(request, 'search.html', context=context)


def statsview(request):
    """Stat view."""
    context = basecontext(request, page='stats', tableofcontents=True)
    context['stats'] = Stat.objects.all()
    context['ownercount'] = Account.objects.filter(ownes=None).count()
    context['suppliercount'] = Account.objects.filter(supplies=None).count()
    context['usercount'] = Account.objects.filter(uses=None).count()
    context['duration'] = Using.objects.all().aggregate(
        duration=Sum(F('endts') - F('startts'))
    )['duration']
    return render(request, 'stats.html', context=context)


def quicksearchview(request):
    """Quick search view."""
    action = request.GET['action']
    what = request.GET['what']
    where = request.GET['where']
    when = request.GET['when']

    context = appcontext(
        request, page='search', action=action, tableofcontents=True
    )
    context['what'] = what
    context['where'] = where
    context['when'] = when
    return render(request, 'search.html', context=context)
