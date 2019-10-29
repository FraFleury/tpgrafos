#Bibliotecas
import numpy as np
import copy
import itertools
import time



nomeAqr = input("Qual o arquivo de entrada:")


# Le o grafo e o retorna no formato matriz de adjacencia.
def lerGrafo():

	file = np.loadtxt(nomeAqr)

	return file


# Retorna o grafo como lista de adjacencia.
def listAdjacencia(matrizAdj):
	listaAdj = []

	for i in range(0, len(matrizAdj)):
		listaAdj.append([])
		for j in range(0 ,len(matrizAdj)):

			if matrizAdj[i][j] != 0:
				listaAdj[i].append([j, matrizAdj[i][j]])

	return listaAdj



# Verifica se o grafo e euleriano.
def verificaGrafoEuleriano(listaAdj):
	resp = 1
	for i in range(0, len(listaAdj)):
		if len(listaAdj[i])%2 != 0:
			resp = 0
			break

	return resp



# Inclui o novo ciclo.
def incluirNovoCiclo(ciclo, cicloAchado):
	novoCiclo = []
	inserido = 0

	if len(ciclo)== 0:
		novoCiclo = cicloAchado.copy()
	else:
		for i in range(0, len(ciclo)):
			novoCiclo.append(ciclo[i])
			#Inserindo o novo Ciclo
			if ciclo[i] == cicloAchado[0] and inserido != 1:
				for j in range(1, len(cicloAchado)):
					novoCiclo.append(cicloAchado[j])
				inserido = 1

			#Ciclo foi inserido


	return novoCiclo



# Apaga aresta do grafo.
def apagarAresta(grafo, extremidadeAresta1, extremidadeAresta2):
	for k in range(0, len(grafo)):
		tamanho = len(grafo[k])
		if grafo[k][tamanho-1] == extremidadeAresta1:
			for j in range(0, tamanho-1):
				if grafo[k][j][0] == extremidadeAresta2:
					del grafo[k][j]
					break

	for k in range(0, len(grafo)):
		tamanho = len(grafo[k])
		if grafo[k][tamanho-1] == extremidadeAresta2:
			for j in range(0, tamanho-1):
				if grafo[k][j][0] == extremidadeAresta1:
					del grafo[k][j]
					break

	return grafo


# Acha o indices de um vertice no grafoRestante que pertence ao ciclo contruido.
def acharVerticeInicial(ciclo, grafoRestante):
	for i in range(0, len(ciclo)):
		for j in range(0, len(grafoRestante)):
			tamanho = len(grafoRestante[j])
			if ciclo[i] == grafoRestante[j][tamanho-1] and tamanho-1 != 0:
				"""print("*******vertice achado:", j)
				print("*******grafoRestante[j]", grafoRestante[j])
				print("*******tamanho-1", tamanho-1)
				print("******* grafoRestante[j][tamanho-1]", grafoRestante[j][tamanho-1])"""
				return j




# Verifica se existe uma aresta no grafo restante.
def estarNografoRestante(extremidadeAresta1, extremidadeAresta2, custo, grafoRestante):
	for i in range(0, len(grafoRestante)):
		tamanho = len(grafoRestante[i])
		if grafoRestante[i][tamanho-1] == extremidadeAresta1 and [extremidadeAresta2, custo] in grafoRestante[i][0]:
			return 1

	return 0



# Verifica se não existe mais lista de adjacencia ou seja se todo mundo tem tamanho 1.
def todosTamanhoUm(grafoRestante):
	for i in range(0, len(grafoRestante)):
		if len(grafoRestante[i]) != 1:
			return 0
	return 1



