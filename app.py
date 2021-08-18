import pandas as pd 
import numpy as np

import plotly.express as px

import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div 

########################################################################################

full_df = pd.read_csv('https://raw.githubusercontent.com/WildBenji/palmares-noms-de-bordeaux/main/full_dataset.csv', encoding='utf8')

########################################################################################
########################################################################################


app = dash.Dash(
                __name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True
                )

app.title = "Palmarès noms de Bordeaux"

server = app.server


########################################################################################
########################################################################################


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


########################################################################################
########################################################################################


navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
    ],
    brand="Palmarès noms de Bordeaux",
    brand_href="page-1",
    color="dark",
    dark=True,
    fluid=True,
)


########################################################################################


sidebar = html.Div(
    [
        html.H1("Menu", className="display-4"),
        html.Hr(), # petite barre de séparation
        html.P(    # 2ème ligne d'informations, ici je la laisse vide
            "Recherche par", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Année", href="/page-1", id="page-1-link"),
                dbc.NavLink("Prénom", href="/page-2", id="page-2-link"),
                dbc.NavLink("À propos", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True, # Petit carré qui entoure le sous-menu choisis
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)


########################################################################################


content = html.Div(
                   id="page-content",
                   style=CONTENT_STYLE
                   )


########################################################################################


page_1 =  html.Div(children=[

    dcc.Dropdown(
        id='dropdown_years',
        options=[
            {'label' : i, 'value' : i } for i in reversed(range(1921, 2021))
        ],
        value='2020',
        searchable=True,
        style={'width': '200px',
                'margin-top': 5,
        },
        clearable=False,
        placeholder="Sélectionnez une année",       
    ),

    dcc.Dropdown(
        id='dropdown_gender',
        options=[
                 {'label': 'Tous', 'value': 'tous'},
                 {'label': 'Fille', 'value': 'female'},
                 {'label': 'Garçon', 'value': 'male'}               
                ],
        value='tous', 
        multi=False,
        searchable=True,
        clearable=False,
        style={'width': '200px',
               'margin-top': 5,
              }
    ),

    dcc.Dropdown(
        id='number_results',
        options=[
            {'label' : i, 'value' : i } for i in range(5, 101, 5)
        ],
        value='10', 
        multi=False,
        searchable=True,
        clearable=False,
        style={'width': '200px',
               'margin-top': 5,
               'margin-bottom' : 20,
              }
    ),


    dcc.Graph(
         id='palmares-fig',
         style={
                'width': '49%', 
                'vertical-align' : 'middle',
                'horizontal-align' : 'middle'
                }
     )
]
)


########################################################################################


page_2 =  html.Div(children=[

    dcc.Dropdown(
        id='dropdown_names',
        options=[
            {'label' : i, 'value' : i } for i in sorted(full_df['prénom'].unique())
        ],
        value='Benjamin',
        searchable=True,
        style = {'display': True,
                 'width' : '200px',
                 'margin-top': 5,
                # 'margin-left': 20,
                 'margin-bottom' : 20},
        clearable=False,
        placeholder="Sélectionnez une année"    
    ),

    dcc.Graph(
            id='palmares-nom-fig',
    )
 ]
)


########################################################################################


page_3 = html.Div([dcc.Markdown("""## À propos du site

Site conçu sous licence ouverte par [Benjamin Baret](https://www.linkedin.com/in/benjamin-baret-6957471bb), Data Analyst

Données publiques de la ville de Bordeaux consultables à ce [lien](https://opendata.bordeaux-metropole.fr/explore/dataset/bor_top100prenoms/information/?disjunctive.premprenom)

Site réalisé grâce à [Dash](https://plotly.com/dash/)

""")])



########################################################################################


app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)


########################################################################################

# Callback et figure update pour page 1
@app.callback(
    Output(component_id="palmares-fig", component_property="figure"),    
    # le graph à l'ID palamres-id affiche la figure générée
    [Input(component_id="dropdown_years", component_property="value"),
    Input(component_id="dropdown_gender", component_property="value"),
    Input(component_id="number_results", component_property="value")],  
    # les values des 3 dropdowns sert à retourner la figure concordante 
)


def update_figure(_year, _gender, _nb):

    if _year:

        if _gender=='tous':
            mask = (full_df['année']==int(_year))
        else:
            mask = (full_df['année']==int(_year)) & (full_df['sexe']==_gender)

        data_used = full_df[mask]  

        data_used.reset_index(drop=True, inplace=True)

        data_used.sort_values(by=['nb', 'prénom'], ascending=[False, True], inplace=True)

        print(data_used)

        _fig_height = 300 + int(_nb) * 20  # en fonction du nombre de noms que l'on veut afficher sur l'axe Y il faut augmenter la taille de la figure

        fig = px.histogram(data_used[:int(_nb)],
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
                                    title=f"Année {str(_year)}", 
                                    title_x=0.5
                                )

        fig.update_xaxes(title="")
        fig.update_yaxes(title="",
                        autorange='reversed'
                        )

        fig.update_traces(hovertemplate='<i>Total %{y} : </i>' + '%{x}')

        return fig
    

########################################################################################


# Callback et figure update pour page 2
@app.callback(
    Output(component_id="palmares-nom-fig", component_property="figure"),    
    # le graph à l'ID palamres-id affiche la figure générée
    [Input(component_id="dropdown_names", component_property="value")]

)


def update_figure_from_name(dropdown_names):

    if dropdown_names:

        data_used = full_df[full_df['prénom']==dropdown_names].sort_values(by='année', ascending=False)
        
        data_used.reset_index(drop=True, inplace=True)

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
        fig.update_yaxes(title="", 
                         )

        fig.update_traces(hovertemplate='<i>Total année %{x} : </i>' + '%{y}',
                        xbins=dict(size=1)
                        )

        return fig
    else:
        return html.Div(children=''''''),


########################################################################################


@app.callback(
    [
     Output("sidebar", "style"),
     Output("page-content", "style"),
     Output("side_click", "data"),
     ],
    [
     Input("btn_sidebar", "n_clicks")
     ],
    [
     State("side_click", "data"),
     ]
)


def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


# Ce callback utilise le pathname actuel pour activer le state du nav link a True
# l'utilisateur peut ainsi savoir sur quel page il se trouve


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input(component_id="url", component_property="pathname")]
)

def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")]
    )

def render_page_content(pathname):

    if pathname in ["/", "/page-1"]:
        return page_1
    elif pathname == "/page-2":
        return page_2
    elif pathname == "/page-3":
        return page_3
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"L'adresse {pathname} n'existe pas..."),
        ]
    )


######################################################################


if __name__ == '__main__':
    app.run_server(debug=True)