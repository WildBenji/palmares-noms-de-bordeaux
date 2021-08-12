import pandas as pd

import plotly.express as px


###############################################################################
###############################################################################


#full_df = pd.read_csv('full_dataset.csv')
full_df = pd.read_csv('https://raw.githubusercontent.com/WildBenji/palmares-noms-de-bordeaux/main/full_dataset.csv', encoding='utf8')


###############################################################################
###############################################################################


def create_palmares_from_full_dataset(_year, _gender, _nb):

    if _gender=='tous':
        mask = (full_df['année']==int(_year))
    else:
        mask = (full_df['année']==int(_year)) & (full_df['sexe']==str(_gender))

    data_used = full_df[mask]

    _fig_height = 300 + int(_nb) * 20  # en fonction du nombre de noms que l'on veut afficher sur l'axe Y il faut augmenter la taille de la figure

    fig = px.histogram(data_used.head(int(_nb)),
                        x="nb",
                        y="prénom",
                        width=900, 
                        height=_fig_height,
                        )

    fig.update_layout(margin=dict(
                                l=20,
                                r=20,
                                b=50,
                                t=100,
                                pad=10
                                ),
                                paper_bgcolor="darkgray",
                                title=f"Année {data_used['année'].iloc[0]}", 
                                title_x=0.5
                            )

    fig.update_xaxes(title="")
    fig.update_yaxes(title="", categoryorder='total ascending')

    fig.update_traces(hovertemplate='<i>Total %{y} : </i>' + '%{x}')

    return fig
    

###############################################################################
###############################################################################

def create_palmares_from_name(_name):

    data_used = full_df[full_df['prénom']==_name].sort_values(by='année', ascending=False)

    _nb = 25

    fig = px.histogram(data_used.head(_nb),
                        x="année",
                        y="nb",
                        width=700, 
                        height=700,
                        nbins=(len(data_used))
                        )

    fig.update_layout(margin=dict(
                                l=20,
                                r=20,
                                b=50,
                                t=100,
                                pad=10
                                ),
                                paper_bgcolor="darkgray",
                                title=f"Années où {data_used['prénom'].iloc[0]} a été dans le top 100", 
                                title_x=0.5,
                                bargap=0.1
                            )

    fig.update_xaxes(title="")
    fig.update_yaxes(title="", categoryorder='total ascending')

    fig.update_traces(hovertemplate='<i>Total année %{x} : </i>' + '%{y}',
                    xbins=dict(size=1)
                    )

    return fig
