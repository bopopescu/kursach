from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from . import models
from . import main_menu_list


# Create your views here.
@login_required
def casino(request):
    menu = []
    for i in main_menu_list.menu:
        tmp = []
        for j in i:
            if request.user.has_perm(j['pex']):
                tmp.append(j)
        menu.append(tmp)
    index = render(request, 'index.old.html', {'menu': menu})
    return index


def todo(request):
    return HttpResponse("Ты этого не сделал.... *звуки сочуствия*")

@login_required
def index(request):
    limited_client = request.user.has_perm('app.limited-client')
    full_provider = request.user.has_perm('app.full-provider')
    return render(request, 'index.html', {'user':request.user,
                                                                                    'limited_client':limited_client,
                                                                                    'full_provider':full_provider},)

@login_required
def client2(request):
    if not (request.user.has_perm('app.limited-client') or request.user.has_perm('app.full-client')):
        return HttpResponseNotFound('404')
    limited_client = request.user.has_perm('app.limited-client')
    perm = request.user.has_perm('app.full-client')
    full_provider = request.user.has_perm('app.full-provider')
    client = models.client.objects.all()
    id = request.GET.get('id')
    if id != '' and id != None:
        client = client.filter(id=id)
    full_client = request.user.has_perm('app.full-client')
    table_head = ['ID', 'ФИО', 'Адрес', 'Номер телефона', 'Баланс','','']
    return render(request, 'client/index.html', {
        'user':request.user,
        'limited_client': limited_client,
        'full_provider':full_provider,
        'client':client,
        'full-client':full_client,
        'table_head':table_head,
        'perm':perm
    })


@login_required
def client(request):
    if not (request.user.has_perm('app.limited-client') or request.user.has_perm('app.full-client')):
        return HttpResponseNotFound('404')  # TODO
    client = models.client.objects.all()
    perm = request.user.has_perm('app.full-client')
    print(type(request.user.has_perm('app.full-client')))
    context = {'perm': perm, 'client': client, }
    return render(request, 'client/client.html', context)


@login_required
def client_delete(request, id):
    if not request.user.has_perm('app.full-client'):
        return HttpResponseNotFound('404')  # TODO
    try:
        client = models.client.objects.get(id=id)
        client.delete()
    except models.client.DoesNotExist:
        return HttpResponseNotFound('<h1>Такого пользователя не существует</h1>')
    return HttpResponseRedirect('..')


@login_required
def client_change(request, id):
    if not (request.user.has_perm('app.limited-client') or request.user.has_perm('app.full-client')):
        return HttpResponseNotFound('404')  # TODO
    perm = request.user.has_perm('app.full-client')
    if request.method == 'GET':
        try:
            client = models.client.objects.get(id=id)
            return render(request, 'client/change.html', {'perm': perm, 'client': client})
        except IntegrityError:
            return HttpResponseNotFound('<h1>Такого пользователя не существует</h1>')
    elif request.method == 'POST':
        if request.user.has_perm('app.full-client'):
            FIO = request.POST.get('FIO')
            addres = request.POST.get('addres')
            phone_number = request.POST.get('phone')
            balance = float(request.POST.get('balance'))
            try:
                client = models.client.objects.get(id=id)
                if FIO != '':
                    client.FIO = FIO
                if addres != '':
                    client.addres = addres
                if phone_number != '':
                    client.phone_number = phone_number
                client.balance = balance + float(client.balance)
                client.save()
                return HttpResponseRedirect('..')
            except IntegrityError:
                return HttpResponseNotFound('<h1>Такого пользователя не существует</h1>')
        elif request.user.has_perm('app.limited-client'):
            balance = float(request.POST.get('balance'))
            phone_number = request.POST.get('phone')
            try:
                client = models.client.objects.get(id=id)
                if phone_number != '':
                    client.phone_number = phone_number
                client.balance = balance + float(client.balance)
                client.save()
                return HttpResponseRedirect('..')
            except IntegrityError:
                return HttpResponseNotFound('<h1>Такого пользователя не существует</h1>')

    else:
        return HttpResponseNotFound('Ты как из палаты сбежал, шизоид?')


