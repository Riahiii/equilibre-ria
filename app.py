# ======================================
    # GRAPHIQUES SÉPARÉS (un par couche)
    # ======================================
    st.subheader("🎨 Construction progressive du graphique")

    # Limites communes (pour que tous les graphes soient alignés)
    max_x = max(income / px, income2 / px2 if show_eq2 else 0) * 1.25
    max_y = max(income / py, income2 / py2 if show_eq2 else 0) * 1.25

    def setup_ax(ax, title):
        """Mise en forme commune à tous les sous-graphes."""
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Bien X')
        ax.set_ylabel('Bien Y')
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

    # Créer une grille : 2 colonnes
    # Nombre de graphes = nombre de couches actives
    graphs = []
    if show_budget:   graphs.append("budget")
    if show_indiff:   graphs.append("indiff")
    if show_eq_pt:    graphs.append("eq")

    # --- Disposition en grille 2 colonnes ---
    n_graphs = len(graphs)
    n_cols = 2
    n_rows = (n_graphs + 1) // 2

    cols = st.columns(n_cols)  # 2 colonnes

    # On parcourt les couches actives
    for idx, kind in enumerate(graphs):
        col = cols[idx % n_cols]  # alterne entre colonne 0 et 1
        with col:
            fig, ax = plt.subplots(figsize=(6, 4.5))

            # --- Couche : Contrainte budgétaire ---
            if kind == "budget":
                x_b = np.linspace(0, income / px, 200)
                y_b = (income - px * x_b) / py
                ax.plot(x_b, y_b, color='blue', linewidth=2.5,
                        label='Contrainte Budgétaire 1')
                ax.fill_between(x_b, 0, y_b, alpha=0.10, color='blue')

                if show_eq2:
                    x_b2 = np.linspace(0, income2 / px2, 200)
                    y_b2 = (income2 - px2 * x_b2) / py2
                    ax.plot(x_b2, y_b2, color='orange', linestyle='--',
                            linewidth=2, label='Contrainte Budgétaire 2')
                    ax.fill_between(x_b2, 0, y_b2, alpha=0.08, color='orange')

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "① Contrainte Budgétaire")

            # --- Couche : Courbe d'indifférence ---
            elif kind == "indiff":
                x_start = max(0.01, min(0.1, x_eq / 2))
                x_v = np.linspace(x_start, income / px * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v = (u_eq / (x_v * alpha)) * (1 / beta)
                mask = np.isfinite(y_v) & (y_v > 0)
                ax.plot(x_v[mask], y_v[mask], color='red', linewidth=2.5,
                        label="Courbe d'Indifférence 1")

                if show_eq2:
                    x_start2 = max(0.01, min(0.1, x_eq2 / 2))
                    x_v2 = np.linspace(x_start2, income2 / px2 * 1.3, 400)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        y_v2 = (u_eq2 / (x_v2 * alpha)) * (1 / beta)
                    mask2 = np.isfinite(y_v2) & (y_v2 > 0)
                    ax.plot(x_v2[mask2], y_v2[mask2], color='purple',
                            linestyle='--', linewidth=2,
                            label="Courbe d'Indifférence 2")

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "② Courbe d'Indifférence")

            # --- Couche : Point d'équilibre ---
            elif kind == "eq":
                # On ajoute les courbes en arrière-plan (grisées) pour contexte
                x_b = np.linspace(0, income / px, 200)
                y_b = (income - px * x_b) / py
                ax.plot(x_b, y_b, color='lightgray', linewidth=1.2,
                        label='CB (contexte)')

                x_start = max(0.01, min(0.1, x_eq / 2))
                x_v = np.linspace(x_start, income / px * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v = (u_eq / (x_v * alpha)) * (1 / beta)
                mask = np.isfinite(y_v) & (y_v > 0)
                ax.plot(x_v[mask], y_v[mask], color='mistyrose', linewidth=1.2,
                        label='CI (contexte)')

                # Point d'équilibre 1
                ax.scatter(x_eq, y_eq, color='green', s=180, zorder=5,
                           edgecolor='black',
                           label=f'E1 ({x_eq:.1f}, {y_eq:.1f})')
                ax.annotate("E1", (x_eq, y_eq), xytext=(10, 10),
                            textcoords="offset points",
                            fontsize=11, color='darkgreen', fontweight='bold')

                # Point d'équilibre 2
                if show_eq2:
                    ax.scatter(x_eq2, y_eq2, color='darkorange', s=180,
                               zorder=5, edgecolor='black',
                               label=f'E2 ({x_eq2:.1f}, {y_eq2:.1f})')
                    ax.annotate("E2", (x_eq2, y_eq2), xytext=(10, 10),
                                textcoords="offset points",
                                fontsize=11, color='darkorange',
                                fontweight='bold')

                ax.legend(loc='best', fontsize=8)
                setup_ax(ax, "③ Point d'Équilibre")

            st.pyplot(fig)
            plt.close(fig)

    # --- Option : vue combinée (toutes les couches ensemble) ---
    with st.expander("🔎 Voir la vue combinée (toutes les couches superposées)"):
        fig_c, ax_c = plt.subplots(figsize=(10, 6))

        if show_budget:
            x_b = np.linspace(0, income / px, 200)
            y_b = (income - px * x_b) / py
            ax_c.plot(x_b, y_b, color='blue', linewidth=2,
                      label='Contrainte Budgétaire 1')
            ax_c.fill_between(x_b, 0, y_b, alpha=0.08, color='blue')
            if show_eq2:
                x_b2 = np.linspace(0, income2 / px2, 200)
                y_b2 = (income2 - px2 * x_b2) / py2
                ax_c.plot(x_b2, y_b2, color='orange', linestyle='--',
                          linewidth=2, label='Contrainte Budgétaire 2')

        if show_indiff:
            x_start = max(0.01, min(0.1, x_eq / 2))
            x_v = np.linspace(x_start, income / px * 1.3, 400)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_v = (u_eq / (x_v * alpha)) * (1 / beta)
            mask = np.isfinite(y_v) & (y_v > 0)
            ax_c.plot(x_v[mask], y_v[mask], color='red', linewidth=2,
                      label="Courbe d'Indifférence 1")
            if show_eq2:
                x_start2 = max(0.01, min(0.1, x_eq2 / 2))
                x_v2 = np.linspace(x_start2, income2 / px2 * 1.3, 400)
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_v2 = (u_eq2 / (x_v2 * alpha)) * (1 / beta)
                mask2 = np.isfinite(y_v2) & (y_v2 > 0)
                ax_c.plot(x_v2[mask2], y_v2[mask2], color='purple',
                          linestyle='--', linewidth=2,
                          label="Courbe d'Indifférence 2")

        if show_eq_pt:
            ax_c.scatter(x_eq, y_eq, color='green', s=150, zorder=5,
                         edgecolor='black', label=f'E1 ({x_eq:.1f}, {y_eq:.1f})')
            if show_eq2:
                ax_c.scatter(x_eq2, y_eq2, color='darkorange', s=150,
                             zorder=5, edgecolor='black',
                             label=f'E2 ({x_eq2:.1f}, {y_eq2:.1f})')

        setup_ax(ax_c, "Vue combinée — Équilibre du Consommateur")
        ax_c.legend(loc='upper right', fontsize=8, ncol=2 if show_eq2 else 1)
        st.pyplot(fig_c)
        plt.close(fig_c)
