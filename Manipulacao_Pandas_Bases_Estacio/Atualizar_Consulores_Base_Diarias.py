# -*- coding: utf-8 -*-
"""
# IMPORTANDO AS BIBLIOTECAS
"""

import pandas as pd
import gc #--> Limpar memoria
from datetime import date, datetime
from pytz import timezone
fuso_horario = timezone('America/Sao_Paulo')
data_e_hora_Manaus = datetime.today().astimezone(fuso_horario)

"""# 0. INPUTS DO USUÁRIO

## 0.1 Qual caminho principal percorrer no código:
"""

caminho = int(input("""Digite uma das opções abaixo para qual tipo de dados você quer trabalhar:
Digite 1 para Relatórios Analíticos
Digite 2 para Gerar Bases Diárias sem atualização dos Consultores
Digite 3 para Atualizar Bases Diárias com base de Consultores
Digite sua Resposta: """))
while (caminho >3 or caminho<1):
  caminho = int(input("""Digite uma das opções abaixo para qual tipo de dados você quer trabalhar:
Digite 1 para Relatórios Analíticos
Digite 2 para Gerar Bases Diárias sem atualização dos Consultores
Digite 3 para Atualizar Bases Diárias com base de Consultores
Digite sua Resposta: """))

"""## 0.2. Número de Base de Consultores para Importar"""

n_consultores = int(input('Digite o número de Consultores que irá atualizar as Bases: '))
while (n_consultores > 7 or n_consultores < 1):
  print("Digite um número de 1 a 7")
  n_consultores = int(input('Digite o número de Consultores que irá atualizar as Bases: '))

"""## 0.3. Maneira que vai importar a Base Geral

"""

tipo_baseGeral = int(input("""Digite uma das opções abaixo para importação da Base Geral:
Digite 1 para inserir Base Geral Única
Digite 2 para inserir 2 ou mais bases)
Digite sua Resposta: """))
while (tipo_baseGeral not in [1,2]):
  tipo_baseGeral = int(input("""Digite uma Resposta válida!, suas opções são:
Digite 1 para inserir Base Geral Única
Digite 2 para inserir 2 ou mais bases)
Digite sua Resposta: """))

"""# 1. CRIANDO FUNÇÕES

##1.1. Função upper
Serve Para tornar todos os elementos de uma coluna MAIÚSCULOS.
"""

def upper(df, col):
  return df.assign(**{col : df[col].str.upper()})
  #Recebe o nome do dataframe e o nome da coluna do dataframe

"""## 1.2. Função FiltrarBase
Serve para verificar as linhas da coluna1 ("CONSULTOR_x") da base geral, criada no merge para verificar pelo nome do candidato, quais desses candidatos pertecem a qual consultor ( da base geral de consultores). 
E também para fazer a mesma coisa com a coluna2 ("CONSULTOR_y") que foi criada através do merge para verificar pelo número de candidato ("INSCRICAO) quais desses candidatos pertecem a qual consultor.
"""

def FiltrarBase(coluna1,coluna2):
  if (coluna1 != " "):      #verifica se os itens da coluna1 são diferentes de " ", sendo diferente retorna o proprio valor da coluna1, se igual a " " vai para o próximo if
    #if (coluna2 == " "): #linha opcional
    return coluna1
    #else:                #linha opcional
      #return coluna2      #linha opcional
  elif (coluna2 != " "):    #veridica se os itens da coluna2 são diferentes de " ", sendo diferente retorna o prorpio valor da coluna2 se igual a " " vai para o else
    return coluna2
  else:                     #caso nehuma das condições anteriores sejam atendidas, retorna 0
    return 0

"""# 2. IMPORTANDO DADOS

## 2.1. Importando Bases de Dados dos Consultores
"""

for n in range(n_consultores):
  try:
    globals()['df_Consultor' + str(n+1)] = pd.read_excel(f'consultor{n+1}.xlsx',sheet_name = 0, skiprows = 0)
  except:
    print('Nenhum arquivo encontrado')
  else:
    print(f'Arquivo de Consultor{n+1} carregado')

"""## 2.2. Importando Base de Dados Geral do SIA"""

lista = ['academicas','financeiras','classificados','te','desistentes']
i=0
if tipo_baseGeral == 1:
  df_basegeral = pd.read_excel(f'{date.today().strftime("%d.%m.%Y")}-basegeral.xlsx',sheet_name = 0, skiprows = 0)
