import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

# Listas de bairros para cada grupo, grupo recebe 1 se o bairro estiver no grupo, caso contrário, recebe 0.
bairros_grupo1 = ['Auxiliadora', 'Bela Vista', 'Boa Vista', 'Central Park', 'Higienopolis', 'Jardim Botanico', 'Jardim Europa', 'Menino Deus', 'Moinhos de Vento', 'Passo da Areia', 'Petropolis', 'Rio Branco', 'Santana', 'Tres Figueiras']
bairros_grupo2 = ['Azenha', 'Bom Fim', 'Centro Historico', 'Cidade Baixa', 'Farroupilha', 'Floresta', 'Independencia', 'Praia de Belas']
bairros_grupo3 = ['Agronomia', 'Jardim do Salso', 'Partenon', 'Vila Jardim']
bairros_grupo4 = ['Alto Petropolis', 'Chacara das Pedras', 'Cristo Redentor', 'Ecoville', 'Humaita', 'Jardim Floresta', 'Jardim Ipiranga', 'Jardim Itu Sabara', 'Jardim Leopoldina', 'Jardim Lindoia', 'Jardim Planalto', 'Navegantes', 'Sao Geraldo', 'Sarandi', 'Vila Ipiranga']
bairros_grupo5 = ['Campo Novo', 'Cavalhada', 'Cristal', 'Espirito Santo', 'Gloria', 'Hipica', 'Ipanema', 'Lami', 'Medianeira', 'Nonoai', 'Restinga', 'Teresopolis', 'Terra Ville', 'Tristeza', 'Vila Assuncao', 'Vila Nova']

def obter_valor_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print('Por favor, insira um valor válido.')

def obter_valor_binario(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in (0, 1):
                return valor
            else:
                print('Por favor, insira um valor válido (1 para Sim, 0 para não.')
        except ValueError:
            print('Por favor, insira um valor válido (1 para Sim, 0 para não.')

def obter_valor_int(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print('Por favor, insira um valor válido.')

def obter_caracteristicas(): # Função para obter a entrada do usuário com as características do imóvel
    vcond = obter_valor_float('Qual é valor do condomínio? ')
    viptu = obter_valor_float('Qual é valor do IPTU (Valor mensal)? ')
    area = obter_valor_float('Qual é a área interna do imóvel (m²)? ')
    andar = obter_valor_int('Qual é o andar? ')
    qdormit = obter_valor_int('Quantos quartos? ')
    qbanheiro = obter_valor_int('Quantos banheiros? ')
    bairro = input('Qual é o bairro? ')

    grupo1 = 1 if bairro in bairros_grupo1 else 0
    grupo2 = 1 if bairro in bairros_grupo2 else 0
    grupo3 = 1 if bairro in bairros_grupo3 else 0
    grupo4 = 1 if bairro in bairros_grupo4 else 0
    grupo5 = 1 if bairro in bairros_grupo5 else 0

    tipo_imovel = input('Qual é o tipo de imóvel? (Apartamento, Casa em Condominio, Casa Residencial/Sobrado, Cobertura, Kitnet/JK/Studio, Loft/Flat) ')

    apartamento = 1 if tipo_imovel == 'Apartamento' else 0
    casasobrado = 1 if tipo_imovel == 'Casa Residencial/Sobrado' else 0
    cobertura = 1 if tipo_imovel == 'Cobertura' else 0
    kt_jk_studio = 1 if tipo_imovel == 'Kitnet/JK/Studio' else 0
    loft_flat = 1 if tipo_imovel == 'Loft/Flat' else 0
    casacondom = 1 if tipo_imovel == 'Casa em Condominio' else 0

    return {
        'ValorCondominio': [vcond],
        'ValorIptu': [viptu],
        'AreaInterna': [area],
        'Andar': [andar],
        'NumeroQuarto': [qdormit],
        'NumeroBanheiro': [qbanheiro],
        'grupo1': [grupo1],
        'grupo2': [grupo2],
        'grupo3': [grupo3],
        'grupo4': [grupo4],
        'grupo5': [grupo5],
        'apartamento': [apartamento],
        'casasobrado': [casasobrado],
        'cobertura': [cobertura],
        'kt_jk_studio': [kt_jk_studio],
        'loft_flat': [loft_flat],
        'casacondom': [casacondom]
    }

def treinar_regressor(X_treino, y_treino): # Função para treinar o modelo à partir do dataset devidamente preparado
    regressor = LinearRegression()
    regressor.fit(X_treino, y_treino)
    return regressor

def main(): #Função principal para interação do usuário e previsão de aluguel
    # Importar dataset para treino
    dataset = pd.read_excel(r"C:\Users\vinim\source\repos\calculadora\dataset.xlsx", engine='openpyxl')

    # Separar os dados treino e teste do modelo
    X = dataset.iloc[:, 3:20]
    y = dataset.iloc[:, 2]
    X_treino, _, y_treino, _ = train_test_split(X, y, test_size=0.3, random_state=42)

    # Treinar o regressor uma vez
    regressor = treinar_regressor(X_treino, y_treino)

    while True:
        caracteristicas = obter_caracteristicas()
        df = pd.DataFrame(data=caracteristicas)
        y_predito = regressor.predict(df)
        print(f'O valor ideal para aluguel do seu imóvel é {round(y_predito[0], 2)}')

        continuar = input('Digite "0" para continuar ou "1" para sair: ')
        if continuar == '1':
            break

    print('Tchau!')

if __name__ == "__main__":
    main()