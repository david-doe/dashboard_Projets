import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(
    page_title="Cockpit de Pilotage — Canada, M2 & Perso",
    page_icon="🍁",
    layout="wide",
)

DATA_FILE = "dashboard_data.csv"

# Jalons initiaux de référence
DEFAULT_TASKS = [
    # PÔLE CANADA
    {"Pôle": "Canada", "Tâche": "Refonte CV au format canadien (sans photo, orienté data/impact)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2026, 10, 15)},
    {"Pôle": "Canada", "Tâche": "Certification Power BI PL-300 (réduction étudiante Pearson VUE)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2026, 11, 20)},
    {"Pôle": "Canada", "Tâche": "Inscription forum Destination Canada 2026", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2026, 11, 1)},
    {"Pôle": "Canada", "Tâche": "Entretiens Destination Canada (virtuel / Bruxelles)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2026, 12, 10)},
    {"Pôle": "Canada", "Tâche": "Passage test linguistique TEF ou TCF Canada (viser C1 / NCLC 7+)", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": date(2027, 2, 28)},
    {"Pôle": "Canada", "Tâche": "Dossier Évaluation des diplômes WES (EDE équivalence Master)", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": date(2027, 4, 30)},
    {"Pôle": "Canada", "Tâche": "Sécurisation offre d'emploi Mobilité francophone (dispense C16)", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 6, 15)},
    {"Pôle": "Canada", "Tâche": "Dépôt demande permis de travail en ligne IRCC", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 7, 1)},
    {"Pôle": "Canada", "Tâche": "Biométrie centre VFS et apposition vignette visa", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 7, 20)},
    {"Pôle": "Canada", "Tâche": "Arrivée aéroport Canada & délivrance permis physique", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 8, 25)},
    {"Pôle": "Canada", "Tâche": "Création profil Entrée express (CEC / Volet Francophone)", "Statut": "À faire", "Priorité": "P3 - Secondaire", "Échéance": date(2028, 8, 30)},

    # PÔLE M2
    {"Pôle": "M2", "Tâche": "Validation des examens théoriques du premier semestre", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 1, 31)},
    {"Pôle": "M2", "Tâche": "Projet tutoré / livrables d'analyse décisionnelle", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": date(2027, 4, 15)},
    {"Pôle": "M2", "Tâche": "Rédaction du mémoire de fin d'études", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 6, 1)},
    {"Pôle": "M2", "Tâche": "Soutenance de Master 2 & récupération attestation de réussite", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 6, 30)},

    # PÔLE PERSO
    {"Pôle": "Perso", "Tâche": "Vérifier validité passeport (> 2 ans de validité recommandée)", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": date(2026, 10, 30)},
    {"Pôle": "Perso", "Tâche": "Préavis logement France & logistique de départ", "Statut": "À faire", "Priorité": "P2 - Important", "Échéance": date(2027, 7, 15)},
    {"Pôle": "Perso", "Tâche": "Souscription assurance santé temporaire pour les 3 premiers mois", "Statut": "À faire", "Priorité": "P1 - Urgent", "Échéance": date(2027, 8, 10)},
]

POLES = ["Canada", "M2", "Perso"]
STATUTS = ["À faire", "En cours", "Terminé"]
PRIORITES = ["P1 - Urgent", "P2 - Important", "P3 - Secondaire"]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["Échéance"] = pd.to_datetime(df["Échéance"]).dt.date
        return df
    df = pd.DataFrame(DEFAULT_TASKS)
    df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- Barre latérale : Ajout rapide et filtres ---
