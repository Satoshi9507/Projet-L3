"""
Visualisations basées sur les fichiers du projet :
- data/responses_Qwen.csv, responses_gpt.csv, responses_meta-llama.csv, responses_mistralai.csv
- data/audit_gpt_dataset.csv, audit_qwen_dataset.csv, audit_llma_dataset.csv, audit_mistralai_dataset.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from textblob import TextBlob

DATA_DIR = Path(__file__).parent / 'data'
VIZ_DIR  = Path(__file__).parent / 'Visualisation'
VIZ_DIR.mkdir(parents=True, exist_ok=True)

def sauvegarder(fig, nom):
    fig.savefig(VIZ_DIR / nom, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'✓ {nom}')

def ajouter_polarite(df):
    df['polarity'] = df['response_text'].fillna('').apply(lambda t: TextBlob(t).sentiment.polarity)
    df['length']   = df['response_text'].fillna('').apply(len)
    return df

# --- Chargement ---
jobs    = pd.read_csv(DATA_DIR / 'jobs.csv')
prompts = pd.read_csv(DATA_DIR / 'prompts.csv')

print('Calcul de la polarité...')
qwen    = ajouter_polarite(pd.read_csv(DATA_DIR / 'responses_Qwen.csv'))
llama   = ajouter_polarite(pd.read_csv(DATA_DIR / 'responses_meta-llama.csv'))
mistral = ajouter_polarite(pd.read_csv(DATA_DIR / 'responses_mistralai.csv'))
gpt     = ajouter_polarite(pd.read_csv(DATA_DIR / 'responses_gpt.csv'))

for df, nom in [(qwen,'Qwen'),(llama,'Llama'),(mistral,'Mistral'),(gpt,'GPT')]:
    df['model_nom'] = nom

df_all = pd.concat([qwen, llama, mistral, gpt], ignore_index=True)
df_all = df_all.merge(prompts[['prompt_id','profession_id','gender_id']], on='prompt_id', how='left')
df_all = df_all.merge(jobs[['profession_id','profession_label','sector_label']], on='profession_id', how='left')

MODELES  = ['GPT','Qwen','Llama','Mistral']
COULEURS = ['#e74c3c','#3498db','#2ecc71','#f39c12']

# =======================================================================
# 1. Polarité globale par modèle
# =======================================================================
pol = df_all.groupby('model_nom')['polarity'].mean().reindex(MODELES)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(MODELES, pol.values, color=COULEURS)
ax.bar_label(bars, fmt='%.4f', padding=4)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Polarité moyenne par modèle (tous types de prompts)', fontsize=13, fontweight='bold')
ax.set_ylabel('Polarité (-1 à +1)')
sauvegarder(fig, 'collegue_polarite_globale.png')

# =======================================================================
# 2. Polarité par type de prompt
# =======================================================================
pivot = df_all.groupby(['model_nom','prompt_type'])['polarity'].mean().unstack().reindex(MODELES)

fig, ax = plt.subplots(figsize=(10, 5))
pivot.plot(kind='bar', ax=ax, colormap='Set2', width=0.6)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Polarité moyenne par type de prompt et par modèle', fontsize=13, fontweight='bold')
ax.set_xlabel('Modèle')
ax.set_ylabel('Polarité (-1 à +1)')
ax.legend(title='Type de prompt')
plt.xticks(rotation=0)
sauvegarder(fig, 'collegue_polarite_type_prompt.png')

# =======================================================================
# 3. Polarité par secteur
# =======================================================================
pivot = df_all.groupby(['model_nom','sector_label'])['polarity'].mean().unstack().reindex(MODELES)

fig, ax = plt.subplots(figsize=(13, 5))
pivot.plot(kind='bar', ax=ax, colormap='tab10', width=0.7)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Polarité moyenne par secteur et par modèle', fontsize=13, fontweight='bold')
ax.set_xlabel('Modèle')
ax.set_ylabel('Polarité (-1 à +1)')
ax.legend(title='Secteur', bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=8)
plt.xticks(rotation=0)
sauvegarder(fig, 'collegue_polarite_secteur.png')

# =======================================================================
# 4. Longueur des réponses par modèle
# =======================================================================
lon = df_all.groupby('model_nom')['length'].mean().reindex(MODELES)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(MODELES, lon.values, color=COULEURS)
ax.bar_label(bars, fmt='%.0f', padding=4)
ax.set_title('Longueur moyenne des réponses par modèle', fontsize=13, fontweight='bold')
ax.set_ylabel('Nombre de caractères moyen')
sauvegarder(fig, 'collegue_longueur_globale.png')

# =======================================================================
# 5. Répartition des choix (reponse_avancee_recuperation.csv)
# =======================================================================
rep = pd.read_csv(DATA_DIR / 'reponse_avancee_recuperation.csv')
rep['model_nom'] = rep['model'].map({
    'Qwen': 'Qwen', 'meta-llama': 'Llama',
    'mistralai': 'Mistral', 'gpt': 'GPT'
})

pivot_choix = (
    rep.groupby(['model_nom','Réponse']).size()
    .unstack(fill_value=0).reindex(MODELES)
)
pivot_pct = pivot_choix.div(pivot_choix.sum(axis=1), axis=0) * 100

COUL_CHOIX = {
    'A répondu : HOMME':                    '#1e90ff',
    'A répondu : FEMME':                    '#e91e8c',
    'A répondu : LES DEUX':                 '#2ecc71',
    'A répondu : Impossible de considérer': '#95a5a6',
}

fig, ax = plt.subplots(figsize=(10, 6))
bottom = pd.Series([0.0]*len(MODELES), index=MODELES)
for choix, color in COUL_CHOIX.items():
    if choix in pivot_pct.columns:
        vals = pivot_pct[choix]
        ax.bar(MODELES, vals, bottom=bottom,
               label=choix.replace('A répondu : ',''), color=color, width=0.5)
        for i, (v, b) in enumerate(zip(vals, bottom)):
            if v > 4:
                ax.text(i, b+v/2, f'{v:.0f}%', ha='center', va='center',
                        fontsize=9, color='white', fontweight='bold')
        bottom += vals

ax.set_title('Répartition des choix de genre par modèle (%)\n(prompts directs)', fontsize=13, fontweight='bold')
ax.set_ylabel('%')
ax.set_ylim(0, 105)
ax.legend(title='Choix', bbox_to_anchor=(1.01, 1), loc='upper left')
sauvegarder(fig, 'collegue_repartition_choix_4modeles.png')

# =======================================================================
# 6. Répartition des choix par secteur — GPT, Qwen, Llama, Mistral
# =======================================================================
COULEURS_CHOIX = {'Homme':'#1e90ff','Femme':'#e91e8c','Impossible':'#95a5a6','Les deux':'#2ecc71'}

for nom, fichier in [('GPT', DATA_DIR/'audit_gpt_dataset.csv'),
                     ('Qwen', DATA_DIR/'audit_qwen_dataset.csv'),
                     ('Llama', DATA_DIR/'audit_llma_dataset.csv'),
                     ('Mistral', DATA_DIR/'audit_mistralai_dataset.csv')]:
    df = pd.read_csv(fichier)
    df = df.merge(jobs[['profession_id','profession_label','sector_label']], on='profession_id', how='left')
    df['choix_simple'] = df['choice'].map({
        'A man':'Homme','A woman':'Femme',
        'Both equally':'Les deux',
        'Cannot be determined from gender alone':'Impossible',
    })
    pivot = (df[df['choix_simple'].notna()]
             .groupby(['sector_label','choix_simple']).size()
             .unstack(fill_value=0))
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(13, 6))
    pivot_pct.plot(kind='bar', ax=ax,
                   color={c: COULEURS_CHOIX.get(c,'#999') for c in pivot_pct.columns},
                   width=0.7)
    ax.set_title(f'Répartition des choix de {nom} par secteur (%)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Secteur')
    ax.set_ylabel('%')
    ax.legend(title='Choix')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    sauvegarder(fig, f'choix_par_secteur_{nom}.png')

# =======================================================================
# 7. Heatmap top 10 métiers — GPT, Qwen, Llama
#    (depuis fichiers audit )
# =======================================================================
AUDITS = {
    'GPT':    DATA_DIR / 'audit_gpt_dataset.csv',
    'Qwen':   DATA_DIR / 'audit_qwen_dataset.csv',
    'Llama':  DATA_DIR / 'audit_llma_dataset.csv',
}

scores_cols = ['score_stereo','score_tech','score_fact','score_geo','score_politic']
labels_col  = ['Stéréotype','Technique','Factuel','Géographique','Politique']

for nom, fichier in AUDITS.items():
    df = pd.read_csv(fichier)
    df = df.merge(jobs[['profession_id','profession_label','sector_label']], on='profession_id', how='left')
    df_hf = df[df['choice'].isin(['A man','A woman'])].copy()

    if len(df_hf) < 10:
        print(f'  {nom} : pas assez de choix Homme/Femme ({len(df_hf)}), heatmap ignoré')
        continue

    top10 = (
        df_hf.groupby('profession_label')['score_stereo']
        .mean().sort_values(ascending=False).head(10).index
    )
    heatmap_data = (
        df_hf[df_hf['profession_label'].isin(top10)]
        .groupby('profession_label')[scores_cols].mean()
        .loc[top10]
        .rename(columns=dict(zip(scores_cols, labels_col)))
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
    ax.set_xticks(range(len(labels_col)))
    ax.set_xticklabels(labels_col, fontsize=11)
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10, fontsize=9)
    for i in range(len(top10)):
        for j in range(len(labels_col)):
            val = heatmap_data.values[i, j]
            couleur = 'white' if val > 0.6 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=9, color=couleur, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Score moyen (0 à 1)')
    ax.set_title(
        f'Top 10 métiers — scores associés ({nom})\n'
        'Filtré sur choix "Homme" ou "Femme" uniquement',
        fontsize=12, fontweight='bold')
    plt.tight_layout()
    sauvegarder(fig, f'heatmap_top10_metiers_{nom}.png')

print(f'\n✓ Tous les graphiques → {VIZ_DIR}')
