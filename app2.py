import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output
from dropdowns import heroeDw,enemigo1,enemigo2,enemigo3,enemigo4,enemigo5
from plotly.subplots import make_subplots

with open('heroes.json', 'rb') as f:
    heroes = json.load(f)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

niveles = [x for x in range(1,13)]
value1='Doom'
print(niveles)

Dmg = go.Figure(data=[],)
HP = go.Figure(data=[],)
EHP = go.Figure(data=[],)
DmgToEnemy = go.Figure(data=[],)
DmgToPick = go.Figure(data=[],)

creep_melee_hp = 550
creep_mele_armor = 2
creep_ranged_hp = 300
creep_ranged_armor = 0
creeps = go.Figure(data=[go.Bar(x=[550],y=[1],showlegend = False,orientation='h',name='creepMeele'),
                        go.Bar(x=[300],y=[2],showlegend = False,orientation='h',name='creepRanged'),
                        go.Bar(x=[0,0],y=[1,2],showlegend = False,orientation='h',name='pick')],)
creeps.update_layout(barmode='stack',barnorm='fraction',yaxis_tickvals=[1,2],xaxis_tickvals=[])

dmg_graf = dcc.Graph(id='dmg-graf',figure=Dmg)
hp_graf = dcc.Graph(id='hp-graf',figure=HP)
ehp_graf = dcc.Graph(id='ehp-graf',figure=EHP)
dmgToEnemy_graf = dcc.Graph(id='dmgToEnemy-graf',figure=DmgToEnemy)
dmgToPick_graf = dcc.Graph(id='dmgToPick-graf',figure=DmgToPick)
creeps_graf = dcc.Graph(id='creeps-graf',figure=creeps,style={'width':280,'height':250})


app.layout = html.Div(id='Todo',children=[
    dbc.Row(html.H1(children='Dota2')),
    dbc.Row([dbc.Col(heroeDw),dbc.Col(enemigo1),dbc.Col(enemigo2),dbc.Col(enemigo3),dbc.Col(enemigo4),dbc.Col(enemigo5)]),
    dbc.Row([dbc.Col(creeps_graf),dbc.Col([])]),
    dbc.Row([dbc.Col(dmg_graf,width=4),dbc.Col(dmgToEnemy_graf,width=4),dbc.Col(dmgToPick_graf,width=4)]),
    dbc.Row([dbc.Col(ehp_graf,width=4),dbc.Col(hp_graf,width=4)]),
    dbc.Row(html.H1(id="hide",)),    
])


@app.callback(
    [Output('dmg-graf','figure'),Output('hp-graf','figure'),Output('ehp-graf','figure'),Output('dmgToEnemy-graf','figure'),Output('dmgToPick-graf','figure'),Output('creeps-graf','figure')],
    [Input('miHeroeDw', 'value'),Input('enemigo1', 'value'),Input('enemigo2', 'value'),Input('enemigo3', 'value'),Input('enemigo4', 'value'),Input('enemigo5', 'value'),])
