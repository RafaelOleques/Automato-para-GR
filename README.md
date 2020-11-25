# Conversor de AFD para GR e gerador de palavras

Desenvolvimento de uma aplicação em python que converte um Autômato Finito Determinístico em uma Gramática Regular e mostra os passos que a GR utiliza
para gerar uma determinada palavra da linguagem. Feito para a disciplina de Linguagens Formais e Autômatos
por João Vitor Moreira Dias, Mateus Luiz Salvi e Rafael Oleques Nunes.

**Execução:**
1. Abra o terminal
2. Entre no diretório conversor , onde está o código do programa
3. Digite o comando python gerador.py
4. Siga as instruções dadas

**Observações:**
- O autômato deve ser dado por meio de um arquivo .txt
- Para ver os ciclos do algoritmo de Earley, escolha o parâmetro print do construtor da classe _Earley_ como True no gerador.py
- Caso a linguagem aceite a palavra vazia, ela deve ser adicionada artificialmente como um símbolo no autômato
