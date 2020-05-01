import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go

def plot_target_lvlUno(heroe,enemigos):
    """Esta funcion permite saber cuanto daño fisico pego y me pegan para un -heroe-"""
    daños = pd.DataFrame()
    daños["%HPpego"] = round(100*((df_target_hero.loc[heroe,"BaseAttack"]-df_target_hero.loc[enemigos,"ArmorPhysical"])/(df_target_hero.loc[enemigos,"BASE HP"])),1)  

    daños["%HPmePegan"] = round(100*((df_target_hero.loc[enemigos,"BaseAttack"]-df_target_hero.loc[heroe,"ArmorPhysical"])/df_target_hero.loc[heroe,"BASE HP"]),1)

    daños["RatioPegoPegan"] = round((daños["%HPpego"]/daños["%HPmePegan"]),1)
    plot_daños(daños,heroe)

def plot_daños(df,heroe):
    layout = go.Layout(width=500,height=300,margin_b=5,title_text=heroe)
    mayor_ratio = df.sort_values(["RatioPegoPegan"],axis=0,ascending=False)
    x = mayor_ratio.index
    fig = go.Figure([go.Bar(x=x, y=mayor_ratio["%HPpego"],name="Pego"),
    go.Bar(x=x, y=mayor_ratio["%HPmePegan"],name="te Pegan"),
    go.Bar(x=x, y=mayor_ratio["RatioPegoPegan"],name="%")])
    fig.update_layout(layout)
    fig.show()

def plot_avanceLevels(dict_dfHeroes,valor,hero_actual):
    layout = go.Layout(height=300,width=1000,margin_b=5,title_text=valor,margin_t=25)
    levels = [x for x in range(1,21)]
    traces = [go.Scatter(x=levels,y=heroeDf.loc[valor,levels],name=heroeName, mode='markers',marker_size=3) for heroeName,heroeDf in dict_dfHeroes.items()]
    fig = go.Figure(data=traces)
    fig.update_layout(layout)
    fig.update_traces(marker=dict(
            symbol='x',
            size=6,
            color='black'
            ),selector={'name':hero_actual})
    fig.show()

if __name__ == "__main__":

    #Esto debe modularse despues:
    df = pd.read_json('npc_heroes.json',dtype='float')
    pd.set_option('display.max_rows', df.shape[0]-80)
    df.drop(["HeroType","SoloDesire","RequiresBabysit","ProvidesBabysit","SurvivalRating","RequiresFarm","ProvidesSetup","RequiresSetup","AttackAcquisitionRange","AttackRange","AttackCapabilities","StatusManaRegen","HeroID","Role","Rolelevels","Complexity","StatusHealthRegen","MovementSpeed"],axis=1,inplace=True)
    df.loc[:,"BaseAttackSpeed"].fillna(100,inplace=True)
    #DF QUE SE USARA PARA CALCULAR EN BASE A UN HEROE
    df_target_hero = df.copy()
    df_target_hero.set_index("Heroe",inplace=True)
    df_target_hero.loc[:,"BASE HP"] =    200 # HPBase
    df_target_hero.loc[:,"BaseAttack"] = (df_target_hero["AttackDamageMin"]+df_target_hero["AttackDamageMax"])/2 # DMG PROMEDIO

    heroe = []
    enemigos = []
    plot_daños(df,heroe)
    plot_target_lvlUno(heroe,enemigos)
