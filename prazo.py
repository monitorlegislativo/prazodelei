import urllib2
from lxml.etree import parse
import json


def getProposicoes(data_inicio, data_fim):
    data_in = data_inicio.replace('-','/')
    url = "http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesTramitadasNoPeriodo?dtInicio="+data_in+"&dtFim="+data_in
    print url
    soup = parse(urllib2.urlopen(url)).getroot()
    
    proposicoes = []
    for p in soup.xpath('//proposicao'):
        if p.xpath('./tipoProposicao')[0].text.strip() == 'PL' :
            proposicoes.append(p.xpath('./codProposicao')[0].text)

    lista = []
    for p in proposicoes:
        print "Getting proposicao " + p
        try:
            soup = parse(urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp=" + p)).getroot()
        except:
            soup = parse(urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp=" + p)).getroot()
        prop = {}
        prop['nome'] = soup.xpath('//nomeProposicao')[0].text
        prop['ultimo'] = soup.xpath('//UltimoDespacho')[0].text
        prop['ementa'] = soup.xpath('//Ementa')[0].text
        prop['autor'] = soup.xpath('//Autor')[0].text + "/" + soup.xpath('//ufAutor')[0].text + "(" + soup.xpath('//partidoAutor')[0].text.strip() + ")"
        prop['indexacao'] = [x.strip() for x in soup.xpath('//Indexacao')[0].text.split(',')]
        lista.append(prop)
    with open("dados/"+data_inicio+".json", "w") as arquivo:
        arquivo.write(json.dumps(lista, indent=4))
    return lista
