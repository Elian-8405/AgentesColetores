import heapq
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
        
import heapq

class AgenteBaseadoObjetivos(Agente):
    def __init__(self, grid, posicao_inicial):
        super().__init__(grid, posicao_inicial)
        self.tipo = "AO"
        self.grid.adicionarAgente(self.posicaoAtual[0], self.posicaoAtual[1], self.tipo)
        self.grid.grid[self.posicaoAtual[0]][self.posicaoAtual[1]] = self.tipo
        self.objetivo = None
        self.caminho = []

    def definirObjetivo(self):
        # Identifica recursos no grid com seus valores
        recursos = [(x, y, self.grid.grid[x][y]) for x in range(self.grid.tamanho) for y in range(self.grid.tamanho)
                    if self.grid.grid[x][y] in [10, 20]]

        if recursos:
            # Prioriza pelo valor do recurso e depois pela distância
            recursos_ordenados = sorted(
                recursos,
                key=lambda r: (-r[2], abs(r[0] - self.posicaoAtual[0]) + abs(r[1] - self.posicaoAtual[1]))
            )
            objetivo = recursos_ordenados[0][:2]
            self.objetivo = objetivo
            self.caminho = self.planejarRota(self.posicaoAtual, objetivo)
            print(f"Novo objetivo do Agente de Objetivo: {self.objetivo}")

    def planejarRota(self, origem, destino):
        def heuristica(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        fila = []
        heapq.heappush(fila, (0, origem))
        veio_de = {}
        custo_ate_aqui = {origem: 0}

        while fila:
            _, atual = heapq.heappop(fila)

            if atual == destino:
                caminho = []
                while atual != origem:
                    caminho.append(atual)
                    atual = veio_de[atual]
                caminho.reverse()
                return caminho

            x, y = atual
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vizinho = (x + dx, y + dy)
                if 0 <= vizinho[0] < self.grid.tamanho and 0 <= vizinho[1] < self.grid.tamanho:
                    if self.grid.grid[vizinho[0]][vizinho[1]] in [0, 10, 20]:  # Células livres ou com recursos
                        novo_custo = custo_ate_aqui[atual] + 1
                        if vizinho not in custo_ate_aqui or novo_custo < custo_ate_aqui[vizinho]:
                            custo_ate_aqui[vizinho] = novo_custo
                            prioridade = novo_custo + heuristica(vizinho, destino)
                            heapq.heappush(fila, (prioridade, vizinho))
                            veio_de[vizinho] = atual
        return []

    def mover(self):
        if self.objetivo is None or not self.caminho:
            self.definirObjetivo()

        if self.caminho:
            proxima_posicao = self.caminho.pop(0)
            valor_celula = self.grid.grid[proxima_posicao[0]][proxima_posicao[1]]
            #self.coletar(proxima_posicao)

            # Permitir movimento para células vazias (0) ou com recursos (10, 20)
            if valor_celula in [0, 10, 20]:
                self.coletar(proxima_posicao)
                self.grid.atualizarPosicaoAgente(self.posicaoAtual, proxima_posicao, self.tipo)
                
                self.posicaoAtual = proxima_posicao
                #print(f"Agente se moveu para {self.posicaoAtual}")


                # Se alcançar o objetivo, coleta o recurso
                if self.posicaoAtual == self.objetivo:
                    self.coletar(self.posicaoAtual)
                    self.objetivo = None
                    self.caminho = []
            else:
                # Replanejar se a célula estiver ocupada
                print(f"Célula {proxima_posicao} ocupada. Replanejando...")
                self.objetivo = None
                self.caminho = []

    def coletar(self, pos):
        x, y = pos
        recurso = self.grid.grid[x][y]
        if recurso in [10, 20]:
            self.grid.grid[x][y] = 0
            if recurso == 10:
                print(f"AgenteBaseadoObjetivo coletou Cristal Energetico em ({x}, {y}).")
            
