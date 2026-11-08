import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (Votre nom ici) ---
st.set_page_config(
    page_title="Équilibre du Producteur — RIAHI", 
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Équilibre du Producteur (Cobb-Douglas) — RIAHI")
st.markdown("Ajustez les paramètres pour voir l'équilibre du producteur (minimisation des coûts).")

# --- BARRE LATÉRALE ---
st.sidebar.header("⚙️ Paramètres de Production")

# Paramètres de la contrainte (Isocoût)
st.sidebar.subheader("Contrainte de Coût")
cost = st.sidebar.slider("Coût total (C)", min_value=10, max_value=200, value=100, step=10)
w = st.sidebar.slider("Salaire (w) - Prix du travail L", min_value=1, max_value=20, value=4, step=1)
r = st.sidebar.slider("Taux de location (r) - Prix du capital K", min_value=1, max_value=20, value=5, step=1)

# Paramètres de la fonction de production (Cobb-Douglas)
st.sidebar.subheader("Technologie de Production")
alpha = st.sidebar.slider("Alpha (poids du travail L)", min_value=0.1, max_value=0.9, value=0.5, step=0.1)
beta = 1 - alpha # Pour simplifier, on garde alpha + beta = 1

# --- CALCULS ---
# Fonction de production Cobb-Douglas : Q(L,K) = L^alpha * K^beta
def production(L, K, a, b):
    return (L**a) * (K**b)

# Calcul de l'équilibre (solution analytique pour Cobb-Douglas)
# L* = (alpha / (alpha + beta)) * (C / w)
# K* = (beta / (alpha + beta)) * (C / r)
L_eq = (alpha / (alpha + beta)) * (cost / w)
K_eq = (beta / (alpha + beta)) * (cost / r)
Q_eq = production(L_eq, K_eq, alpha, beta)

# --- GRAPHIQUE 1 : ÉQUILIBRE (ISOQUANTES ET ISOCOÛT) ---
fig, ax = plt.subplots(figsize=(8, 5))

# Droite d'isocoût : K = (C - w*L) / r
L_isocost = np.linspace(0, cost/w, 100)
K_isocost = (cost - w * L_isocost) / r
ax.plot(L_isocost, K_isocost, color='blue', linewidth=2, label=f'Droite d\'Isocoût (C={cost})')

# Isoquantes (courbes de niveau de production)
# On trace l'isoquante d'équilibre et quelques autres autour
levels = [Q_eq * 0.6, Q_eq * 0.8, Q_eq, Q_eq * 1.2]
L_vals = np.linspace(0.1, cost/w + 5, 400)

for level in levels:
    # Pour une production Q, K = (Q / L^alpha)^(1/beta)
    K_vals = (level / (L_vals**alpha))**(1/beta)
    mask = (K_vals > 0) & (K_vals < cost/r + 5)
    if level == Q_eq:
        ax.plot(L_vals[mask], K_vals[mask], color='red', linewidth=2, label=f'Isoquante (Q={level:.2f})')
    else:
        ax.plot(L_vals[mask], K_vals[mask], color='gray', linestyle='--', alpha=0.6)

# Point d'équilibre
ax.scatter(L_eq, K_eq, color='green', s=100, zorder=5, label=f'Équilibre (L={L_eq:.1f}, K={K_eq:.1f})')

# Mise en forme
ax.set_xlabel('Travail (L)')
ax.set_ylabel('Capital (K)')
ax.set_title('Équilibre du Producteur', fontsize=14)
ax.set_xlim(0, cost/w + 5)
ax.set_ylim(0, cost/r + 5)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

st.pyplot(fig)

# Affichage des résultats
st.subheader("📊 Résultats de l'Équilibre")
col1, col2, col3 = st.columns(3)
col1.metric("Travail optimal (L)", f"{L_eq:.2f}")
col2.metric("Capital optimal (K)", f"{K_eq:.2f}")
col3.metric("Production totale (Q)", f"{Q_eq:.2f}")

# --- GRAPHIQUE 2 : DEMANDE CONDITIONNELLE DE TRAVAIL ---
st.subheader("📉 Demande de Travail (L) en fonction du Salaire (w)")
st.markdown(f"Pour un coût de *{cost}* et un taux de location de *{r}*, voici comment la demande de travail varie avec le salaire :")

# Génération des points pour la courbe de demande de L
wages = np.linspace(1, 20, 50)
demand_L = (alpha / (alpha + beta)) * (cost / wages)

fig_demand, ax_demand = plt.subplots(figsize=(8, 3))
ax_demand.plot(wages, demand_L, color='purple', linewidth=2)
ax_demand.scatter(w, L_eq, color='green', s=100, zorder=5, label='Salaire actuel')
ax_demand.set_xlabel('Salaire (w)')
ax_demand.set_ylabel('Quantité de travail demandée (L)')
ax_demand.legend()
st.pyplot(fig_demand)

st.latex(r"L^* = \frac{\alpha}{\alpha + \beta} \cdot \frac{C}{w}")
