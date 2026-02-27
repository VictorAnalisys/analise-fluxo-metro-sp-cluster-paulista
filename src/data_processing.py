import pandas as pd
import re

# MAPEAMENTO DE ESTAÇÕES

LINE_1_MAPPING = {
    "JAB": "Jabaquara",
    "CON": "Conceição",
    "JUD": "São Judas",
    "SAU": "Saúde",
    "ARV": "Praça da Árvore",
    "SCZ": "Santa Cruz",
    "VMN": "Vila Mariana",
    "ANR": "Ana Rosa",
    "PSO": "Paraíso",
    "VGO": "Vergueiro",
    "JQM": "Japão-Liberdade",
    "LIB": "Liberdade",
    "PSE": "Sé",
    "BTO": "São Bento",
    "LUZ": "Luz",
    "TRD": "Tiradentes",
    "PPQ": "Armênia",
    "TTE": "Tietê",
    "CDU": "Carandiru",
    "SAN": "Santana",
    "JPA": "Jardim São Paulo",
    "PIG": "Parada Inglesa",
    "TUC": "Tucuruvi"
}

LINE_2_MAPPING = {
    "VPT": "Vila Prudente",
    "TTI": "Tamanduateí",
    "SAC": "Sacomã",
    "AIP": "Alto do Ipiranga",
    "IMG": "Imigrantes",
    "CKB": "CHácara Klabin",
    "ANR": "Ana Rosa",
    "PSO": "Paraíso",
    "BGD": "Brigadeiro",
    "TRI": "Trianon-MASP",
    "CNS": "Consolação",
    "CLI": "Clínicas",
    "SUM": "Sumaré",
    "VMD": "Vila Madalena"
}

LINE_3_MAPPING = {
    "ITQ": "Itaquera",
    "ART": "Artur Alvim",
    "PCA": "Patriarca",
    "VPA": "Vila Matilde",
    "VTD": "Vila Esperança",
    "PEN": "Penha",
    "CAR": "Carrão",
    "TAT": "Tatuapé",
    "BEL": "Belém",
    "BRE": "Bresser-Mooca",
    "BAS": "Brás",
    "PDS": "Pedro II",
    "PSE": "Sé",
    "GBU": "Guaianases",
    "REP": "República",
    "CEC": "Corintians-Itaquera",
    "DEO": "Dom Bosco",
    "BFU": "Barra Funda"
}

LINE_4_MAPPING = {
    "LUZ": "Luz",
    "REP": "República",
    "HIG": "Higienópolis-Mackenzie",
    "PAU": "Paulista",
    "PIN": "Pinheiros",
    "BUT": "Butantã",
    "MOR": "São Paulo-Morumbi"
}

LINE_15_MAPPING = {
    "VPM": "Vila Prudente",
    "ORT": "Oratório",
    "SLU": "São Lucas",
    "CAD": "Camilo Haddad",
    "VTL": "Vila Tolstói",
    "VUN": "Vila União",
    "JPL": "Jardim Planalto",
    "SAP": "Sapopemba",
    "FJT": "Fazenda da Juta",
    "MAT": "São Mateus",
    "IGT": "Jardim Colonial"
}

STATION_MAPPING = {
    "1-AZUL": LINE_1_MAPPING,
    "2-VERDE": LINE_2_MAPPING,
    "3-VERMELHA": LINE_3_MAPPING,
    "4-AMARELA": LINE_4_MAPPING,
    "15-PRATA": LINE_15_MAPPING
}

#DEFINIÇÃO DAS ESTAÇÕES DENTRO DO CLUSTER PAULISTA
PAULISTA_STATIONS = [
    "Trianon-MASP",
    "Brigadeiro",
    "Consolação",
    "Paulista"
]

#FUNÇÕES DE PROCESSAMENTO DE DADOS
def create_paulista_dummy(df: pd.DataFrame) -> pd.DataFrame:
    df["cluster_paulista"] = df["estacao"].isin(PAULISTA_STATIONS).astype(int) #PUXAR A COLUNA DE ESTAÇÃO E CRIAR A DUMMY
    return df

#FUNÇÃO DE DIVISÃO DO DATAFRAME EM 3 CLUSTERS
def create_analysis_groups(df: pd.DataFrame): 
    df_paulista = df[df["cluster_paulista"] == 1]
    
    df_linha2_sem_paulista = df[
        (df["linha"] == "2-VERDE") &
        (df["cluster_paulista"] == 0) 
        ]
    
    df_outras_linhas = df[df["linha"] != "2-VERDE"]
    return df_paulista, df_linha2_sem_paulista, df_outras_linhas

