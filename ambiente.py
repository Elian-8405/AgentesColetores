import random

class Grid:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.grid = [[0] * self.tamanho for _ in range(self.tamanho)]
        self.agentes = []  
        self.recursos = []
    
    def posicaoLivre(self, x, y):
        return self.grid[x][y] == 0

    def adicionarAgente(self, x, y, tipo):
        if self.grid[x][y] != 0:  # Verifica se a posição está ocupada (onde 0 indica célula vazia)
            raise ValueError("Posição Ocupada")  # Lança erro se a posição não estiver vazia
        self.grid[x][y] = tipo# Marca a posição com 1 ou outro valor que indique que o agente está ali

    def atualizarPosicaoAgente(self, posicaoAntiga, novaPos, tipo):
        # Remove o agente da posição antiga
        x_old, y_old = posicaoAntiga
        self.grid[x_old][y_old] = 0

        # Adiciona o agente na nova posição
        x_new, y_new = novaPos
        self.grid[x_new][y_new] = tipo

    def gerarObstaculo(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if random.random() < 0.1:  # Aproximadamente 10% de chance para colocar um obstáculo
                    self.grid[i][j] = "O"  # O representa obstácul

    def gerarRecursos(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if random.random() < 0.2:  # Aproximadamente 20% de chance para colocar um recurso
                    self.grid[i][j] = random.choice([10, 20, 50])
    
    def mostrarGrid(self):
        for row in self.grid:
            for val in row:
                if val == 0:
                    print("[]", end=" ")
                if val == "O":
                    print("[O]", end=" ")
                if val == "AR":
                    print("[AR]", end=" ")
                if val == "AE":
                    print("[AR]", end=" ")
                if val == "AO":
                    print("[AO]", end=" ")
                if val == 10:
                    print("[CE]", end=" ")
                if val == 20:
                    print("[BM]", end=" ")
                if val == 50:
                    print("[EA]", end=" ")
            print()


