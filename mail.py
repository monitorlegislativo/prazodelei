# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,os
import json
from pprint import pprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import *
import prazo


if len(sys.argv)==1:
	print "Usage: mail.py 12-03-2016 palavras,chaves usuario@email.com"
	exit()

server = smtplib.SMTP(settings['SMTP_SERVER'], settings['SMTP_PORT'])

data_inicio = sys.argv[1]
tags = sys.argv[2].decode('utf-8').split(',')
recipient = ''
if len(sys.argv) > 3:
	recipient = sys.argv[3]

if os.path.isfile("dados/"+data_inicio+".json"):
	lista = json.load(open("dados/"+data_inicio+".json", 'r'))   
else:
	lista = prazo.getProposicoes(data_inicio, data_inicio)


selecionados = []
for pl in lista:
	for tag in tags:
		#print "Checking " + tag
		if tag.strip().upper() in pl['indexacao']:
			selecionados.append(pl)
			break #quebra caso ja tenha encontrado a lei

subject = "PLs tramitados em " + data_inicio
body = 'Nenhum PL tramitou com as TAGS: '+ ','.join(tags)+'\n\n'
if selecionados:
	body = "\nPLs tramitados em " + data_inicio + " com TAGS: " + ','.join(tags) +'\n\n'
	for s in selecionados:
		body += """:: {nome} ::
Autor: {autor}

Ementa: {ementa}
		
Último despacho: {ultimo}

#############

""".format(**s)
			
	
if recipient:
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = settings['EMAIL_USER']
	msg['To'] = recipient
	msg.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))

	server.ehlo()
	server.starttls()
	server.login(settings['EMAIL_USER'], settings['EMAIL_PASS'])
	server.sendmail("pedro@markun.com.br", recipient, msg.as_string())
else:
	print body