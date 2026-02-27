import pandas as pd

from src.descriptive_analysis import summarize_group
from src.data_processing import (
    parse_raw_file,
    create_paulista_dummy,
    create_analysis_groups
    )
from src.inferential_analysis import (
    test_normality,
    welch_t_test,
    mann_whitney_test,
    cohens_d,
    anova_teste,
    anova_eta_squared,
    correlation_test
    )
from src.visualization import (
    plot_group_means,
    plot_monthly_trends,
    plot_cluster_correlation,
    plot_group_boxplot,
    plot_interannual_comparison
    )


def main():
    #==============================================================================
    # BLOCO 1 - REPROCESSAMENTO DA BASE BRUTA
    # (Descomentar apenas quando alterar parsing/mapping))
    # (para funcionar você deve, descomentar, rodar o programa, comentar esta parte novamente, rodar novamente para carregar a base processada)
    
    anos = ["2023", "2024", "2025"]
    
    dfs = []
    
    for ano in anos:
        print(f"\nReprocessamento base {ano}...")
        
        df_temp = parse_raw_file(
            f"projeto-metro-sp/data/raw/passageiros_dia_{ano}.csv",
            year=ano
        )
        
        df_temp["ano"] = ano
        
        dfs.append(df_temp)
        
        print(f"Linhas processadas ({ano}):", len(df_temp))
    
    #Concatenar todos os anos
    df_historico = pd.concat(dfs, ignore_index=True)
    
    print("\nTotal consolidade:", len(df_historico))
    
    df_historico.to_csv(
        "projeto-metro-sp/data/processed/metro_2023_2024_2025_clean.csv",
        index=False
    )
    
    print("Dataset histórico salvo com sucesso")
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 2 - CARREGAR BASE PROCESSADA
    
    df = pd.read_csv(
        "projeto-metro-sp/data/processed/metro_2025_clean.csv",
    parse_dates=["data"]
    )
    
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 3 - VALIDAÇÃO DE INTEGRIDADE (DEBUG OPCIONAL)
    #(Descomentar se quiser validar mapping)
    
    #------------verificar estações desconhecidas------------------
    #print("\nQuantidade de estações DESCONHECIDAS:")
    #print((df["estacao"] == "DESCONHECIDA").sum())
    #------------verificar siglas não mapeadas---------------------
    #print("\nSiglas com estacao DESCONHECIDA:")
    #print(df[df["estacao"] == "DESCONHECIDA"]["sigla"].unique())
    #-------------verificar desconhecidas por linha----------------
    #print("\nDESCONHECIDAS POR LINHA:")
    #print(
        #df[df["estacao"] == "DESCONHECIDA"]
        #.groupby("linha")
        #.size()
    #)
    
    #------------verificar siglas da linha X----------------------
    #print("\nSIGLAS DA LINHA 2:")
    #print(df[df["linha"] == "2-VERDE"]["sigla"].unique())
    #------------verificar sigla x estação da linha X-------------
    #print("\nLINHA 2 - SIGLA X ESTACAO:")
    #print(
        #df[df["linha"] == "2-VERDE"][["sigla", "estacao"]]
        #.drop_duplicates()
        #.sort_values("sigla")
    #)
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 4 - PREPARAÇÃO PARA ANÁLISE
    
    df = create_paulista_dummy(df)
    
    df_paulista, df_linha2_sem_paulista, df_outras_linhas = create_analysis_groups(df)
    
    #------------verificar cluster paulista----------------------
    #print("\nEstações no Cluster Paulista:")
    #print(df[df["cluster_paulista"] == 1]["estacao"].unique())
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 5 - ANÁLISE DESCRITIVA
    
    print("\n" + "="*50)
    print("ANÁLISE COMPARATIVA - CLUSTER PAULISTA")
    print("="*50)
    
    summarize_group(df_paulista, "Cluster Paulista")
    summarize_group(df_linha2_sem_paulista, "Linha 2 (sem Paulista)")
    summarize_group(df_outras_linhas, "Outras Linhas")
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 6 - ANÁLISE INFERENCIAL
    
    print("\n" + "="*50)
    print("TESTES INFERENCIAIS")
    print("="*50)
    
    #------------teste de normalidade----------------------
    test_normality(df_paulista["fluxo"], "Cluster Paulista")
    test_normality(df_linha2_sem_paulista["fluxo"], "Linha 2 (sem Paulista)")
    test_normality(df_outras_linhas["fluxo"], "Outras Linhas")
    
    #------------teste t de welch-------------------------
    welch_t_test(
        df_paulista["fluxo"],
        df_linha2_sem_paulista["fluxo"],
        "Cluster Paulista",
        "Linha 2 (sem Paulista)"
    )
    #------------teste de Mann-Whitney----------------------
    mann_whitney_test(
        df_paulista["fluxo"],
        df_linha2_sem_paulista["fluxo"],
        "Cluster Paulista",
        "Linha 2 (sem Paulista)"
    )
    #------------teste de Cohen's d------------------------
    cohens_d(
        df_paulista["fluxo"],
        df_linha2_sem_paulista["fluxo"],
        "Cluster Paulista",
        "Linha 2 (sem Paulista)"
    )
    #--------------teste ANOVA------------------------------
    anova_teste(
        df[df["linha"] == "1-AZUL"]["fluxo"],
        df[df["linha"] == "2-VERDE"]["fluxo"],
        df[df["linha"] == "3-VERMELHA"]["fluxo"],
        df[df["linha"] == "15-PRATA"]["fluxo"]
    )
    #--------------eta squared para ANOVA-------------------
    anova_eta_squared(
        df[df["linha"] == "1-AZUL"]["fluxo"].values,
        df[df["linha"] == "2-VERDE"]["fluxo"].values,
        df[df["linha"] == "3-VERMELHA"]["fluxo"].values,
        df[df["linha"] == "15-PRATA"]["fluxo"].values
    )
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 7 - ANÁLISE DE CORRELAÇÃO ENTRE ESTAÇÕES DO CLUSTER PAULISTA
    
    print("\n" + "="*50)
    print("CORRELAÇÃO - CLUSTER PAULISTA")
    print("="*50)
    
    #Filtrar apenas as estações do cluster paulista
    df_cluster = df[df["cluster_paulista"] == 1]
    
    #Criar tabela pivot: fatas nas linhas, estações nas colunas
    df_pivot = df_cluster.pivot_table(
        index="data",
        columns="estacao",
        values="fluxo"
    )
    
    #Matriz de correlação entre as estações do cluster
    correlation_matrix = df_pivot.corr()
    
    print("\nMatriz de Correlação *(Pearson):")
    print(correlation_matrix)
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 8 - ANÁLISE TEMPORAL MENSAL
    
    print("\n" + "="*50)
    print("ANÁLISE TEMPORAL - MÉDIA MENSAL")
    print("="*50)
    
    #Criar coluna de mês
    df["mes"] = df["data"].dt.month
    
    #Separar grupos novamente
    df_paulista, df_linha2_sem_paulista, df_outras_linhas = create_analysis_groups(df)
    
    #Média mensal por grupo
    media_mensal_paulista = df_paulista.groupby("mes")["fluxo"].mean()
    media_mensal_linha2 = df_linha2_sem_paulista.groupby("mes")["fluxo"].mean()
    media_mensal_outras = df_outras_linhas.groupby("mes")["fluxo"].mean()
    
    print("\nCluster Paulista - Média Mensal:")
    print(media_mensal_paulista)
    
    print("\nLinha 2 (sem Paulista) - Média Mensal:")
    print(media_mensal_linha2)
    
    print("\nOutras Linhas - Média Mensal:")
    print(media_mensal_outras)
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 9 - VARIAÇÃO PERCENTUAL MENSAL
    
    print("\n" + "="*50)
    print("ANÁLISE TEMPORAL - VARIAÇÃO PERCENTUAL MENSAL")
    print("="*50)
    
    #Calcular variação percentual mensal
    var_pct_paulista = media_mensal_paulista.pct_change() * 100
    var_pct_linha2 = media_mensal_linha2.pct_change() * 100
    var_pct_outras = media_mensal_outras.pct_change() * 100
    
    print("\nCluster Paulista - Variação %:")
    print(var_pct_paulista.round(2))
    
    print("\nLinha 2 (sem Paulista) - Variação %:")
    print(var_pct_linha2.round(2))
    
    print("\nOutras Linhas - Variação %:")
    print(var_pct_outras.round(2))
    #==============================================================================
    
    
    #==============================================================================
    # BLOCO 10 - VISUALIZAÇÕES
    
    plot_group_means(df_paulista,
                    df_linha2_sem_paulista,
                    df_outras_linhas)
    
    plot_monthly_trends(media_mensal_paulista,
                        media_mensal_linha2,
                        media_mensal_outras)
    
    plot_cluster_correlation(correlation_matrix)
    
    plot_group_boxplot(df_paulista,
                    df_linha2_sem_paulista,
                    df_outras_linhas)
    #=============================================================================
    
    
    #=============================================================================
    #BLOCO 11 - ANÁLISE INTERANUAL
    print("\n" + "="*50)
    print("ANÁLISE INTERANUAL")
    print("="*50)
    
    df_hist = pd.read_csv(
        "projeto-metro-sp/data/processed/metro_2023_2024_2025_clean.csv",
        parse_dates=["data"]
    )
    
    df_hist = create_paulista_dummy(df_hist)
    
    # Garantir coluna ano
    df_hist["ano"] = df_hist["data"].dt.year
    
    # Média geral por ano
    media_ano = (
        df_hist
        .groupby("ano")["fluxo"]
        .mean()
    )
    
    print("\nMédia Geral por Ano:")
    print(media_ano.round(0))
    
    # Média anual por cluster vs não cluster
    media_cluster_ano = (
        df_hist
        .groupby(["ano", "cluster_paulista"])["fluxo"]
        .mean()
        .unstack()
    )
    
    print("\nMédia ANual - Cluster vs Não Cluster")
    print(media_cluster_ano.round(0))
    
    #Gráfico Interanual
    plot_interannual_comparison(media_cluster_ano)
    
    #Participação percentual do cluster
    participacao = (
    df_hist
        .groupby("ano")
        .apply(
            lambda x: (
                x.loc[x["cluster_paulista"] == 1, "fluxo"].sum()
                /
                x["fluxo"].sum()
            )
        )
    )
    
    print("\nParticipação do Cluster no Total do Sistema (%):")
    print((participacao * 100).round(2))
    #===========================================================================
if __name__ == "__main__":
    main()