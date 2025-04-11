import streamlit as st
import matplotlib.pyplot as plt

# --- Initialisation de la session ---
if "connecte" not in st.session_state:
    st.session_state.connecte = False

# --- Écran de connexion ---
if not st.session_state.connecte:
    st.title("Coach Financier Intelligent")
    nom_utilisateur = st.text_input("Nom d'utilisateur")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if nom_utilisateur == "utilisateur_test" and mot_de_passe == "motdepasse123":
            st.session_state.connecte = True
            st.success("Connexion réussie !")
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect.")

# --- Interface principale ---
else:
    st.title("Bienvenue dans votre espace bancaire intelligent")

    st.subheader("1. Définir votre objectif")
    objectif = st.selectbox("Quel est votre objectif ?", ["Maison", "Voiture", "Mariage", "Voyage"])
    duree_mois = st.slider("Durée souhaitée pour atteindre cet objectif (en mois)", 12, 60, step=6)

    # ============ OBJECTIF : MAISON ============
    if objectif == "Maison":
        st.markdown("### Objectif : Achat d'une Maison")

        salaire = st.number_input("Votre salaire mensuel (DH)", min_value=1000)
        mode_paiement_maison = st.selectbox("Mode de paiement", ["Cash", "Crédit", "Hybride"])

        budget_min = salaire * 12
        budget_max = salaire * 20
        budget_maison = round((budget_min + budget_max) / 2)
        st.write(f"Budget conseillé : entre *{budget_min} DH* et *{budget_max} DH*")
        st.write(f"Budget cible proposé : *{budget_maison} DH*")

        st.markdown("#### Vos charges mensuelles")
        loyer = st.number_input("Loyer / crédit logement", min_value=0)
        credit_voiture = st.number_input("Crédit voiture", min_value=0)
        abonnements = st.number_input("Abonnements (internet...)", min_value=0)
        courses = st.number_input("Courses", min_value=0)
        transport = st.number_input("Transport / carburant", min_value=0)
        loisirs = st.number_input("Loisirs", min_value=0)
        imprevus = st.number_input("Budget pour imprévus", min_value=0)

        total_charges = loyer + credit_voiture + abonnements + courses + transport + loisirs
        total_depenses = total_charges + imprevus
        reste_a_vivre = salaire - total_depenses

        if reste_a_vivre < 0:
            st.error("Vos dépenses dépassent votre salaire.")
        else:
            st.success(f"Reste à vivre mensuel : *{reste_a_vivre} DH*")

        if mode_paiement_maison == "Cash":
            st.info("Épargne totale nécessaire (cash)")

            type_epargne = st.selectbox("Type d'épargne", [
                "Compte sur carnet",
                "Fond de placement",
                "Investissement en actions (avec risque)",
                "E-Daret"
            ])
            epargne_mensuelle = st.number_input("Montant épargné chaque mois (DH)", min_value=500)
            if epargne_mensuelle > reste_a_vivre:
                st.warning("Ce montant dépasse votre reste à vivre.")
            epargne_totale = epargne_mensuelle * duree_mois

            st.write(f"Épargne prévue : *{epargne_totale} DH*")
            if epargne_totale >= budget_maison:
                st.success("Objectif atteint !")
                st.write("Maisons partenaires : Villa Zen, Appartement Luxe")
            else:
                st.warning("Épargne insuffisante.")

        elif mode_paiement_maison == "Crédit":
            st.info("Crédit immobilier")

            taux_interet = 0.05
            mensualite = (budget_maison * taux_interet) / 12
            st.write(f"Mensualité estimée : *{mensualite:.0f} DH/mois*")
            st.write("Maisons disponibles : Duplex Jardin, Appartement Centre-ville")

        elif mode_paiement_maison == "Hybride":
            st.info("Paiement mixte : 50% épargne + 50% crédit")

            part_epargne = budget_maison * 0.5
            part_credit = budget_maison * 0.5
            mensualite_credit = (part_credit * 0.05) / 12

            epargne_mensuelle = st.number_input("Montant à épargner chaque mois (DH)", min_value=500)
            if epargne_mensuelle > reste_a_vivre:
                st.warning("Ce montant dépasse votre reste à vivre.")
            epargne_totale = epargne_mensuelle * duree_mois

            st.write(f"Épargne cible : {part_epargne} DH / Crédit : {part_credit} DH")
            st.write(f"Mensualité crédit : *{mensualite_credit:.0f} DH/mois*")
            if epargne_totale >= part_epargne:
                st.success("Plan validé ! Maison disponible via partenaire E.")
            else:
                st.warning("Épargne insuffisante.")

    # ============ OBJECTIF : VOITURE ============
    elif objectif == "Voiture":
        st.markdown("### Objectif : Achat d'une Voiture")

        salaire = st.number_input("Votre salaire mensuel (DH)", min_value=1000)
        type_voiture = st.radio("Type de voiture :", ["Occasion", "Neuve"])

        budget_voiture = salaire * 3 if type_voiture == "Occasion" else salaire * 6
        st.write(f"Budget estimé : *{budget_voiture} DH*")

        st.markdown("#### Vos charges mensuelles")
        loyer = st.number_input("Loyer / crédit logement", min_value=0)
        credit_voiture = st.number_input("Autre crédit", min_value=0)
        abonnements = st.number_input("Abonnements", min_value=0)
        courses = st.number_input("Courses", min_value=0)
        transport = st.number_input("Transport", min_value=0)
        loisirs = st.number_input("Loisirs", min_value=0)
        imprevus = st.number_input("Budget pour imprévus", min_value=0)

        total_charges = loyer + credit_voiture + abonnements + courses + transport + loisirs
        reste_a_vivre = salaire - (total_charges + imprevus)

        if reste_a_vivre < 0:
            st.error("Vous êtes en dépassement de budget.")
        else:
            st.success(f"Reste à vivre : *{reste_a_vivre} DH*")

        if type_voiture == "Occasion":
            st.info("Paiement uniquement en cash")

            type_epargne = st.selectbox("Type d'épargne", [
                "Compte sur carnet",
                "Fond de placement",
                "Investissement en actions (avec risque)",
                "E-Daret"
            ])
            epargne_mensuelle = st.number_input("Épargne mensuelle (DH)", min_value=500)
            if epargne_mensuelle > reste_a_vivre:
                st.warning("Ce montant dépasse votre budget.")
            epargne_totale = epargne_mensuelle * duree_mois
            st.write(f"Total épargné : *{epargne_totale} DH*")

            if epargne_totale >= budget_voiture:
                st.success("Vous pouvez acheter une voiture d'occasion.")
                st.write("Voitures partenaires : Clio 4, Dacia Sandero")
            else:
                st.warning("Épargne insuffisante.")

        elif type_voiture == "Neuve":
            mode_paiement_voiture = st.selectbox("Mode de paiement", ["Cash", "Crédit"])

            if mode_paiement_voiture == "Cash":
                st.info("Paiement complet en cash")

                type_epargne = st.selectbox("Type d'épargne", [
                    "Compte sur carnet",
                    "Fond de placement",
                    "Investissement en actions (avec risque)",
                    "E-Daret"
                ])
                epargne_mensuelle = st.number_input("Épargne mensuelle (DH)", min_value=500)
                if epargne_mensuelle > reste_a_vivre:
                    st.warning("Ce montant dépasse votre budget.")
                epargne_totale = epargne_mensuelle * duree_mois
                st.write(f"Total épargné : *{epargne_totale} DH*")

                if epargne_totale >= budget_voiture:
                    st.success("Vous pouvez acheter une voiture neuve.")
                    st.write("Voitures partenaires : Duster, Peugeot 208")
                else:
                    st.warning("Montant insuffisant.")

            elif mode_paiement_voiture == "Crédit":
                st.info("Crédit automobile avec intérêt 7%")

                taux_credit = 0.07
                mensualite = (budget_voiture * taux_credit) / 12
                st.write(f"Mensualité estimée : *{mensualite:.0f} DH/mois*")
                st.write("Voitures partenaires : Citroën C3, Toyota Yaris")