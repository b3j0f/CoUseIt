# coding: utf-8
"""View module."""
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from account.models import Account
from product.models import Product
from stock.models import Stock

from uuid import uuid4 as uuid

from .utils import sendemail


def basecontext(request, page='home', tableofcontents=False):
    """Get base context.

    :rtype: dict
    """
    productcount = Product.objects.count()
    stockcount = Stock.objects.count()
    accountcount = Account.objects.count()

    result = {
        'productcount': productcount, 'stockcount': stockcount,
        'accountcount': accountcount, 'page': page,
        'tableofcontents': tableofcontents,
        'next': request.GET.get('next', page),
        'host': settings.HOST, 'api': settings.API
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


def productsview(request):
    """Product view."""
    context = basecontext(request, 'products')
    context['products'] = Product.objects.all()
    return render(request, 'products.html', context=context)


def shareview(request):
    """Shared product view."""
    context = basecontext(request, 'share')


def stocksview(request):
    """Need locations view."""
    context = basecontext(request, 'stocks')
    context['stocks'] = Stock.objects.order_by('-datetime')
    return render(request, 'stocks.html', context=context)


def accountview(request):
    """Supply locations view."""
    context = basecontext(request, 'account')
    return render(request, 'acount.html', context=context)


def homeview(request):
    """Home view."""
    context = basecontext(request, 'home')

    return render(request, 'home.html', context=context)


def faqview(request):
    """Faq view."""
    context = basecontext(request, 'faq')
    return render(request, 'faq.html', context=context)


def aboutview(request):
    """about view."""
    context = basecontext(request, 'about', True)
    return render(request, 'about.html', context=context)