# Achar o ciclo euleriano.
def acharEulerCiclo(listAdj):

	grafoRestante = copy.deepcopy(listAdj)
	for i in range(0, len(grafoRestante)):
		grafoRestante[i].append(i)

	indiceVerticeInicio = 0
	ciclo = []


	while len(grafoRestante) != 0:

		cicloAchado = []
		tamanho = len(grafoRestante[indiceVerticeInicio])
		verticeInicio = grafoRestante[indiceVerticeInicio][tamanho-1]
		cicloAchado.append(grafoRestante[indiceVerticeInicio][tamanho-1])

		extremidadeAresta = grafoRestante[indiceVerticeInicio][0][0]
		cicloAchado.append(extremidadeAresta)
		apagarAresta(grafoRestante, grafoRestante[indiceVerticeInicio][tamanho-1], extremidadeAresta)

		while extremidadeAresta != indiceVerticeInicio:

			#Procurando a próxima aresta a incluir no ciclo
			for i in range(0, len(listAdj[extremidadeAresta])):

				"""print("i:", i)
				print("Visitando", listAdj[extremidadeAresta][i])
				print("#####tamanho-1",tamanho-1)"""

				#Verificando se a aresta já não foi descoberta
				if listAdj[extremidadeAresta][i] in grafoRestante[extremidadeAresta] :
					cicloAchado.append(listAdj[extremidadeAresta][i][0])
					grafoRestante = apagarAresta(grafoRestante, extremidadeAresta, listAdj[extremidadeAresta][i][0])
					extremidadeAresta = listAdj[extremidadeAresta][i][0]
					break


					#Quando o vertice não tem mais arrestas incidente nele no grafoRestante, apagamos o
					"""if len(grafoRestante[extremidadeAresta]) == 1:
					del grafoRestante[extremidadeAresta]"""


		ciclo = incluirNovoCiclo(ciclo, cicloAchado)

		if  todosTamanhoUm(grafoRestante) == 1:
			break

		if len(grafoRestante) != 0 :
			#grafoRestante = limparGrafoRestante(grafoRestante)
			indiceVerticeInicio = acharVerticeInicial(ciclo, grafoRestante)

	return	ciclo


# Verifica se o grafo e euleriano.
def euLerianoGrafo(listAdj):
	if(verificaGrafoEuleriano(listAdj)) == 0:
		return 0
	else:
		return (acharEulerCiclo(listAdj))


# Encontra os vertices que so possuem uma aresta e retorna estas arestas.
def acharFinsDeLinha(listaAdj):
	verticesSozinhos = []
	listaAdjAux = copy.deepcopy(listaAdj)

	for i in range(0, len(listaAdj)):
		if(len(listaAdj[i]) == 1):
			verticesSozinhos.append(i)

	arestasSozinhas = []
	j = 0

	for i in verticesSozinhos:
		arestasSozinhas.append(listaAdjAux[i])
		arestasSozinhas[j].append(i)
		j += 1

	return arestasSozinhas

# Adiciona uma aresta a um par de vertices.
def adicionaAresta(listaAdj, aresta):
	listaAdj[aresta[-1]].append(aresta[0])
	arestaAux = [copy.deepcopy(aresta[-1]), copy.deepcopy(aresta[0][1])]
	listaAdj[aresta[0][0]].append(arestaAux)

# Retorna uma lista dos vertices de grau impar do grafo.
def retornaImpares(listaAdj):
	verticesImpares = []

	for i in range(0, len(listaAdj)):
		if(len(listaAdj[i]) % 2 != 0):
			verticesImpares.append(i)

	return verticesImpares

# Constroi todos os duplas possiveis de vertices de grau impar.
def constroiDuplas(listaAdj):
	verticesImpares = retornaImpares(listaAdj)

	return [x for x in itertools.combinations(verticesImpares, 2)]

# Acha o custo total do grafo.
def achaCustoTotal(listaAdj):
	custoTotal = 0
	for i in range(0, len(listaAdj)):
		for j in range(0, len(listaAdj[i])):
			custoTotal += listaAdj[i][j][1]

	return custoTotal / 2

# Retorna um dicionario com as arestas disponiveis para o vertice.
def opcoesDeAresta(listaAdj, vertice):
	opcoes = []
	for i in range(0, len(listaAdj[vertice])):
		opcoes.append(listaAdj[vertice][i])

	return opcoes

# Resume uma cadeia de vertices anteriores e retorna um caminho.
def resumeCaminho(fim, verticesAnteriores):
	caminho = []
	anterior = fim
	while anterior != None:
		caminho.insert(0, anterior)
		anterior = verticesAnteriores[anterior]

	return caminho

# Retorna o custo minimo e uma rota do vertice inicial para o final. (Dijkstra)
def achaCusto(caminho, listaAdj):
	inicio = copy.deepcopy(caminho[0])
	fim = copy.deepcopy(caminho[1])

	vertices = [i for i in range(0, len(listaAdj))]
	naoVisitados = set(vertices)

	custoTotal = achaCustoTotal(listaAdj)
	# Inicializa todos os vertices com custo maximo.
	custosVertices = {vertice: custoTotal for vertice in vertices}
	custosVertices[inicio] = 0 # Vertice inicial tem custo zero.

	verticesAnteriores = {vertice: None for vertice in vertices}

	vertice = inicio

	while naoVisitados:
		for opcao in opcoesDeAresta(listaAdj, vertice):
			proxVertice = opcao[0]
			if proxVertice not in naoVisitados:
				continue # Andar sempre para frente.
			# Se este caminho for mais barato que o anterior, atualiza.
			if custosVertices[proxVertice] > custosVertices[vertice] + opcao[1]:
				custosVertices[proxVertice] = custosVertices[vertice] + opcao[1]
				verticesAnteriores[proxVertice] = vertice
		naoVisitados.remove(vertice)
		# O proximo vertice tem de ser o mais proximo nao visitado.
		opcoes = {}
		for i in range(0, len(custosVertices)):
			if(i in naoVisitados):
				opcoes[i] = custosVertices[i]
		try:
			# Acha chave de menor valor no dicionario.
			vertice = min(opcoes, key = opcoes.get) # Pega o vertice mais proximo
		except ValueError: # Fim da linha.
			break
		if vertice == fim: # Podemos sair mais cedo.
			break

	custo = custosVertices[fim]
	menorCaminho = resumeCaminho(fim, verticesAnteriores)

	return custo, menorCaminho

