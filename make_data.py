import json,re,pathlib
base=pathlib.Path(__file__).resolve().parent
vehicles=[
  {'id':'VSAV','name':'VSAV','subtitle':'Véhicule de secours et d’assistance aux victimes','enabled':True,'icon':'ambulance'},
  {'id':'FPT','name':'FPT','subtitle':'Fourgon pompe-tonne','enabled':False,'icon':'fire'},
  {'id':'VPSID','name':'VPSID','subtitle':'Véhicule polyvalent','enabled':False,'icon':'van'},
  {'id':'VRE','name':'VRE','subtitle':'Véhicule réserve émulseur','enabled':False,'icon':'van'},
  {'id':'CCFM','name':'CCFM','subtitle':'Camion-citerne feux de forêts moyen','enabled':False,'icon':'fire'},
  {'id':'VIM','name':'VIM','subtitle':'Véhicule intervention mousse','enabled':False,'icon':'fire'},
  {'id':'CCFL1','name':'CCFL 1','subtitle':'Camion-citerne feux de forêts léger','enabled':False,'icon':'van'}
]
data=[
('cabine','Cabine','p. 5',[ 'Classeur + plan du site', 'Carnet fiches bilan + 2 stylos', '3 GHV', '1 Projecteur', '5 Masques chirurgicaux', '1 Aniosgel', 'Triangle de pré-signalisation', 'Raclette gel', '3 Casques F2', '2 Sacs anti chute', '1 Extincteur']),
('lateral_conducteur','Latéral conducteur','p. 6',[ 'Brancard cuillère','Plan dur + support cale-tête','Chaise de transport','1 ACT','1 Bouteille B11 O₂ 3 m³','2 Cales de roue']),
('cellule','Cellule','p. 7',[ 'Brancard + support brancard','Couverture','MID','4 Attelles à dépression','Aspirateur à mucosité + 1 sonde d’aspiration','DAE','Kit brûlure','Kit membres sectionnés','2 Colliers cervicaux','2 Cales tête','Sangle araignée','Pompe','3 Boîtes de gants (M/L/XL)','3 Kits de protection risque infectieux','Valise protections airbag','Brise-vitre']),
('tiroir_1','Tiroir 1 • Cellule','p. 8',[ '3 Lunettes de protection','Kit AES']),
('tiroir_2','Tiroir 2 • Cellule','p. 9',[ '2 Masques HC adulte','2 Masques HC enfant','2 Sacs aspirateur de mucosité','1 Sonde d’aspiration','1 Sachet raccord biconique 7/10 4/7','1 Filtre PAL']),
('tiroir_3','Tiroir 3 • Cellule','p. 9',[ '1 CHU','5 Dosettes NaCl','5 Chlorexidines','10 Compresses stériles','5 Pansements américains','1 Champ stérile','2 Sparadraps','5 Petites bandes','5 Grandes bandes','1 Paire de ciseaux','1 Pince à épiler','1 Garrot tourniquet']),
('tiroir_4','Tiroir 4 • Cellule','p. 10',[ '2 Couvertures de survie','1 Poche de froid','2 Écharpes']),
('tiroir_5','Tiroir 5 • Cellule','p. 10',[ '2 Draps UU']),
('tiroir_6','Tiroir 6 • Cellule','p. 11',[ 'Boîtes de lingettes désinfectantes','Rouleau de sacs DASRI','Boîte à aiguilles','Aniospray']),
('tiroir_7','Tiroir 7 • Cellule','p. 11',[ 'Brancard souple']),
('tiroir_8','Tiroir 8 • Cellule','p. 11',[ 'Boîte de masques chirurgicaux','Boîte de masques FFP2','1 Urinal','4 Sacs vomitoires']),
('tiroir_9','Tiroir 9 • Cellule','p. 12',[ 'Kit Ambu adulte']),
('sac_avant','Sac PS • Poche avant','p. 13',[ 'Tensiomètre électrique','Brassard à tension','Stéthoscope','Oxymètre de pouls','Thermomètre','Lecteur glycémie + autopiqueurs + bandelettes + NaCl']),
('sac_droite','Sac PS • Poche de droite','p. 13',[ '5 Sacs DASRI','10 Paires de gants stériles','1 Collier cervical adulte','Boîte à aiguilles DASRI']),
('sac_gauche','Sac PS • Poche de gauche','p. 14',[ '2 Masques HC enfant','Boîte de canules de Guedel','Lot BAVU enfant','1 Collier cervical enfant']),
('sac_bleue','Sac PS • Pochette bleue','p. 14',[ 'Boîte de canules de Guedel adulte','2 Masques HC adulte','Lot BAVU adulte']),
('sac_rouge','Sac PS • Pochette rouge','p. 15',[ '5 Dosettes NaCl','5 Dosettes chlorhexidine','10 Compresses stériles','1 CHU','2 Pansements américains','1 Champ stérile','1 Garrot tourniquet','1 Sparadrap','1 Paire de ciseaux','5 Petites bandes','5 Grandes bandes']),
('sac_verte','Sac PS • Pochette verte','p. 15',[ '2 Écharpes','3 Sacs vomitoires','2 Poches de froid','2 Couvertures de survie','1 Brulstop 10 × 10 cm','1 Brulstop 20 × 20 cm','1 Brulstop 2,5 × 5 cm','1 Gel hydroalcoolique']),
]
sections=[]
for sid,title,page,labels in data:
  items=[]
  for idx,label in enumerate(labels):
    m=re.match(r'^(\d+)\s+',label)
    qty=int(m.group(1)) if m else None
    items.append({'id':f'{sid}_{idx+1:02}', 'label':label, 'quantity':qty,'active':True})
  sections.append({'id':sid,'title':title,'source':page,'items':items})
catalog={'version':1,'source':'INVENTAIRES & CONTRÔLES DU PARC VEHICULES V2.pdf, pages 3 à 16','vehicles':vehicles, 'sections':sections,'controls':{'fuel_options':['1/4','2/4','3/4','4/4'],'o2_min':0,'o2_max':10,'co_next_check':'2026-11','body_options_source':'options carrosserie VSAV illisibles dans le PDF; constat et commentaire libre'}}
out=base/'assets/catalog.json'
out.write_text(json.dumps(catalog,ensure_ascii=False,indent=2), encoding='utf-8')
print('wrote',out,'sections',len(sections),'items',sum(len(s['items']) for s in sections))
