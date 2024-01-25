from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import VisitedURL, CreatedSites
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def user_authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user and user.check_password(password):
                login(request, user)
                return redirect('user_cabinet')
            if user and not user.check_password(password):
                return HttpResponse('Incorrect password')
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('user_cabinet')
    return render(request, 'single_point.html')


@login_required
def user_cabinet(request):
    statistics = VisitedURL.objects.filter(user=request.user)
    created_sites = CreatedSites.objects.filter(user=request.user)
    context = {'statistics': statistics, 'created_sites': created_sites}
    return render(request, 'user_cabinet.html', context)


@login_required
def change_attribute(request):
    if request.method == 'POST':
        value = request.POST.get('inputField')
        attribute = request.POST.get('attributeList')
        user = request.user
        setattr(user, attribute, value)
        user.save()
        return redirect('user_cabinet')
    return JsonResponse({'error': 'Invalid request method'})


def proxy_view(request, url=None):
    try:
        if request.method == 'POST':
            url = request.POST.get('url')
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://' + url
            if url.endswith('/'):
                url = url[:-1]
            visited_url_entry = VisitedURL.objects.filter(user=request.user, url=url).first()
            if visited_url_entry:
                visited_url_entry.counter += 1
                visited_url_entry.save()
            else:
                VisitedURL.objects.create(user=request.user, url=url)

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(url, href)

            if urlparse(absolute_url).netloc == urlparse(url).netloc:
                a_tag['href'] = f'http://localhost:8000/proxy/{absolute_url}'

        content_type = response.headers['content-type']
        modified_content = str(soup)
        data_sent = len(response.content)
        data_received = len(request.body)
        db_url = urlparse(url).scheme + '://' + urlparse(url).netloc
        print(urlparse(url))
        visited_url_entry = VisitedURL.objects.filter(user=request.user, url=db_url).first()
        if not visited_url_entry:
            visited_url_entry = VisitedURL.objects.create(user=request.user, url=db_url)
        visited_url_entry.data_sent += data_sent
        visited_url_entry.data_received += data_received
        if urlparse(url).path == '/' or urlparse(url).path == '':
            visited_url_entry.counter += 1
        visited_url_entry.save()

        return HttpResponse(modified_content, content_type=content_type)

    except requests.RequestException as e:
        return HttpResponse(str(e), status=500)


def create_site(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('site_url')
        CreatedSites.objects.create(user=request.user, url=url, name=name)
    return redirect('user_cabinet')
