import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="Tableau de bord Agile — Suivi des tâches",
    page_icon="📊",
    layout="wide",
)

DATA_FILE = "roadmap_agile.csv"

# --- Style CSS : Reproduction fidèle du visuel blanc / gris / cartes ---
st.markdown("""
<style>
    .main {
        background-color: #f1f3f6;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .dash-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    .dash-title {
        font-size: 26px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 20px;
    }
    .kpi-badge {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
    }
    .kpi-number {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
    }
    .kpi-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .blue-tile {
        background-color: #0284c7;
        color: white;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .blue-tile-number {
        font-size: 32px;
        font-weight: 800;
    }
    .blue-tile-sub {
        font-size: 13px;
        opacity: 0.85;
    }
</style>
""", unsafe_allow_html=True)

# --- Données initiales par défaut ---
DEFAULT_TASKS = [
    {"Tâche": "Refonte CV au format canadien (orienté data/projets)", "Pôle": "Canada", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-10-15"},
    {"Tâche": "Certification Power BI PL-300 (réduction étudiante)", "Pôle": "Canada", "Statut": "En cours", "Priorité": "P1 - Urgent", "Échéance": "2026-11-20"},
    {"Tâche": "Inscription forum Destination Canada 2026", "Pôle": "Canada", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-11-01"},
    {"Tâche": "Entretiens Destination Canada (virtuel & Bruxelles)", "Pôle": "Canada", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2026-12-10"},
    {"Tâche": "Passage test linguistique TEF / TCF Canada (C1 / NCLC 7+)", "Pôle": "Canada", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-02-28"},
    {"Tâche": "Évaluation des diplômes WES (EDE équivalence Master)", "Pôle": "Canada", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-04-30"},
    {"Tâche": "Validation des examens théoriques du premier semestre", "Pôle": "M2", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2027-01-31"},
    {"Tâche": "Projet tutoré d'aide à la décision / BI", "Pôle": "M2", "Statut": "En cours", "Priorité": "P2 - Important", "Échéance": "2027-04-15"},
    {"Tâche": "Rédaction et soutenance du mémoire de M2", "Pôle": "M2", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": "2027-06-30"},
    {"Tâche": "Vérification validité passeport (> 2 ans)", "Pôle": "Perso", "Statut": "Terminé", "Priorité": "P2 - Important", "Échéance": "2026-10-30"},
    {"Tâche": "Logistique logement et préavis France", "Pôle": "Perso", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": "2027-07-15"},
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

# --- Calcul des indicateurs clés ---
total_tasks = len(df)
done_tasks = len(df[df["Statut"] == "Terminé"])
in_progress = len(df[df["Statut"] == "En cours"])
todo_tasks = len(df[df["Statut"] == "À faire"])
p1_urgent = len(df[(df["Priorité"] == "P1 - Urgent") & (df["Statut"] != "Terminé")])
pct_done = round((done_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
pct_committed = round(100 - pct_done, 1)

# --- Titre Principal ---
st.markdown("<div class='dash-title'>Tableau de bord Agile Sprint avec suivi des tâches</div>", unsafe_allow_html=True)

# ==========================================
# LIGNE SUPÉRIEURE (3 COLONNES)
# ==========================================
c_top1, c_top2, c_top3 = st.columns([1, 1.4, 1.2])

with c_top1:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    # Deux badges métriques
    kb1, kb2 = st.columns(2)
    with kb1:
        st.markdown(f"<div class='kpi-badge'><div class='kpi-number'>{p1_urgent}</div><div class='kpi-label'>Urgences P1</div></div>", unsafe_allow_html=True)
    with kb2:
        st.markdown(f"<div class='kpi-badge'><div class='kpi-number'>{todo_tasks}</div><div class='kpi-label'>À démarrer</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:12px; font-size:13px; font-weight:600; color:#475569;'>Tâches restantes par priorité</div>", unsafe_allow_html=True)
    prio_counts = df[df["Statut"] != "Terminé"]["Priorité"].value_counts().reset_index()
    prio_counts.columns = ["Priorité", "Nombre"]
    fig_prio = px.bar(prio_counts, x="Nombre", y="Priorité", orientation="h", color_discrete_sequence=["#0284c7"])
    fig_prio.update_layout(height=140, margin=dict(l=0, r=0, t=10, b=10), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_prio, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_top2:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    
    with g1:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=done_tasks,
            gauge={"axis": {"range": [0, total_tasks]}, "bar": {"color": "#0284c7"}},
            title={"text": "Tâches Réalisées", "font": {"size": 13}}
        ))
        fig_g1.update_layout(height=130, margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig_g1, use_container_width=True, config={"displayModeBar": False})
        
    with g2:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct_done,
            number={"suffix": "%"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#10b981"}},
            title={"text": "Avancement Global", "font": {"size": 13}}
        ))
        fig_g2.update_layout(height=130, margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig_g2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='font-size:13px; font-weight:600; color:#475569;'>Vélocité par Pôle (Terminé vs En attente)</div>", unsafe_allow_html=True)
    pole_stat = df.groupby(["Pôle", "Statut"]).size().reset_index(name="Total")
    fig_bar = px.bar(pole_stat, x="Pôle", y="Total", color="Statut", barmode="group",
                     color_discrete_map={"Terminé": "#10b981", "En cours": "#0284c7", "À faire": "#cbd5e1"})
    fig_bar.update_layout(height=140, margin=dict(l=0, r=0, t=10, b=10), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_top3:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; font-weight:600; color:#475569;'>Sprint Goal (% Réalisé)</div>", unsafe_allow_html=True)
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Fait", "Restant"],
        values=[pct_done, pct_committed],
        hole=0.65,
        marker_colors=["#0284c7", "#e2e8f0"],
        textinfo="percent",
    )])
    fig_pie.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown(f"<div style='font-size:12px; color:#64748b; margin-top:8px;'>Capacité couverte : <b>{pct_done} %</b></div>", unsafe_allow_html=True)
    st.progress(pct_done / 100)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# LIGNE INFÉRIEURE : ACTIONS ET VALIDATIONS
# ==========================================
c_bot1, c_bot2, c_bot3 = st.columns([1, 1.4, 1.2])

with c_bot1:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; font-weight:600; color:#475569; margin-bottom:12px;'>Opérations & Volume</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='blue-tile'>
        <div class='blue-tile-number'>{total_tasks}</div>
        <div class='blue-tile-sub'>Total des jalons du plan</div>
    </div>
    <div class='blue-tile' style='background-color:#0369a1;'>
        <div class='blue-tile-number'>{in_progress}</div>
        <div class='blue-tile-sub'>Jalons actuellement en cours</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_bot2:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:15px; font-weight:700; color:#1e293b; margin-bottom:6px;'>✅ Validation rapide des tâches</div>", unsafe_allow_html=True)
    st.caption("Coche une tâche pour la marquer instantanément comme **Terminé** :")

    # Liste des tâches en cours ou à faire avec checkbox de validation directe
    pending_tasks = df[df["Statut"] != "Terminé"].index.tolist()
    
    if not pending_tasks:
        st.success("Toutes les tâches sont terminées !")
    else:
        for idx in pending_tasks:
            row = df.loc[idx]
            tag_color = "#dc2626" if "P1" in row["Priorité"] else "#d97706"
            label = f"**[{row['Pôle']}]** {row['Tâche']} *(Échéance : {row['Échéance']})*"
            
            if st.checkbox(label, key=f"task_{idx}"):
                df.at[idx, "Statut"] = "Terminé"
                save_data(df)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with c_bot3:
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px; font-weight:700; color:#1e293b; margin-bottom:10px;'>➕ Ajouter une tâche</div>", unsafe_allow_html=True)
    
    with st.form("form_add_task", clear_on_submit=True):
        new_pole = st.selectbox("Pôle", ["Canada", "M2", "Perso"])
        new_task = st.text_input("Intitulé de la tâche")
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
            st.success("Tâche ajoutée avec succès !")
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
