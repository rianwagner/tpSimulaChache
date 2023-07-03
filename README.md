# Simulação de Sistemas de Cache
Este projeto consiste em uma simulação de dois sistemas de cache: um sistema de cache exclusivo e um sistema de cache inclusivo. O objetivo é analisar as taxas de erros nos dois sistemas para um determinado código em C.

## Especificações
Tamanho da palavra: 4 bytes.
Tamanho da linha: 16 bytes.
Cache L1: 4 kiB diretamente mapeada.
Cache L2: 64 kiB diretamente mapeada.
Políticas de escrita: write-through.
Código em C
O código em C fornecido realiza operações em matrizes A e B. A matriz A possui dimensões 2048x2048 e a matriz B possui dimensão 2048x1. O código percorre as matrizes e realiza operações de multiplicação e soma.

## Como Executar
Compile o programa cache.py

## Resultados
Após a execução dos programas, serão exibidos os seguintes resultados:

Taxa de acertos e erros na cache L1 para cada sistema de cache.
Taxa de acertos e erros na cache L2 apenas para o sistema de cache inclusivo.

## Análise dos Resultados
Com base nos resultados exibidos, é possível responder às seguintes questões:

a) Houve diferença entre as taxas de erros nos esquemas inclusivo e exclusivo de cache? Compare a taxa de erros somente na L1 e erros nos dois níveis de cache para os dois sistemas simulados.

b) No esquema exclusivo, quantas referências resultaram na utilização da cache L2 como cache de vítima (alocando um bloco removido da cache L1)?

##vObservações
Este projeto foi desenvolvido como uma simulação dos sistemas de cache exclusivo e inclusivo. Os resultados podem variar dependendo do tamanho das caches e dos arrays.