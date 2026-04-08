import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('Agg')

# 1. Função de carregamento com a limpeza que validamos
def carregar_dados_amfri():
    df = pd.read_csv(
        'sinannet_cnv_exantsc_sarampo.csv',
        sep=';', encoding='ISO-8859-1', skiprows=3, skipfooter=12, engine='python'
    )
    
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    df.columns = ['Municipio', 'Ign'] + meses + ['Total']
    
    # Limpeza de números e nomes
    for col in meses + ['Total']:
        df[col] = df[col].astype(str).str.replace('"', '').str.replace('.', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    df['Municipio'] = df['Municipio'].str.replace('"', '').str.replace(r'^\d+\s', '', regex=True).str.strip()
    
    # Filtro da sua Região (AMFRI)
    cidades_amfri = ['BOMBINHAS', 'ITAJAI', 'BALNEARIO CAMBORIU', 'NAVEGANTES', 'CAMBORIU', 'ITAPEMA', 'PORTO BELO', 'PENHA', 'BALNEARIO PICARRAS']
    return df[df['Municipio'].isin(cidades_amfri)], meses

try:
    df_amfri, lista_meses = carregar_dados_amfri()
    
    # Criando a Tabela de Picos
    resumo_pico = []
    for _, linha in df_amfri.iterrows():
        dados_meses = linha[lista_meses]
        valor_max = dados_meses.max()
        mes_pico = dados_meses[dados_meses == valor_max].index.tolist()
        
        resumo_pico.append({
            'Município': linha['Municipio'],
            'Mês de Pico': ", ".join(mes_pico),
            'Casos no Pico': valor_max,
            'Total do Período': linha['Total']
        })
    
    df_resumo = pd.DataFrame(resumo_pico).sort_values(by='Total do Período', ascending=False)
    
    print("\n--- RESUMO GERENCIAL: PICOS DE SARAMPO NA AMFRI ---")
    print(df_resumo.to_string(index=False))

    # 2. Gerando o Mapa de Calor (Visualização de Impacto)
    df_heatmap = df_amfri.set_index('Municipio')[lista_meses]
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(df_heatmap, annot=True, cmap='YlOrRd', fmt='d')
    
    plt.title('Mapa de Calor: Intensidade de Casos de Sarampo por Mês (AMFRI)', fontsize=15)
    plt.xlabel('Meses do Ano')
    plt.ylabel('Municípios da Região')
    
    plt.tight_layout()
    plt.savefig('heatmap_sarampo_amfri.png')
    print("\n📊 Sucesso! O gráfico 'heatmap_sarampo_amfri.png' foi gerado.")

except Exception as e:
    print(f"❌ Erro ao gerar resumo: {e}")