Este parser assume que o formato do relatório anual do Metrô de São Paulo mantém a estrutura de blocos por linha conforme padrão 2023–2025.



### Análise de Fluxo de Passageiros - Metrô de São Paulo (2023-2025)



##### Objetivo do Projeto

Este projeto tem como objetivo analisar o fluxo diário de passageiros do Metrô de São Paulo entre 2023 e 2025, com foco especial no chamado Cluster Paulista (estações Brigadeiro, Consolação e Trianon-MASP).



A análise busca responder:

* O CLuster Paulista apresenta comportamento estruturalmente diferente do restante do sistema?
* Existe diferença estatisticamente significativa?
* Como o cluster evolui ao longo do tempo?
* Qual sua participação no sistema total?



##### Pipeline de Processamento

1. Parsing das bases brutas (obtidas no site oficial do metrô de sp)
   As bases originais possuem:

* Estrtura mensal
* Colunas duplicadas de DIA
* Valores em formato de texto com vírgula decimal
* valores em milhares



O processamento realiza:

* Identificação dinâmica da linha de cabeçalho
* Padronização das colunas
* Transformação para formato longo
* Criação da coluna data
* conversão do fluxo para valor absoluto



##### Construção dos Grupos de Análise

Foi criada a variável dummy: *cluster\_paulista*



Definindo

* 1 - Brigadeiro, Consolação e Trianon-MASP
* 0 - Demais estações



Grupos finais:

* Cluster Paulista
* Linha 2(sem paulista)
* Outras Linhas



##### Análise Descritiva



Médias Diárias

|Grupo|Média|Desvio Padrão|
|-|-|-|
|Cluster Paulista|~52.592|~28.104|
|Linha 2(sem paulista)|~24.115|~23.772|
|Outras Linhas|~27.781|~28.576|



Obs: o Cluster apresenta fluxo médio de aproximadamente 2x superior.



##### Testes Inferenciais



* Teste de Normalidade (Shapiro-Wilk)

&nbsp;	Distribuições não normais (p<0.001)



* Teste t de Welch

&nbsp;	Comparando Cluster Paulista vs Linha 2

&nbsp;	Diferença estatisticamente significativa (p<0.001)



* Mann-Whitney

&nbsp;	Confirma diferença robusta sem assumir normalidade



* Tamanho de Efeito (Cohen's d)

&nbsp;	d=~1.15

&nbsp;	efeito muito grande



* Anova de 4 linhas

&nbsp;	F significativo (p<0.001)



* Eta^2

&nbsp;	n^2 =~0.147

&nbsp;	efeito muito grande



##### Correlação entre estações do cluster



Correlação de Pearson

|Estação|Brigadeiro|Consolação|Trianon|
|-|-|-|-|
|Brigadeiro|1.00|0.98|0.98|
|Consolação|0.98|1.00|0.98|
|Trianon|0.98|0.98|1.00|

Movimento altamente sincronizado - comportamento estrutural conjunto



##### Análise temporal

Média Mensal

Padrão Observado

* Pico consistente em Fevereiro
* Crescimento até Setembro
* Queda no último trimestre

Comportamento semelhante entre cluster e sistema, porém em escala superior.



##### Variação Percentual Mensal

* Fevereiro - forte crescimento
* Junho a Julho - retração
* Setembro - novo pico
* Novembro a Dezembro - desaceleração



##### Análise Interanual (23-25)



Média Geral por ano

Ano  | Média

2023 | 27.318

2024 | 28.195

2025 | 28.299



crescimento moderado do sistema



##### Participação do Cluster

Ano  | Participação

2023 | 8.28%

2024 | 8.34%

2025 | 8.46%



o cluster mantém participação estável com leve crescimento



##### Dashboard Power BI

Estrutura criada



Página 1 - Overview

* Fluxo Médio Cluster
* Fluxo Médio não cluster
* Participação (%)
* Crescimento YoY
* Evolução Interanual



Página 2 - Comparação Estrutural

* Colunas agrupadas
* diferença de médias
* desvio padrão



Página 3 - Dinâmica Temporal

* Evolução Mensal
* Variação percentual
* Heatmap por ano e mês



##### Principais Conclusões

* O Cluster Paulista apresenta fluxo médio significativamente superior
* A diferença é estatística robusta
* O comportamento das estações do cluster é altamente correlacionado
* A participação do cluster é estruturalmente estável (~8-9%)
* O padrão temporal é semelhante ao sistema, porém com maior magnitude
