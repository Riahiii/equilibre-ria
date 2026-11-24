import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Économie Micro — RIAHI",
    page_icon="📊",
    layout="wide"
)

# --- SIGNATURE EN SIDEBAR ---
st.sidebar.markdown("## 📊 Économie Micro")
st.sidebar.caption("Pr. RIAHI · Microéconomie L1")
st.sidebar.markdown("---")

# --- MENU ---
mode = st.sidebar.radio(
    "Choisissez le mode :",
    ["Consommateur", "Producteur"],
    key="choix_mode"
)

st.sidebar.markdown("---")


# ==========================================
# FONCTION UTILITAIRE : légende propre
# ==========================================
def clean_legend(ax, two_eq=False):
    """Place la légende de façon lisible."""
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(
            handles, labels,
            loc='upper right',
            fontsize=8,
            ncol=2 if two_eq else 1,
            framealpha=0.9
        )


# ==========================================
# MODE CONSOMMATEUR
# ==========================================
if mode == "Consommateur":

    st.title("📈 Équilibre du Consommateur — RIAHI")
    st.markdown(
        "Ajustez les paramètres dans la barre latérale pour visualiser "
        "l'équilibre du consommateur (modèle Cobb-Douglas)."
    )

    # --- PARAMÈTRES EQ 1 ---
    st.sidebar.header("⚙️ Paramètres (Équilibre 1)")
    income = st.sidebar.slider("Revenu (R)", 10, 200, 100, 10, key="inc1")
    px = st.sidebar.slider("Prix du bien X (Px)", 1, 20, 4, 1, key="px1")
    py = st.sidebar.slider("Prix du bien Y (Py)", 1, 20, 5, 1, key="py1")
    alpha = st.sidebar.slider("Alpha (poids du bien X)", 0.1, 0.9, 0.5, 0.1, key="alpha1")
    beta = 1 - alpha

    # --- EQ 2 ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔄 Comparaison (Équilibre 2)")
    show_eq2 = st.sidebar.checkbox("Afficher un 2ème équilibre", value=False, key="eq2_cons")

    if show_eq2:
        income2 = st.sidebar.slider("Revenu 2 (R2)", 10, 200, 150, 10, key="inc2")
        px2 = st.sidebar.slider("Prix du bien X 2 (Px2)", 1, 20, 6, 1, key="px2")
        py2 = st.sidebar.slider("Prix du bien Y 2 (Py2)", 1, 20, 5, 1, key="py2")
    else:
        income2 = px2 = py2 = None

    # --- OPTIONS D'AFFICHAGE ---
    st.sidebar.markdown("---")
    st.sidebar.header("👁️ Options d'affichage")
    show_budget = st.sidebar.checkbox("Contrainte Budgétaire", value=True)
    show_indiff = st.sidebar.checkbox("Courbes d'Indifférence", value=True)
    show_eq_pt  = st.sidebar.checkbox("Point d'équilibre", value=True)

    # --- GARDE-FOU ---
    if not (show_budget or show_indiff or show_eq_pt):
        st.warning("⚠️ Activez au moins une couche d'affichage dans la barre latérale.")
        st.stop()

    # --- CALCULS EQ 1 ---
    x_eq = alpha * income / px
    y_eq = beta  * income / py
    u_eq = (x_eq * alpha) * (y_eq * beta)

    # --- CALCULS EQ 2 ---
    if show_eq2:
        x_eq2 = alpha * income2 / px2
        y_eq2 = beta  * income2 / py2
        u_eq2 = (x_eq2 * alpha) * (y_eq2 * beta)

    # ======================================
    # GRAPHIQUES SÉPARÉS
    # ======================================
    st.subheader("🎨 Construction progressive du graphique")

    max_x = max(income / px, income2 / px2 if show_eq2 else 0) * 1.25
    max_y = max(income / py, income2 / py2 if show_eq2 else 0) * 1.25

    def setup_ax(ax, title):
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Bien X')
        ax.set_ylabel('Bien Y')
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

    graphs = []
    if show_budget:   graphs.append("budget")
    if show_indiff:   graphs.append("indiff")
    if show_eq_pt:    graphs.append("eq")

    n_cols = 2
    cols = st.columns(n_cols)

    for idx, kind in enumerate(graphs):
        col = cols[idx % n_cols]
        with col:
            fig, ax = plt.subplots(figsize=(6, 4.5))

            if kind == "budget":
                x_b = np.linspace(0, income / px, 200)
                y_b = (income - px * x_b) / py
                ax.plot(x_b, y_b, color='blue', linewidth=2.5, label='Contrainte Budgétaire 1')
                ax.fill_between(x_b, 0, y_b, alpha=0.10, color='blue')

                if show_eq2:
                    x_b2 = np.linspace(0, income2 / px2, 200)
                    y_b2 = (income2 - px2 * x_b2) / py2
                    ax.plot(x_b2, y_b2, color='orange', linestyle='--', linewidth=2, label='Contrainte Budgétaire 2')
                    ax.fill_between(x_b2, 0, y_b2, alpha=0.08, color='orange')

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "① Contrainte Budgétaire")

            elif kind == "indiff":
                x_start = max(0.01, min(0.1, x_eq / 2))
                x_v = np.linspace(x_start, income / px * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v = (u_eq / (x_v * alpha)) * (1 / beta)
                mask = np.isfinite(y_v) & (y_v > 0)
                ax.plot(x_v[mask], y_v[mask], color='red', linewidth=2.5, label="Courbe d'Indifférence 1")

                if show_eq2:
                    x_start2 = max(0.01, min(0.1, x_eq2 / 2))
                    x_v2 = np.linspace(x_start2, income2 / px2 * 1.3, 400)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        y_v2 = (u_eq2 / (x_v2 * alpha)) * (1 / beta)
                    mask2 = np.isfinite(y_v2) & (y_v2 > 0)
                    ax.plot(x_v2[mask2], y_v2[mask2], color='purple', linestyle='--', linewidth=2, label="Courbe d'Indifférence 2")

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "② Courbe d'Indifférence")

            elif kind == "eq":
                x_b = np.linspace(0, income / px, 200)
                y_b = (income - px * x_b) / py
                ax.plot(x_b, y_b, color='lightgray', linewidth=1.2, label='CB (contexte)')

                x_start = max(0.01, min(0.1, x_eq / 2))
                x_v = np.linspace(x_start, income / px * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v = (u_eq / (x_v * alpha)) * (1 / beta)
                mask = np.isfinite(y_v) & (y_v > 0)
                ax.plot(x_v[mask], y_v[mask], color='mistyrose', linewidth=1.2, label='CI (contexte)')

                ax.scatter(x_eq, y_eq, color='green', s=180, zorder=5, edgecolor='black', label=f'E1 ({x_eq:.1f}, {y_eq:.1f})')
                ax.annotate("E1", (x_eq, y_eq), xytext=(10, 10), textcoords="offset points", fontsize=11, color='darkgreen', fontweight='bold')

                if show_eq2:
                    ax.scatter(x_eq2, y_eq2, color='darkorange', s=180, zorder=5, edgecolor='black', label=f'E2 ({x_eq2:.1f}, {y_eq2:.1f})')
                    ax.annotate("E2", (x_eq2, y_eq2), xytext=(10, 10), textcoords="offset points", fontsize=11, color='darkorange', fontweight='bold')

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "③ Point d'Équilibre")

            st.pyplot(fig)
            plt.close(fig)

    # --- VUE COMBINÉE ---
    with st.expander("🔎 Voir la vue combinée (toutes les couches superposées)"):
        fig_c, ax_c = plt.subplots(figsize=(10, 6))

        if show_budget:
            x_b = np.linspace(0, income / px, 200)
            y_b = (income - px * x_b) / py
            ax_c.plot(x_b, y_b, color='blue', linewidth=2, label='Contrainte Budgétaire 1')
            ax_c.fill_between(x_b, 0, y_b, alpha=0.08, color='blue')
            if show_eq2:
                x_b2 = np.linspace(0, income2 / px2, 200)
                y_b2 = (income2 - px2 * x_b2) / py2
                ax_c.plot(x_b2, y_b2, color='orange', linestyle='--', linewidth=2, label='Contrainte Budgétaire 2')

        if show_indiff:
            x_start = max(0.01, min(0.1, x_eq / 2))
            x_v = np.linspace(x_start, income / px * 1.3, 400)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_v = (u_eq / (x_v * alpha)) * (1 / beta)
            mask = np.isfinite(y_v) & (y_v > 0)
            ax_c.plot(x_v[mask], y_v[mask], color='red', linewidth=2, label="Courbe d'Indifférence 1")
            if show_eq2:
                x_start2 = max(0.01, min(0.1, x_eq2 / 2))
                x_v2 = np.linspace(x_start2, income2 / px2 * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v2 = (u_eq2 / (x_v2 * alpha)) * (1 / beta)
                mask2 = np.isfinite(y_v2) & (y_v2 > 0)
                ax_c.plot(x_v2[mask2], y_v2[mask2], color='purple', linestyle='--', linewidth=2, label="Courbe d'Indifférence 2")

        if show_eq_pt:
            ax_c.scatter(x_eq, y_eq, color='green', s=150, zorder=5, edgecolor='black', label=f'E1 ({x_eq:.1f}, {y_eq:.1f})')
            if show_eq2:
                ax_c.scatter(x_eq2, y_eq2, color='darkorange', s=150, zorder=5, edgecolor='black', label=f'E2 ({x_eq2:.1f}, {y_eq2:.1f})')

        setup_ax(ax_c, "Vue combinée — Équilibre du Consommateur")
        ax_c.legend(loc='upper right', fontsize=8, ncol=2 if show_eq2 else 1)
        st.pyplot(fig_c)
        plt.close(fig_c)

    # ======================================
    # RÉSULTATS
    # ======================================
    st.subheader("📌 Résultats — Équilibre 1")
    c1, c2, c3 = st.columns(3)
    c1.metric("X* (Bien X)", f"{x_eq:.2f}")
    c2.metric("Y* (Bien Y)", f"{y_eq:.2f}")
    c3.metric("Utilité U*", f"{u_eq:.3f}")

    if show_eq2:
        st.subheader("📌 Résultats — Équilibre 2")
        c1, c2, c3 = st.columns(3)
        c1.metric("X*₂", f"{x_eq2:.2f}", delta=f"{x_eq2 - x_eq:+.2f}")
        c2.metric("Y*₂", f"{y_eq2:.2f}", delta=f"{y_eq2 - y_eq:+.2f}")
        c3.metric("U*₂", f"{u_eq2:.3f}", delta=f"{u_eq2 - u_eq:+.3f}")

    st.info(
        "💡 *Condition d'optimalité (Cobb-Douglas)* : à l'équilibre, le TMS égale le rapport des prix.\n\n"
        f"*X\\ = α · R/Px = {alpha:.1f} × {income}/{px} = {x_eq:.2f}**  \n"
        f"*Y\\ = (1−α) · R/Py = {beta:.1f} × {income}/{py} = {y_eq:.2f}**"
    )

    with st.expander("📖 Voir les formules utilisées"):
        st.latex(r"U(X,Y) = X^\alpha \, Y^\beta, \quad \beta = 1-\alpha")
        st.latex(r"X^* = \frac{\alpha}{\alpha+\beta} \cdot \frac{R}{P_x}")
        st.latex(r"Y^* = \frac{\beta}{\alpha+\beta} \cdot \frac{R}{P_y}")
        st.latex(r"U^* = (X^*)^\alpha \, (Y^*)^\beta")


# ==========================================
# MODE PRODUCTEUR
# ==========================================
else:

    st.title("🏭 Équilibre du Producteur (Cobb-Douglas) — RIAHI")
    st.markdown(
        "Ajustez les paramètres pour visualiser la minimisation des coûts du producteur."
    )

    st.sidebar.header("⚙️ Paramètres (Équilibre 1)")
    cost = st.sidebar.slider("Coût total (C)", 10, 200, 100, 10, key="cost1")
    w = st.sidebar.slider("Salaire (w)", 1, 20, 4, 1, key="w1")
    r = st.sidebar.slider("Taux de location (r)", 1, 20, 5, 1, key="r1")
    alpha_p = st.sidebar.slider("Alpha (poids du travail L)", 0.1, 0.9, 0.5, 0.1, key="alpha_p")
    beta_p = 1 - alpha_p

    st.sidebar.markdown("---")
    st.sidebar.header("🔄 Comparaison (Équilibre 2)")
    show_eq2 = st.sidebar.checkbox("Afficher un 2ème équilibre", value=False, key="eq2_prod")

    if show_eq2:
        cost2 = st.sidebar.slider("Coût total 2 (C2)", 10, 200, 150, 10, key="cost2")
        w2 = st.sidebar.slider("Salaire 2 (w2)", 1, 20, 6, 1, key="w2")
        r2 = st.sidebar.slider("Taux de location 2 (r2)", 1, 20, 5, 1, key="r2")
    else:
        cost2 = w2 = r2 = None

    st.sidebar.markdown("---")
    st.sidebar.header("👁️ Options d'affichage")
    show_isocost   = st.sidebar.checkbox("Droites d'Isocoût", value=True)
    show_isoquant  = st.sidebar.checkbox("Isoquantes", value=True)
    show_eq_pt     = st.sidebar.checkbox("Point d'équilibre", value=True)

    if not (show_isocost or show_isoquant or show_eq_pt):
        st.warning("⚠️ Activez au moins une couche d'affichage dans la barre latérale.")
        st.stop()

    L_eq = alpha_p * cost / w
    K_eq = beta_p  * cost / r
    Q_eq = (L_eq * alpha_p) * (K_eq * beta_p)

    if show_eq2:
        L_eq2 = alpha_p * cost2 / w2
        K_eq2 = beta_p  * cost2 / r2
        Q_eq2 = (L_eq2 * alpha_p) * (K_eq2 * beta_p)

    # ======================================
    # GRAPHIQUES SÉPARÉS
    # ======================================
    st.subheader("🎨 Construction progressive du graphique")

    max_L = max(cost / w, cost2 / w2 if show_eq2 else 0) * 1.25
    max_K = max(cost / r, cost2 / r2 if show_eq2 else 0) * 1.25

    def setup_ax_prod(ax, title):
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Travail (L)')
        ax.set_ylabel('Capital (K)')
        ax.set_xlim(0, max_L)
        ax.set_ylim(0, max_K)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

    graphs = []
    if show_isocost:   graphs.append("isocost")
    if show_isoquant:  graphs.append("isoquant")
    if show_eq_pt:     graphs.append("eq")

    n_cols = 2
    cols = st.columns(n_cols)

    for idx, kind in enumerate(graphs):
        col = cols[idx % n_cols]
        with col:
            fig, ax = plt.subplots(figsize=(6, 4.5))

            if kind == "isocost":
                L_iso = np.linspace(0, cost / w, 200)
                K_iso = (cost - w * L_iso) / r
                ax.plot(L_iso, K_iso, color='blue', linewidth=2.5, label='Isocoût 1')
                ax.fill_between(L_iso, 0, K_iso, alpha=0.10, color='blue')

                if show_eq2:
                    L_iso2 = np.linspace(0, cost2 / w2, 200)
                    K_iso2 = (cost2 - w2 * L_iso2) / r2
                    ax.plot(L_iso2, K_iso2, color='orange', linestyle='--', linewidth=2, label='Isocoût 2')
                    ax.fill_between(L_iso2, 0, K_iso2, alpha=0.08, color='orange')

                ax.legend(loc='best', fontsize=8)
                setup_ax_prod(ax, "① Droite d'Isocoût")

            elif kind == "isoquant":
                L_start = max(0.01, min(0.1, L_eq / 2))
                L_v = np.linspace(L_start, cost / w * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    K_v = (Q_eq / (L_v * alpha_p)) * (1 / beta_p)
                mask = np.isfinite(K_v) & (K_v > 0)
                ax.plot(L_v[mask], K_v[mask], color='red', linewidth=2.5, label='Isoquante 1')

                if show_eq2:
                    L_start2 = max(0.01, min(0.1, L_eq2 / 2))
                    L_v2 = np.linspace(L_start2, cost2 / w2 * 1.3, 400)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        K_v2 = (Q_eq2 / (L_v2 * alpha_p)) * (1 / beta_p)
                    mask2 = np.isfinite(K_v2) & (K_v2 > 0)
                    ax.plot(L_v2[mask2], K_v2[mask2], color='purple', linestyle='--', linewidth=2, label='Isoquante 2')

                ax.legend(loc='best', fontsize=8)
                setup_ax_prod(ax, "② Isoquante")

            elif kind == "eq":
                L_iso = np.linspace(0, cost / w, 200)
                K_iso = (cost - w * L_iso) / r
                ax.plot(L_iso, K_iso, color='lightgray', linewidth=1.2, label='Isocoût (contexte)')

                L_start = max(0.01, min(0.1, L_eq / 2))
                L_v = np.linspace(L_start, cost / w * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    K_v = (Q_eq / (L_v * alpha_p)) * (1 / beta_p)
                mask = np.isfinite(K_v) & (K_v > 0)
                ax.plot(L_v[mask], K_v[mask], color='mistyrose', linewidth=1.2, label='Isoquante (contexte)')

                ax.scatter(L_eq, K_eq, color='green', s=180, zorder=5, edgecolor='black', label=f'E1 (L={L_eq:.1f}, K={K_eq:.1f})')
                ax.annotate("E1", (L_eq, K_eq), xytext=(10, 10), textcoords="offset points", fontsize=11, color='darkgreen', fontweight='bold')

                if show_eq2:
                    ax.scatter(L_eq2, K_eq2, color='darkorange', s=180, zorder=5, edgecolor='black', label=f'E2 (L={L_eq2:.1f}, K={K_eq2:.1f})')
                    ax.annotate("E2", (L_eq2, K_eq2), xytext=(10, 10), textcoords="offset points", fontsize=11, color='darkorange', fontweight='bold')

                ax.legend(loc='best', fontsize=8)
                setup_ax_prod(ax, "③ Point d'Équilibre")

            st.pyplot(fig)
            plt.close(fig)

    # --- VUE COMBINÉE ---
    with st.expander("🔎 Voir la vue combinée (toutes les couches superposées)"):
        fig_c, ax_c = plt.subplots(figsize=(10, 6))

        if show_isocost:
            L_iso = np.linspace(0, cost / w, 200)
            K_iso = (cost - w * L_iso) / r
            ax_c.plot(L_iso, K_iso, color='blue', linewidth=2, label='Isocoût 1')
            ax_c.fill_between(L_iso, 0, K_iso, alpha=0.08, color='blue')
            if show_eq2:
                L_iso2 = np.linspace(0, cost2 / w2, 200)
                K_iso2 = (cost2 - w2 * L_iso2) / r2
                ax_c.plot(L_iso2, K_iso2, color='orange', linestyle='--', linewidth=2, label='Isocoût 2')

        if show_isoquant:
            L_start = max(0.01, min(0.1, L_eq / 2))
            L_v = np.linspace(L_start, cost / w * 1.3, 400)
            with np.errstate(divide='ignore', invalid='ignore'):
                K_v = (Q_eq / (L_v * alpha_p)) * (1 / beta_p)
            mask = np.isfinite(K_v) & (K_v > 0)
            ax_c.plot(L_v[mask], K_v[mask], color='red', linewidth=2, label='Isoquante 1')
            if show_eq2:
                L_start2 = max(0.01, min(0.1, L_eq2 / 2))
                L_v2 = np.linspace(L_start2, cost2 / w2 * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    K_v2 = (Q_eq2 / (L_v2 * alpha_p)) * (1 / beta_p)
                mask2 = np.isfinite(K_v2) & (K_v2 > 0)
                ax_c.plot(L_v2[mask2], K_v2[mask2], color='purple', linestyle='--', linewidth=2, label='Isoquante 2')

        if show_eq_pt:
            ax_c.scatter(L_eq, K_eq, color='green', s=150, zorder=5, edgecolor='black', label=f'E1 (L={L_eq:.1f}, K={K_eq:.1f})')
            if show_eq2:
                ax_c.scatter(L_eq2, K_eq2, color='darkorange', s=150, zorder=5, edgecolor='black', label=f'E2 (L={L_eq2:.1f}, K={K_eq2:.1f})')

        setup_ax_prod(ax_c, "Vue combinée — Équilibre du Producteur")
        ax_c.legend(loc='upper right', fontsize=8, ncol=2 if show_eq2 else 1)
        st.pyplot(fig_c)
        plt.close(fig_c)

    # ======================================
    # RÉSULTATS
    # ======================================
    st.subheader("📌 Résultats — Équilibre 1")
    c1, c2, c3 = st.columns(3)
    c1.metric("L* (Travail)", f"{L_eq:.2f}")
    c2.metric("K* (Capital)", f"{K_eq:.2f}")
    c3.metric("Q* (Production)", f"{Q_eq:.3f}")

    if show_eq2:
        st.subheader("📌 Résultats — Équilibre 2")
        c1, c2, c3 = st.columns(3)
        c1.metric("L*₂", f"{L_eq2:.2f}", delta=f"{L_eq2 - L_eq:+.2f}")
        c2.metric("K*₂", f"{K_eq2:.2f}", delta=f"{K_eq2 - K_eq:+.2f}")
        c3.metric("Q*₂", f"{Q_eq2:.3f}", delta=f"{Q_eq2 - Q_eq:+.3f}")

    st.info(
        "💡 *Condition d'optimalité (Cobb-Douglas)* : à l'équilibre, le TMST égale le rapport des prix des facteurs.\n\n"
        f"*L\\ = α · C/w = {alpha_p:.1f} × {cost}/{w} = {L_eq:.2f}**  \n"
        f"*K\\ = (1−α) · C/r = {beta_p:.1f} × {cost}/{r} = {K_eq:.2f}**"
    )

    with st.expander("📖 Voir les formules utilisées"):
        st.latex(r"Q(L,K) = L^\alpha \, K^\beta, \quad \beta = 1-\alpha")
        st.latex(r"L^* = \frac{\alpha}{\alpha+\beta} \cdot \frac{C}{w}")
        st.latex(r"K^* = \frac{\beta}{\alpha+\beta} \cdot \frac{C}{r}")
        st.latex(r"Q^* = (L^*)^\alpha \, (K^*)^\beta")

# ==========================================
# FOOTER COMMUN
# ==========================================
st.markdown("---")
st.caption("© 2026 — Pr. RIAHI · Outil pédagogique de microéconomie · Modèle Cobb-Douglas")