def display_output(pick,value2,value3,value4,value5,value6):

    level=1
    dmg_l =go.Layout(title_text='Dmg')
    dmgToEnemy_l =go.Layout(title_text='DmgToEnemy')
    dmgToPick_l =go.Layout(title_text='DmgToPick')
    hp_l =go.Layout(title_text='HP')
    ehp_l = go.Layout(title_text='EHP')
    enemigos = [value2,value3,value4,value5,value6]
     #ATK
    dmg = {}
    dmgToPick = {}
    dmgPickToEnemy = {}
    primary_pick = heroes[pick]['AtributoPrimario']
    dmg[pick] = [(heroes[pick]["BaseAttack"] + heroes[pick][primary_pick]["Gain"]*x) for x in range(1,31)]
    print(dmg[pick][level])
    creeps.update_traces(marker_color='green')
    creeps.update_traces(y=[1,2],x=[dmg[pick][level],dmg[pick][level]],marker_color='red',selector={'name':'pick'})

    for enemigo in enemigos:
        primary = heroes[enemigo]['AtributoPrimario']
        dmg[enemigo] = [(heroes[enemigo]["BaseAttack"] + heroes[enemigo][primary]["Gain"]*x) for x in range(1,31)]
        dmgToPick[enemigo] = [(heroes[enemigo]["BaseAttack"] + heroes[enemigo][primary]["Gain"]*x)*heroes[pick]["Dmg Mult"][f'{x}'] for x in range(1,31)]
        dmgPickToEnemy[enemigo] = [(heroes[pick]["BaseAttack"] + heroes[pick][primary_pick]["Gain"]*x)/heroes[enemigo]["Dmg Mult"][f'{x}'] for x in range(1,31)]
    return ({'data':[go.Scatter(x=niveles, y=dmg[pick], name=pick,marker_color='black'),
    go.Scatter(x=niveles, y=dmg[value2], name=value2),
    go.Scatter(x=niveles, y=dmg[value3], name=value3),
    go.Scatter(x=niveles, y=dmg[value4], name=value4),
    go.Scatter(x=niveles, y=dmg[value5], name=value5),
    go.Scatter(x=niveles, y=dmg[value6], name=value6),
    ],'layout':dmg_l},{
    'data':[go.Scatter(x=niveles, y=list(heroes[pick]['HP'].values()), name=pick,marker_color='black'),
    go.Scatter(x=niveles, y=list(heroes[value2]['HP'].values()), name=value2),
    go.Scatter(x=niveles, y=list(heroes[value3]['HP'].values()), name=value3),
    go.Scatter(x=niveles, y=list(heroes[value4]['HP'].values()), name=value4),
    go.Scatter(x=niveles, y=list(heroes[value5]['HP'].values()), name=value5),
    go.Scatter(x=niveles, y=list(heroes[value6]['HP'].values()), name=value6),
    ],'layout':hp_l},
    {
    'data':[go.Scatter(x=niveles, y=list(heroes[pick]['EHP'].values()), name=pick,marker_color='black'),
    go.Scatter(x=niveles, y=list(heroes[value2]['EHP'].values()), name=value2),
    go.Scatter(x=niveles, y=list(heroes[value3]['EHP'].values()), name=value3),
    go.Scatter(x=niveles, y=list(heroes[value4]['EHP'].values()), name=value4),
    go.Scatter(x=niveles, y=list(heroes[value5]['EHP'].values()), name=value5),
    go.Scatter(x=niveles, y=list(heroes[value6]['EHP'].values()), name=value6),
    ],'layout':ehp_l},
    {'data':[go.Scatter(x=niveles, y=dmgPickToEnemy[value2], name=value2),
    go.Scatter(x=niveles, y=dmgPickToEnemy[value3], name=value3),
    go.Scatter(x=niveles, y=dmgPickToEnemy[value4], name=value4),
    go.Scatter(x=niveles, y=dmgPickToEnemy[value5], name=value5),
    go.Scatter(x=niveles, y=dmgPickToEnemy[value6], name=value6),
    ],'layout':dmgToEnemy_l},
    {'data':[go.Scatter(x=niveles, y=dmgToPick[value2], name=value2),
    go.Scatter(x=niveles, y=dmgToPick[value3], name=value3),
    go.Scatter(x=niveles, y=dmgToPick[value4], name=value4),
    go.Scatter(x=niveles, y=dmgToPick[value5], name=value5),
    go.Scatter(x=niveles, y=dmgToPick[value6], name=value6),
    ],'layout':dmgToPick_l},creeps)
@app.callback(Output('hide','children'),
    [Input('miHeroeDw', 'value'),
    Input('enemigo1', 'value'),
    Input('enemigo2', 'value'),
    Input('enemigo3', 'value'),
    Input('enemigo4', 'value'),
    Input('enemigo5', 'value'),
    ])
def calcularTabla(pick,value2,value3,value4,value5,value6):
    dmg = {}
    dmgToPick = {}
    dmgPickToEnemy = {}
    primary_pick = heroes[pick]['AtributoPrimario']
    dmg[pick] = [(heroes[pick]["BaseAttack"] + heroes[pick][primary_pick]["Gain"]*x) for x in range(1,31)]
    enemigos = [value2,value3,value4,value5,value6]
    for enemigo in enemigos:
        primary = heroes[enemigo]['AtributoPrimario']
        dmg[enemigo] = [(heroes[enemigo]["BaseAttack"] + heroes[enemigo][primary]["Gain"]*x) for x in range(1,31)]
        dmgToPick[enemigo] = [(heroes[enemigo]["BaseAttack"] + heroes[enemigo][primary]["Gain"]*x)*heroes[pick]["Dmg Mult"][f'{x}'] for x in range(1,31)]
        dmgPickToEnemy[enemigo] = [(heroes[pick]["BaseAttack"] + heroes[pick][primary_pick]["Gain"]*x)/heroes[enemigo]["Dmg Mult"][f'{x}'] for x in range(1,31)]
    enemigos.append(pick)
    heroes_list = enemigos
    nivel5 = {'dmg':[]}
    nivel10 = {'dmg':[]}
    nivel15 = {'dmg':[]}
    for heroe in heroes_list:
        nivel5['dmg'].append((heroe,dmg[heroe][4]))
        nivel10['dmg'].append((heroe,dmg[heroe][9])) 
        nivel15['dmg'].append((heroe,dmg[heroe][14])) 
    nivel5['dmg'].sort(key=lambda x:x[1])
    nivel10['dmg'].sort(key=lambda x:x[1])
    nivel15['dmg'].sort(key=lambda x:x[1])
    nivel5['dmg'].reverse()
    nivel10['dmg'].reverse()
    nivel15['dmg'].reverse()
    return "DMG 5: "+str(nivel5['dmg']).replace("('","").replace("',",":").replace(")","")
if __name__ == '__main__':
    # pass
    app.run_server(debug=True)