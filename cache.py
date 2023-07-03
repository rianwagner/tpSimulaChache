# Trabalho partico de AOC2 (Arquitetura e Organização de Computadores)
# Codigo desenvolvido por Rian Wagner 
import copy

class Memorias():
    class Bloco(): # Define bloco
        def __init__(self, estado, endereco_RAM, tamanho):
            self.estado = estado
            self.endereco_RAM = endereco_RAM
            self.palavra = [None]*tamanho

        def altera_bloco(self, estado, endereco_RAM, bloco):
            self.estado = estado
            self.endereco_RAM = endereco_RAM
            self.palavra = bloco


    class RAM(): # Define a RAM
        def __init__(self, tamanho_palavra, tamanho_linha, tamanho_RAM, A, B):
            self.num_linha = int(tamanho_RAM/tamanho_linha)
            self.num_palavra = int(tamanho_linha/tamanho_palavra)
            self.linha = []
            linha = []
            
            # Blocos da RAM são criados vazios
            for i in range(0, self.num_linha):
                # Cria um novo objeto Bloco com estado 'E', endereço na RAM 'i' e tamanho de palavra 'tamanho_palavra'
                self.linha.append(Memorias.Bloco('E', i, tamanho_palavra))
            # Preenche os blocos com os vetores A[i][j] e B[i]
            i = -1
            for j in range(0, len(A)):
                for k in range(0, len(A[j])):
                    if(k % self.num_palavra == 0):
                        if(i != -1):
                            # Atualiza o bloco anterior com o estado 'E', endereço na RAM 'i' e lista 'linha'
                            self.linha[i].altera_bloco('E', i, linha)
                            linha = []
                        i = i+1
                    # Adiciona o valor A[j][k] a lista de linha
                    linha.append(A[j][k])
            
            self.linha[i].altera_bloco('E', i, linha)
            linha = []
            i = i+1

            for j in range(0, len(B)):
                if((j % self.num_palavra == 0) and (j != 0)):
                    # Atualiza o bloco
                    self.linha[i].altera_bloco('E', i, linha)
                    # Cria uma lista para armazenar as palavras
                    linha = []
                    # incrementa para o proximo bloco
                    i = i+1
                linha.append(B[j]) # Adiciona os valores de B 
            # Atualiza o bloco
            self.linha[i].altera_bloco('E', i, linha) 
        
        def altera_linha(self, lines):
            # Atualaiza a linha atual com as novas linhas passasas como argumento
            self.line = lines
    
    class Cache(): # Estrutura da Cache
        def __init__(self, tamanho_palavra, tamanho_linha, tamanho_cache):
            self.num_linha = int(tamanho_cache/tamanho_linha)
            self.num_palavras = int(tamanho_linha/tamanho_palavra)
            self.hit = 0
            self.miss = 0
            self.linha = [] # Lista vazia a ser preenchida

            for i in range(0, self.num_linha):
                self.linha.append(Memorias.Bloco('I', -1, tamanho_palavra))

        # altera_linha substitui a linha atual da cache por uma nova lista de linhas fornecida como argumento.
        def altera_linha(self, linhas):
            self.linha = linhas
        # ivalidado ivalida um bloco especifico da cache
        def invalidado(self, i):
            self.linha[i].altera_bloco('I', -1, [None, None, None, None])

    def escritor(self, alto, baixo, ocorrencia, destino):
        if(destino == -1):
            destino = alto.linha[ocorrencia].endereco_RAM % baixo.num_linha
        
        baixo.linha[destino] = copy.deepcopy(alto.linha[ocorrencia])
        return baixo.linha
    
    def modificador(self, cache, endereco):
        endereco_RAM = cache.linha[endereco].endereco_RAM
        bloco = cache.linha[endereco].palavra
        # Altera o estado do bloco para 'M' (modificado) e atualiza o endereço RAM e a palavra do bloco
        cache.linha[endereco].altera_bloco('M', endereco_RAM, bloco)
        return cache
    
    def busca_inclusiva(self, memoria, RAM, endereco_RAM, palavra):
        tamanho_L1 = memoria.L1.num_linha
        tamanho_L2 = memoria.L2.num_linha

        # Verifica se a palavra está presente na linha da cache L1 correspondente ao endereço_RAM
        resultado = palavra in memoria.L1.linha[endereco_RAM % tamanho_L1].palavra

        # Se a palavra não estiver presente na cache L1
        if(resultado == False):
            memoria.L1.miss += 1 # +1 cache miss em L1

            # Calcula o endereço da cache L2 onde a palavra poderia estar presente
            endCache_L2 = endereco_RAM % (memoria.L2.num_linha - memoria.L1.num_linha) + memoria.L1.num_linha
            # Verifica se a palavra está presente na linha da cache L2 correspondente a endCache_L2
            if(palavra in memoria.L2.linha[endCache_L2].palavra):
                endereco_Cache = endereco_RAM % memoria.L1.num_linha

                # Se o bloco na cache L1 correspondente a endereco_Cache estiver no estado 'M', escreve de volta na RAM
                if(memoria.L1.linha[endereco_Cache].estado == 'M'):
                    linha = self.escritor(memoria.L1, RAM, endereco_Cache, -1)
                    RAM.altera_linha(linha)
                
                auxiliar = copy.deepcopy(memoria.L1)
                # Move o bloco da cache L2 para a cache L1
                linha = self.escritor(memoria.L2, memoria.L1, endCache_L2, -1)
                 # Move o bloco da cache L2 para o mesmo local em que estava na cache L1
                linhaA = self.escritor(memoria.L2, memoria.L2, endCache_L2, endereco_Cache)
                # Atualiza a linha correspondente da cache L2 com a linha movida da cache L1
                memoria.L2.altera_linha(linhaA)
                # Invalida o bloco movido da cache L2
                memoria.L2.invalidado(endCache_L2)

                
                # Se o bloco na cache L1 não estiver no estado 'I', ele é movido para L2 na posição correspondente
                if(auxiliar.linha[endereco_Cache].estado != 'I'):
                    enderecoCache_L2 = auxiliar.linha[endereco_Cache].endereco_RAM % (memoria.L2.num_linha - memoria.L1.num_linha) + memoria.L1.num_linha
                    linhaAA = self.escritor(auxiliar, memoria.L2, endereco_Cache, enderecoCache_L2)
                    memoria.L2.altera_linha(linhaAA)

                # Atualiza a linha correspondente da cache L1 com a linha movida da cache L2
                memoria.L1.altera_linha(linha)
                memoria.L1.altera_linha(linha)
                memoria.L2.hit += 1 # +1 cache hit em L2
                return True
            
             # Se a palavra também não estiver presente na L2, ocorre um miss
            if(resultado == False):
                memoria.L2.miss += 1 # +1 miss em L2
                self.substituicao_i(memoria, RAM, endereco_RAM)
        # Se a palavra estiver em L1, ocorre um hit
        if(resultado == True):
            memoria.L1.hit +=1 # +1 hit em L1

        return resultado
            
    # Basicamente igual a busca_inclusiva, no entanto so busca em L2 se L1 falhar
    def busca_exclusiva(self, memoria, RAM, endereco_RAM, palavra):
        tamanho_L1 = memoria.L1.num_linha
        tamanho_L2 = memoria.L2.num_linha

        resultado = palavra in memoria.L1.linha[endereco_RAM % tamanho_L1].palavra
        
        if(resultado == True):
            memoria.L1.hit += 1
            return resultado

        if(resultado == False):
            memoria.L1.miss += 1

            endCache_L2 = endereco_RAM % memoria.L2.num_linha 
            if(palavra in memoria.L2.linha[endCache_L2].palavra): 
                endereco_Cache = endereco_RAM % memoria.L1.num_linha

                if(memoria.L1.linha[endereco_Cache].estado == 'M'):
                    linha = self.escritor(memoria.L1, RAM, endereco_Cache, -1)
                    RAM.altera_linha(linha)

                auxiliar = copy.deepcopy(memoria.L1)
                linha = self.escritor(memoria.L2, memoria.L1, endCache_L2 , -1)
                memoria.L2.invalidado(endCache_L2)

                if(auxiliar.linha[endereco_Cache].estado != 'I'):
                    L2_endereco = auxiliar.linha[endereco_Cache].endereco_RAM % memoria.L2.num_linha 
                    linhaAA = self.escritor(auxiliar, memoria.L2, endereco_Cache, L2_endereco)
                    memoria.L2.altera_linha(linhaAA)

                memoria.L1.altera_linha(linha)
                memoria.L2.hit += 1
                return True
        
            if(resultado == False):
                memoria.L2.miss += 1
                self.substituicao_e(memoria, RAM, endereco_RAM)
        
    

        return resultado

            
    def substituicao_i(self, Cache, RAM, endereco_RAM):
        # Obtém o endereço da cache correspondente ao endereço de RAM fornecido
        endereco_cache = endereco_RAM % Cache.L1.num_linha

        # Verifica se o estado do bloco na cache L1 é 'M' (modificado)
        if(Cache.L1.linha[endereco_cache].estado == 'M'):
            # Se sim, escreve o bloco de volta na RAM antes de substituí-lo
            linha = self.escritor(Cache.L1, RAM, endereco_cache, -1)
            RAM.altera_linha(linha)

         # Calcula o endereço correspondente na cache L2
        L2_endereco = Cache.L1.linha[endereco_cache].endereco_RAM % (Cache.L2.num_linha - Cache.L1.num_linha) + Cache.L1.num_linha
    
         # Verifica se o bloco na cache L1 não está no estado inválido
        if(Cache.L1.linha[endereco_cache].estado != 'I'):
            # transfere o bloco para a cache L2 antes de substituí-lo
            linha = self.escritor(Cache.L1, Cache.L2, endereco_cache, L2_endereco) # L2 usada como cache de vitimas
            Cache.L2.altera_linha(linha)

        # Escreve o bloco da RAM na cache L1
        linha = self.escritor(RAM, Cache.L1, endereco_RAM, endereco_cache)
        Cache.L1.altera_linha(linha)
        # Escreve o bloco da RAM na cache L2
        linha = self.escritor(RAM, Cache.L2, endereco_RAM, endereco_cache)
        Cache.L2.altera_linha(linha)

    def substituicao_e(self, Cache, RAM, endereco_RAM):
        # Obtém o endereço da cache correspondente ao endereço de RAM fornecido
        endereco_cache = endereco_RAM % Cache.L1.num_linha

        # Verifica se o estado do bloco na cache L1 é modificado
        if(Cache.L1.linha[endereco_cache].estado == 'M'):
            # Escreve o bloco de volta na RAM antes de substituir
            linha = self.escritor(Cache.L1, RAM, endereco_cache, -1)
            RAM.altera_linha(linha)

         # Calcula o endereço correspondente na cache L2
        L2_endereco = Cache.L1.linha[endereco_cache].endereco_RAM % Cache.L2.num_linha

        # Verifica se o bloco na cache L1 não está inválido
        if(Cache.L1.linha[endereco_cache].estado != 'I'):
            # transfere o bloco para a cache L2 antes de substituir
            linha = self.escritor(Cache.L1, Cache.L2, endereco_cache, L2_endereco)
            Cache.L2.altera_linha(linha)

         # Escreve o bloco da RAM na cache L1
        linha = self.escritor(RAM, Cache.L1, endereco_RAM, endereco_cache)
        Cache.L1.altera_linha(linha)