@login_required
def client_create(request):
    if request.user.has_perm('app.full-client') and request.method == 'POST':
        client = models.client(FIO=request.POST.get('FIO'),
                               addres=request.POST.get('addres'),
                               phone_number=request.POST.get('phone'),
                               balance=0.00)
        client.save()
        return HttpResponseRedirect('.')
    else:
        return HttpResponseNotFound('403')  # TODO


@login_required
def provider(request):
    if not (request.user.has_perm('app.full-provider') and request.user.has_perm('app.read-service')):
        return HttpResponseNotFound('404')  # TODO
    provider = models.provider.objects.all()
    service = models.service.objects.all()
    context = {'provider': provider, 'service': service}
    return render(request, 'provider/provider.html', context)


@login_required
def provider_create(request):
    if not request.user.has_perm('app.full-provider'):
        return HttpResponseNotFound('404')
    if request.method == 'POST':
        name = request.POST.get('provider_name')
        service = request.POST.get('service')
        try:
            service = models.service.objects.get(id=service)
            provider = models.provider(provider_name=name, provide_service=service)
            provider.save()
            return HttpResponseRedirect('.')
        except models.service.DoesNotExist:
            return HttpResponseNotFound("Frgkjdfj;")  # ToDO
        except ValueError:
            return HttpResponse("Неправильный ввод")


@login_required
def provider_delete(request, id):
    if not request.user.has_perm('app.full-provider'):
        return HttpResponseNotFound('404')
    try:
        provider = models.provider.objects.get(id=id)
        provider.delete()
        return HttpResponseRedirect('..')
    except models.provider.DoesNotExist:
        return HttpResponseNotFound('404')
    return HttpResponse('Не, ну а вдруг это все таки случится?')


@login_required
def provider_change(request, id):
    if not (request.user.has_perm('app.full-provider')):
        return HttpResponseNotFound('404')  # TODO
    if request.method == 'GET':
        try:
            provider = models.provider.objects.get(id=id)
            return render(request, 'provider/change.html', {'provider': provider})
        except IntegrityError:
            return HttpResponseNotFound('<h1>Такого поставщика не существует</h1>')
    elif request.method == 'POST':
        name = request.POST.get('name')
        service_code = request.POST.get('service')
        try:
            provider = models.provider.objects.get(id=id)
            if name != '':
                provider.provider_name = name
            if service_code != '':
                provider.provide_service_id = service_code
            provider.save()
            return HttpResponseRedirect('..')
        except IntegrityError:
            return HttpResponseNotFound('<h1>Такого пользователя не существует</h1>')
    return HttpResponse('Похоже все таки это случилось')


@login_required
def service(request):
    if not (check_permission_or(request, ['app.read-service', 'full-client'])):
        return HttpResponseNotFound('404')
    sevices = models.service.objects.all()
    return render(request, 'service/service.html',
                  {'services': sevices, 'perm': request.user.has_perm('app.full-service')})


@login_required
def service_create(request):
    if not request.user.has_perm('app.full-service'):
        return HttpResponseNotFound('404')
    if request.method == 'POST':
        name = request.POST.get('name')
        cost = request.POST.get('cost')
        tarif = request.POST.get('tarif_type')
        try:
            service = models.service(service_name=name, cost=cost, tarif_type=tarif)
            service.save()
            return HttpResponseRedirect('.')
        except models.service.DoesNotExist:
            return HttpResponseNotFound("Frgkjdfj;")  # ToDO
        except ValueError:
            return HttpResponse("Неправильный ввод")


@login_required
def service_delete(request, id):
    if not request.user.has_perm('app.full-service'):
        return HttpResponseNotFound('404')
    try:
        service = models.service.objects.get(id=id)
        service.delete()
        return HttpResponseRedirect('..')
    except models.provider.DoesNotExist:
        return HttpResponseNotFound('404')


