import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR    = PROJECT_DIR / 'data'
VIZ_DIR     = PROJECT_DIR / 'outputs' / 'visualisations'
VIZ_DIR.mkdir(parents=True, exist_ok=True)

def sauvegarder(fig, nom):
    fig.savefig(VIZ_DIR / nom, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'✓ {nom}')

# --- Chargement ---
df   = pd.read_csv('/Users/mac/Downloads/audit_d_dataset.csv')
jobs = pd.read_csv(DATA_DIR / 'jobs.csv')

df = df.merge(jobs[['profession_id','profession_label','sector_label']], on='profession_id', how='left')

# Simplifier les choix
df['choix_simple'] = df['choice'].map({
    'A man':                               'Homme',
    'A woman':                             'Femme',
    'Both equally':                        'Les deux',
    'Cannot be determined from gender alone': 'Impossible',
})

print(f'Réponses : {len(df)}')
print(df['choix_simple'].value_counts())

# =======================================================================
# 1. Répartition globale des choix de GPT
# =======================================================================
counts = df['choix_simple'].value_counts()
colors = ['#1e90ff', '#e91e8c', '#2ecc71', '#95a5a6']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(counts.index, counts.values, color=colors)
ax.bar_label(bars, fmt='%d', padding=4)
ax.set_title('Répartition globale des choix de GPT\n(prompts directs "who is more likely")',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Choix')
ax.set_ylabel('Nombre de réponses')
sauvegarder(fig, '22_repartition_choix_gpt.png')

# =======================================================================
# 2. Répartition des choix par secteur
# =======================================================================
pivot = (
    df.groupby(['sector_label', 'choix_simple'])
    .size()
    .unstack(fill_value=0)
)
# Normaliser en %
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 6))
pivot_pct.plot(kind='bar', ax=ax,
               color={'Homme': '#1e90ff', 'Femme': '#e91e8c',
                      'Les deux': '#2ecc71', 'Impossible': '#95a5a6'},
               width=0.7)
ax.set_title('Répartition des choix de GPT par secteur (%)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Secteur')
ax.set_ylabel('%')
ax.legend(title='Choix')
plt.xticks(rotation=30, ha='right')
sauvegarder(fig, '23_choix_gpt_par_secteur.png')

# =======================================================================
# 3. Proportion de justifications stéréotypées par secteur
#    (score_stereo > 0.5 = justification contient un raisonnement stéréotypé)
# =======================================================================
SEUIL = 0.5
scores = ['score_tech', 'score_fact', 'score_geo', 'score_politic', 'score_stereo']
labels = ['Technique', 'Factuel', 'Géographique', 'Politique', 'Stéréotype']

prop_secteur = pd.DataFrame({
    label: (df.groupby('sector_label')[col].apply(lambda x: (x > SEUIL).mean()) * 100)
    for col, label in zip(scores, labels)
})

fig, ax = plt.subplots(figsize=(13, 6))
prop_secteur.plot(kind='bar', ax=ax, colormap='tab10', width=0.7)
ax.set_title(
    'Proportion des justifications de GPT contenant un raisonnement biaisé par secteur (%)\n'
    f'(score > {SEUIL} = justification biaisée selon la dimension)',
    fontsize=12, fontweight='bold')
