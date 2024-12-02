import random
from ambiente import Grid


class Agente:
    def __init__(self, grid, posicao_inicial):
        self.grid = grid
        self.posicaoAtual = posicao_inicial
        self.memoria = set()
        
        
      

    def mover(self):
        raise NotImplemented("Erro, implemente o método")
    

    def coletar(self):
        raise NotImplemented("Erro, implemente o método")
    

   
class AgenteReativoSimples(Agente):
    def __init__(self, grid, posicao_inicial):
        super().__init__(grid, posicao_inicial)
        self.tipo = "AR"  # Definindo o tipo do agente
        self.grid.adicionarAgente(self.posicaoAtual[0], self.posicaoAtual[1], self.tipo)  # Passando o tipo para adicionarAgente
        self.grid.grid[self.posicaoAtual[0]][self.posicaoAtual[1]] = self.tipo

    def mover(self):
        movimentos = [
            (self.posicaoAtual[0] + dx, self.posicaoAtual[1] + dy)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ]
        movimentos_validos = [
            (x, y) for x, y in movimentos
            if 0 <= x < self.grid.tamanho and 0 <= y < self.grid.tamanho
            and self.grid.grid[x][y] in [0, 10]  # Permite movimento para células vazias ou com recursos
        ]
        if movimentos_validos:
            nova_pos = random.choice(movimentos_validos)
            if self.grid.grid[nova_pos[0]][nova_pos[1]] == 10:
                self.coletar(nova_pos)
                self.grid.atualizarPosicaoAgente(self.posicaoAtual, nova_pos, self.tipo)
                self.posicaoAtual = nova_pos
                
            else:
                self.grid.atualizarPosicaoAgente(self.posicaoAtual, nova_pos, self.tipo)
                self.posicaoAtual = nova_pos

    def coletar(self, pos):
        x, y = pos
        recurso = self.grid.grid[x][y]
        if recurso == 10:  # Coleta Cristais Energéticos
            self.grid.grid[x][y] = 0
            print(f"AgenteReativoSimples coletou Cristal Energético em ({x}, {y}).")
        

class AgenteBaseadoEstado(Agente):
    def __init__(self, grid, posicao_inicial):
        super().__init__(grid, posicao_inicial)
        self.tipo = "AE"  # Definindo o tipo do agente
        self.grid.adicionarAgente(self.posicaoAtual[0], self.posicaoAtual[1], self.tipo)  # Passando o tipo para adicionarAgente
        self.grid.grid[self.posicaoAtual[0]][self.posicaoAtual[1]] = self.tipo

    def mover(self):
        
        movimentos = [
            (self.posicaoAtual[0] + dx, self.posicaoAtual[1] + dy)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ]
        movimentos_validos = [
            (x, y) for x, y in movimentos
            if 0 <= x < self.grid.tamanho and 0 <= y < self.grid.tamanho
            and self.grid.grid[x][y] in [0, 10, 20] and (x,y) not in self.memoria # Permite movimento para células vazias ou com recursos
        ]
        if movimentos_validos:
            nova_pos = random.choice(movimentos_validos)
            self.memoria.add(self.posicaoAtual)
            if(self.grid.grid[nova_pos[0]][nova_pos[1]] == 10 or self.grid.grid[nova_pos[0]][nova_pos[1]] == 20):
                self.coletar(nova_pos)
            
            self.grid.atualizarPosicaoAgente(self.posicaoAtual, nova_pos,self.tipo)
            self.posicaoAtual = nova_pos
           

    def coletar(self, pos):
        x, y = pos
        recurso = self.grid.grid[x][y]
        if recurso == 10:  # Coleta Cristais Energéticos
            self.grid.grid[x][y] = 0
            print(f"AgenteBaseadoEstado coletou Cristal Energético em ({x}, {y}).")
        elif recurso == 20:  # Coleta Blocos de Metal Raro
            self.grid.grid[x][y] = 0
            print(f"AgenteBaseadoEstado coletou Bloco de Metal Raro em ({x}, {y}).")
        

class AgenteBaseadoObjetivos(Agente):
    def __init__(self, grid, posicao_inicial):
        super().__init__(grid, posicao_inicial)
        self.tipo = "AO"  # Definindo o tipo do agente
        self.grid.adicionarAgente(self.posicaoAtual[0], self.posicaoAtual[1], self.tipo)  # Passando o tipo para adicionarAgente
        self.grid.grid[self.posicaoAtual[0]][self.posicaoAtual[1]] = self.tipo
        self.objetivo = None

    def definirObjetivo(self):
        recursos = [(x, y) for x in range(self.grid.tamanho) for y in range(self.grid.tamanho) 
                    if self.grid.grid[x][y] in [10, 20, 50]]
        if recursos:
            self.objetivo = min(recursos, key=lambda pos: abs(pos[0] - self.posicaoAtual[0]) + abs(pos[1] - self.posicaoAtual[1]))

    def mover(self):
        if self.objetivo is None:
            self.definirObjetivo()
        if self.objetivo:
            x, y = self.posicaoAtual
            gx, gy = self.objetivo
            dx, dy = gx - x, gy - y
            movimento = (x + (1 if dx > 0 else -1 if dx < 0 else 0), 
                         y + (1 if dy > 0 else -1 if dy < 0 else 0))
            if self.grid.grid[movimento[0]][movimento[1]] == 0:
                self.grid.atualizarPosicaoAgente(self.posicaoAtual, movimento, self.tipo)
                self.posicaoAtual = movimento
                if self.posicaoAtual == self.objetivo:
                    self.objetivo = None

    def coletar(self):
        x, y = self.posicaoAtual
        recurso = self.grid.grid[x][y]
        if recurso == 10:  # Coleta Cristais Energéticos
            self.grid.grid[x][y] = 0
            print(f"AgenteBaseadoObjetivos coletou Cristal Energético em ({x}, {y}).")
        elif recurso == 20:  # Coleta Blocos de Metal Raro
            self.grid.grid[x][y] = 0
            print(f"AgenteBaseadoObjetivos coletou Bloco de Metal Raro em ({x}, {y}).")
        
