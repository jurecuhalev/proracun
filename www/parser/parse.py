#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import re
import locale 
def thous(x):
    # return re.sub(r'(\d{3})(?=\d)', r'\1,', str(x)[::-1])[::-1]
    locale.setlocale(locale.LC_ALL, "en_AU.UTF-8") 
    return locale.format("%0.2f", float(x), True) 

f = open('proracun_2010.csv', 'r')
import simplejson

struct = dict()
myint = None

c = 0
for line in f:
  line = line.replace(' "', '"')
  line = line.replace('"', '')
  line = line.replace('\n','')
  data = line.split('\t')
  
  # pprint(data)
  
  #empty lines
  if (data[0] == '') and (data[1] == ''):
    continue
    
  if data[1].startswith('Prora'):
    continue
  
  try:
    myint = int(data[0][:4])
    myint_s = str(myint)
    
    if struct.get(myint_s, None) == None:
      struct[myint_s] = {'postavke': dict(),
                         'name': data[0]}
      
  except ValueError:
    pass
    
  if data[0].startswith('Skupaj'):
    vsota = 0
    postavke = struct[myint_s]['postavke']
    for i in postavke:
      vsota += float(postavke[i]['vrednost'].replace(',', '.'))
    
    #print "vsota", vsota, struct[myint_s]['name']
    struct[myint_s]['skupaj'] = vsota
    
    myint = None
    continue
    
  if (data[0] == '') and (data[1] != ''):
    subdata_s = data[1]+str(c)
    c+=1
    
    struct[myint_s]['postavke'][subdata_s] = {'postavka_koda': data[1],
                                  'postavka_opis': data[2],
                                  'podkonto_koda': data[3],
                                  'podkonto_opis': data[4],
                                  'element_koda':  data[5],
                                  'element_opis':  data[6],
                                  'namen_koda':    data[7],
                                  'namen_opis':    data[8],
                                  'kolicina':      data[9],
                                  'cena_enote':    data[10].replace(',', '.'),
                                  'vrednost':      data[11].replace(',', '.'),
                                  'opomba':        data[12]
                                 }
    
  # pprint(struct[myint_s])
  # print '---------------'
  
#pprint(struct)

vsota = 0
for i in struct:
  vsota += struct[i]['skupaj']
  
print thous(vsota)
  
print """
  function init() {
      var json = """,

json = dict()
json['id'] = 'nodeTop'
json['name'] = 'IT Proračun 2010'
json['data'] = {'$area': vsota,
                '$color': 16,
                'skupaj': thous(vsota)}
json['children'] = list()

c = 0

for i in struct:
    data = struct[i]
    # print data
    child = dict()
    child['name'] = data['name']
    child['id'] = 'child'+str(c)
    c += 1        
    child['data'] = {'$area': data['skupaj'],
                    '$color': 5,
                    'skupaj': thous(data['skupaj'])}
    child['children'] = list()
    
    for postavka in data['postavke']:
        p = data['postavke'][postavka]
        pos_child = dict()
        pos_child['name'] = "" #p['element_opis']
        pos_child['id'] = 'child'+str(c)
        c += 1
        pos_child['data'] = {'$area': p['vrednost']}
        
        koda = int(p['element_koda'])
        
        if (koda > 10000 and koda < 80002):
          pos_child['data']['$color'] = 90; # hardware
          
        elif (koda > 100000 and koda < 100017):
          pos_child['data']['$color'] = 90; # multimedia

        elif (koda > 110007 and koda < 180011) or (koda >= 290001 and koda <= 300001) or (koda in [350002, 350003, 350004, 350007, 350008, 400014, 400015, 400018, 400022]):
          pos_child['data']['$color'] = 65; # network

        elif (koda > 190001 and koda <= 300001) or (koda in [3500005, 400006, 400012]):
          pos_child['data']['$color'] = 50; # serverji

        elif (koda >= 310001 and koda < 410007):
          pos_child['data']['$color'] = 10; # software, vzdrzevanje, licence
          
        elif (koda > 420000 and koda < 450006):
          pos_child['data']['$color'] = 30; # Zunanje storitve, izobrazevanje
          
        else:
          pos_child['data']['$color'] = 30;
        for key in p:
          pos_child['data'][key] = p[key]
          
        pos_child['data']['cena_enote'] = thous(pos_child['data']['cena_enote'])
        pos_child['data']['vrednost'] = thous(pos_child['data']['vrednost'])
                             
        pos_child['children'] = list()
      
        child['children'].append(pos_child)
    json['children'].append(child)


print simplejson.dumps(json, ensure_ascii=True), # sort_keys=True, indent=4)
print ';'

print """
    var tm = new TM.Squarified({
                //Where to inject the Treemap
                rootId: 'infovis',
                addLeftClickHandler: true,  
                addRightClickHandler: true,
                Color: {
                  allow: true,
                  minValue: 0,
                  maxValue: 100,
                  minColorValue: [0, 255, 50],
                  maxColorValue: [255, 0, 50] 
                },
                
                Tips: {
                  allow: true,
                  offsetX: 20,
                  offsetY: 20,
                  
                  onShow: function(tip, node, isLeaf, domElement) {
                    if (node.data.cena_enote) {
                      tip.innerHTML = "<b>" + node.data.namen_opis + "</b>" + "<br />" + node.data.podkonto_opis + "<br /></br >" + node.data.kolicina + ' * ' + node.data.cena_enote + ' EUR = ' + node.data.vrednost + ' EUR  <br />' + node.data.element_opis + ' (' + node.data.element_koda + ')';
                    } else {
                      tip.innerHTML = "<b>" + node.name + "</b>" + "<br />" + node.data.skupaj + ' EUR';
                    }; 
                  }
                
                }
             });
            //load JSON data
    tm.loadJSON(json);
}
""".replace('', '')

# for i in struct:
#   data = struct[i]
#   for postavka in data['postavke']:
#     p = data['postavke'][postavka]
#     print "%s %s %s" % (p['element_koda'], p['element_opis'], p['namen_opis'])