import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pickle
import json

dir_data = "datos"
with open(f'{dir_data}/diccionario_entidad_cve.json', 'r', encoding='utf8') as jsfile:
    dicc_ent_cve = json.load(jsfile)
    dicc_cve_ent = {v: k for k, v in dicc_ent_cve.items()}


with open(f'{dir_data}/dicc_scian_sectores.pkl', 'rb') as jsfile:
    dicc_scian = pickle.load(jsfile)
    dicc_nombre_scian = {v: k for k, v in dicc_scian.items()}

with open(f'{dir_data}/dicc_municipios.pkl', 'rb') as jsfile:
    dicc_cve_mun = pickle.load(jsfile)
    dicc_mun_cve = {v: k for k, v in dicc_cve_mun.items()}

norm = mpl.colors.Normalize(vmin=-30, vmax=30)


def procesa_df_comun(df: pd.DataFrame) -> pd.DataFrame:
    out = df.assign(prop_altas=lambda x: 100 * x['num_altas'] / x['total_2015'],
                    prop_bajas=lambda x: 100 * x['num_bajas'] / x['total_2015'],
                    diff=lambda x: x['prop_altas'] - x['prop_bajas'],
                    color=lambda x: x['diff'].apply(lambda y: 'green' if y > 0 else 'red')) \
        .sort_values('prop_altas', ascending=True) \
        .fillna(0)
    return out


def procesa_df_entidad(df: pd.DataFrame) -> pd.DataFrame:
    out = df.reset_index() \
        .pipe(procesa_df_comun) \
        .assign(entidad=lambda x: x['cve_ent'].map(dicc_cve_ent)) \
        .reset_index()
    return out


def procesa_df_sector(df: pd.DataFrame) -> pd.DataFrame:
    out = df.reset_index() \
        .pipe(procesa_df_comun) \
        .assign(sector=lambda x: x['sector'].add('. ').add(x['sector'].map(dicc_scian).str[0:50]).add(
        x['sector'].map(dicc_scian).str.len().gt(50).apply(lambda y: y * '...'))) \
        .reset_index()
    return out


def grafica_entidad(df: pd.DataFrame, xoffset: float = 0.2) -> plt.figure:
    fig = grafica_altas_bajas(df, entidad_sector='entidad', xoffset=xoffset)
    return fig


def grafica_sector(df: pd.DataFrame, xoffset: float = 0.2) -> plt.figure:
    fig = grafica_altas_bajas(df, entidad_sector='sector', xoffset=xoffset)
    return fig


def grafica_altas_bajas(df: pd.DataFrame, entidad_sector: str, xoffset: float = 0.2) -> plt.figure:
    fig, (ax, ax2) = plt.subplots(figsize=(10, 12), ncols=2, sharey=True,
                                  gridspec_kw={'width_ratios': [0.8, 0.2], 'wspace': 0.1})
    ax.hlines(y=df[entidad_sector], xmin=df['prop_bajas'], xmax=df['prop_altas'], color=df['color'], alpha=0.7,
              zorder=-1)
    ax.scatter(x=df['prop_bajas'], y=df[entidad_sector], color='red', alpha=1, label='2015')
    ax.scatter(x=df['prop_altas'], y=df[entidad_sector], color='green', alpha=1, label='2019')
    ax.set_title('Altas y bajas')
    ax2.barh(data=df, width='diff', y=entidad_sector, alpha=1, label='2019',
             color=plt.cm.RdYlGn(df['diff'].apply(norm)), edgecolor='k')

    ax2.set_title('Crecimiento de UE')
    ax2.set_ylabel('')
    ax.legend(['diferencia', 'Bajas', 'Altas'], loc='center right')
    ax.yaxis.grid(alpha=0.3)
    ax.xaxis.grid(alpha=0.3)
    ax.set_xlabel('Porcentaje del número de UE en 2015')
    sns.despine(left=True, bottom=True)
    xvar = 'prop_altas'
    x2var = 'diff'
    xlabeloffset = xoffset * df.loc[df[xvar] > 0.1, xvar].min()
    decimales = 1
    for index, row in df.iterrows():
        ha = 'right' if row['diff'] < 0 else 'left'
        signo = -1 if row['diff'] < 0 else 1
        text = str(round(row[xvar], decimales)) if decimales else str(int(row[xvar]))
        ax.text(x=row[xvar] + signo * xlabeloffset, y=index, s=f'{text}%', ha=ha, va='center')
        ax2.text(row[x2var] + xlabeloffset if row[x2var] > 0 else row[x2var], index,
                 str(round(row[x2var], decimales)) + '%', ha="left" if row[x2var] > 0 else 'right', va='center')
    return fig
