import dash_core_components as dcc
import json
with open('heroes.json', 'rb') as f:
    heroes = json.load(f)
lvls = range(1,13)

lvl= dcc.Dropdown(id='lvl',
        options = [{'label':x,'value':x } for x in lvls],
        value=1
    ),


heroeDw = dcc.Dropdown(id='miHeroeDw',
        options = [{'label':x,'value':x } for x in heroes],
        value="Pudge",
        clearable=False
    ),
enemigo1 = dcc.Dropdown(id='enemigo1',
 options = [{'label':x,'value':x } for x in heroes],
        value="Mirana",
        clearable=False
    ),
enemigo2 = dcc.Dropdown(id='enemigo2',
 options = [{'label':x,'value':x } for x in heroes],
        value="Doom",
        clearable=False,
    ),
enemigo3 = dcc.Dropdown(id='enemigo3',
 options = [{'label':x,'value':x } for x in heroes],
        value="Clinkz"
    ),
enemigo4 = dcc.Dropdown(id='enemigo4',
 options = [{'label':x,'value':x } for x in heroes],
        value="Razor"
    ),
enemigo5 = dcc.Dropdown(id='enemigo5',
 options = [{'label':x,'value':x } for x in heroes],
        value="Lion"
    ),