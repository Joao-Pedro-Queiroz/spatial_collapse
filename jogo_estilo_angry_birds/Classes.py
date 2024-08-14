import pygame
from random import randint, random
import numpy as np
class Canhao:
    def __init__(self,tamanho,posicao):
        self.imagem = pygame.image.load('assets/img/canhao.png')
        self.tamanho_imagem= tamanho
        self.posicao = posicao

    def desenha(self, window):
        canhao = pygame.transform.scale(self.imagem, self.tamanho_imagem) # Redefinir dimensão da imagem
        window.blit(canhao, self.posicao) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).


        

class Atrator:
    def __init__(self, posição, raio, gravidade, tamanho):
        self.imagem_atrator = pygame.image.load('assets/img/planeta2.png')
        self.tamanho_imagem = tamanho
        self.posicao = posição   
        self.raio = raio
        self.gravidade = gravidade
        

        
    def calcula_atracao(self, posicao_jogador):
        # Calcular vetor de distância
        d_vec = self.posicao - posicao_jogador
        d = np.linalg.norm(d_vec)

        # Calcular aceleração gravitacional
        if d > 0:
            a = (self.gravidade / d**2) * (d_vec / d)
        else:
            a = np.array([0, 0])

        return a
    

    def desenha(self, window):
        nave = pygame.transform.scale(self.imagem_atrator, self.tamanho_imagem) # Redefinir dimensão da imagem
        window.blit(nave, self.posicao) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

class Bolinha():
    def __init__(self,s0,v0,quantidade,torre,tamanho):
        self.imagem = pygame.image.load('assets/img/bola+canhao.png')
        self.posicoes = []
        self.velocidades = []
        self.s0 = s0
        self.v0=v0
        self.torre=torre
        self.tamanho=tamanho
        self.quantidade=quantidade
        for i in range(quantidade):
            self.posicoes.append(self.s0)
            self.velocidades.append(self.v0)
        for i in range(len(self.velocidades)):
            p = np.random.rand()
            self.velocidades[i]=self.elocidades[i]*(p+1) 
    
    def atualiza_estado(self,posicoes,velocidades,torre,aceleracao):
            for i in range(len(posicoes)):
                if posicoes[i][0]<10 or posicoes[i][0]>390 or posicoes[i][1]<10 or posicoes[i][1]>390: # Se eu chegar ao limite da tela, reinicio a posição do personagem
                    posicoes[i]= self.s0
                    velocidades[i] = torre-self.v0
                    velocidades[i]= velocidades[i]*0.05
                else:
                    velocidades[i]= velocidades[i] + aceleracao
                    posicoes[i] = posicoes[i] +  velocidades[i]
    
    def desenha(self,window):
        for i in range(self.quantidade):
            bolinha = pygame.transform.scale(self.imagem, self.tamanho) # Redefinir dimensão da imagem
            window.blit(bolinha, self.posicoes[i]) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).


class TelaInicial:
    def __init__(self, largura_jogo, altura_jogo, fonte_padrao):
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo
        self.font_texto = pygame.font.Font(fonte_padrao, 18)
        self.image_fundo = pygame.image.load('assets/img/starfield.png') # Carrega uma imagem
        self.tamanho_fundo = (largura_jogo, altura_jogo)
    

    def atualiza_estado(self):
        for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
            if event.type == pygame.QUIT: 
                return -1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return 1
        
        return 0
        

    def desenha(self, window):
        window.fill((0, 0, 0))

        fundo = pygame.transform.scale(self.image_fundo, self.tamanho_fundo) # Redefinir dimensão da imagem
        window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        texto_inicio = self.font_texto.render(f'CLIQUE "EBTER" PARA INICIAR O JOGO', True, (255, 255, 255)) # Cria uma imagem do texto
        window.blit(texto_inicio, (100, 300)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        pygame.display.update()


class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_jogo = 550
        self.altura_jogo = 600
        self.fonte_padrao = pygame.font.get_default_font() # Carrega a fonte padrão
        self.largura_nave = 60
        self.altura_nave = 50
        self.window = pygame.display.set_mode((self.largura_jogo, self.altura_jogo))
        pygame.display.set_caption('Space Atari') # Define o título da janela
        self.indice_tela_atual = 0
        self.telas = [TelaInicial(self.largura_jogo, self.altura_jogo, self.fonte_padrao)]

    def game_loop(self):
        tela_atual = self.telas[self.indice_tela_atual]

        rodando = True
        while rodando:
            self.indice_tela_atual = tela_atual.atualiza_estado()

            if self.indice_tela_atual == -1:
                rodando = False
            elif self.indice_tela_atual == 1:
                tela_atual = self.telas[self.indice_tela_atual]
                tela_atual.desenha(self.window)
            else:
                tela_atual = self.telas[self.indice_tela_atual]
                tela_atual.desenha(self.window)
                pygame.mixer.music.pause()