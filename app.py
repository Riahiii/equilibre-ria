
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

# ==========================================
# MODE CONSOMMATEUR
# ==========================================
if mode == "Consommateur":
    st.title("📈 Équilibre du Consommateur — RIAHI")
    st.markdown("Ajustez les paramètres pour voir l'équilibre du consommateur.")

    st.sidebar.header("⚙️ Paramètres (Équilibre 1)")
    income = st.sidebar.slider("Revenu (R)", min_value=10, max_value=200, value=100, step=10, key="inc1")
    px = st.sidebar.slider("Prix du bien X (Px)", min_value=1, max_value=20, value=4, step=1, key="px1")
    py = st.sidebar.slider("Prix du bien Y (Py)", min_value=1, max_value=20, value=5, step=1, key="py1")
    alpha = st.sidebar.slider("Alpha (poids du bien X)", min_value=0.1, max_value=0.9, value=0.5, step=0.1, key="alpha1")
    beta = 1 - alpha

    # --- OPTION POUR LE 2EME ÉQUILIBRE ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔄 Comparaison (Équilibre 2)")
    show_eq2_cons = st.sidebar.checkbox("Afficher un 2ème équilibre", value=False)
    
    if show_eq2_cons:
        income2 = st.sidebar.slider("Revenu 2 (R2)", min_value=10, max_value=200, value=150, step=10, key="inc2")
        px2 = st.sidebar.slider("Prix du bien X 2 (Px2)", min_value=1, max_value=20, value=6, step=1, key="px2")
        py2 = st.sidebar.slider("Prix du bien Y 2 (Py2)", min_value=1, max_value=20, value=5, step=1, key="py2")

    # --- OPTIONS D'AFFICHAGE ---
    st.sidebar.markdown("---")
    st.sidebar.header("👁️ Options d'affichage")
    show_budget = st.sidebar.checkbox("Afficher la Contrainte Budgétaire", value=True)
    show_indiff = st.sidebar.checkbox("Afficher les Courbes d'Indifférence", value=True)
    show_eq = st.sidebar.checkbox("Afficher le point d'équilibre", value=True)

    # Calculs Eq 1
    def utility(x, y, a, b):
        return (x**a) * (y**b)

    x_eq = (alpha / (alpha + beta)) * (income / px)
    y_eq = (beta / (alpha + beta)) * (income / py)
    u_eq = utility(x_eq, y_eq, alpha, beta)

    # Calculs Eq 2
    if show_eq2_cons:
        x_eq2 = (alpha / (alpha + beta)) * (income2 / px2)
        y_eq2 = (beta / (alpha + beta)) * (income2 / py2)
        u_eq2 = utility(x_eq2, y_eq2, alpha, beta)

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # --- TRACÉ EQUILIBRE 1 (Bleu / Rouge) ---
    if show_budget:
        x_budget = np.linspace(0, income/px, 100)
        y_budget = (income - px * x_budget) / py
        ax.plot(x_budget, y_budget, color='blue', linewidth=2, label='Contrainte Budgétaire 1')

    if show_indiff:
        x_vals = np.linspace(0.1, income/px + 5, 400)
        y_vals = (u_eq / (x_vals**alpha))**(1/beta)
        mask = (y_vals > 0) & (y_vals < income/py + 5)
        ax.plot(x_vals[mask], y_vals[mask], color='red', linewidth=2, label='Courbe d\'Indifférence 1')

    if show_eq:
        ax.scatter(x_eq, y_eq, color='green', s=100, zorder=5, label=f'Équilibre 1 ({x_eq:.1f}, {y_eq:.1f})')

    # --- TRACÉ EQUILIBRE 2 (Orange / Violet) ---
    if show_eq2_cons:
        if show_budget:
            x_budget2 = np.linspace(0, income2/px2, 100)
            y_budget2 = (income2 - px2 * x_budget2) / py2
            ax.plot(x_budget2, y_budget2, color='orange', linewidth=2, linestyle='--', label='Contrainte Budgétaire 2')

        if show_indiff:
            x_vals2 = np.linspace(0.1, income2/px2 + 5, 400)
            y_vals2 = (u_eq2 / (x_vals2**alpha))**(1/beta)
            mask2 = (y_vals2 > 0) & (y_vals2 < income2/py2 + 5)
            ax.plot(x_vals2[mask2], y_vals2[mask2], color='purple', linewidth=2, linestyle='--', label='Courbe d\'Indifférence 2')

        if show_eq:
            ax.scatter(x_eq2, y_eq2, color='darkorange', s=100, zorder=5, label=f'Équilibre 2 ({x_eq2:.1f}, {y_eq2:.1f})')

    ax.set_xlabel('Bien X')
    ax.set_ylabel('Bien Y')
    
    # Ajustement automatique des limites du graphique pour tout voir
    max_x = max(income/px, income2/px2) + 5 if show_eq2_cons else income/px + 5
    max_y = max(income/py, income2/py2) + 5 if show_eq2_cons else income/py + 5
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)


