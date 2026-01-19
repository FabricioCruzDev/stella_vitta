import pandas as pd

import os
import io

import segno
import cairosvg
from PIL import Image



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
        valor_formatado = f"{valor_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
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
        
        <text x="{w/2}" y="3" font-family="Georgia, Geneva, sans-serif" font-size="2" 
              text-anchor="middle" fill="#888" letter-spacing="0.2">{sku_str}</text>
        
        <g transform="translate({(w-9)/2}, 4.5) scale(0.35)">
            {qrcode_svg}
        </g>
    </svg>"""
    
    return frente, verso


def salvar_etiquetas(df, pasta_destino="etiquetas"):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for i, row in df.iterrows():
        # 1. Obter os conteúdos SVG (usando sua função gerar_etiquetas_frente_verso)
        frente_svg, verso_svg = gerar_etiquetas_frente_verso(row)
        sku_nome = str(row['SKU']).replace("/", "-").replace(" ", "_")

        # 2. Processar Frente e Verso
        for tipo, conteudo_svg in [("FRENTE", frente_svg), ("VERSO", verso_svg)]:
            
            # --- PASSO A: SVG para PNG em memória ---
            # Aumentamos a escala (output_width) para garantir alta qualidade na impressão
            png_data = cairosvg.svg2png(bytestring=conteudo_svg.encode('utf-8'), output_width=1000)
            
            # --- PASSO B: PNG para JPG com Pillow ---
            img_png = Image.open(io.BytesIO(png_data))
            
            # Garantir fundo branco (caso haja transparência no SVG)
            if img_png.mode in ("RGBA", "P"):
                fundo_branco = Image.new("RGB", img_png.size, (255, 255, 255))
                fundo_branco.paste(img_png, mask=img_png.split()[3]) # Usa o alpha como máscara
                img_final = fundo_branco
            else:
                img_final = img_png.convert("RGB")

            # --- PASSO C: Salvar no Disco ---
            nome_arquivo = f"{sku_nome}_{tipo}.jpg"
            caminho_final = os.path.join(pasta_destino, nome_arquivo)
            
            # Salvamos com qualidade máxima
            img_final.save(caminho_final, "JPEG", quality=100, subsampling=0)

    print(f"Sucesso! Etiquetas JPG geradas em: {pasta_destino}")

# Buscando e preparando os dados
df = pd.read_excel('./datawarehouse/raw/produtos-precificacao.xlsx', skiprows=1)
print(df.info())
df = df[['SKU', 'DESCRICAO', 'VALOR FINAL']].copy()
df['VALOR FINAL'] = round(df['VALOR FINAL'], 2)
df['DESC'] = df['DESCRICAO'].apply(normalize_descricao)
df['VALOR_STR'] = df['VALOR FINAL'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(df.head(10))
df_etiqueta = df[['DESC', 'VALOR FINAL', 'SKU']]

salvar_etiquetas(df)
df_etiqueta.to_excel('etiquetas/etiquetas.xlsx', index=False)


if __name__ == "__main__":
   ...