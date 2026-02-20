import pandas as pd

def normalize_descricao(text):
    if not isinstance(text, str):
        return text
    
    # 1. Limpeza básica
    text = text.strip().upper()
    words = text.split()
    
    # 2. Filtro de conectivos
    stopwords = ["DE", "DAS", "DOS", "DA", "DO", "COM", "PARA"]
    filtered_words = [w for w in words if w not in stopwords]
    
    # 3. Regra de abreviação: 2 letras para a 1ª, 3 letras para as outras
    parts = []
    for i, w in enumerate(filtered_words[:4]):
        if i == 0:
            parts.append(w[:2]) # Apenas 2 letras da primeira
        else:
            parts.append(w[:3]) # 3 letras das demais
            
    # 4. Une as partes (ex: BR PO LU ZIR)
    return " ".join(parts)


# Buscando e preparando os dados
df = pd.read_excel('./datawarehouse/raw/2- PRODUTOS - PRECIFICAÇAO segunda compra 10.02.xlsx', skiprows=1, sheet_name='Sheet1')
print(df.info())
df = df[['SKU', 'DESCRICAO', 'VALOR FINAL AJUSTADO']].copy()
df['VALOR FINAL AJUSTADO'] = round(df['VALOR FINAL AJUSTADO'], 2)
df['DESC'] = df['DESCRICAO'].apply(normalize_descricao)
df['VALOR_STR'] = df['VALOR FINAL AJUSTADO'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
df['VALOR FINAL'] = df['VALOR_STR']
print(df)

df_ag = (df.loc[df['SKU'].str.endswith('AG', na=False)])
print(df_ag)
df_au = (df.loc[df['SKU'].str.endswith('AU', na=False)])
print(df_au)

df.to_excel('./datawarehouse/etiquetas/etiquetas_2.xlsx', index=False)
df_ag.to_excel('./datawarehouse/etiquetas/etiquetas_ag_2.xlsx', index=False)
df_au.to_excel('./datawarehouse/etiquetas/etiquetas_au_2.xlsx', index=False)