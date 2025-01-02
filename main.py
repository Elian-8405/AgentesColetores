from ambiente import Grid
from agentes import AgenteReativoSimples, AgenteBaseadoEstado, AgenteBaseadoObjetivos

def main():
    # Criação do grid
    grid = Grid(15)

    # Gerar recursos e obstáculos
    grid.gerarRecursos()
    grid.gerarObstaculo()
   
    # Mostrar o grid inicial
    print("Grid Inicial:")
    grid.mostrarGrid()

    # Criar agentes
    agente1 = AgenteReativoSimples(grid, (0, 0))  # Agente reativo simples na posição (0, 0)
    agente2 = AgenteBaseadoEstado(grid, (1, 1))   # Agente baseado em estado na posição (1, 1)
    agente3 = AgenteBaseadoObjetivos(grid, (2, 2))  # Agente baseado em objetivos na posição (2, 2)
    print()
   
    print("Grid Após Adicionar Agentes:")
    grid.mostrarGrid()

    
    for _ in range(20):  
        print("\nMovimento dos Agentes:")
        agente1.mover()
        agente2.mover()
        agente3.mover()
       
        
       
        print("-"*40)
        grid.mostrarGrid()  
        print("-"*40)
       
    
      

if __name__ == "__main__":
    main()



