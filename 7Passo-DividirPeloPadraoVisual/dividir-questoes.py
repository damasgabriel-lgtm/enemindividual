"""
Propósito: Dividir as questões por padrão.
Autor: Alexandre Nassar de Peder
Atualização: 03/06/2026
"""

from PIL import Image
import os

def encontrar_faixa_padrao(imagem, cor_alvo=(35, 31, 32), tolerancia=15, altura_faixa=15):
    """
    Encontra posições onde há um padrão visual vertical da cor especificada
    analisando o último pixel da direita.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Percorre a imagem de cima para baixo
    y = 0
    while y <= altura - altura_faixa:
        # Verifica se há uma sequência vertical de 'altura_faixa' pixels da cor alvo
        faixa_encontrada = True
        
        for dy in range(altura_faixa):
            # Analisa o último pixel da direita (largura - 1)
            pixel = pixels[largura - 1, y + dy]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se a cor está dentro da tolerância
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Corta 17 pixels antes do padrão começar para mantê-los no início do corte
            posicao_corte = y - 17
            if posicao_corte < 0:  # Evita posições negativas
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão encontrado iniciando em y={y}, cortando em y={posicao_corte}")
            # Pula a faixa para evitar detecções múltiplas do mesmo padrão
            y += altura_faixa
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo=(35, 31, 32)):
    """
    Divide a imagem verticalmente cortando nas posições identificadas
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_padrao(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} posições de corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Corta a seção final (após o último corte)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "./inteiras/pagina_enem_27.png"  # Substitua pelo caminho da sua imagem
    pasta_saida = "pg_27"           # Substitua pelo nome da pasta desejada

    # Cor RGB direta (35, 31, 32)
    cor_do_padrao = (35, 31, 32)
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    
    print("Divisão concluída!")