if tipo_baseGeral == 2:
  for n in (lista):
    try:
      if n in ['financeiras','classificados']: #Trata de criar variáveis globais para planilhas que tem 3 abas
        for g in range(3):
          globals()[f'df_{n}{g}'] = pd.read_excel(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-{n}.xlsx',sheet_name = g, skiprows = 0)
          i+=1
        #if n == "financeiras":
          #globals()[f'df_Inter{n}'] = pd.concat([df_financeiras0, df_financeiras1,df_financeiras2])
        #else:
          #globals()[f'df_Inter{n}'] = pd.concat([df_classificados0, df_classificados1,df_classificados2])
      else:  #Trata de criar variáveis globais para as planilhas que tem apenas uma aba
          globals()[f'df_{n}'] = pd.read_excel(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-{n}.xlsx',sheet_name = 0, skiprows = 0)
          i+=1
    except:
        print(f'A base {datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-{n} não existe!')
    else:
      if n in ['financeiras','classificados']:
        print(f'Todas as 3 Abas da base {datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-{n} foram registradas com sucesso!')
      else:
         print(f'A base {datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-{n} foi registrada com sucesso!')
  print(f'O total de bases registradas foram: {i}')

"""## 3. Concatenando Tabelas do SIA"""

df_basegeral= pd.DataFrame()
if 'df_academicas' in globals():
  df_basegeral = df_basegeral.append(df_academicas,ignore_index=True)
  print('O DataFrame df_basegeral foi concatenado')
if'df_financeiras0' in globals():
  df_basegeral = df_basegeral.append(df_financeiras0,ignore_index=True)
  print('O DataFrame df_financeira0 foi concatenado')
if'df_financeiras1' in globals():
  df_basegeral = df_basegeral.append(df_financeiras1,ignore_index=True)
  print('O DataFrame df_financeira1 foi concatenado')                 
if'df_financeiras2' in globals():
  df_basegeral = df_basegeral.append(df_financeiras2,ignore_index=True)
  print('O DataFrame df_financeira2 foi concatenado')
if'df_te' in globals():
  df_basegeral = df_basegeral.append(df_te,ignore_index=True)
  print('O DataFrame df_te foi concatenado')
if'df_desistentes' in globals():
  df_basegeral = df_basegeral.append(df_desistentes,ignore_index=True)
  print('O DataFrame df_desistentes foi concatenado')
if'df_classificados0' in globals():
  df_basegeral = df_basegeral.append(df_classificados0,ignore_index=True)
  print('O DataFrame df_classificados0 concatenado')
if'df_classificados1' in globals():
  df_basegeral = df_basegeral.append(df_classificados1,ignore_index=True)
  print('O DataFrame df_classificados1 foi concatenado')
if'df_classificados2' in globals():
  df_basegeral = df_basegeral.append(df_classificados2,ignore_index=True)
  print('O DataFrame df_classificados2 foi concatenado')

"""# CONCATENANDO TABELAS DE CONSULTORES"""

# Concatenando Tabelas dentro do condicional
if n_consultores ==1:
    df_Consultores = pd.concat([df_Consultor1])
elif n_consultores ==2:
    df_Consultores = pd.concat([df_Consultor1,df_Consultor2])
elif n_consultores ==3:
    df_Consultores = pd.concat([df_Consultor1,df_Consultor2,df_Consultor3])
elif n_consultores ==4:
    df_Consultores = pd.concat([df_Consultor1,df_Consultor2,df_Consultor3,df_Consultor4])
elif n_consultores ==5:
  df_Consultores = pd.concat([df_Consultor1,df_Consultor2,df_Consultor3,df_Consultor4,df_Consultor5])
elif n_consultores ==6:
  df_Consultores = pd.concat([df_Consultor1,df_Consultor2,df_Consultor3,df_Consultor4,df_Consultor5,df_Consultor6])
elif n_consultores ==7:
  df_Consultores = pd.concat([df_Consultor1,df_Consultor2,df_Consultor3,df_Consultor4,df_Consultor5,df_Consultor6,df_Consultor7])
else:
  print("Você não pode inserir mais que 7 dataframes")

"""# USANDO FUNÇÃO CRIADA (UPPER)"""

df_basegeral = upper(df_basegeral, "NOME")
df_Consultores = upper(df_Consultores, "Nome")
#FUNCAO PARA TORNAR TODAS AS LINHAS DA COLUNA NOME DA BASE GERAL E Nome DA BASE CONSULTORES MAIUSCULAS

"""# Excluindo Colunas"""

df_Consultores = df_Consultores.rename(columns={'Nome':'NOME','Matrícula':'MATRICULA','Número Inscrição':'INSC.INIT','Número Candidato':'INSCRICAO','Forma de Ingresso':'FDI','Data Classificado':'DT_CLASS','Data Financeiro':'DT_FIN','Data da Prova':'DT_PROVA','Data Acadêmico':'DT_ACAD'})
#Renomeando colunas

df_Consultores = df_Consultores[['Consultor','MATRICULA','NOME','INSC.INIT','INSCRICAO','Tipo de Plano de Ação','CPF','Celular','Curso','Unidade','Modalidade','FDI','DT_CLASS','DT_FIN','DT_ACAD','DT_PROVA']].copy()
#Excluindo as colunas que não interessam

"""# SUBSTITUINDO NOME DOS CONSULTORES DE TODAS AS LINHAS"""

df_Consultores['Consultor'].replace(
    to_replace=['KARLA CORTEZ RODRIGUES'],
    value='KARLA',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['PEDRO CHAVES DE AZEVEDO JUNIOR'],
    value='PEDRO',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['KELY ALBERTO SIMONETE DOS SANTOS MONTEIRO'],
    value='ALBERTO',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['SKARLATH DA SILVEIRA'],
    value='SKARLATH',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['IRISMAR PEDROSA DA SILVA'],
    value='IRIS',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['WENDSON BARRETO RESZENDE DA SILVA'],
    value='WENDSON',
    inplace=True
)

df_Consultores['Consultor'].replace(
    to_replace=['Thiago Freire de Araújo'],
    value='THIAGO',
    inplace=True
)

df_fdv = df_Consultores[['Consultor','NOME','INSCRICAO']].copy()
#Atribuindo a filtragem apenas do Consultor e Nome do candidato para df_fdv

"""# CRUZANDO DADOS"""

df_basegeral = pd.merge(df_basegeral,df_fdv, on =['NOME'], how='left')
df_basegeral = df_basegeral.rename(columns={'INSCRICAO_x':"INSCRICAO"})
#Esse primeiro merge serve para procurar os dados de uma base na outra levando como parâmetro o "NOME"
#Renomeando coluna "INSCRICAO", durante o merge essa coluna havia sido renomeada para "INSCRICAO_x"

df_basegeral = pd.merge(df_basegeral,df_fdv, on =['INSCRICAO'], how='left')
#Realizando um segundo merge para procurar os dados de uma base na outra levando como parâmetro a "INSCRICAO"
#Como tentativa de conseguir pegar o máximo de dados de uma tabela na outra

"""# MODIFICANDO TIPO DE COLUNA"""

df_basegeral['Consultor_x'] = df_basegeral['Consultor_x'].astype(str) #Transformamos a coluna "Consultor_x" em str. fazemos isso para que a funcao FiltrarBase possa ser usada
df_basegeral['Consultor_y'] = df_basegeral['Consultor_y'].astype(str) #Transformamos a coluna "Consultor_x" em str. fazemos isso para que a funcao FiltrarBase possa ser usada
df_basegeral['SEMESTRE']= df_basegeral['SEMESTRE'].astype(str) #Transformamos a coluna "SEMESTRE" em str. Fazemso isso pois algumas linhas são encaradas como inteiras (2021.1)
df_basegeral['NOME_x']= df_basegeral['NOME_x'].astype(str)
df_basegeral['Consultor_y'] = df_basegeral['Consultor_y'].fillna(" ") #Ele ira colocar ' ' no lugar dos NAN.
df_basegeral['Consultor_x'] = df_basegeral['Consultor_x'].fillna(" ") #Ele ira colocar ' ' no lugar dos NAN.

"""# UTILIZANDO FUNCAO CRIADA (FiltrarBase)"""

#Utilizamos o apply para aplicar internamente o lambda row, para que a funcao seja utlizada linha a linha.
df_basegeral['Consultor'] = df_basegeral.apply(lambda row: FiltrarBase(row['Consultor_x'], row['Consultor_y']),axis='columns')
df_basegeral['Consultor'].replace(   #depois renomeamos todos os 'nan' encontrados por ''.
    to_replace=['nan'],
    value='',
    inplace=True
)

df_basegeral = df_basegeral.drop(['CONSULTOR',"Consultor_x","INSCRICAO_y","Consultor_y","NOME_y"], axis = 'columns')

#df_basegeral = df_basegeral.drop(['Unnamed: 0'], axis = 'columns')

df_basegeral = df_basegeral[['FORMA_INGRESSO','SEMESTRE','CAMPUS','CURSO','TURNO','INSCRICAO','DT_APURACAO','NOME_x','SITUACAO','DT_PAGAMENTO','DDD','TELEFONE','ddd','CELULAR','MATRICULA_FINANCEIRA','ENTREGOU_DOCUMENTACAO','OBS','ATENDENTE','Consultor','WHATSAPP']].copy()

df_basegeral = df_basegeral.rename(columns={'Consultor':'CONSULTOR'})
df_basegeral = df_basegeral.rename(columns={'NOME_x':'NOME'})

df_BaseGeral = df_basegeral

"""# DIVISAO DAS BASES

"""

df_desistentes = df_basegeral.loc[df_basegeral['SITUACAO']=='DESISTENTE / NÃO FORMOU TURMA']

df_baseaprovados = df_basegeral.loc[df_basegeral['SITUACAO'].isin(['Aprovado Classificado','Aprovado'])]

df_te = df_baseaprovados.loc[df_baseaprovados['FORMA_INGRESSO']=='TRANSF. EXTERNA']

df_classificados = df_baseaprovados.loc[df_baseaprovados['MATRICULA_FINANCEIRA']=='NAO']

df_financeiras = df_baseaprovados.loc[df_baseaprovados['MATRICULA_FINANCEIRA']=='SIM']

df_classificadoss = df_classificados.loc[df_classificados['FORMA_INGRESSO'].isin(['MSV - Externa','Vestibular'])]

df_financeirass = df_financeiras.loc[df_financeiras['FORMA_INGRESSO'].isin(['MSV - Externa','Vestibular'])]

"""# RETIRANDO DUPLICADOS"""

df_classificadoss = df_classificadoss.drop_duplicates(subset='NOME', keep='first')
df_financeirass = df_financeirass.drop_duplicates(subset='NOME', keep='first')
df_te = df_te.drop_duplicates(subset='NOME', keep='first')
df_desistentes = df_desistentes.drop_duplicates(subset='NOME', keep='first')

"""# CRIANDO ABAS"""

df_classificados1 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1 EAD'] 
df_classificados2 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1 - F'] 
df_classificados3 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1'] 
df_classificados4 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2020.4 EAD']

df_financeiras1 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1 EAD']
df_financeiras2 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1 - F'] 
df_financeiras3 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1'] 
df_financeiras4 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2020.4 EAD']

"""# OUTPUT DADOS

### OUTPUT CLASSIFICADOS
"""

classificados = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-classificadosABC.xlsx')
df_classificados1.to_excel(classificados, sheet_name = 'EAD-2021.1',index=False)
df_classificados2.to_excel(classificados, sheet_name = 'FLEX',index=False)
df_classificados3.to_excel(classificados, sheet_name = 'PRESENCIAL',index=False)
df_classificados4.to_excel(classificados, sheet_name = 'EAD-2020.4',index=False)
df_classificadoss.to_excel(classificados, sheet_name = 'GERAL',index=False)
classificados.save()

"""### OUTPUT FINANCEIRAS"""

financeiras = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-financeirasABC.xlsx')
df_financeiras1.to_excel(financeiras, sheet_name = 'EAD-2021.1',index=False)
df_financeiras2.to_excel(financeiras, sheet_name = 'FLEX',index=False)
df_financeiras3.to_excel(financeiras, sheet_name = 'PRESENCIAL',index=False)
df_financeiras4.to_excel(financeiras, sheet_name = 'EAD-2020.4',index=False)
df_financeirass.to_excel(financeiras, sheet_name = 'GERAL',index=False)
financeiras.save()

"""### OUTPUT DESISTENTES"""

desistentes = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-desistentesABC.xlsx')
df_desistentes.to_excel(desistentes, sheet_name = 'desistentes',index=False)
desistentes.save()

"""### OUTPUT TRANFERÊCIA EXTERNA"""

te = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-teABC.xlsx')
df_te.to_excel(te, sheet_name = 'te',index=False)
te.save()

"""### OUTPUT BASE GERAL DE CONSULTORES"""

consultoresgeral = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-ConsultoresGeral.xlsx')
df_Consultores.to_excel(consultoresgeral, sheet_name = 'consultores',index=False)
consultoresgeral.save()

basegeral = pd.ExcelWriter(f'{datetime.today().astimezone(fuso_horario).strftime("%d.%m.%Y")}-BaseGeral.xlsx')
df_BaseGeral.to_excel(basegeral, sheet_name = 'geral',index=False)
basegeral.save()