@login_required
def service_change(request, id):
    if not check_permission_or(request, ['app.full-service', 'app.read-service']):
        return HttpResponseNotFound('404')
    args = ['service_name', 'cost', 'tarif_type']
    if request.method == 'POST':
        res = [request.POST.get(x) for x in args]
        try:
            service = models.service.objects.get(id=id)
            if res[0] != '':
                service.service_name = args[0]
            if res[1] != '':
                tt = float(res[1])
                service.cost = Decimal(tt)
            if args[2] != '':
                service.tarif_type = res[2]
            service.save()
            return HttpResponseRedirect('..')
        except models.service.DoesNotExist:
            return HttpResponseNotFound('404')
    else:
        try:
            service = models.service.objects.get(id=id)
            return render(request, 'service/change.html', {'service': service, 'args': args})
        except models.service.DoesNotExist:
            return HttpResponseNotFound('404')


def rendered_service_create(request):
    if not check_permission_and(request, ['app.create-rendered-service', 'app.limited-client', 'app.read-service']):
        return HttpResponseNotFound('404')
    if request.method == 'POST':
        id_client = request.POST.get('id_client')
        id_service = request.POST.get('id_service')
        count = request.POST.get('count')
        try:

            service = models.service.objects.get(id=id_service)
            client = models.client.objects.get(id=id_client)
            sum = float(count) * float(service.cost)
            client.balance = float(client.balance) - sum
            RSO = models.rendered_service(id_client=client, id_service=service,
                                          sum=sum)
            RSO.save()
            client.save()
            return HttpResponseRedirect('.')
        except models.service.DoesNotExist:
            return HttpResponseNotFound("Такого сервиса не существует")  # ToDO
        except models.client.DoesNotExist:
            return HttpResponseNotFound("Такого клиента не существует")
        except ValueError:
            return HttpResponse("Неправильный ввод")
    else:
        service = models.service.objects.all()
        client = models.client.objects.all()
        full_provider = request.user.has_perm('app.full-provider')
        limited_client = request.user.has_perm('app.limited-client')
        full_client = request.user.has_perm('app.full-client')
        table_head = ['ID', 'Дата', 'Клиент', 'Услуга', 'Сумма']
        #return render(request, 'rendered_service/create.old.html', {'service': service, 'client': client})
        return render(request, 'rendered_service/create.html', {
            'user': request.user,
            'limited_client': limited_client,
            'full_provider': full_provider,
            'client': client,
            'full-client': full_client,
            'service': service,
            'rendered_service': rendered_service
        })

@login_required
def rendered_service(request):
    if not (check_permission_or(request, ['app.create-rendered-service', 'app.read-rendered-service', 'app.full-rendered-service']) and check_permission_and(request, ['app.limited-client', 'app.read-service']) ):
        return HttpResponseNotFound('404')
    service = models.service.objects.all()
    rendered_service = models.rendered_service.objects.all()
    limited_client = request.user.has_perm('app.limited-client')
    full_provider = request.user.has_perm('app.full-provider')
    client = models.client.objects.all()
    full_client = request.user.has_perm('app.full-client')
    table_head = ['ID', 'Дата', 'Клиент', 'Услуга', 'Сумма']
    return render(request, 'rendered_service/index.html', {
        'user': request.user,
        'limited_client': limited_client,
        'full_provider': full_provider,
        'client': client,
        'full-client': full_client,
        'table_head': table_head,
        'servce':service,
        'rendered_service':rendered_service
    })

@login_required
def provided_service(request):
    if not check_permission_and(request, ['app.full-provided-service', 'app.full-provider', 'app.read-service']):
        return HttpResponseNotFound('404')
    limited_client = request.user.has_perm('app.limited-client')
    full_client = request.user.has_perm('app.full-client')
    full_provider = request.user.has_perm('app.full-provider')
    provider = models.provider.objects.all()
    service = models.service.objects.all()
    provided_service = models.provided_service.objects.all()
    perm = request.user.has_perm('app.full-provider')
    table_head = ['ID', 'Дата', 'Поставщик', 'Услуга', 'Сумма', '']
    return render(request, 'provided_service/index.html', {'provider':provider,
                                                           'service':service,
                                                           'provided_service':provided_service,
                                                           'pern':perm,
                                                           'limited_client':limited_client,
                                                           'full_provider':full_provider,
                                                           'full_client': full_client,
                                                           'table_head':table_head})


