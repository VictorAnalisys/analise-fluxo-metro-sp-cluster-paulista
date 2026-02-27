import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd

from pathlib import Path

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 11
})

sns.set(style="whitegrid")

#----------comparação de médias por grupo---------------
def plot_group_means(df_paulista, df_linha2, df_outras):
    """
    Comparação Visual do fluxo médio diário entre grupos.
    """
    
    means =  [
        df_paulista["fluxo"].mean(),
        df_linha2["fluxo"].mean(),
        df_outras["fluxo"].mean()
    ]
    
    labels = [
        "Cluster Paulista",
        "Linha 2 (sem Paulista)",
        "Outras Linhas"
    ]
    
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    
    plt.figure(figsize=(9, 6))
    bars = plt.bar(labels, means, color=colors)
    
    plt.title("Comparação de Fluxo Médio Diário por Grupo", fontsize=14)
    plt.ylabel("Fluxo Médio Diário (passageiros)", fontsize=11)
    plt.xticks(rotation=15)
    
    #Remover topo e direita
    sns.despine()
    
    #Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{int(height):,}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=10
        )
    
    plt.tight_layout()
    
    #Salvar automaticamente
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "outputs" / "figures"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "comparacao_medias.png"
    
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    
    plt.show()
#-------------------------------------------------------


#-------------- Evolução Mensal-------------------------
def plot_monthly_trends(media_paulista,
                        media_linha2,
                        media_outras):

    """
    Gráfico de linhas da evolução mensal
    """
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(media_paulista.index,
            media_paulista.values,
            marker="o",
            label="Cluster Paulista")
    
    plt.plot(media_linha2.index,
            media_linha2.values,
            marker="o",
            label="Linha 2 (sem paulista)")
    
    plt.plot(media_outras.index,
            media_outras.values,
            marker="o",
            label="Outras Linhas")
    
    plt.title("Evolução Mensal do Fluxo Médio")
    plt.xlabel("Mês")
    plt.ylabel("Fluxo Médio")
    plt.legend()
    plt.tight_layout()
    
    #salvar automaticamente
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "outputs" / "figures"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "evolucao_mensal.png"
    
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    
    plt.show()
#--------------------------------------------------


#------------Heatmap da Correlação mensal----------
def plot_cluster_correlation(corr_matrix):
    """
    Heatmap da correlação entre estações do Cluster Paulista.
    """
    
    plt.figure(figsize=(7, 6))
    
    sns.heatmap(corr_matrix,
                annot=True,
                cmap="mako",
                fmt="2f",
                vmin=0.97,
                vmax=1.00,
                linewidths=0.6,
                square=True,
                cbar_kws={"shrink": 0.8,
                        "label": "Coeficiente de Correlação (Pearson)"
                        }
                )
    
    plt.title("Correlação entre Estações - Cluster Paulista")
    plt.xlabel("")
    plt.ylabel("")
    
    sns.despine(left=True, bottom=True)
    
    plt.tight_layout()
    
    #Caminho absoluto baseado na raiz do projeto
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "outputs" / "figures"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "heatmap_cluster_paulista.png"
    
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    
    plt.show()
#--------------------------------------------------


#------------Boxplot entre cluster e linhas--------

def plot_group_boxplot(df_paulista, df_linha2, df_outras):
    """
    Boxplot comparando a distribuição do fluxo diário entre os grupos.
    """
    
    #Criar dataframe consolidado
    df_box = pd.DataFrame({
        "fluxo": pd.concat([
            df_paulista["fluxo"],
            df_linha2["fluxo"],
            df_outras["fluxo"]
        ], ignore_index=True),
        
        "grupo": (
            ["Cluster Paulista"] * len(df_paulista) +
            ["Linha 2 (sem Paulista)"] * len(df_linha2) +
            ["Outras Linhas"] * len(df_outras)
        )
    })
    
    plt.figure(figsize=(9, 6))
    
    sns.boxplot(
        data=df_box,
        x="grupo",
        y="fluxo",
        palette=["#1f77b4", "#ff7f0e", "#2ca02c"]
    )
    
    plt.title("Distribuição do Fluxo Diário por Grupo")
    plt.ylabel("Fluxo Diário (passageiros)")
    plt.xlabel("")
    plt.xticks(rotation=15)
    
    sns.despine()
    plt.tight_layout()
    
    #Salvar automaticamente
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root /  "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "boxplot_comparative.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    
    plt.show()
    
#--------

def plot_interannual_comparison(media_cluster_ano):
    """
    Gráfico executivo de comparação interanual
    """

    os.makedirs("projeto-metro-sp/outputs/figures", exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(
        media_cluster_ano.index,
        media_cluster_ano[1],
        marker="o",
        linewidth=2,
        label="Cluster Paulista"
    )

    plt.plot(
        media_cluster_ano.index,
        media_cluster_ano[0],
        marker="o",
        linewidth=2,
        label="Não Cluster"
    )

    plt.title("Evolução Interanual - Cluster vs Sistema")
    plt.xlabel("Ano")
    plt.ylabel("Fluxo Médio Diário")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "projeto-metro-sp/outputs/figures/interannual_comparison.png",
        dpi=300
    )

    plt.show()