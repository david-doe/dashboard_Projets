import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="DASHBOARD PROJETS",
    page_icon="⚡",
    layout="wide",
)

DATA_FILE = "roadmap.csv"

# --- THEME SOMBRE ULTRA-LISIBLE & CORRIGÉ ---
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    /* Correction de la marge supérieure pour éviter que la barre Streamlit ne coupe le titre */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 98% !important;
    }
    .dash-card {
        background: linear-gradient(145deg, #131b2e, #0f172a);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
    }
    .dash-header {
        font-size: 24px;
        font-weight: 800;
        line-height: 1.4;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 22px;
        padding-bottom: 10px;
        border-bottom: 1px solid #1e293b;
        word-wrap: break-word;
    }
    .kpi-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .kpi-val {
        font-size: 26px;
        font-weight: 800;
        color: #38bdf8;
    }
    .kpi-sub {
        font-size: 11px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-tile-blue {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        border-radius: 10px;
        padding: 16px;
        color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
    }
    .metric-tile-indigo {
        background: linear-gradient(135deg, #4f46e5, #4338ca);
        border-radius: 10px;
        padding: 16px;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
    }
    .tile-num {
        font-size: 32px;
        font-weight: 800;
        line-height: 1;
    }
    .tile-text {
        font-size: 12px;
        font-weight: 600;
        color: #e2e8f0;
        margin-top: 4px;
        text-transform: uppercase;
    }
    .badge-p1 {
        background-color: #ef4444;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-p2 {
        background-color: #f59e0b;
        color: #111827;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-p3 {
        background-color: #06b6d4;
        color: #111827;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-done {
        background-color: #10b981;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

DEFAULT_TASKS = [
    {"Pôle": "Canada", "Tâche": "Refonte CV format canadien (orienté data/projets)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-10-15"},
    {"Pôle": "Canada", "Tâche": "Passage certification Power BI PL-300", "Statut": "En cours", "Priorité": "P1 - Urgent", "Échéance": "2026-11-20"},
    {"Pôle": "Canada", "Tâche": "Inscription officielle forum Destination Canada 2026", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-11-01"},
    {"Pôle": "Canada", "Tâche": "Entretiens Destination Canada (virtuel & Bruxelles)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-12-10"},
    {"Pôle": "Canada", "Tâche": "Passage test linguistique TEF/TCF Canada (C1 / NCLC 7+)", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-02-28"},
    {"Pôle": "Canada", "Tâche": "Évaluation des diplômes WES (EDE équivalence Master)", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-04-30"},
    {"Pôle": "Canada", "Tâche": "Dépôt dossier Mobilité francophone (dispense C16)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2027-07-01"},
    {"Pôle": "M2", "Tâche": "Validation examens théoriques premier semestre", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2027-01-31"},
    {"Pôle": "M2", "Tâche": "Projet d'aide à la décision / BI", "Statut": "En cours", "Priorité": "P2 - Important", "Échéance": "2027-04-15"},
    {"Pôle": "M2", "Tâche": "Rédaction et soutenance du mémoire de M2", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2027-06-30"},
    {"Pôle": "Perso", "Tâche": "Vérification validité passeport (> 2 ans)", "Statut": "Terminé", "Priorité": "P2 - Important", "Échéance": "2026-10-30"},
    {"Pôle": "Perso", "Tâche": "Préavis logement France & logistique départ", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-07-15"},
]

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    df = pd.DataFrame(DEFAULT_TASKS)
    df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- CALCUL DES INDICATEURS ---
total_tasks = len(df)
done_tasks = len(df[df["Statut"] == "Terminé"])
in_progress = len(df[df["Statut"] == "En cours"])
todo_tasks = len(df[df["Statut"] == "À faire"])
p1_urgent = len(df[(df["Priorité"] == "P1 - Urgent") & (df["Statut"] != "Terminé")])
pct_done = round((done_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
pct_remaining = round(100 - pct_done, 1)

# --- TITRE PRINCIPAL PARFAITEMENT VISIBLE ---
st.markdown("<div class='dash-header'>⚡ Tableau de bord Agile Sprint & Suivi Opérationnel (Canada • M2 • Perso)</div>", unsafe_allow_html=True)

# ==========================================
# LIGNE SUPÉRIEURE : ANALYTICS & VISUELS AGILE
# ==========================================
c_top1, c_top2, c_top3 = st.columns([1, 1.4, 1.2])

with c_top1:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    kb1, kb2 = st.columns(2)
    with kb1:
        st.markdown(f"<div class='kpi-box'><div class='kpi-val' style='color:#ef4444;'>{p1_urgent}</div><div class='kpi-sub'>Urgences P1</div></div>", unsafe_allow_html=True)
    with kb2:
        st.markdown(f"<div class='kpi-box'><div class='kpi-val' style='color:#38bdf8;'>{todo_tasks}</div><div class='kpi-sub'>À démarrer</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:14px; font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;'>Backlog par priorité</div>", unsafe_allow_html=True)
    prio_counts = df[df["Statut"] != "Terminé"]["Priorité"].value_counts().reset_index()
    prio_counts.columns = ["Priorité", "Nombre"]
    
    fig_prio = px.bar(prio_counts, x="Nombre", y="Priorité", orientation="h", color_discrete_sequence=["#38bdf8"])
    fig_prio.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        height=140,
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='#1e293b'),
        yaxis_title=""
    )
    st.plotly_chart(fig_prio, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_top2:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    
    with g1:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=done_tasks,
            gauge={
                "axis": {"range": [0, total_tasks], "tickcolor": "#94a3b8"},
                "bar": {"color": "#38bdf8"},
                "bgcolor": "#1e293b"
            },
            title={"text": "Jalons Livrés", "font": {"size": 13, "color": "#f1f5f9"}},
            number={"font": {"color": "#ffffff", "size": 28}}
        ))
        fig_g1.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=130, margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig_g1, use_container_width=True, config={"displayModeBar": False})
        
    with g2:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct_done,
            number={"suffix": "%", "font": {"color": "#ffffff", "size": 28}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#10b981"},
                "bgcolor": "#1e293b"
            },
            title={"text": "Progression Globale", "font": {"size": 13, "color": "#f1f5f9"}}
        ))
        fig_g2.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=130, margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig_g2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;'>Vélocité par Pôle</div>", unsafe_allow_html=True)
    pole_stat = df.groupby(["Pôle", "Statut"]).size().reset_index(name="Total")
    fig_bar = px.bar(
        pole_stat, x="Pôle", y="Total", color="Statut", barmode="group",
        color_discrete_map={"Terminé": "#10b981", "En cours": "#38bdf8", "À faire": "#475569"}
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        height=140,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(font=dict(size=10)),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#1e293b'),
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_top3:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;'>Sprint Goal (% Done)</div>", unsafe_allow_html=True)
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Terminé", "Restant"],
        values=[pct_done, pct_remaining],
        hole=0.68,
        marker_colors=["#10b981", "#1e293b"],
        textinfo="percent",
        textfont=dict(color="#ffffff", size=12)
    )])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#94a3b8"))
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown(f"<div style='font-size:13px; color:#cbd5e1; margin-top:8px;'>Taux d'accomplissement : <b style='color:#38bdf8;'>{pct_done} %</b></div>", unsafe_allow_html=True)
    st.progress(pct_done / 100)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# LIGNE INFÉRIEURE : ACTIONS, VALIDATION & AJOUT
# ==========================================
c_bot1, c_bot2, c_bot3 = st.columns([1, 1.4, 1.2])

with c_bot1:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase; margin-bottom:12px;'>Volume d'Opérations</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-tile-blue'>
        <div class='tile-num'>{total_tasks}</div>
        <div class='tile-text'>Jalons enregistrés</div>
    </div>
    <div class='metric-tile-indigo'>
        <div class='tile-num'>{in_progress}</div>
        <div class='tile-text'>Chantiers en cours</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_bot2:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:16px; font-weight:800; color:#ffffff; margin-bottom:4px;'>📋 Suivi des Tâches par Pôle</div>", unsafe_allow_html=True)
    st.caption("Coche pour valider une tâche, ou décoche dans l'historique pour la réactiver :")

    tab_can, tab_m2, tab_per = st.tabs(["🍁 Canada", "🎓 M2 SIAD", "👤 Personnel"])

    def render_pole_tasks(pole_name):
        pending = df[(df["Pôle"] == pole_name) & (df["Statut"] != "Terminé")]
        done = df[(df["Pôle"] == pole_name) & (df["Statut"] == "Terminé")]

        st.markdown("<div style='font-size:12px; font-weight:700; color:#38bdf8; text-transform:uppercase; margin:8px 0 4px 0;'>⚡ Actions en cours / À faire</div>", unsafe_allow_html=True)
        if pending.empty:
            st.markdown("<div style='color:#10b981; font-size:13px; font-weight:600; padding:4px 0;'>✨ Aucune tâche en attente sur ce pôle !</div>", unsafe_allow_html=True)
        else:
            for idx, row in pending.iterrows():
                prio_style = "badge-p1" if "P1" in row["Priorité"] else ("badge-p2" if "P2" in row["Priorité"] else "badge-p3")
                col_chk, col_txt = st.columns([0.1, 0.9])
                with col_chk:
                    checked = st.checkbox("", key=f"chk_pending_{idx}", label_visibility="collapsed")
                with col_txt:
                    st.markdown(
                        f"<span class='{prio_style}'>{row['Priorité'][:2]}</span> "
                        f"<span style='color:#f8fafc; font-weight:600;'>{row['Tâche']}</span> "
                        f"<span style='color:#94a3b8; font-size:12px;'>({row['Échéance']})</span>",
                        unsafe_allow_html=True
                    )
                if checked:
                    df.at[idx, "Statut"] = "Terminé"
                    save_data(df)
                    st.rerun()

        st.markdown("<div style='border-top: 1px solid #1e293b; margin: 14px 0 10px 0;'></div>", unsafe_allow_html=True)

        with st.expander(f"✅ Tâches validées ({len(done)})", expanded=False):
            if done.empty:
                st.caption("Aucune action clôturée pour le moment.")
            else:
                for idx, row in done.iterrows():
                    col_chk, col_txt = st.columns([0.1, 0.9])
                    with col_chk:
                        revert = st.checkbox("", value=True, key=f"chk_done_{idx}", label_visibility="collapsed")
                    with col_txt:
                        st.markdown(
                            f"<span class='badge-done'>FAIT</span> "
                            f"<span style='text-decoration: line-through; color:#64748b; font-weight:500;'>{row['Tâche']}</span> "
                            f"<span style='color:#475569; font-size:11px;'>({row['Échéance']})</span>",
                            unsafe_allow_html=True
                        )
                    if not revert:
                        df.at[idx, "Statut"] = "En cours"
                        save_data(df)
                        st.rerun()

    with tab_can:
        render_pole_tasks("Canada")
    with tab_m2:
        render_pole_tasks("M2")
    with tab_per:
        render_pole_tasks("Perso")

    st.markdown("</div>", unsafe_allow_html=True)

with c_bot3:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:16px; font-weight:800; color:#ffffff; margin-bottom:8px;'>➕ Nouveau Jalon</div>", unsafe_allow_html=True)
    
    with st.form("form_add_task", clear_on_submit=True):
        new_pole = st.selectbox("Pôle cible", ["Canada", "M2", "Perso"])
        new_task = st.text_input("Intitulé de la tâche / action")
        new_prio = st.selectbox("Priorité", ["P1 - Urgent", "P2 - Important", "P3 - Secondaire"])
        new_stat = st.selectbox("Statut initial", ["À faire", "En cours", "Terminé"])
        new_date = st.date_input("Échéance", value=date.today())
        
        btn_submit = st.form_submit_button("Ajouter à la roadmap")
        if btn_submit and new_task.strip():
            new_row = pd.DataFrame([{
                "Pôle": new_pole,
                "Tâche": new_task.strip(),
                "Statut": new_stat,
                "Priorité": new_prio,
                "Échéance": str(new_date)
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Tâche enregistrée !")
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
