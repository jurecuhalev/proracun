#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import re
import locale 
def thous(x):
    locale.setlocale(locale.LC_ALL, "en_AU.UTF-8") 
    return locale.format("%0.2f", float(x), True) 
    
def getColor(name):
    # if name[:3] in ['553', '554']:
    #   return '#CF1911' #dark red
    # elif name[:3] in ['555']:
    #   return '#FF0000' #red
    if name[:2] in ['55']: 
      return '#B5242E'                #dolg
    elif name[:3] in ['400', '401']:
      return '#1E4F34'                #place
    elif name[:2] in ['41']:
      return '#537B99'                #tekoci transferi
    elif name[:2] in ['43', '42']:
      return '#1E214F'                #investicije
    else:
      return '#D6BE96'                #drugo

f = open('odhodki_2010-2.txt', 'r')
import simplejson

struct = dict()
myint = None

c = 0
for line in f:
  line = line.replace('"', '')
  line = line.replace('\n','')
  data = line.split('\t')
  
  # print data
    
  if data[0].startswith('II.'):
    struct = {'id': 'nodeTop',
              'name': data[0],
              'data': {'$area': int(data[3].replace('.', '')),
                       '$color': getColor(data[0]),
                       'znesek': data[3]
                      },
              'children': []
             }
    continue
  
  if len(data[0]) == 2:
    s = {'id': 'p'+data[0],
         'name': "%s %s" % (data[0], data[1]),
         'data': {'$area': int(data[3].replace('.', '')),
                  '$color': getColor("%s %s" % (data[0], data[1])),
                  'znesek': data[3]
                 },
         'children': []
        }
        
    struct['children'].append(s)
  
  elif len(data[0]) == 3:
    s = {'id': 'p'+data[0],
         'name': "%s %s" % (data[0], data[1]),
         'data': {'$area': int(data[3].replace('.', '')),
                  '$color': getColor("%s %s" % (data[0], data[1])),
                  'znesek': data[3]
                 },
         'children': []
         
        }
        
    ch = struct['children']
    for i in ch:
      if i['id'] == 'p'+data[0][:2]:
        struct['children'][struct['children'].index(i)]['children'].append(s)
  
  elif data[0] == '':
    s = {'id': 'p'+data[1],
         'name': "%s %s" % (data[1], data[2]),
         'data': {'$area': int(data[3].replace('.', '')),
                  '$color': getColor("%s %s" % (data[1], data[2])),
                  'znesek': data[3]
                 },
         'children': []
        }

    ch = struct['children']
    for i in ch:
      if i['id'] == 'p'+data[1][:2]:
        l2i = struct['children'].index(i)
        l2ch = struct['children'][struct['children'].index(i)]['children']
        for k in l2ch:
          if k['id'] == 'p'+data[1][:3]:
            l3i = struct['children'][l2i]['children'].index(k)
            struct['children'][l2i]['children'][l3i]['children'].append(s)
    
# pprint(struct)

print """
  function init() {
      var json = """,

print simplejson.dumps(struct, ensure_ascii=True), ';' # sort_keys=True, indent=4)

print """
    TM.Squarified.implement({  
       'setColor': function(json) {  
        return json.data.$color;  
      }  
    });

    var tm = new TM.Squarified({
                //Where to inject the Treemap
                rootId: 'infovis',
                addLeftClickHandler: true,  
                addRightClickHandler: true,
                Color: {
                  allow: true,
                  minValue: 0,
                  maxValue: 100,
                  minColorValue: [0, 150, 50],
                  maxColorValue: [255, 0, 50] 
                },
                
                Tips: {
                  allow: true,
                  offsetX: 20,
                  offsetY: 20,
                  onShow: function(tip, node, isLeaf, domElement) {
                      tip.innerHTML = "<b>" + node.data.znesek + " EUR</b>";
                      }
                }
             });
            //load JSON data
    tm.loadJSON(json);
}
""".replace('', '')