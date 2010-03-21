#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import re
import locale 
def thous(x):
    # return re.sub(r'(\d{3})(?=\d)', r'\1,', str(x)[::-1])[::-1]
    locale.setlocale(locale.LC_ALL, "en_AU.UTF-8") 
    return locale.format("%0.2f", float(x), True) 

def getColor(name):
    if name[:2] in ['50']:
      return '#B5242E' #red
    elif name[:2] in ['70']:
      return '#1E214F' # bright green
    else:
      return '#537B99' # dark green

f = open('prihodki_2010-2.txt', 'r')
import simplejson

struct = dict()
myint = None

c = 0
for line in f:
  # if line[0] == '#':
  #   continue
  
  line = line.replace('"', '')
  line = line.replace('\n','')
  data = line.split('\t')
  
  if data[0].startswith('SKUPAJ'):
    struct = {'id': 'nodeTop',
              'name': data[0],
              'data': {'$area': int(data[2].replace('.', '')),
                       '$color': getColor(data[0]),
                       'znesek': data[2]
                      },
              'children': []
             }
    continue
  
  # print data
  
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