ax.set_xlabel('Secteur')
ax.set_ylabel('% des justifications')
ax.legend(title='Type de raisonnement', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
plt.xticks(rotation=25, ha='right')
sauvegarder(fig, '24_proportion_justifications_biaisees.png')

# =======================================================================
# 4. Top 10 métiers où GPT justifie le plus par des stéréotypes
# =======================================================================
top_justif = (
    df.groupby('profession_label')['score_stereo']
    .apply(lambda x: (x > SEUIL).mean() * 100)
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.barh(top_justif.index[::-1], top_justif.values[::-1], color='#e74c3c')
ax.bar_label(bars, fmt='%.0f%%', padding=4, fontsize=9)
ax.set_title(
    'Top 10 métiers où GPT justifie le plus son choix par des stéréotypes\n'
    '(% de justifications avec score_stereo > 0.5)',
    fontsize=12, fontweight='bold')
ax.set_xlabel('% des justifications stéréotypées')
ax.set_xlim(0, 115)
sauvegarder(fig, '25_top_metiers_justifications_stereo.png')

# =======================================================================
# 6. Quand GPT justifie par stéréotype — quel choix fait-il ?
#    Proportion de justifications stéréotypées (score_stereo > 0.5) par choix
# =======================================================================
prop_stereo_choix = (
    df.groupby('choix_simple')['score_stereo']
    .apply(lambda x: (x > SEUIL).mean() * 100)
    .reindex(['Homme', 'Femme', 'Les deux', 'Impossible'])
)

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#1e90ff', '#e91e8c', '#2ecc71', '#95a5a6']
bars = ax.bar(prop_stereo_choix.index, prop_stereo_choix.values, color=colors)
ax.bar_label(bars, fmt='%.0f%%', padding=4)
ax.set_title('% de justifications stéréotypées selon le choix de GPT\n'
             '(quand GPT choisit "Homme", justifie-t-il plus par des stéréotypes ?)',
             fontsize=12, fontweight='bold')
ax.set_xlabel('Choix de GPT')
ax.set_ylabel('% des justifications avec score_stereo > 0.5')
ax.set_ylim(0, 110)
sauvegarder(fig, '26_justif_stereo_par_choix.png')

# =======================================================================
# 7. HTML interactif : choix de GPT par métier (top 20 justif. stéréotypées)
# =======================================================================
try:
    import plotly.graph_objects as go

    top20_justif = (
        df.groupby('profession_label')['score_stereo']
        .apply(lambda x: (x > SEUIL).mean())
        .sort_values(ascending=False)
        .head(20)
        .index
    )
    choix_metier = df[df['profession_label'].isin(top20_justif)].groupby(
        ['profession_label', 'choix_simple']).size().unstack(fill_value=0)
    choix_metier = choix_metier.reindex(top20_justif)

    fig_html = go.Figure()
    color_map = {'Homme': '#1e90ff', 'Femme': '#e91e8c',
                 'Les deux': '#2ecc71', 'Impossible': '#95a5a6'}

    for choix in ['Homme', 'Femme', 'Les deux', 'Impossible']:
        if choix in choix_metier.columns:
            fig_html.add_trace(go.Bar(
                name=choix,
                x=choix_metier.index,
                y=choix_metier[choix],
                marker_color=color_map[choix],
            ))

    fig_html.update_layout(
        title='Choix de GPT — Top 20 métiers avec le plus de justifications stéréotypées\n'
              '(métiers où GPT justifie le plus souvent avec des stéréotypes)',
        xaxis_title='Métier',
        yaxis_title='Nombre de réponses',
        barmode='stack',
        legend_title='Choix de GPT',
        height=600,
    )
    fig_html.write_html(str(VIZ_DIR / '27_audit_metiers_interactif.html'))
    print('✓ 27_audit_metiers_interactif.html')

except ImportError:
    print('  (plotly non installé)')

# =======================================================================
# 8. Tableau heatmap — Top 10 métiers (Homme/Femme uniquement)
#    Scores moyens par dimension pour voir ce qui s'associe au stéréotype
# =======================================================================
# Filtrer : on garde seulement quand GPT choisit Homme ou Femme
df_genre = df[df['choix_simple'].isin(['Homme', 'Femme'])].copy()

scores     = ['score_stereo', 'score_tech', 'score_fact', 'score_geo', 'score_politic']
labels_col = ['Stéréotype', 'Technique', 'Factuel', 'Géographique', 'Politique']

top10 = (
    df_genre.groupby('profession_label')['score_stereo']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .index
)

heatmap_data = (
    df_genre[df_genre['profession_label'].isin(top10)]
    .groupby('profession_label')[scores]
    .mean()
    .loc[top10]
    .rename(columns=dict(zip(scores, labels_col)))
)

fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)

ax.set_xticks(range(len(labels_col)))
ax.set_xticklabels(labels_col, fontsize=11)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(top10, fontsize=9)

# Valeurs dans chaque cellule
for i in range(len(top10)):
    for j in range(len(labels_col)):
        val = heatmap_data.values[i, j]
        couleur = 'white' if val > 0.6 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                fontsize=9, color=couleur, fontweight='bold')

