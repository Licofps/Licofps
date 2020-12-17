def acha_palavra(linhas, palavra): #Verificar se a palavra é menor  ou igual o numero de linhas.
	pode_horizontal = True if len(linhas[0]) >= len(palavra) else False	
	pode_vertical = True if len(linhas) >= len(palavra) else False
	pode_diagonal = pode_horizontal and pode_vertical

	for direcao, possivel in [('H', pode_horizontal), ('V', pode_vertical)]: #Procuras as posições das palavras.
		if possivel:
			linhas_direcionadas = zip(*linhas) if direcao == 'V' else linhas 
			for index_linha, linha in enumerate(linhas_direcionadas):
				indices_letra = acha_horizontal(linha, palavra)
				if indices_letra:
					posicoes = [(index_linha, index_letra) for index_letra in indices_letra]
					posicoes = [posicao[::-1] for posicao in posicoes] if direcao == 'V' else posicoes
					return posicoes

	if pode_diagonal:
		diagonais = [(monta_matriz_diagonal(linhas, 'E'), 'E'), (monta_matriz_diagonal(linhas, 'D'), 'D')]#Cria matrizes e retorna a posição das linhas com a palavra
		for diagonal, sentido in diagonais:
			for index_comeco_diagonal, linha in enumerate(diagonal):
				linhas_palavra = acha_horizontal(linha, palavra)
				if linhas_palavra:
					sobra = index_comeco_diagonal - (len(linha) - 1)
					index_comeco_diagonal = len(linha) - 1 if index_comeco_diagonal >= len(linha) - 1 else index_comeco_diagonal

					linha_letras = [letra for letra in linha if letra.strip()]
					linha_letras = linha_letras[::-1] if sentido == 'E' else linha_letras

					diagonal_posicoes = [(0 - (index_comeco_diagonal - (len(linha) - 1) - x) + sobra, y) for x, y in enumerate(linha_letras)]
					posicoes_na_linha = acha_posicoes_na_linha(diagonal_posicoes, palavra, sentido)
					return list(zip(linhas_palavra, posicoes_na_linha))

def acha_horizontal(linha, palavra): 
	linha = ''.join(linha)
	invertida = palavra[::-1]
	for estilo_palavra in (palavra, invertida):
		if estilo_palavra in linha:
			return [linha.index(estilo_palavra) + n for n in range(len(estilo_palavra))]
	return False

def monta_matriz_diagonal(linhas, sentido):
	linhas_diagonal = []
	for index_linha, linha in enumerate(linhas):
		qtd_espacos_inicio = index_linha if sentido == 'E' else len(linhas) - index_linha - 1
		qtd_espacos_fim = index_linha if sentido == 'D' else len(linhas) - index_linha - 1
		linhas_diagonal.append([' '] * qtd_espacos_inicio + linha + [' '] * qtd_espacos_fim)
	return zip(*linhas_diagonal)

def acha_posicoes_na_linha(diagonal_posicao, palavra, sentido):
	linha = ''.join([diagonal[1] for diagonal in diagonal_posicao])
	invertida = palavra[::-1]

	indices_palavra = range(len(palavra)) if sentido == 'D' else range(len(palavra))[::-1]

	for estilo_palavra in (palavra, invertida):
		if estilo_palavra in linha:
			n = linha.index(estilo_palavra)
			return [diagonal_posicao[n + letra_index][0] for letra_index in indices_palavra]


def main():
	arq = open('arq1in.txt', 'r')		#abre o arquivo com o caça-palavras
	lido = arq.readlines()		#armazena o que foi lido em uma variável
	arq.close()		#fecha o arquivo


	#formata a leitura do arquivo (remove as quebras de linha)
	leitura = []
	for l in lido:					
		leitura.append(l.replace('\n', ''))		


	#criação da matriz com as linhas do caça-palavras
	linhas = []		
	while True:
		for c in range(len(leitura)):		#percorre a lista da leitura
			if leitura[c].isdigit():		#verifica se um número foi informado
				break
			linhas.append(leitura[c].split())	#adiciona o texto lido às linhas da matriz
		break
	palavras = leitura[c + 1:]						#fatia o resto da lista (palavras a serem buscadas)

	posicoes_achou = []
	for palavra in palavras:
		posicoes = acha_palavra(linhas, palavra)
		if posicoes:
			posicoes_achou.extend(posicoes)


	#escreve as linhas no arquivo
	arq = open('arq1res.txt', 'w')		#abre o arquivo
	for index_linha, linha in enumerate(linhas): 		
		impressao_linha = ''
		for index_letra, letra in enumerate(linha):
			if (index_linha, index_letra) in posicoes_achou:	#se as posições de linha e letra estiverem na lista das posições salvas
				impressao_linha += letra + ' '		#adiciona a letra e o espaço em branco à linha que será escrita
			else:
				impressao_linha += '. '				#se não, substitui por um ponto
		linha_arquivo = impressao_linha.strip()   #remove os espaços extras que podem sobrar no final da linha
		linha_arquivo += '\n'					#adiciona uma quebra de linha na string que vai ser escrita
		arq.write(linha_arquivo)				#escreve no arquivo a string que foi gerada
	arq.close()									#fecha o arquivo

main()
