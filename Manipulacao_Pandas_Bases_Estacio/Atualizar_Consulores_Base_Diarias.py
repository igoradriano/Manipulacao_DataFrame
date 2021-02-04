# -*- coding: utf-8 -*-
import pandas as pd

"""# FUNÇÃO UPPER"""

def upper(df, col):
  return df.assign(**{col : df[col].str.upper()})
  #Recebe o nome do dataframe e o nome da coluna do dataframe

df_consultor1 = pd.read_excel('consultor1.xlsx',sheet_name = 0, skiprows = 0)
df_consultor2 = pd.read_excel('consultor2.xlsx',sheet_name = 0, skiprows = 0)
df_consultor3 = pd.read_excel('consultor3.xlsx',sheet_name = 0, skiprows = 0)
df_consultor4 = pd.read_excel('consultor4.xlsx',sheet_name = 0, skiprows = 0)
df_consultor5 = pd.read_excel('consultor5.xlsx',sheet_name = 0, skiprows = 0)
df_consultor6 = pd.read_excel('consultor6.xlsx',sheet_name = 0, skiprows = 0)
df_consultor7 = pd.read_excel('consultor7.xlsx',sheet_name = 0, skiprows = 0)

df_desistentes = pd.read_excel('desistentes.xlsx',sheet_name = 0, skiprows = 0)

df_classificados1 = pd.read_excel('classificados.xlsx',sheet_name = 0, skiprows = 0)
df_classificados2 = pd.read_excel('classificados.xlsx',sheet_name = 1, skiprows = 0)
df_classificados3 = pd.read_excel('classificados.xlsx',sheet_name = 2, skiprows = 0)

df_financeiras1 = pd.read_excel('financeiras.xlsx',sheet_name = 0, skiprows = 0)
df_financeiras2 = pd.read_excel('financeiras.xlsx',sheet_name = 1, skiprows = 0)
df_financeiras3 = pd.read_excel('financeiras.xlsx',sheet_name = 2, skiprows = 0)

df_te = pd.read_excel('te.xlsx',sheet_name = 0, skiprows = 0)

df_academicas = pd.read_excel('academicas.xlsx',sheet_name = 0, skiprows = 0)

"""# Concatenando Tabelas

"""

df_consultores = pd.concat([df_consultor1,df_consultor2,df_consultor3,df_consultor4,df_consultor5,df_consultor6,df_consultor7])

df_basegeral = pd.concat([df_classificados1,df_classificados2,df_classificados3,df_financeiras1,df_financeiras2,df_financeiras3,df_te,df_desistentes,df_academicas])

"""# USANDO FUNÇÃO CRIADA NO INICIO (UPPER)"""

df_basegeral = upper(df_basegeral, "NOME")
df_consultores = upper(df_consultores, "Nome")

"""# Excluindo Colunas"""

df_consultores = df_consultores.rename(columns={'Nome':'NOME','Matrícula':'MATRICULA','Número Inscrição':'INSC.INIT','Número Candidato':'INSCRICAO','Forma de Ingresso':'FDI','Data Classificado':'DT_CLASS','Data Financeiro':'DT_FIN','Data da Prova':'DT_PROVA','Data Acadêmico':'DT_ACAD'})

df_consultores = df_consultores[['Consultor','MATRICULA','NOME','INSC.INIT','INSCRICAO','CPF','Celular','Curso','Unidade','Modalidade','FDI','DT_CLASS','DT_FIN','DT_ACAD','DT_PROVA']].copy()

df_consultores = df_consultores.reset_index(drop=True)

"""# Substituindo os Nomes """

df_consultores['Consultor'].replace(
    to_replace=['KARLA CORTEZ RODRIGUES'],
    value='KARLA',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['PEDRO CHAVES DE AZEVEDO JUNIOR'],
    value='PEDRO',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['KELY ALBERTO SIMONETE DOS SANTOS MONTEIRO'],
    value='ALBERTO',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['SKARLATH DA SILVEIRA'],
    value='SKARLATH',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['IRISMAR PEDROSA DA SILVA'],
    value='IRIS',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['WENDSON BARRETO RESZENDE DA SILVA'],
    value='WENDSON',
    inplace=True
)

df_consultores['Consultor'].replace(
    to_replace=['Thiago Freire de Araújo'],
    value='THIAGO',
    inplace=True
)

