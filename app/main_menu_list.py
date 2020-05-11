menu = [
        [
            {'name':"Клиенты",'url':"/client", 'pex':'app.limited-client'},
            {'name':"Поставщики",'url':"/provider", 'pex':'app.full-provider'},
            {'name':'Список услуг','url':'/service', 'pex':'app.read-service'}
        ],
        [
            {'name':'Создать оказанную услугу', 'url':'/rendered_service/create', 'pex':'app.create-rendered-service'},
            {'name':'Создать поставку', 'url':'/provided_service/create', 'pex':'app.full-provided-service'}
        ],
        [
            {'name':'Журнал услуг', 'url':'/rendered_service', 'pex':'app.read-rendered-service'},
            {'name':'Журнал поставок', 'url':'/provided_service', 'pex':'app.full-provided-service'}
        ],
        [
            {'name':'регистрация нового пользователя', 'url':'/admin/registrations', 'pex':''},
            {'name':'Права пользователей', 'url':'/admin/add_pex', 'pex':''},
            {'name':'Проверить права (не забыть удалть)', 'url':'/admin/check_perm', 'pex':''},
            {'name':'UsErSSSSSSSSSSSSSS (Не забыть переименовать)', 'url':'/admin/user', 'pex':''}
        ]
]