# ==========================================
# MODE PRODUCTEUR
# ==========================================
else:
    st.title("🏭 Équilibre du Producteur (Cobb-Douglas) — RIAHI")
    st.markdown("Ajustez les paramètres pour voir l'équilibre du producteur (minimisation des coûts).")

    st.sidebar.header("⚙️ Paramètres (Équilibre 1)")
    cost = st.sidebar.slider("Coût total (C)", min_value=10, max_value=200, value=100, step=10, key="cost1")
    w = st.sidebar.slider("Salaire (w)", min_value=1, max_value=20, value=4, step=1, key="w1")
    r = st.sidebar.slider("Taux de location (r)", min_value=1, max_value=20, value=5, step=1, key="r1")
    alpha_prod = st.sidebar.slider("Alpha (poids du travail L)", min_value=0.1, max_value=0.9, value=0.5, step=0.1, key="alpha1_prod")
    beta_prod = 1 - alpha_prod

    # --- OPTION POUR LE 2EME ÉQUILIBRE ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔄 Comparaison (Équilibre 2)")
    show_eq2_prod = st.sidebar.checkbox("Afficher un 2ème équilibre", value=False)
    
    if show_eq2_prod:
        cost2 = st.sidebar.slider("Coût total 2 (C2)", min_value=10, max_value=200, value=150, step=10, key="cost2")
        w2 = st.sidebar.slider("Salaire 2 (w2)", min_value=1, max_value=20, value=6, step=1, key="w2")
        r2 = st.sidebar.slider("Taux de location 2 (r2)", min_value=1, max_value=20, value=5, step=1, key="r2")

    # --- OPTIONS D'AFFICHAGE ---
    st.sidebar.markdown("---")
    st.sidebar.header("👁️ Options d'affichage")
    show_isocost = st.sidebar.checkbox("Afficher les Droites d'Isocoût", value=True)
    show_isoquant = st.sidebar.checkbox("Afficher les Isoquantes", value=True)
    show_eq_prod = st.sidebar.checkbox("Afficher le point d'équilibre", value=True)

    # Calculs Eq 1
    def production(L, K, a, b):
        return (L**a) * (K**b)

    L_eq = (alpha_prod / (alpha_prod + beta_prod)) * (cost / w)
    K_eq = (beta_prod / (alpha_prod + beta_prod)) * (cost / r)
    Q_eq = production(L_eq, K_eq, alpha_prod, beta_prod)

    # Calculs Eq 2
    if show_eq2_prod:
        L_eq2 = (alpha_prod / (alpha_prod + beta_prod)) * (cost2 / w2)
        K_eq2 = (beta_prod / (alpha_prod + beta_prod)) * (cost2 / r2)
        Q_eq2 = production(L_eq2, K_eq2, alpha_prod, beta_prod)

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # --- TRACÉ EQUILIBRE 1 (Bleu / Rouge) ---
    if show_isocost:
        L_isocost = np.linspace(0, cost/w, 100)
        K_isocost = (cost - w * L_isocost) / r
        ax.plot(L_isocost, K_isocost, color='blue', linewidth=2, label='Isocoût 1')

    if show_isoquant:
        L_vals = np.linspace(0.1, cost/w + 5, 400)
        K_vals = (Q_eq / (L_vals**alpha_prod))**(1/beta_prod)
        mask = (K_vals > 0) & (K_vals < cost/r + 5)
        ax.plot(L_vals[mask], K_vals[mask], color='red', linewidth=2, label='Isoquante 1')

    if show_eq_prod:
        ax.scatter(L_eq, K_eq, color='green', s=100, zorder=5, label=f'Équilibre 1 (L={L_eq:.1f}, K={K_eq:.1f})')

    # --- TRACÉ EQUILIBRE 2 (Orange / Violet) ---
    if show_eq2_prod:
        if show_isocost:
            L_isocost2 = np.linspace(0, cost2/w2, 100)
            K_isocost2 = (cost2 - w2 * L_isocost2) / r2
            ax.plot(L_isocost2, K_isocost2, color='orange', linewidth=2, linestyle='--', label='Isocoût 2')

        if show_isoquant:
            L_vals2 = np.linspace(0.1, cost2/w2 + 5, 400)
            K_vals2 = (Q_eq2 / (L_vals2**alpha_prod))**(1/beta_prod)
            mask2 = (K_vals2 > 0) & (K_vals2 < cost2/r2 + 5)
            ax.plot(L_vals2[mask2], K_vals2[mask2], color='purple', linewidth=2, linestyle='--', label='Isoquante 2')

        if show_eq_prod:
            ax.scatter(L_eq2, K_eq2, color='darkorange', s=100, zorder=5, label=f'Équilibre 2 (L={L_eq2:.1f}, K={K_eq2:.1f})')

    ax.set_xlabel('Travail (L)')
    ax.set_ylabel('Capital (K)')
    
    max_L = max(cost/w, cost2/w2) + 5 if show_eq2_prod else cost/w + 5
    max_K = max(cost/r, cost2/r2) + 5 if show_eq2_prod else cost/r + 5
    ax.set_xlim(0, max_L)
    ax.set_ylim(0, max_K)
    
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)
