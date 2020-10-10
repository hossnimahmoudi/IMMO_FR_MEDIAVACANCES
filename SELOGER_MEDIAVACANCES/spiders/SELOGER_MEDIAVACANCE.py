# -*- coding: utf-8 -*-
import re
import os
import scrapy
import logging
from items import Immobilier
import iso3166
from iso3166 import countries
import logging
logger = logging.getLogger()
import subprocess
from subprocess import check_output

class MediavacancesSpider(scrapy.Spider):
    name = "SELOGERMEDIAVACANCES_2020_09"
    allowed_domains = ["mediavacances.com"]
    start_urls = ['http://www.mediavacances.com/locations-vacances.php']


    def parse(self, response):
        self.pagination_page(response)

        page_count_tag = response.css('a[class="pagination_item"]:not([rel])')
        if len(page_count_tag) == 0:
            logging.info('ERROR GETTING PAGE COUNT TAG')
            return

        page_count = page_count_tag[len(page_count_tag) - 1].css(' ::text').extract_first(default='').strip()

        try:
            page_count = int(page_count)
        except ValueError:
            logging.info('ERROR GETTING PAGE COUNT : ' + page_count)
            return

        for i in range(2, int(page_count) + 1):
            link = response.url + "?cur_page=" + str(i)
            yield scrapy.Request(link, callback=self.pagination_page)

    def pagination_page(self, response):
        links_list = response.xpath("//div[contains(@class, 'property-bloc-autour')]//@href").extract()
        for link in links_list:
            if "/locations-vacances/" in link:
               yield scrapy.Request(link, callback=self.adv_page)
            

    def adv_page(self, response):
        adv = Immobilier(ANNONCE_LINK='', FROM_SITE='', ID_CLIENT='', ANNONCE_DATE='', ACHAT_LOC='', SOLD='',
                         MAISON_APT='', CATEGORIE='', NEUF_IND='', NOM='', ADRESSE='', CP='', VILLE='', QUARTIER='',
                         DEPARTEMENT='', REGION='', PROVINCE='', ANNONCE_TEXT='', ETAGE='', NB_ETAGE='', LATITUDE='',
                         LONGITUDE='', M2_TOTALE='', SURFACE_TERRAIN='', NB_GARAGE='', PHOTO='', PIECE='', PRIX='',
                         PRIX_M2='', URL_PROMO='', STOCK_NEUF='', PAYS_AD='', PRO_IND='', SELLER_TYPE='',
                         MINI_SITE_URL='', MINI_SITE_ID='', AGENCE_NOM='', AGENCE_ADRESSE='', AGENCE_CP='',
                         AGENCE_VILLE='', AGENCE_DEPARTEMENT='', EMAIL='', WEBSITE='', AGENCE_TEL='', AGENCE_TEL_2='',
                         AGENCE_TEL_3='', AGENCE_TEL_4='', AGENCE_FAX='', AGENCE_CONTACT='', PAYS_DEALER='', FLUX='',
                         SITE_SOCIETE_URL='', SITE_SOCIETE_ID='', SITE_SOCIETE_NAME='', SIREN='', SPIR_ID='')
        adv['ANNONCE_LINK'] = response.url
        adv['FROM_SITE'] = adv['ANNONCE_LINK'].split('/')[2]
        adv['ID_CLIENT'] = ''
        id_client = re.findall('[\d]+$', adv['ANNONCE_LINK'])
        if len(id_client) == 1:
            adv['ID_CLIENT'] = id_client[0]
        adv['ANNONCE_DATE'] = ''
        annonce_date = response.css(
            '#resume_proprio_reservation > div:nth-child(5) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) ::text').re(
            ':(.*)')
        if len(annonce_date) > 0:
            adv['ANNONCE_DATE'] = annonce_date[0].strip().encode('utf-8')
        adv['ACHAT_LOC'] = '8'
        adv['SOLD'] = ''
        adv['MAISON_APT'] = ''
        try:
           categorie = response.xpath("//div[contains(@class,'bloc__content')]/ul[contains(@class,'property_list2')]/li//text()").extract_first().encode('utf-8')
           if len(categorie) > 1 and "Type" in categorie:
              adv['CATEGORIE'] = categorie.replace("Type : ","")
           else:
              adv['CATEGORIE'] = ''
        except:
              pass
        adv['NEUF_IND'] = ''
        try:
           adv['NOM'] = response.css('title ::text').extract_first(default='').strip().encode('utf-8')
        except:
              pass
        adv['ADRESSE'] = ''
        """try:
          adresse = response.xpath("//div[contains(@id,'onglet_fr_nfmgn7')]//text()").extract()
          cp = re.findall("\d{5}", str(adresse))
          if len(cp) > 1:
             adv['CP'] = cp[0]
        except:
              pass"""
        try:
          adresse = response.xpath("//div[contains(@class, 'bloc background--light')]/div[contains(@class, 'bloc__content')]/ul[contains(@class, 'property_list2')]/li//text()").extract()
          adresse1 = re.findall('Commune :.*\d{5}', str(adresse))

          adv['CP'] = "".join(re.findall('\d{5}', str(adresse1)))
        except:
              pass
        try:
          adv['REGION'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(3) ::text').extract_first( default='').strip().encode('utf-8')
          adv['VILLE'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(5) ::text').extract_first(default='').strip().encode('utf-8')
          if adv['VILLE'] == "":
             adresse = response.xpath("//div[contains(@class, 'bloc background--light')]/div[contains(@class, 'bloc__content')]/ul[contains(@class, 'property_list2')]/li//text()").extract()
             adresse1 = re.findall('Commune :.*\d{5}', str(adresse))
             if len(adresse1)>0:
                adv['VILLE'] = str(adresse1).split(":")[1].split("(")[0].strip()       
             else:  
                adv['VILLE'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(3) ::text').extract_first( default='').strip().encode('utf-8')
                adv['REGION'] = ""  
        except:
              pass
        """try:
           adv['VILLE'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(5) ::text').extract_first(default='').strip().encode('utf-8')
        except:
              pass"""
        adv['QUARTIER'] = ''
        try:
           adv['DEPARTEMENT'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(4) ::text').extract_first(default='').strip().encode('utf-8')
        except:
              pass
        """try:
           adv['REGION'] = response.css('.property_list1 > li:nth-child(1) > a:nth-child(3) ::text').extract_first( default='').strip().encode('utf-8')
        except:
              pass"""
        try:
          adv['ANNONCE_TEXT'] =' '.join(response.xpath('//span[@class="traductions-text"]//text()').extract()).rstrip().encode('utf-8').replace("\r\n"," ").replace("\n","").replace("'","").replace('"','').replace(";"," ")
        except:
              pass
        adv['ETAGE'] = ''
        adv['NB_ETAGE'] = ''
        adv['LATITUDE'] = ''
        adv['LONGITUDE'] = ''
        try:
           script_line = response.css('#localisation > script:nth-child(5) ::text').extract_first(default='').split('\n')
           long_lat_list = [x.strip(' ') for x in script_line if not x.isspace() and 'var annonce_' in x]
           if len(long_lat_list) == 2:
              LONGITUDE = [x.strip(' ') for x in long_lat_list if 'var annonce_lng =' in x]
              if len(LONGITUDE) == 1:
                  LONGITUDE = LONGITUDE[0]
                  LONGITUDE = re.findall('[\d\.]+', LONGITUDE)
                  if len(LONGITUDE) == 1:
                      adv['LONGITUDE'] = LONGITUDE[0]
              LATITUDE = [x.strip(' ') for x in long_lat_list if 'var annonce_lat =' in x]
              if len(LATITUDE) == 1:
                  LATITUDE = LATITUDE[0]
                  LATITUDE = re.findall('[\d\.]+', LATITUDE)
                  if len(LATITUDE) == 1:
                     adv['LATITUDE'] = LATITUDE[0]

        except:
              pass

        adv['M2_TOTALE'] = ''
        try:
           m2_totale = response.xpath('//ul[@class="property_list2"]/li[contains(text(),"Surface habitable")]/text()').re(':[^\d]+([\d\s\.,]+)')
           if len(m2_totale) > 0:
              adv['M2_TOTALE'] = m2_totale[0].strip().encode('utf-8')
        except:
              pass
        adv['SURFACE_TERRAIN'] = ''
        try:
           surface_terrain = response.xpath('//ul[@class="property_list2"]/li[contains(text(),"Jardin")]/text()').re(':[^\d]+([\d\s\.,]+)')
           if len(surface_terrain) > 0:
              adv['SURFACE_TERRAIN'] = surface_terrain[0].encode('utf-8')
        except:
              pass
        adv['NB_GARAGE'] = ''
        adv['PHOTO'] = ''
        adv['PHOTO'] = len(response.css('div.paysage'))
        adv['PIECE'] = ''
        try:
           piece = response.xpath("//div[contains(@class,'bloc__content')]/ul[contains(@class,'property_list2')]/li//text()").extract()
           adv['PIECE'] = ' '.join(re.findall("([0-9]+) pi", str(piece)))
        except:
              pass
        try:
           prix = response.xpath("//span[contains(@class,'text--xxl')]//text()").extract_first()
           prix1 = re.findall("\d+", prix)
           if len(prix) != 0:
              adv['PRIX'] = ''.join(prix1[0].split()).encode('utf-8')

           prix_per = response.css('#prop_prix_per ::text').extract_first(default='')
           if 'nuit' in prix_per:
              adv['PRIX'] = str(int(adv['PRIX']) * 7)
        except:
              pass
        adv['PRIX_M2'] = ''
        adv['URL_PROMO'] = ''
        adv['STOCK_NEUF'] = ''
        try:
           pays = response.css('.property_list1 > li:nth-child(1) > a:nth-child(2) ::text').extract_first(default='').strip().encode('utf-8')
           nom = response.css('title ::text').extract_first(default='').strip().encode('utf-8')
           adv['PAYS_AD'] = countries.get(pays)[1]
           if "Italie" in pays or "Italie" in nom:
              adv['PAYS_AD']="IT"
           elif "Espagne" in pays or "Espagne" in nom :
               adv['PAYS_AD']="ES"
           elif "Portugal" in pays or "Portugal" in nom:
              adv['PAYS_AD']="PT"
           elif "Martinique" in pays or "Martinique" in nom :
               adv['PAYS_AD']="MQ"
           elif "Suisse" in pays or "Suisse" in nom :
               adv['PAYS_AD']="CH"
           elif "Belgique" in pays or "Belgique" in nom :
               adv['PAYS_AD']="BE"
           elif "Maurice" in pays or "Maurice" in nom :
               adv['PAYS_AD']="MU"
           elif "Ile de la Réunion" in pays or "Ile de la Réunion" in nom :
               adv['PAYS_AD']="RE"
           elif "Maroc" in pays or "Maroc" in nom :
               adv['PAYS_AD']="MA"
           elif "Croatie" in pays or "Croatie" in nom :
               adv['PAYS_AD']="HR"
           elif "Grande Terre Guadeloupe" in pays or "Grande Terre Guadeloupe" in nom :
               adv['PAYS_AD']="GP"
           elif "Sénégal" in pays or "Sénégal" in nom :
               adv['PAYS_AD']="SN"
           elif "Tunisie" in pays or "Tunisie" in nom :
               adv['PAYS_AD']="TN"
           elif "Autriche" in pays or "Autriche" in nom :
               adv['PAYS_AD']="AT"
           elif "Slovénie" in pays or "Slovénie" in nom :
               adv['PAYS_AD']="SI"
           elif "Andorre" in pays or "Andorre" in nom :
               adv['PAYS_AD']="AD"
           elif "Pays-Bas" in pays or "Pays-Bas" in nom :
               adv['PAYS_AD']="NL"
           elif "Mexique" in pays or "Mexique" in nom :
               adv['PAYS_AD']="MX"
           elif "Pologne" in pays or "Pologne" in nom :
               adv['PAYS_AD']="PL"
           elif "Grèce" in pays or "Grèce" in nom :
               adv['PAYS_AD']="GR"
           elif "Cap Vert" in pays or "Cap Vert" in nom :
               adv['PAYS_AD']="CV"

        except:
              pass
        adv['SELLER_TYPE'] = 'Part'
        adv['MINI_SITE_URL'] = ''
        adv['MINI_SITE_ID'] = ''
        try:
           adv['AGENCE_NOM'] = ' '.join(response.xpath("//div[contains(@class,'bloc__content')]/span[contains(@class,'text--lg text--fat')]//text()").extract()).encode('utf-8')
        except:
              pass
        adv['AGENCE_ADRESSE'] = ''
        adv['AGENCE_CP'] = ''
        adv['AGENCE_VILLE'] = ''
        adv['AGENCE_DEPARTEMENT'] = ''
        adv['EMAIL'] = ''
        adv['WEBSITE'] = ''
        try:
          tel = response.xpath("//div[contains(@class,'bloc-icon')]//@src").extract_first()
          if tel is not None:
             tel=tel.replace("data:image/png;base64,","")
             file = open("image.base64","a")
             file.write(tel)
             file.close()
             p = subprocess.Popen("base64 -d image.base64 > img.jpg ; convert img.jpg img.pnm ; texte=$(gocr img.pnm) ; rm img.pnm ; rm img.jpg ; rm image.base64 ; echo $texte", stdout=subprocess.PIPE, shell=True)
             out, err = p.communicate()
             telephone = out.replace("\n","")
             adv['AGENCE_TEL']= ''.join(re.findall("[0-9]+",telephone ))
         
             #os.system("base64 -d image.base64 > img.jpg ; convert img.jpg img.pnm ; texte=$(gocr img.pnm); rm img.jpg ; rm img.pnm ; rm image.base64 ")
             #adv['AGENCE_TEL'] =os.system("echo $texte")
          else:
             adv['AGENCE_TEL']=""
        except:
              pass
        """try:
          tel = response.xpath("//div[contains(@class,'bloc-icon')]//@src").extract()
          if len(tel) > 1:
            adv['AGENCE_TEL_2'] = tel[1]
          else:
             adv['AGENCE_TEL_2'] = ''
        except:
              pass"""

        adv['AGENCE_FAX'] = ''
        adv['AGENCE_CONTACT'] = ''
        adv['PAYS_DEALER'] = response.css(
            '#tel_proprio_reservation > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) ::text').extract_first(
            default='').strip().encode('utf-8')
        adv['FLUX'] = ''
        adv['SITE_SOCIETE_URL'] = ''
        adv['SITE_SOCIETE_ID'] = ''
        adv['SITE_SOCIETE_NAME'] = ''
        adv['SIREN'] = ''
        adv['SPIR_ID'] = ''
        yield adv


def get_phone1(imgstring):
    return ''

def get_phone(imgstring):
    return ''

#def try_get_phone_temchi(image, psm_para):
def try_get_phone(image, psm_para):
    return ''
