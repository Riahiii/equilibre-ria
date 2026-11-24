import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Économie Micro — RIAHI", 
    page_icon="📊",
    layout="wide"
)

# --- MENU DANS LA BARRE LATÉRALE ---
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choisissez le mode :", ["Consommateur", "Producteur"], key="choix_mode")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Économie Micro — RIAHI", 
    page_icon="📊",
    layout="wide"
)

# --- MENU DANS LA BARRE LATÉRALE ---
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choisissez le mode :", ["Consommateur", "Producteur"])

# ==========================================
# MODE CONSOMMATEUR
# ==========================================
if mode == "Consommateur":
    st.title("📈 Équilibre du Consommateur — RIAHI")
    st.markdown("Ajustez les paramètres pour voir l'équilibre du consommateur.")

    st.sidebar.header("⚙️ Paramètres")
    income = st.sidebar.slider("Revenu (R)", min_value=10, max_value=200, value=100, step=10)
    px = st.sidebar.slider("Prix du bien X (Px)", min_value=1, max_value=20, value=4, step=1)
    py = st.sidebar.slider("Prix du bien Y (Py)", min_value=1, max_value=20, value=5, step=1)
    alpha = st.sidebar.slider("Alpha (poids du bien X)", min_value=0.1, max_value=0.9, value=0.5, step=0.1)
    beta = 1 - alpha

    # --- NOUVELLES OPTIONS D'AFFICHAGE ---
    st.sidebar.header("👁️ Options d'affichage")
    show_budget = st.sidebar.checkbox("Afficher la Contrainte Budgétaire", value=True)
    show_eq = st.sidebar.checkbox("Afficher le point d'équilibre", value=True)
    num_curves = st.sidebar.slider("Nombre de courbes d'indifférence", min_value=1, max_value=5, value=3)
    
    # Cases à cocher individuelles pour les courbes
    curve_toggles = []
    for i in range(num_curves):
        toggle = st.sidebar.checkbox(f"Afficher Courbe {i+1}", value=True, key=f"cons_{i}")
        curve_toggles.append(toggle)

    # Calculs
    def utility(x, y, a, b):
        return (x**a) * (y**b)

    x_eq = (alpha / (alpha + beta)) * (income / px)
    y_eq = (beta / (alpha + beta)) * (income / py)
    u_eq = utility(x_eq, y_eq, alpha, beta)

    # Graphique
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 1. Contrainte budgétaire
    if show_budget:
        x_budget = np.linspace(0, income/px, 100)
        y_budget = (income - px * x_budget) / py
        ax.plot(x_budget, y_budget, color='blue', linewidth=2, label='Contrainte Budgétaire')

    # 2. Courbes d'indifférence
    # On génère une liste de niveaux d'utilité autour de l'équilibre
    if num_curves == 1:
        levels = [u_eq]
    else:
        levels = np.linspace(u_eq * 0.5, u_eq * 1.5, num_curves)
        
    x_vals = np.linspace(0.1, income/px + 5, 400)
    
    for i, level in enumerate(levels):
        if curve_toggles[i]: # Vérifie si la case est cochée
            y_vals = (level / (x_vals**alpha))**(1/beta)
            mask = (y_vals > 0) & (y_vals < income/py + 5)
            
            # Mise en évidence de la courbe d'équilibre (la plus proche de u_eq)
            if abs(level - u_eq) < 0.1: 
                ax.plot(x_vals[mask], y_vals[mask], color='red', linewidth=2, label=f'Courbe d\'Indifférence (U={level:.1f})')
            else:
                ax.plot(x_vals[mask], y_vals[mask], color='gray', linestyle='--', alpha=0.6)

    # 3. Point d'équilibre
    if show_eq:
        ax.scatter(x_eq, y_eq, color='green', s=100, zorder=5, label=f'Équilibre ({x_eq:.1f}, {y_eq:.1f})')

    ax.set_xlabel('Bien X')
    ax.set_ylabel('Bien Y')
    ax.set_xlim(0, income/px + 5)
    ax.set_ylim(0, income/py + 5)
    ax.legend()
    st.pyplot(fig)


# ==========================================
# MODE PRODUCTEUR
# ==========================================
else:
    st.title("🏭 Équilibre du Producteur (Cobb-Douglas) — RIAHI")
    st.markdown("Ajustez les paramètres pour voir l'équilibre du producteur (minimisation des coûts).")

    st.sidebar.header("⚙️ Paramètres de Production")
    cost = st.sidebar.slider("Coût total (C)", min_value=10, max_value=200, value=100, step=10)
    w = st.sidebar.slider("Salaire (w) - Prix du travail L", min_value=1, max_value=20, value=4, step=1)
    r = st.sidebar.slider("Taux de location (r) - Prix du capital K", min_value=1, max_value=20, value=5, step=1)
    alpha = st.sidebar.slider("Alpha (poids du travail L)", min_value=0.1, max_value=0.9, value=0.5, step=0.1)
    beta = 1 - alpha

    # --- NOUVELLES OPTIONS D'AFFICHAGE ---
    st.sidebar.header("👁️ Options d'affichage")
    show_isocost = st.sidebar.checkbox("Afficher l'Isocoût", value=True)
    show_eq_prod = st.sidebar.checkbox("Afficher le point d'équilibre", value=True)
    num_isoquants = st.sidebar.slider("Nombre d'isoquantes", min_value=1, max_value=5, value=3)
    
    # Cases à cocher individuelles pour les isoquantes
    isoquant_toggles = []
    for i in range(num_isoquants):
        toggle = st.sidebar.checkbox(f"Afficher Isoquante {i+1}", value=True, key=f"prod_{i}")
        isoquant_toggles.append(toggle)

    # Calculs
    def production(L, K, a, b):
        return (L**a) * (K**b)

    L_eq = (alpha / (alpha + beta)) * (cost / w)
    K_eq = (beta / (alpha + beta)) * (cost / r)
    Q_eq = production(L_eq, K_eq, alpha, beta)

    # Graphique
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 1. Droite d'isocoût
    if show_isocost:
        L_isocost = np.linspace(0, cost/w, 100)
        K_isocost = (cost - w * L_isocost) / r
        ax.plot(L_isocost, K_isocost, color='blue', linewidth=2, label='Droite d\'Isocoût')

    # 2. Isoquantes
    if num_isoquants == 1:
        levels_prod = [Q_eq]
    else:
        levels_prod = np.linspace(Q_eq * 0.5, Q_eq * 1.5, num_isoquants)
        
    L_vals = np.linspace(0.1, cost/w + 5, 400)
    
    for i, level in enumerate(levels_prod):
        if isoquant_toggles[i]: # Vérifie si la case est cochée
            K_vals = (level / (L_vals**alpha))**(1/beta)
            mask = (K_vals > 0) & (K_vals < cost/r + 5)
            
            if abs(level - Q_eq) < 0.1:
                ax.plot(L_vals[mask], K_vals[mask], color='red', linewidth=2, label=f'Isoquante (Q={level:.1f})')
            else:
                ax.plot(L_vals[mask], K_vals[mask], color='gray', linestyle='--', alpha=0.6)

    # 3. Point d'équilibre
    if show_eq_prod:
        ax.scatter(L_eq, K_eq, color='green', s=100, zorder=5, label=f'Équilibre (L={L_eq:.1f}, K={K_eq:.1f})')

    ax.set_xlabel('Travail (L)')
    ax.set_ylabel('Capital (K)')
    ax.set_xlim(0, cost/w + 5)
    ax.set_ylim(0, cost/r + 5)
    ax.legend()
    st.pyplot(fig)
