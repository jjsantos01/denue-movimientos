import pandas as pd
import streamlit as st
from funciones import grafica_entidad, grafica_sector, procesa_df_sector, procesa_df_entidad, dicc_scian, dicc_cve_ent, dicc_cve_mun, dicc_mun_cve, dicc_ent_cve, dicc_nombre_scian
import base64
import io


dir_data = "datos"

vars_table_sector = ['sector', 'total_2015', 'total_2019', 'prop_bajas', 'prop_altas', 'diff']
vars_table_entidad = ['entidad', 'total_2015', 'total_2019', 'prop_bajas', 'prop_altas', 'diff']
@st.cache
def get_data_sector_entidad():
    df_sector = pd.read_pickle(f'{dir_data}/df_sec_ent.pkl')
    return df_sector


@st.cache
def get_data_sector_municipio():
    df_sector = pd.read_pickle(f'{dir_data}/df_sec_mun.pkl')
    return df_sector


def get_lnppl_logo():
    with open('images/logo.svg', 'r') as logofile:
        svg = logofile.read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    logo = r'<img src="data:image/svg+xml;base64,%s" width="400px"/>' % b64
    st.write(logo, unsafe_allow_html=True)


def render_svg(svg, width='800px'):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html_svg = r'<img src="data:image/svg+xml;base64,%s" width=%s/>' % (b64, width)
    st.write(html_svg, unsafe_allow_html=True)


df_sec_ent = get_data_sector_entidad()
df_sec_mun = get_data_sector_municipio()

# INICIA APP
# get_lnppl_logo()
grafica = st.sidebar.selectbox("Visualiza por:", ['Entidad', 'Sector', 'Municipio'], 0)

if grafica == 'Entidad':
    st.subheader('Gráfica')
    sel_ent = st.selectbox("Entidad", list(dicc_cve_ent.values()), 0)
    df_table = df_sec_ent.loc[dicc_ent_cve[sel_ent]].pipe(procesa_df_sector)
    plot = grafica_sector(df_table)
    titulo = f'Unidades económicas dadas de alta y baja entre 2015 y 2019,\n {sel_ent}'
    plot.suptitle(titulo, fontsize=14)
    svgfile = io.StringIO()
    plot.savefig(svgfile, bbox_inches='tight', format='svg')
    render_svg(svgfile.getvalue())
    st.subheader('Datos')
    st.write(df_table[vars_table_sector].sort_values('prop_altas', ascending=False).rename(columns={'diff': 'crecimiento'}))
elif grafica == "Sector":
    st.subheader('Gráfica')
    sel_sector = st.selectbox("Sector", list(dicc_nombre_scian.keys()), 0)
    df_table = df_sec_ent.xs(dicc_nombre_scian[sel_sector], axis=0, level=1).pipe(procesa_df_entidad)
    plot = grafica_entidad(df_table, xoffset=0.02)
    titulo = f'Unidades económicas dadas de alta y baja entre 2015 y 2019,\n sector {sel_sector}'
    plot.suptitle(titulo, fontsize=14)
    svgfile = io.StringIO()
    plot.savefig(svgfile, bbox_inches='tight', format='svg')
    render_svg(svgfile.getvalue())
    st.subheader('Datos')
    st.write(df_table[vars_table_entidad].sort_values('prop_altas', ascending=False).rename(columns={'diff': 'crecimiento'}))
elif grafica == 'Municipio':
    st.subheader('Gráfica')
    sel_ent = st.selectbox("Entidad", list(dicc_cve_ent.values())[1:], 0)
    cve_ent = dicc_ent_cve[sel_ent]
    lista_municipios = [dicc_cve_mun[m] for m in dicc_cve_mun if m[0:2] == cve_ent]
    sel_mun = st.selectbox("Municipio", lista_municipios, 0)
    df_table = df_sec_mun.loc[dicc_mun_cve[sel_mun]].pipe(procesa_df_sector)
    plot = grafica_sector(df_table)
    titulo = f'Unidades económicas dadas de alta y baja entre 2015 y 2019,\n {sel_mun} ({dicc_mun_cve[sel_mun]})'
    plot.suptitle(titulo, fontsize=14)
    svgfile = io.StringIO()
    plot.savefig(svgfile, bbox_inches='tight', format='svg')
    render_svg(svgfile.getvalue())
    st.subheader('Datos')
    st.write(df_table[vars_table_sector].sort_values('prop_altas', ascending=False).rename(columns={'diff': 'crecimiento'}))