@login_required
def provided_service_create(request):
    if not check_permission_and(request, ['app.full-provided-service', 'app.limited-client', 'app.read-service']):
        return HttpResponseNotFound('404')
    if request.method == 'POST':
        service_id = request.POST.get('service')
        provider_id = request.POST.get('provider')
        count = request.POST.get('count')
        try:

            service = models.service.objects.get(id=service_id)
            provider = models.provider.objects.get(id=provider_id)
            sum = float(count) * float(service.cost)
            RSO = models.provided_service(provider=provider, service=service,
                                          sum=sum)
            RSO.save()
            return HttpResponseRedirect('.')
        except models.service.DoesNotExist:
            return HttpResponseNotFound("Такого сервиса не существует")  # ToDO
        except models.client.DoesNotExist:
            return HttpResponseNotFound("Такого поставщика не существует")
        except ValueError:
            return HttpResponse("Неправильный ввод")
    else:
        service = models.service.objects.all()
        provider = models.provider.objects.all()
        return render(request, 'provided_service/create.html', {'service': service, 'provider': provider})

def check_permission_or(request, perms):
    perm = [request.user.has_perm(x) for x in perms]
    return True in perm


def check_permission_and(request, perms):
    perm = [request.user.has_perm(x) for x in perms]
    return not False in perm


@login_required
def pemission_check(request):
    username = request.user.username
    kk = request.user.get_all_permissions()
    return HttpResponse(username)


@login_required
def register_new_user(request):
    if request.user.is_superuser:
        if type(request.POST.get('login')) == type("str"):

            succes = True
            try:
                user = User.objects.create_user(username=request.POST.get('login'),
                                                email=request.POST.get('email'),
                                                password=request.POST.get('password'))
                user.save()
            except IntegrityError:
                return render(request, 'registration_result.html', {'result': 'Пользователь уже существует'})
            except ValueError:
                return render(request, 'registration_result.html', {'result': 'Некорректый ввод'})
            return render(request, 'registration_result.html', {'result': 'Пользователь успешно создан'})
        else:
            return render(request, 'registration.html')
    else:
        return HttpResponseNotFound("Страницы не существует(((")  # TODO


def admin(request):
    return HttpResponseRedirect('/')


@login_required
def add_permission_to_user(request):
    if not request.user.is_superuser:
        return HttpResponseNotFound("Страницы не существует(((")  # TODO
    if request.method == 'GET':
        return render(request, 'pex/get_template.html')
    else:
        login = request.POST.get('login')
        pex = request.POST.get('pex')
        act = request.POST.get('type')
        if User.objects.all().filter(username=login).exists():
            user = User.objects.get(username=login)
            if isinstance(pex, str) and isinstance(act, str):
                try:
                    if act == 'add':
                        user.user_permissions.add(pex)
                    elif act == 'remove':
                        user.user_permissions.remove(pex)
                    else:
                        return render(request, 'pex/result.html', {'user_pex': user.user_permissions.all(),
                                                                   'login': login,
                                                                   'error': 'Произошол тролленк'})
                except Exception:
                    return render(request, 'pex/result.html', {'user_pex': user.user_permissions.all(),
                                                               'login': login,
                                                               'error': 'Неверный код права'})
            return render(request, 'pex/result.html', {'user_pex': user.user_permissions.all(), 'login': login})
        else:
            return render(request, 'pex/get_template.html', {'error': 'Пользователя не существует'})


@login_required
def check_perms(request):
    if request.method == 'POST':
        return HttpResponse(request.user.has_perm(request.POST.get('pex')))
    return render(request, 'pex/chek_perms.html')


@login_required
def user(request):
    if not request.user.is_superuser:
        return HttpResponseNotFound("Страницы не существует(((")  # TODO
    users = User.objects.all()
    return render(request, 'admin/Users.html', {'users': users})


@login_required
def delete(request, id):
    if not request.user.is_superuser:
        return HttpResponseNotFound("Страницы не существует(((")
    try:
        person = User.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


def change_user(request, id):
    if not request.user.is_superuser:
        return HttpResponseNotFound("Страницы не существует(((")
    try:
        user = User.objects.get(id=id)
        if request.method == "POST":
            password = request.POST.get('password')
            user.email = request.POST.get("email")
            if password != '':
                user.set_password(password)
            user.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "admin/change.html", {"user": user})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
