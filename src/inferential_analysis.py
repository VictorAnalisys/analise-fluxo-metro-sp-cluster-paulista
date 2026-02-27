from os import stat

import numpy as np
import pandas as pd
from scipy import stats

#==============================================================================
# TESTE DE NORMALIDADE

def test_normality(series: pd.Series, group_name: str):
    """
    Aplica teste de Shapiro-Wilk para verificar normalidade da distribuição dos dados.
    """
    stat, p_value = stats.shapiro(series)
    
    print(f"\nTeste de Normalidade - {group_name}")
    print("-" * 40)
    print(f"Estatística:: {stat:.4f}")
    print(f"p-valor: {p_value:.6f}")
    
    if p_value > 0.05:
        print("Resultado: A distribuição é aproximadamente normal (falha em rejeitar H0)")
    else:
        print("Resultado: A distribuição NÃO é normal (rejeita H0)")
        
    return stat, p_value
#==============================================================================


#==============================================================================
# TESTE T 

def welch_t_test(group1: pd.Series, group2: pd.Series,
                name1: str, name2: str):
    """
    Teste t de Welch para comparação de médias
    (não assume variâncias iguais).
    """
    stat, p_value = stats.ttest_ind(
        group1,
        group2,
        equal_var=False
    )
    
    print(f"\nTeste t (Welch) - {name1} vs {name2}")
    print("-" * 40)
    print(f"Estatística t: {stat:.4f}")
    print(f"P-valor: {p_value:.6f}")
    
    if p_value < 0.05:
        print("Diferença estatisticamente SIGNIFICATIVA")
    else:
        print("Diferença NÃO é estatisticamente significativa")
        
    return stat, p_value
#==============================================================================


#==============================================================================
# TESTE DE MANN-WHITNEY

def mann_whitney_test(group1: pd.Series, 
                    group2: pd.Series,
                    name1: str,
                    name2: str):
    """
    Teste não-paramétrico de Mann-Whitney
    para comapração de duas distribuições independentes.
    """
    stat, p_value = stats.mannwhitneyu(group1, 
                                    group2, 
                                    alternative="two-sided"
    )
    
    print(f"\nTeste de Mann-Whitney - {name1} vs {name2}")
    print("-" * 40)
    print(f"Estatística U: {stat:.4f}")
    print(f"P-valor: {p_value:.6f}")
    
    if p_value < 0.05:
        print("Diferença estatisticamente SIGNIFICATIVA")
    else:
        print("Diferença NÃO é estatisticamente significativa")
        
    return stat, p_value
#==============================================================================


#==============================================================================
#TESTE DE COHEN'S D

def cohens_d(group1: pd.Series, 
            group2: pd.Series,
            name1: str,
            name2: str):
    """
    Cálculo do tamanho de efeito Cohen's d para comparação de duas médias.
    """
    mean1 = group1.mean()
    mean2 = group2.mean()
    
    std1 = group1.std()
    std2 = group2.std()
    
    n1 = len(group1)
    n2 = len(group2)
    
    #Desvio padrão agrupado
    pooled_std = np.sqrt(
        ((n1 - 1) * std1**2 + (n2 - 1) * std2**2) /
        (n1 + n2 - 2)
    )
    
    d= (mean1 - mean2) / pooled_std
    
    print(f"\nCohen's d - {name1} vs {name2}")
    print("-" * 40)
    print(f"Tamanho de efeito (d): {d:.4f}")
    
    #Interpretação
    abs_d = abs(d)
    
    if abs_d < 0.2:
        interpretation = "Efeito pequeno"
    elif abs_d < 0.5:
        interpretation = "Efeito médio"
    elif abs_d < 0.8:
        interpretation = "Efeito grande"
    else:
        interpretation = "Efeito muito grande"
        
    print(f"Interpretação: {interpretation}")
    
    return d
#==============================================================================


#==============================================================================
# TESTE ANOVA

def anova_teste(*groups):
    """
    ANOVA de um fator para comparar múltiplos grupos.
    """
    stat, p_value = stats.f_oneway(*groups)
    
    print("\nANOVA - Comparação entre múltiplos grupos")
    print("-" * 40)
    print(f"Estatística F: {stat:.4f}")
    print(f"P-valor: {p_value:.6f}")
    
    if p_value < 0.05:
        print("Há diferença significativa entre pelo menos um grupo")
    else:
        print("Não há diferença significativa entre os grupos")
        
    return stat, p_value
#==============================================================================


#==============================================================================
#TESTE ANOVA ETA^2

def anova_eta_squared(*groups):
    """
    Cálculo do tamanho de efeito Eta^2 para ANOVA de um fator.
    Mede proporção da variância explicada pelo fator.
    """
    #junta o sgrupos corretamente
    all_data = np.concatenate(groups)
    
    grand_mean = np.mean(all_data)
    
    #Soma dos quadrados entre grupos (SS_between)
    ss_between = sum(
        len(group) * (np.mean(group) - grand_mean)**2
        for group in groups
        )
    
    #Soma dos quadrados total (SS_total)
    ss_total = np.sum((all_data - grand_mean)**2 )
    
    eta_sq = ss_between / ss_total
    
    print("\nTamanho de Efeito Eta^2 - ANOVA")
    print("-" * 40)
    print(f"Eta^2: {eta_sq:.4f}")
    
    if eta_sq < 0.01:
        interpretation = "Efeito pequeno"
    elif eta_sq < 0.06:
        interpretation = "Efeito médio"
    elif eta_sq < 0.14:
        interpretation = "Efeito grande"
    else:
        interpretation = "Efeito muito grande"
        
    print(f"Interpretação: {interpretation}")
    
    return eta_sq
#==============================================================================


#==============================================================================
# TESTE DE CORRELAÇÃO DE PEARSON

def correlation_test(series1: pd.Series, series2: pd.Series,
    name1: str, name2: str):
    """
    Correlação de Pearson entre duas séries
    """
    
    stat, p_value = stats.pearsonr(series1, series2)
    
    print(f"\nCorrelação de Pearson - {name1} vs {name2}")
    print("-" * 40)
    print(f"Correlação: {stat:.4f}")
    print(f"P-valor: {p_value:.6f}")
    
    return stat, p_value
#==============================================================================

