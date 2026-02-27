import pandas as pd

#def calculate_descriptive_stats(df: pd.DataFrame) -> dict:
   # return {
   #    "std": df["flow"].std(),
   #     "var": df["flow"].var(),
   #     "median": df["flow"].median()
   # }
   
def calculate_descriptive_stats(df):
   stats = df["fluxo"].describe()
   return stats

def summarize_group(df, group_name):
   print(f"\n{group_name}")
   print("-" * len(group_name))
   print(f"Observações: {len(df):,}")
   print(f"Média diária: {df['fluxo'].mean():,.0f} passageiros")
   print(f"Desvio padrão: {df['fluxo'].std():,.0f}")