def criador_vetores(tamanho_A, tamanho_B):
    A = [] # Inicializa A
    B = [] # Inicializa B
    for i in range(0, tamanho_A): # Ate o tamanho passado
        A.append([])
        for j in range(0, tamanho_A):
            A[i].append('A['+ str(i) +']['+ str(j) +']')

    for i in range(0, tamanho_B):
        B.append('B['+ str(i) + ']')

    return A, B # Retorna os arrays A e B

class indice(): # Define os niveis de cache
    def __init__(self):
        self.L1 = Memorias.Cache(4, 16, 4096) 
        self.L2 = Memorias.Cache(4, 16, 65536) 

def main():
    tamanho_array = 2048 # Define o tamanho dos arrays A e B

    # Calcula o tamanho necessário da memória RAM com base no tamanho do array
    tamanho_RAM = (tamanho_array**2 + tamanho_array) * 4
    A, B = criador_vetores(tamanho_array, tamanho_array)
    # Parâmetros: 4 (tamanho da palavra em bytes), 16 (tamanho da linha em palavras),
    RAM = Memorias.RAM(4, 16, tamanho_RAM, A, B)
    CPU = Memorias()
    Cache = indice()

    # Teste:
    for i in range(0, tamanho_array):
        for j in range(0, tamanho_array):
            # Calcula os endereços de B e A na RAM
            endereco_B = (tamanho_array**2 + j) // RAM.num_palavra
            endereco_A = (i*tamanho_array + j) // RAM.num_palavra
            # Realiza a busca no sistema inclusivo
            resultado = CPU.busca_inclusiva(Cache, RAM, endereco_B, B[j])
            resultado = CPU.busca_inclusiva(Cache, RAM, endereco_A, A[i][j])
            # Modifica se necessario
            Cache.L1 = CPU.modificador(Cache.L1, endereco_A % Cache.L1.num_linha)


    print('\nSistema de cache inclusiva:')
    hit = Cache.L1.hit + Cache.L2.hit
    print("Total de Cache Hit: ", hit)
    print("Hit em L1: ", Cache.L1.hit)
    print("Hit em L2: ", Cache.L2.hit)
    miss = Cache.L1.miss + Cache.L2.miss
    print("Total de Cache Miss: ", miss)
    print("Miss em L1: ", Cache.L1.miss)
    print("Miss em L2: ", Cache.L2.miss)

    # Cria a RAM noavemente, com os paramentros iguais, para o outro sistema de cache
    RAM = Memorias.RAM(4, 16, tamanho_RAM, A, B)
    CPU = Memorias()
    Cache = indice()

    for i in range(0, tamanho_array):
        for j in range(0, tamanho_array):
            # Calcula os endereços de B e A na RAM
            endereco_B = (tamanho_array**2 + j) // RAM.num_palavra
            endereco_A = (i*tamanho_array + j) // RAM.num_palavra
            # Realiza a busca no sistema inclusivo
            resultado = CPU.busca_exclusiva(Cache, RAM, endereco_B, B[j])
            resultado = CPU.busca_exclusiva(Cache, RAM, endereco_A, A[i][j])
            # Modifica se necessario
            Cache.L1 = CPU.modificador(Cache.L1, endereco_A % Cache.L1.num_linha)
    
    print('\nSistema de cache exclusiva:')
    hit = Cache.L1.hit + Cache.L2.hit
    print("Total de Cache Hit: ", hit)
    print("Hit em L1: ", Cache.L1.hit)
    print("Hit em L2: ", Cache.L2.hit)
    miss = Cache.L1.miss + Cache.L2.miss
    print("Total de Cache Miss: ", miss)
    print("Miss em L1: ", Cache.L1.miss)
    print("Miss em L2: ", Cache.L2.miss)

main()