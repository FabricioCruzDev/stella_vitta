import pandas as pd
import os
import segno

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


def gerar_etiquetas_frente_verso(row):
    # Dimensões e Padding
    w, h = 25, 15
    pad = w * 0.02
    
    # --- TRATAMENTO DE ERRO NA DESCRIÇÃO ---
    # Se for nulo (NaN), vira string vazia. Se não, garante que é string.
    descricao = str(row['DESC']) if pd.notnull(row['DESC']) else ""
    desc_clean = descricao[:18]
    
    # Tratamento do Valor
    try:
        valor_num = float(row['VALOR FINAL'])
        valor_formatado = f"R$ {valor_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        valor_formatado = "0,00"

    # FRENTE
    frente = f"""<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="white"/>
        
        <text x="{w/2}" y="5.5" font-family="Georgia, Geneva, sans-serif" font-size="2.5" 
              font-weight="bold" letter-spacing="0.1" text-anchor="middle" fill="#555">{desc_clean}</text>
        
        <line x1="{w*0.2}" y1="7.5" x2="{w*0.8}" y2="7.5" stroke="#DDD" stroke-width="0.1"/>
        
        <text x="{w/2}" y="12" font-family="Georgia, serif" font-size="3.5" 
              font-weight="bold" text-anchor="middle" fill="black">R$ {valor_formatado}</text>
    </svg>"""

    # VERSO (QR Code)
    sku_str = str(row['SKU']).upper() if pd.notnull(row['SKU']) else "SKU"
    qr = segno.make_qr(sku_str)
    qrcode_svg = qr.svg_inline(light="white", dark="black", scale=1)

    verso = f"""<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="white"/>
        
        <text x="{w/2}" y="3" font-family="Verdana, sans-serif" font-size="2" 
              text-anchor="middle" fill="#888" letter-spacing="0.2">{sku_str}</text>
        
        <g transform="translate({(w-9)/2}, 4.5) scale(0.35)">
            {qrcode_svg}
        </g>
    </svg>"""
    
    return frente, verso


def salvar_etiquetas(df, pasta_destino="etiquetas_output"):
    # Cria a pasta se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for i, row in df.iterrows():
        # Nome base usando o SKU para evitar duplicatas
        sku_limpo = str(row['SKU']).replace("/", "-")
        
        # Gerar conteúdo (usando a lógica de 25x15mm anterior)
        frente, verso = gerar_etiquetas_frente_verso(row)
        
        # Salvar Arquivo Frente
        nome_frente = f"{sku_limpo}_01_FRENTE.svg"
        with open(os.path.join(pasta_destino, nome_frente), "w", encoding="utf-8") as f:
            f.write(frente)
            
        # Salvar Arquivo Verso
        nome_verso = f"{sku_limpo}_02_VERSO.svg"
        with open(os.path.join(pasta_destino, nome_verso), "w", encoding="utf-8") as f:
            f.write(verso)

    print(f"Processo concluído! Arquivos salvos em: {pasta_destino}")

# Buscando e preparando os dados
df = pd.read_excel('./datawarehouse/raw/produtos-precificacao.xlsx', skiprows=1)
print(df.info())
df = df[['SKU', 'DESCRICAO', 'VALOR FINAL']].copy()
df['VALOR FINAL'] = round(df['VALOR FINAL'], 2)
df['DESC'] = df['DESCRICAO'].apply(normalize_descricao)
df['VALOR_STR'] = df['VALOR FINAL'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(df.head(10))

salvar_etiquetas(df)



if __name__ == "__main__":
   ...