#FUNÇÃO DE PARSE DO ARQUIVO BRUTO
def parse_raw_file(file_path, year: str) -> pd.DataFrame:
    print("ano recebido na função:", year)
    
    lista_dfs = []
    
    #Ler arquivo bruto como texto primeiro
    with open(file_path, "r", encoding="latin1") as f:
        lines = f.readlines()
        
    #Encontrar lin que começa com dia
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("DIA;"):
            header_index = i
            break
    
    if header_index is None:
        raise ValueError("Cabeçalho 'DIA' não encontrado no arquivo.")
    
    #Agora ler o csv a partir da linha correta
    df_raw = pd.read_csv(
        file_path,
        sep=";",
        header=header_index,
        encoding="latin-1"
        
    )
    
    print("Colunas detectadas:")
    print(df_raw.columns)
    
    #REMOVER COLUNAS VAZIAS
    df_raw = df_raw.loc[:, ~df_raw.columns.str.contains("^Unnamed")]
    
    #TRABALHAR COM A PRIMEIRA COLUNA DIA PARA DETECTAR O MÊS
    df_raw["DIA"] = pd.to_numeric(df_raw["DIA"], errors="coerce")
    
    #REMOVER LINHAS ONDE DIA É NaN
    df_raw = df_raw.dropna(subset=["DIA"])
    
    #DETECTAR REÍNICIO DE CICLO MENSAL
    df_raw["novo_mes"] = df_raw["DIA"] < df_raw["DIA"].shift(1)
    
    #CRIAR CONTADOR DE MÊS
    df_raw["mes"] = df_raw["novo_mes"].cumsum() + 1
    
    print(df_raw[["DIA", "mes"]].head(50))#degub temp
    
    line1 = extract_line_block(df_raw, "DIA", "TOTAL", "1-AZUL")
    line2 = extract_line_block(df_raw, "DIA.1", "TOTAL.1", "2-VERDE")
    line3 = extract_line_block(df_raw, "DIA.2", "TOTAL.2", "3-VERMELHA")
    line15 = extract_line_block(df_raw, "DIA.3", "TOTAL.3", "15-PRATA")
    
    #CONCATENAR LINHAS
    df_final = pd.concat([line1, line2, line3, line15], ignore_index=True)
    
    #PADRONIZAR SIGLAS
    df_final["sigla"] = (
        df_final["sigla"]
        .str.strip()
        .str.replace(r"\.\d+$", "", regex=True)
    )
    
    print(df_final["dia"].unique()[:20])
    print(df_final["dia"].dtype)
    print("Valores únicos de fluxo_raw (amostra):")
    print(df_final["fluxo_raw"].unique()[:20])
    print("Tipo fluxo_raw:", df_final["fluxo_raw"].dtype)
    
    #FILTROS
    
    #REMOVER CABEÇALHOS REPETIDOS
    df_final = df_final[df_final["dia"] != "DIA"]
    
    print(df_final[df_final["fluxo_raw"].str.contains("[A-Za-z]", na=False)].head())
    
    #CONVERTER FLUXO
    df_final["fluxo"] = (
        df_final["fluxo_raw"]
        .str.replace(",", ".", regex=False)
        .replace("-", None)
    )
    df_final["fluxo"] = (
        pd.to_numeric(df_final["fluxo"], errors="coerce")
        .mul(1000)
        .round(0)
        .astype("Int64")
        )
    
    #REMOVER LINHAS ONDE O FLUXO VIROU NaN
    df_final = df_final.dropna(subset=["fluxo"])
    
    #REMOVER COLUNA DE FLUXO BRUTO
    df_final = df_final.drop(columns=["fluxo_raw"])
    
    #EXTRAIR APENAS NÚMEROS DO INÍCIO DA STRING
    df_final["dia"] = (
        df_final["dia"]
        .astype(str)
        .str.extract(r"^(\d+)", expand=False)
    )
    
    df_final["dia"] = pd.to_numeric(df_final["dia"], errors="coerce")
    df_final = df_final.dropna(subset=["dia"])
    
    
    #REMOVER DIAS INVÁLIDOS
    df_final = df_final[df_final["dia"].between(1, 31)]
    df_final["dia"] = df_final["dia"].astype(int)
    
    print("ano recebido", year)
    print("Valores únicos de mes:", df_final["mes"].unique()[:5])
    
    #CRIAR COLUNA DE DATA COMPLETA
    df_final["data"] = pd.to_datetime(
        dict(
            year=year,
            month=df_final["mes"],
            day=df_final["dia"]
        ),
        errors="coerce"
    )
    
    #APLICAR MAPEAMENTO
    df_final["estacao"] = df_final.apply(map_station_name, axis=1)
    
    #REORDENAR COLUNAS
    df_final = df_final[["data", "linha", "sigla", "estacao",  "fluxo"]]
    
    #SALVA O DATASET LIMPO
    df_final.to_csv("projeto-metro-sp/data/processed/metro_2025_clean.csv", index=False)
    
    return df_final


def extract_line_block(df_raw, dia_col, total_col, line_name):

    #SELECIONAR AS COLUNAS DO BLOCO
    start_idx = df_raw.columns.get_loc(dia_col)
    end_idx = df_raw.columns.get_loc(total_col)
    
    block = df_raw.iloc[:, start_idx:end_idx + 1]
    
    #RENOMEAR A COLUNA DIA PARA PADRÃO
    block = block.rename(columns={dia_col: "dia"})
    
    #REMOVER COLUNA TOTAL
    block = block.drop(columns=[total_col])
    
    #GARANTE QUE O MêS ESTEJA DENTRO DO BLOCO
    block["mes"] = df_raw["mes"]
    
    #TRANSFORMAR O FORMATO DE DADOS DE LARGO PARA LONGO
    block_long = block.melt(
        id_vars=["dia", "mes"],
        var_name="sigla",
        value_name="fluxo_raw"
    )
    
    #ADICIONAR NOME DA LINHA
    block_long["linha"] = line_name
    
    return block_long

def map_station_name(row):
    line = row["linha"]
    sigla = row["sigla"]
    
    if line in STATION_MAPPING:
        return STATION_MAPPING[line].get(sigla, "DESCONHECIDA")
    return "DESCONHECIDA"


