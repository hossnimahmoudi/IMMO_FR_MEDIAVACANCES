# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Immobilier(Item):
	ANNONCE_LINK = Field(serializer=str)
	FROM_SITE = Field(serializer=str)
	ID_CLIENT = Field(serializer=str)
	ANNONCE_DATE = Field(serializer=str)
	ACHAT_LOC = Field(serializer=str)
	SOLD = Field(serializer=str)
	MAISON_APT = Field(serializer=str)
	CATEGORIE = Field(serializer=str)
	NEUF_IND = Field(serializer=str)
	NOM = Field(serializer=str)
	ADRESSE = Field(serializer=str)
	CP = Field(serializer=str)
	VILLE = Field(serializer=str)
	QUARTIER = Field(serializer=str)
	DEPARTEMENT = Field(serializer=str)
	REGION = Field(serializer=str)
	PROVINCE = Field(serializer=str)
	ANNONCE_TEXT = Field(serializer=str)
	ETAGE = Field(serializer=str)
	NB_ETAGE = Field(serializer=str)
	LATITUDE = Field(serializer=str)
	LONGITUDE = Field(serializer=str)
	M2_TOTALE = Field(serializer=str)
	SURFACE_TERRAIN = Field(serializer=str)
	NB_GARAGE = Field(serializer=str)
	PHOTO = Field(serializer=str)
	PIECE = Field(serializer=str)
	PRIX = Field(serializer=str)
	PRIX_M2 = Field(serializer=str)
	URL_PROMO = Field(serializer=str)
	STOCK_NEUF = Field(serializer=str)
	PAYS_AD = Field(serializer=str)
	PRO_IND = Field(serializer=str)
	SELLER_TYPE = Field(serializer=str)
	MINI_SITE_URL = Field(serializer=str)
	MINI_SITE_ID = Field(serializer=str)
	AGENCE_NOM = Field(serializer=str)
	AGENCE_ADRESSE = Field(serializer=str)
	AGENCE_CP = Field(serializer=str)
	AGENCE_VILLE = Field(serializer=str)
	AGENCE_DEPARTEMENT = Field(serializer=str)
	EMAIL = Field(serializer=str)
	WEBSITE = Field(serializer=str)
	AGENCE_TEL = Field(serializer=str)
	AGENCE_TEL_2 = Field(serializer=str)
	AGENCE_TEL_3 = Field(serializer=str)
	AGENCE_TEL_4 = Field(serializer=str)
	AGENCE_FAX = Field(serializer=str)
	AGENCE_CONTACT = Field(serializer=str)
	PAYS_DEALER = Field(serializer=str)
	FLUX = Field(serializer=str)
	SITE_SOCIETE_URL = Field(serializer=str)
	SITE_SOCIETE_ID = Field(serializer=str)
	SITE_SOCIETE_NAME = Field(serializer=str)
	SIREN = Field(serializer=str)
	SPIR_ID = Field(serializer=str)