df_fdv = df_consultores[['Consultor','NOME','INSCRICAO']].copy()
#Atribuindo a filtragem apenas do Consultor e Nome do candidato para df_fdv

"""# CRUZANDO DADOS"""

df_basegeral = pd.merge(df_basegeral,df_fdv, on =['NOME'], how='left')
df_basegeral = df_basegeral.rename(columns={'INSCRICAO_x':"INSCRICAO"})

df_basegeral = pd.merge(df_basegeral,df_fdv, on =['INSCRICAO'], how='left')

df_basegeral['Consultor_x'] = df_basegeral['Consultor_x'].astype(str)
df_basegeral['Consultor_y'] = df_basegeral['Consultor_y'].astype(str)
df_basegeral['Consultor_y'] = df_basegeral['Consultor_y'].fillna(" ") #Ele ira colocar ' ' no lugar dos NAN.
df_basegeral['Consultor_x'] = df_basegeral['Consultor_x'].fillna(" ") #Ele ira colocar ' ' no lugar dos NAN.
def FiltrarBase(coluna1,coluna2):
  if (coluna1 != " "):
    #if (coluna2 == " "):
    return coluna1
    #else:
      #return coluna2
  elif (coluna2 != " "):
    return coluna2
  else:
    return 0
df_basegeral['Consultor'] = df_basegeral.apply(lambda row: FiltrarBase(row['Consultor_x'], row['Consultor_y']),axis='columns')
df_basegeral['Consultor'].replace(
    to_replace=['nan'],
    value='',
    inplace=True
)

df_basegeral = df_basegeral.drop(['CONSULTOR',"Consultor_x","INSCRICAO_y","Consultor_y","NOME_y"], axis = 'columns')

#df_basegeral = df_basegeral.drop(['Unnamed: 0'], axis = 'columns')

df_basegeral = df_basegeral[['FORMA_INGRESSO','SEMESTRE','CAMPUS','CURSO','TURNO','INSCRICAO','DT_APURACAO','NOME_x','SITUACAO','DT_PAGAMENTO','DDD','TELEFONE','ddd','CELULAR','MATRICULA_FINANCEIRA','ENTREGOU_DOCUMENTACAO','OBS','ATENDENTE','Consultor','WHATSAPP']].copy()

df_basegeral = df_basegeral.rename(columns={'Consultor':'CONSULTOR'})
df_basegeral = df_basegeral.rename(columns={'NOME_x':'NOME'})

"""# MODIFICANDO TIPO DE COLUNA"""

df_basegeral['SEMESTRE']= df_basegeral['SEMESTRE'].astype(str)
df_basegeral['NOME']= df_basegeral['NOME'].astype(str)

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

"""## CRIANDO ABAS"""

df_classificados1 = df_classificadoss.loc[df_classificadoss['SEMESTRE'].isin(['2020.4 EAD','2021.1 EAD'])] 
df_classificados2 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1 - F'] 
df_classificados3 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1']

df_financeiras1 = df_financeirass.loc[df_financeirass['SEMESTRE'].isin(['2020.4 EAD','2021.1 EAD'])] 
df_financeiras2 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1 - F'] 
df_financeiras3 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1']

classificados = pd.ExcelWriter('classificadosA.xlsx')
df_classificados1.to_excel(classificados, sheet_name = 'EAD',index=False)
df_classificados2.to_excel(classificados, sheet_name = 'FLEX',index=False)
df_classificados3.to_excel(classificados, sheet_name = 'PRESENCIAL',index=False)
classificados.save()

financeiras = pd.ExcelWriter('financeirasA.xlsx')
df_financeiras1.to_excel(financeiras, sheet_name = 'EAD',index=False)
df_financeiras2.to_excel(financeiras, sheet_name = 'FLEX',index=False)
df_financeiras3.to_excel(financeiras, sheet_name = 'PRESENCIAL',index=False)
financeiras.save()

desistentes = pd.ExcelWriter('desistentesA.xlsx')
df_desistentes.to_excel(desistentes, sheet_name = 'desistentes',index=False)
desistentes.save()

te = pd.ExcelWriter('teA.xlsx')
df_te.to_excel(te, sheet_name = 'te',index=False)
te.save()

consultoresgeral = pd.ExcelWriter('consultoresGeral.xlsx')
df_consultores.to_excel(consultoresgeral, sheet_name = 'consultores',index=False)
consultoresgeral.save()