# Retorna caminho e custo para todos as duplas.
def achaSolucoesParaAsDuplas(pares, listaAdj):
	solucoes = {}

	for par in pares:
		custo, caminho = achaCusto(par, listaAdj)
		solucoes[par] = (custo, caminho)
		# Tambem guarda o par reverso.
		solucoes[par[::-1]] = (custo, caminho[::-1])

	return solucoes

# Gera conjuntos de pares unicos de vertices de grau impar.
def duplasUnicas(items):
	for item in items[1:]:
		par = items[0], item
		restos = [a for a in items if a not in par]
		if restos:
			for fim in duplasUnicas(restos):
				yield [par] + fim
		else:
			yield [par]

# Retorna o menor custo & caminho para todos os conjuntos de duplas.
def achaMinimo(conjuntos, solucoes):
	maisBarato = None
	custoMin = float('inf')
	caminhoMin = []

	for conjunto in conjuntos:
		custoConjunto = sum(solucoes[par][0] for par in conjunto)
		if custoConjunto < custoMin:
			maisBarato = conjunto
			custoMin = custoConjunto
			caminhoMin = [solucoes[par][1] for par in conjunto]

	return maisBarato, caminhoMin



def acharArestaCaminho(listaAdj , caminho):

	 arestaCaminho = []

	 i = 0
	 while i+1 < len(caminho):
	 	for j in range(0, len(listaAdj[caminho[i]])):
	 		if listaAdj[caminho[i]][j][0] ==  caminho[i+1]:
	 			arestaCaminho.append([listaAdj[caminho[i]][j], caminho[i]])


	 	i = i+1

	 return arestaCaminho





def main():
	start = time.time()
	grafo = lerGrafo()
	print(grafo, '\n')
	listaAdj = listAdjacencia(grafo)
	#print("VerificaGrafoEuleriano(listAdj):", verificaGrafoEuleriano(listAdj))

	#print(grafo)
	#print(listAdj)
	#cicloEuler = acharEulerCiclo(listaAdj)

	#print("Caminho: ", euLerianoGrafo(listaAdj))
	arestas = acharFinsDeLinha(listaAdj)
	print("Vertices sozinhos: ", arestas)
	for i in arestas:
		adicionaAresta(listaAdj, i)

	#adicionaAresta(listaAdj, arestas[1])
	impares = retornaImpares(listaAdj)

	print("Grafo final: ", listaAdj)
	combinacoes = constroiDuplas(listaAdj)
	print("Combinacoes: ", combinacoes)
	print("Custo total: ", achaCustoTotal(listaAdj))
	print("Arestas possiveis para o vertice 1: ", opcoesDeAresta(listaAdj, 1))
	solucaoDuplas = achaSolucoesParaAsDuplas(combinacoes, listaAdj)

	print("Custos e caminhos: ", solucaoDuplas)
	print("Vertices impares: ", impares)
	conjuntosDeDuplas = []
	for item in duplasUnicas(impares):
		conjuntosDeDuplas.append(item)

	print("Duplas unicas: ", conjuntosDeDuplas)

	# BASTA CHAMAR ACHA MINIMO E DEPOIS ADICIONAR AS ARESTAS NO GRAFO, PARA
	# QUE ELE SE TRANSFORME EM UM GRAFO EULERIANO, ENTAO SO ACHAR O CAMINHO.
	achaMin = achaMinimo(conjuntosDeDuplas, solucaoDuplas)
	print("Caminhos: ", achaMin)


	for i in achaMin[1]:
		for j in acharArestaCaminho(listaAdj, i):
			adicionaAresta(listaAdj, j)

	print("Grafo Euleriano: ", listaAdj)

	#####################################



	print("Ciclo Euleriano", acharEulerCiclo(listaAdj))

	end = time.time()
	print(end - start)

main()
