from ambiente import Grid
from agentes import AgenteReativoSimples, AgenteBaseadoEstado, AgenteBaseadoObjetivos

def main():
    # Criação do grid
    grid = Grid(10)

    # Gerar recursos e obstáculos
    grid.gerarRecursos()
    grid.gerarObstaculo()
   
    # Mostrar o grid inicial
    print("Grid Inicial:")
    grid.mostrarGrid()

    # Criar agentes
    agente1 = AgenteReativoSimples(grid, (0, 0))  # Agente reativo simples na posição (0, 0)
    #agente2 = AgenteBaseadoEstado(grid, (1, 1))   # Agente baseado em estado na posição (1, 1)
    #agente3 = AgenteBaseadoObjetivos(grid, (2, 2))  # Agente baseado em objetivos na posição (2, 2)
    print()
    # Mostrar o grid após adicionar os agentes
    print("Grid Após Adicionar Agentes:")
    grid.mostrarGrid()

    # Executar as ações dos agentes por alguns turnos
    for _ in range(1):  # Número de iterações (turnos)
        print("\nMovimento dos Agentes:")
        agente1.mover()
        agente1.mover()
        agente1.mover()
        agente1.mover()
        agente1.mover()
        agente1.mover()
        agente1.mover()
        agente1.mover()
        
        agente1.mover()
        #agente2.mover()
        #agente3.mover()
        grid.mostrarGrid()  # Exibe o estado do grid após o movimento

        print("\nColeta de Recursos:")
        agente1.coletar()
        #agente2.coletar()
        #agente3.coletar()
        grid.mostrarGrid()  # Exibe o estado do grid após a coleta

if __name__ == "__main__":
    main()
