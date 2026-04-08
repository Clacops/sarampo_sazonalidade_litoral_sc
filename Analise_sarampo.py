import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('Agg')

# --- 1. CARREGAMENTO E LIMPEZA (O que já funcionou) ---
def carregar_sarampo():
    df = pd.read_csv(
        'sinannet_cnv_exantsc_sarampo.csv',
        sep=';', encoding='ISO-8859-1', skiprows=3, skipfooter=12, engine='python',
        na_values=['-', '...', ' ', '0']
    )
    # Limpando nomes e valores
    df.columns = ['Municipio', 'Ign', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total_Casos']
    df['Municipio'] = df['Municipio'].str.replace(r'^\d+\s', '', regex=True).str.strip()
    df['Total_Casos'] = pd.to_numeric(df['Total_Casos'].astype(str).str.replace('.', '', regex=False), errors='coerce').fillna(0).astype(int)
    return df[['Municipio', 'Total_Casos']]

# --- 2. DADOS POPULACIONAIS DA AMFRI (Censo 2022) ---
dados_amfri = {
    'Municipio': [
        'ITAJAI', 'BALNEARIO CAMBORIU', 'NAVEGANTES', 'CAMBORIU', 
        'ITAPEMA', 'PENHA', 'BALNEARIO PICARRAS', 'BOMBINHAS', 
        'PORTO BELO', 'ILHOTA', 'LUIZ ALVES'
    ],
    'Populacao': [
        264054, 139155, 86401, 103074, 
        75940, 33663, 27103, 25058, 
        27688, 17046, 11684
    ]
}
df_pop_amfri = pd.DataFrame(dados_amfri)

# --- 3. PROCESSAMENTO DOS DADOS ---
try:
    print("⏳ Processando análise proporcional da AMFRI...")
    df_sarampo = carregar_sarampo()
    
    # Cruzando os casos com a nossa tabela de população da AMFRI
    # O 'inner' merge garante que só fiquem as cidades da sua região
    df_final = pd.merge(df_sarampo, df_pop_amfri, on='Municipio', how='inner')
    
    # CÁLCULO DA TAXA DE INCIDÊNCIA (O indicador gerencial)
    # Fórmula: (Casos / População) * 100.000
    df_final['Taxa_Incidencia'] = (df_final['Total_Casos'] / df_final['Populacao']) * 100000
    
    # Ordenar pelo maior risco (Taxa)
    df_final = df_final.sort_values(by='Taxa_Incidencia', ascending=False)

    print("\n✅ ANÁLISE DE RISCO EPIDEMIOLÓGICO (AMFRI):")
    print(df_final[['Municipio', 'Total_Casos', 'Taxa_Incidencia']].to_string(index=False))

    # --- 4. GRÁFICO DE TAXA DE INCIDÊNCIA ---
    plt.figure(figsize=(12, 7))
    sns.barplot(x='Taxa_Incidencia', y='Municipio', data=df_final, palette='YlOrRd_r')
    
    plt.title('Risco de Sarampo na AMFRI: Casos por 100 mil Habitantes', fontsize=14)
    plt.xlabel('Taxa de Incidência (Proporcional à População)', fontsize=12)
    plt.ylabel('Município', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('risco_sarampo_amfri.png')
    
    print("\n📊 Sucesso! O gráfico 'risco_sarampo_amfri.png' foi gerado.")

except Exception as e:
    print(f"❌ Erro na análise: {e}")
