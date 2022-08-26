#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
 
# Импортируем python-модули
import ldap
 
# Задаем необходимые переменные
domain = 'dmosk.local'
base = 'DC=dmosk,DC=local'
bind_dn = f'export_emails@{domain}'
bind_dn_password = 'export_emails_12345!'
scope = ldap.SCOPE_SUBTREE
filter = "(&(mail=*))"
attrs = ['mail','proxyAddresses']
result_set = []
all_emails = []
 
# Подключаемся к глобальному каталогу по LDAP
try:
    lconn = ldap.initialize(f'ldap://{domain}:389')
    lconn.protocol_version = ldap.VERSION3
    lconn.set_option(ldap.OPT_REFERRALS, 0)
    lconn.simple_bind_s(bind_dn, bind_dn_password)
except ldap.SERVER_DOWN:
    print("Error connection to AD")
 
# Получаем результаты поиска объектов в AD
ldap_result_id = lconn.search_ext(base, scope, filter, attrs)
 
Все результаты поиска объектов заносим в переменную result_set
try:
  while 1:
    result_type, result_data = lconn.result(ldap_result_id, 0)
    if (result_data == []):
      break
    else:
      if result_type == ldap.RES_SEARCH_ENTRY:
        result_set.append(result_data)
except ldap.SIZELIMIT_EXCEEDED:
    print()
 
# Получаем список email-адресов и заносим его в переменную all_emails
for user in result_set:
    proxyAddresses = user[0][1].get('proxyAddresses')
    mail = user[0][1].get('mail')
    if (proxyAddresses):
        for email_b in proxyAddresses:
            email = email_b.decode("utf-8")
            all_emails.append(email.split(':')[1])
    else:
        all_emails.append(mail[0].decode("utf-8"))
 
# Получаем уникальные значения электронных адресов и заносим их в переменную unique_all_emails
unique_all_emails = list(set(all_emails))
 
# Выводим результат на экран
print(*unique_all_emails, sep = '\n')