# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import json
from pprint import pprint
import smtplib
from config import *

server = smtplib.SMTP(settings['SMTP_SERVER'], settings['SMTP_PORT'])

data_inicio = sys.argv[1]
tags = sys.argv[2].decode('utf-8').split(',')
recipient = ''
if len(sys.argv) > 3:
	recipient = sys.argv[3]

lista = json.load(open("dados/"+data_inicio+".json", 'r'))   

selecionados = []
for pl in lista:
	for tag in tags:
		#print "Checking " + tag
		if tag in pl['indexacao']:
			selecionados.append(pl)
			break #quebra caso ja tenha encontrado a lei

if selecionados:
	subject = "PLs Tramitados em " + data_inicio
	msg = "\nPLs Tramitados em " + data_inicio + " com TAGS: " + ','.join(tags) +'\n\n'
	for s in selecionados:
		msg += """:: {nome} ::
Autor: {autor}

Ementa: {ementa}
		
Último despacho: {ultimo}

#############

""".format(**s)

if recipient:
	server.ehlo()
	server.starttls()
	server.login(settings['EMAIL_USER'], settings['EMAIL_PASS'])
	server.sendmail("pedro@markun.com.br", recipient, msg.encode('utf-8'))
else:
	print msg