with st.sidebar:
    st.header("⚡ Ajouter une tâche")
    with st.form("new_task_form", clear_on_submit=True):
        f_pole = st.selectbox("Pôle", POLES)
        f_task = st.text_input("Intitulé de la tâche / action")
        f_prio = st.selectbox("Priorité", PRIORITES)
        f_stat = st.selectbox("Statut", STATUTS)
        f_date = st.date_input("Échéance", value=date.today())
        
        submitted = st.form_submit_button("Enregistrer la tâche")
        if submitted and f_task.strip():
            new_row = pd.DataFrame([{
                "Pôle": f_pole,
                "Tâche": f_task.strip(),
                "Statut": f_stat,
                "Priorité": f_prio,
                "Échéance": f_date
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Tâche ajoutée !")
            st.rerun()

    st.divider()
    st.header("🔍 Filtres")
    selected_poles = st.multiselect("Filtrer par Pôle", options=POLES, default=POLES)
    selected_statuts = st.multiselect("Filtrer par Statut", options=STATUTS, default=STATUTS)

# --- Métriques d'avancement et KPI globaux ---
st.title("🍁 Cockpit d'Évolution — Canada, M2 & Perso")

def get_progress(data, pole_name=None):
    sub = data[data["Pôle"] == pole_name] if pole_name else data
    if len(sub) == 0:
        return 0
    return int((sub["Statut"] == "Terminé").sum() / len(sub) * 100)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🇨🇦 Avancement Canada", f"{get_progress(df, 'Canada')} %")
col2.metric("🎓 Avancement M2", f"{get_progress(df, 'M2')} %")
col3.metric("👤 Avancement Perso", f"{get_progress(df, 'Perso')} %")
p1_restantes = len(df[(df["Priorité"] == "P1 - Urgent") & (df["Statut"] != "Terminé")])
col4.metric("🚨 Urgences P1 en cours", p1_restantes)

st.progress(get_progress(df) / 100)
st.write("")

# --- Vues de travail ---
tab_editor, tab_canada, tab_metrics = st.tabs(["📝 Tableau de bord complet", "🍁 Focus Roadmap Canada", "📊 Vue synthétique"])

with tab_editor:
    st.subheader("Pilotage interactif des actions")
    st.caption("Modifie directement les statuts, priorités et dates ci-dessous. Pense à cliquer sur « Sauvegarder les modifications ».")

    filtered_df = df[(df["Pôle"].isin(selected_poles)) & (df["Statut"].isin(selected_statuts))].copy()

    edited_df = st.data_editor(
        filtered_df,
        column_config={
            "Pôle": st.column_config.SelectboxColumn("Pôle", options=POLES, required=True),
            "Tâche": st.column_config.TextColumn("Tâche", required=True, width="large"),
            "Statut": st.column_config.SelectboxColumn("Statut", options=STATUTS, required=True),
            "Priorité": st.column_config.SelectboxColumn("Priorité", options=PRIORITES, required=True),
            "Échéance": st.column_config.DateColumn("Échéance", format="YYYY-MM-DD"),
        },
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor"
    )

    if st.button("💾 Sauvegarder les modifications du tableau"):
        df.update(edited_df)
        save_data(df)
        st.success("Modifications sauvegardées avec succès.")
        st.rerun()

with tab_canada:
    st.subheader("Jalons critiques du projet d'immigration")
    canada_df = df[df["Pôle"] == "Canada"].sort_values(by="Échéance")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.dataframe(
            canada_df[["Échéance", "Tâche", "Priorité", "Statut"]],
            use_container_width=True,
            hide_index=True
        )
    with col_r:
        st.info(
            "**Rappels clés procédure Mobilité francophone :**\n"
            "- Poste qualifié FEER 0, 1, 2 ou 3 hors Québec.\n"
            "- Dispense d'EIMT (code C16) : coût employeur limité à 230 $ CAD.\n"
            "- Aucun justificatif de fonds requis si permis de travail valide sur place.\n"
            "- Le test NCLC 7+ (C1) au TEF/TCF Canada servira directement pour la Résidence permanente."
        )

with tab_metrics:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Répartition des tâches par statut")
        st.bar_chart(df["Statut"].value_counts())
    with col_chart2:
        st.subheader("Charge restante par Pôle (non terminées)")
        pending = df[df["Statut"] != "Terminé"]["Pôle"].value_counts()
        st.bar_chart(pending)
