### Grupo: SO-TI-40
# Aluno 1: João Ferreira (fc54600)
# Aluno 2: João Assunção (fc56902)
# Aluno 3: Diogo Piçarra (fc60858)


### Exemplos de comandos para executar o pwordcount:
1) ./pwordcount -m -t file1.txt
	Ao executar este comando no terminal devolve-nos o número total de palavras que existem no ficheiro file1.txt.

2) ./pwordcount -m u -p 2 file1.txt file2.txt file3.txt
	Ao executar este comando o mesmo devolve-nos o número de palavras únicas em vários arquivos com nível de paralelismo 2.

3) ./pwordcount -m o -l resultado.log file1.txt
	Ao executar este comando o mesmo devolve-nos o número de ocurrências que uma palavra aparece e regista os reesultados parciais num arquivo .log.

4) ./pwordcount -m t -i 5 file1.txt file2.txt file 3.txt
	Ao executar este comando o mesmo devolve-nos a contagem total de palavras com resultados parciais de 5 em 5 segundos.

5) ./pwordcount -m u -p 3 -l resultado.log file1.txt file2.txt
	Ao exectura este comando o mesmo devolve-nos o total de palavras únicas nos ficheiros com nível de paralelismo 3 e guarda os resultados parciais num ficheiro .log



### Limitações da implementação:

- Ao utilizar o SIGNINT(Ctrl+C) o para interromper um processo, o término do processo pode não ser instantàneo para todos os casos.

- Existe dependència de bibliotecas externas tais com o 'argparse' 'multiprocessing' 'signal'.

- Quando se processa arquivos muito grandes o script lê os arquivos de texto na memória antes de contar as palavaras, isso para arquivos muito grandes pode ser problemático.

- O argumento -i define um intervalo de tempo fixo para imprimir os resultados parciais, isso pode não ser benéfico caso 2 arquivos sejam processados em tempos diferentes.

- Ao utilizar contadores é preciso a utilização de locks para acessos concorrentes, isto pode aumentar a complexidade e causar problemas de desempenho.

- É necessário usar o linux ou uma VM para correr os programas.



### Abordagem para a divisão dos ficheiros:


- Dividir por tamanho de ficheiro(dividir de x em x megabytes)

- Dividir por número de linhas(Dividir um ficheiro de x em x linhas)

- Divisão aleatória(Divide o ficheiro aleatoriamente)

- Divisão por delimitadores



### Outras informações pertinentes:

- O script aceita os argumetos -m(modo de contagem), -p(nível de paralelismo), -i(intervalo de tempo para resultados parciais), -l(arquivo .log) e os ficheiros a processar(ex: file1.txt) na linha de comando de maneira a poder personalizar o que nos queremos obter.

- Script usa  contadores compartilhados 'Queue' e 'Value' para partilhar dados entre processos paralelos.

- Consegue registrar o tempo de execução e se for especificado consegue gravar os resultados parciais num ficheiro .log.

- Utiliza biblioteca 'multiprocessing' para o processamento paralelo.

- Todo o código principal está contido na função 'main' que apenas é chamada quando o script é diretamente executado.

- Se acontecer algum erro com processamento de de ficheiros ou ficheiros não encontrados por algum motivo o script tem tratamento de exceções para lidar com esses erros que podem acontecer.

