import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('Agg')

def carregar_mensal_corrigido():
    # Lemos o arquivo bruto
    df = pd.read_csv(
        'sinannet_cnv_exantsc_sarampo.csv',
        sep=';', encoding='ISO-8859-1', skiprows=3, skipfooter=12, engine='python'
    )
    
    # Definindo nomes de colunas fixos para evitar erro de índice
    colunas = ['Municipio', 'Ign', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
    df.columns = colunas
    
    # Limpeza rigorosa: Remove aspas, remove pontos de milhar e garante que é número
    for col in colunas[1:]:
        df[col] = df[col].astype(str).str.replace('"', '', regex=False)
        df[col] = df[col].str.replace('.', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Limpando o nome do município
    df['Municipio'] = df['Municipio'].str.replace('"', '', regex=False)
    df['Municipio'] = df['Municipio'].str.replace(r'^\d+\s', '', regex=True).str.strip()
    
    return df

try:
    print("⏳ Recalculando dados com precisão...")
    df_completo = carregar_mensal_corrigido()
    
    # Filtrando apenas Bombinhas para conferência real
    df_bombinhas = df_completo[df_completo['Municipio'] == 'BOMBINHAS']
    
    print("\n--- CONFERÊNCIA DE DADOS: BOMBINHAS ---")
    # Mostra os meses e o total para conferirmos com o seu CSV
    print(df_bombinhas[['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']].to_string(index=False))

    # Agora preparamos para o gráfico apenas se os dados estiverem certos
    cidades_amfri = ['BOMBINHAS', 'ITAJAI', 'BALNEARIO CAMBORIU', 'ITAPEMA']
    df_amfri = df_completo[df_completo['Municipio'].isin(cidades_amfri)]
    
    # Transformando para o formato de gráfico (Melt)
    df_grafico = pd.melt(df_amfri, id_vars=['Municipio'], 
                         value_vars=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], 
                         var_name='Mes', value_name='Casos')

    # Gerando o gráfico corrigido
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_grafico, x='Mes', y='Casos', hue='Municipio', marker='o')
    plt.title('Distribuição Mensal de Casos - AMFRI (Dados Conferidos)')
    plt.grid(True, alpha=0.3)
    plt.savefig('sazonalidade_corrigida.png')
    
    print("\n✅ Conferência finalizada. Verifique se os números acima batem com o seu CSV.")

except Exception as e:
    print(f"❌ Erro: {e}")