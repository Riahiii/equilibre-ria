import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (Votre nom ici) ---
st.set_page_config(
    page_title="Équilibre Cobb-Douglas — RIAHI", 
    page_icon="📈",
    layout="wide"
)

st.title("📈 Équilibre Cobb-Douglas — RIAHI")
st.markdown("Ajustez les paramètres pour voir l'équilibre du consommateur.")

# --- BARRE LATÉRALE ---
st.sidebar.header("⚙️ Paramètres")
income = st.sidebar.slider("Revenu (R)", min_value=10, max_value=200, value=100, step=10)
px = st.sidebar.slider("Prix du bien X (Px)", min_value=1, max_value=20, value=4, step=1)
py = st.sidebar.slider("Prix du bien Y (Py)", min_value=1, max_value=20, value=5, step=1)
alpha = st.sidebar.slider("Alpha (poids du bien X)", min_value=0.1, max_value=0.9, value=0.5, step=0.1)
beta = 1 - alpha

# --- CALCULS ---
def utility(x, y, a, b):
    return (x**a) * (y**b)

x_eq = (alpha / (alpha + beta)) * (income / px)
y_eq = (beta / (alpha + beta)) * (income / py)
u_eq = utility(x_eq, y_eq, alpha, beta)

# --- GRAPHIQUE 1 : ÉQUILIBRE ---
fig, ax = plt.subplots(figsize=(8, 5))
x_budget = np.linspace(0, income/px, 100)
y_budget = (income - px * x_budget) / py
ax.plot(x_budget, y_budget, color='blue', linewidth=2, label='Contrainte Budgétaire')

levels = [u_eq * 0.6, u_eq * 0.8, u_eq, u_eq * 1.2]
x_vals = np.linspace(0.1, income/px + 5, 400)
for level in levels:
    y_vals = (level / (x_vals**alpha))**(1/beta)
    mask = (y_vals > 0) & (y_vals < income/py + 5)
    if level == u_eq:
        ax.plot(x_vals[mask], y_vals[mask], color='red', linewidth=2, label='Courbe d\'Indifférence')
    else:
        ax.plot(x_vals[mask], y_vals[mask], color='gray', linestyle='--', alpha=0.6)

ax.scatter(x_eq, y_eq, color='green', s=100, zorder=5, label=f'Équilibre ({x_eq:.1f}, {y_eq:.1f})')
ax.set_xlabel('Bien X')
ax.set_ylabel('Bien Y')
ax.set_xlim(0, income/px + 5)
ax.set_ylim(0, income/py + 5)
ax.legend()
st.pyplot(fig)

# --- GRAPHIQUE 2 : DEMANDE ---
st.subheader("📉 Fonction de Demande (Bien X)")
prices_x = np.linspace(1, 20, 50)
demand_x = (alpha / (alpha + beta)) * (income / prices_x)

fig_demand, ax_demand = plt.subplots(figsize=(8, 3))
ax_demand.plot(prices_x, demand_x, color='purple', linewidth=2)
ax_demand.scatter(px, x_eq, color='green', s=100, zorder=5, label='Prix actuel')
ax_demand.set_xlabel('Prix du bien X (Px)')
ax_demand.set_ylabel('Quantité demandée')
ax_demand.legend()
st.pyplot(fig_demand)