plt.colorbar(im, ax=ax, label='Score moyen (0 à 1)')
ax.set_title(
    'Top 10 métiers (score stéréotype le plus élevé) — scores associés\n'
    'Filtré sur les choix "Homme" ou "Femme" uniquement',
    fontsize=12, fontweight='bold')
plt.tight_layout()
sauvegarder(fig, '28_heatmap_top10_metiers_scores.png')

# Même chose : barres groupées pour plus de lisibilité
fig, ax = plt.subplots(figsize=(14, 6))
heatmap_data.plot(kind='bar', ax=ax, colormap='tab10', width=0.75)
ax.set_title(
    'Top 10 métiers — scores moyens par dimension de biais dans la justification\n'
    '(filtré sur choix "Homme" ou "Femme" — quelles raisons accompagnent le stéréotype ?)',
    fontsize=11, fontweight='bold')
ax.set_xlabel('Métier')
ax.set_ylabel('Score moyen (0 à 1)')
ax.set_ylim(0, 1.15)
ax.legend(title='Dimension', bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
plt.xticks(rotation=35, ha='right')
sauvegarder(fig, '29_top10_metiers_dimensions.png')

# =======================================================================
# 9. Tableau récapitulatif par métier
#    Pour chaque métier : nb prompts, nb Homme, nb Femme, scores moyens par choix
# =======================================================================
TABLE_DIR = PROJECT_DIR / 'outputs' / 'tables'
TABLE_DIR.mkdir(parents=True, exist_ok=True)

scores_cols = ['score_stereo', 'score_tech', 'score_fact', 'score_geo', 'score_politic']

lignes = []
for metier, grp in df.groupby('profession_label'):
    total      = len(grp)
    nb_homme   = (grp['choix_simple'] == 'Homme').sum()
    nb_femme   = (grp['choix_simple'] == 'Femme').sum()
    pct_homme  = round(nb_homme / total * 100, 1) if total else 0
    pct_femme  = round(nb_femme / total * 100, 1) if total else 0

    grp_h = grp[grp['choix_simple'] == 'Homme']
    grp_f = grp[grp['choix_simple'] == 'Femme']

    ligne = {
        'metier':     metier,
        'secteur':    grp['sector_label'].iloc[0],
        'nb_prompts': total,
        'nb_homme':   nb_homme,
        'pct_homme':  pct_homme,
        'nb_femme':   nb_femme,
        'pct_femme':  pct_femme,
    }
    for col in scores_cols:
        short = col.replace('score_', '')
        ligne[f'H_{short}'] = round(grp_h[col].mean(), 3) if len(grp_h) else None
        ligne[f'F_{short}'] = round(grp_f[col].mean(), 3) if len(grp_f) else None

    lignes.append(ligne)

df_table = pd.DataFrame(lignes).sort_values('pct_homme', ascending=False)
df_table.to_csv(TABLE_DIR / 'tableau_metiers_choix_scores.csv', index=False)
print('✓ tableau_metiers_choix_scores.csv')

# Visualisation : top 15 métiers les plus "Homme" — barres Homme vs Femme
top15 = df_table.head(15)
fig, ax = plt.subplots(figsize=(13, 6))
x = range(len(top15))
w = 0.4
b_h = ax.bar([i - w/2 for i in x], top15['pct_homme'], width=w, label='Homme', color='#1e90ff')
b_f = ax.bar([i + w/2 for i in x], top15['pct_femme'], width=w, label='Femme', color='#e91e8c')
ax.bar_label(b_h, fmt='%.0f%%', padding=3, fontsize=8)
ax.bar_label(b_f, fmt='%.0f%%', padding=3, fontsize=8)
ax.set_xticks(list(x))
ax.set_xticklabels(top15['metier'], rotation=35, ha='right', fontsize=8)
ax.set_title('Top 15 métiers les plus orientés "Homme" par GPT\n(% des prompts où GPT choisit Homme ou Femme)',
             fontsize=12, fontweight='bold')
ax.set_ylabel('% des prompts')
ax.legend()
sauvegarder(fig, '30_top15_metiers_homme_femme.png')

print(f'\n✓ Visualisations audit → {VIZ_DIR}')
