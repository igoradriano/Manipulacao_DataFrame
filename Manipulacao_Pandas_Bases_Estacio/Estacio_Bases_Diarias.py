# -*- coding: utf-8 -*-

import pandas as pd
#Importando a biblioteca pandas

"""# FUNÇÃO UPPER E ASSIGN"""

def upper(df, col):
  return df.assign(**{col : df[col].str.upper()})
  #Recebe o nome do dataframe e o nome da coluna do dataframe

"""# LEITURA DE ARQUIVOS"""

df_basegeral1 = pd.read_excel('base1.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral2 = pd.read_excel('base2.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral3 = pd.read_excel('base3.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral4 = pd.read_excel('base4.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral5 = pd.read_excel('base5.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral6 = pd.read_excel('base6.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral7 = pd.read_excel('base7.xlsx',sheet_name = 0, skiprows = 0)
df_basegeral8 = pd.read_excel('base8.xlsx',sheet_name = 0, skiprows = 0)
#Imputando Bases do SIA - 2021.1;2020.4 EAD; 2021.1 EAD e 2021.1- F

df_ontem_desistentes = pd.read_excel('ontem-desistentes.xlsx',sheet_name = 0, skiprows = 0)
df_ontem_classificados1 = pd.read_excel('ontem-classificados.xlsx',sheet_name = 0, skiprows = 0)
df_ontem_classificados2 = pd.read_excel('ontem-classificados.xlsx',sheet_name = 1, skiprows = 0)
df_ontem_classificados3 = pd.read_excel('ontem-classificados.xlsx',sheet_name = 2, skiprows = 0)
#Imputando Base de Classificados sem Financeira do dia anterior

df_ontem_financeiras1 = pd.read_excel('ontem-financeiras.xlsx',sheet_name = 0, skiprows = 0)
df_ontem_financeiras2 = pd.read_excel('ontem-financeiras.xlsx',sheet_name = 1, skiprows = 0)
df_ontem_financeiras3 = pd.read_excel('ontem-financeiras.xlsx',sheet_name = 2, skiprows = 0)
#Imputando Base de Financeiras sem Acadêmicas do dia anterior

df_ontem_te = pd.read_excel('ontem-te.xlsx',sheet_name = 0, skiprows = 0)
#Imputando Base de TE do dia anterior

"""# TRATAMENTO DE DADOS

## CONCATENANDO TABELAS
"""

df_basegeral = pd.concat([df_basegeral1,df_basegeral2,df_basegeral3,df_basegeral4,df_basegeral5,df_basegeral6,df_basegeral7,df_basegeral8])
#Unindo todas as tabelas das bases do dia de hoje

df_baseontem = pd.concat([df_ontem_desistentes,df_ontem_te,df_ontem_classificados1,df_ontem_classificados2,df_ontem_classificados3,df_ontem_financeiras1,df_ontem_financeiras2,df_ontem_financeiras3])
#Unindo todas as tabelas das bases do dia de ontem

"""## USANDO A FUNÇÃO CRIADA"""

df_basegeral = upper(df_basegeral, "NOME")
df_baseontem = upper(df_baseontem, "NOME")
#Tornando toda a coluna nome em letras maiúsculas, através da função  upper criada no início do código

"""## RENOMEANDO COLUNAS

"""

df_basegeral = df_basegeral.rename(columns={'DDD_TELEFONE':'DDD','DDD_CELULAR':'ddd'})

"""## APAGANDO COLUNAS"""

df_basegeral = df_basegeral[['FORMA_INGRESSO','SEMESTRE','CAMPUS','CURSO','TURNO','INSCRICAO','DT_APURACAO','NOME','SITUACAO','DT_PAGAMENTO','DDD','TELEFONE','ddd','CELULAR','MATRICULA_FINANCEIRA','ENTREGOU_DOCUMENTACAO']].copy()
df_baseontem = df_baseontem[['INSCRICAO','OBS','ATENDENTE','CONSULTOR','WHATSAPP']].copy()
df_onteminter = df_baseontem                #Criando uma cópia dessa instância da Base Ontem

"""## ALTERANDO TIPO DE COLUNAS"""

df_basegeral.dtypes

df_baseontem.dtypes

df_basegeral[['DDD','TELEFONE','ddd','CELULAR']]= df_basegeral[['DDD','TELEFONE','ddd','CELULAR']].fillna(0).astype(int)
#Modificando tipo das colunas "DDD, TELEFONE, ddd e CELULAR" para inteiro e tornando as linhas vazias com valor nulo.

df_basegeral['SEMESTRE']= df_basegeral['SEMESTRE'].astype(str)
#Modificando tipo da coluna semestre para string, pois algumas linhas de presencial(2021.1) são consideradas float

"""# FILTRANDO COLUNAS

"""

df_basegeral = df_basegeral.loc[df_basegeral['CAMPUS'].isin(['CONSTANTINO NERY','EAD MANAUS - SÃO JOSÉ I - AM','EAD MANAUS - CENTRO - AM','EAD MANAUS - CIDADE NOVA II - AM','EAD MANAUS - PARQUE 10 DE NOVEMBRO - AM','EAD MANAUS - PLANALTO - AM','EAD MANAUS - TIRADENTES - AM','EAD CONSTANTINO NERY - AM','EAD ITACOATIARA - AM','EAD IRANDUBA - CENTRO - AM','EAD MANACAPURU - AM'])].copy()
#Filtrando na coluna "CAMPUS" apenas os campus do núcleo Manaus.

"""# CORRELACIONANDO DADOS - MERGE - similar ao PROCV

"""

df_basegeral = pd.merge(df_basegeral,df_baseontem, on =['INSCRICAO'], how='left')
#Unindo basegeral com basegeral ontem, através da inscrição do candidata, para adicionar colunas com informações do dia anterior

df_acad = df_basegeral.loc[df_basegeral['SITUACAO']=='Matriculado']
#Filtrando coluna situação da basegeral, apenas com linhas de matriculados e atribuindo essa tabela filtrada a variável df_acad

df_basegeralinter = df_basegeral
#Criando uma cópia dessa instancia da basegeral e atribuindo ao df_basegeralinter

df_desistentes = df_basegeral.loc[df_basegeral['SITUACAO']=='DESISTENTE / NÃO FORMOU TURMA']
#Filtrando a coluna "Situação" com valores de "desistente/não formou turma" da basegeral e atribundo a variável df_desistentes

df_baseaprovados = df_basegeral.loc[df_basegeral['SITUACAO'].isin(['Aprovado Classificado','Aprovado'])]
#Filtrando a coluna "Situação" com valores de "Aprovado Classificado e Aprovado" da basegeral e atribuindo a variável df_baseaprovados

df_te = df_baseaprovados.loc[df_baseaprovados['FORMA_INGRESSO']=='TRANSF. EXTERNA']
df_te = df_te.loc[df_te['SEMESTRE']=='2021.1 EAD']
#Filtrando a coluna "Forma Ingresso" os valores "Transf. Externa" da baseaprovados e atribuindo a variável df_te

df_classificados = df_baseaprovados.loc[df_baseaprovados['MATRICULA_FINANCEIRA']=='NAO']
#Filtrando a coluna "Matricula_FInanciera" os valores "NAO" da basegeral e atribuindo a variável df_classificados. Neste caso quero apenas os classificados sem financeiras

df_financeiras = df_baseaprovados.loc[df_baseaprovados['MATRICULA_FINANCEIRA']=='SIM']
#Filtrando a coluna "Matricula_FInanciera" os valores "SIM" da basegeral e atribuindo a variável df_financeiras. Neste caso quero apenas as Financeiras sem academicas.

"""# REMOVENDO DUPLICADOS"""

df_classificados = df_classificados.drop_duplicates(subset='NOME', keep='first')
df_classificadoss = df_classificados.loc[df_classificados['FORMA_INGRESSO'].isin(['MSV - Externa','Vestibular'])] 
df_financeiras = df_financeiras.drop_duplicates(subset='NOME', keep='first')
df_financeirass = df_financeiras.loc[df_financeiras['FORMA_INGRESSO'].isin(['MSV - Externa','Vestibular'])] 
#Removendo os duplicados de cada base filtrada e gerada na etapa anterior. Mantendo o primeiro valor encontrado.

"""# DIVIDINDO ABAS"""

df_classificados1 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1 EAD']
df_classificados2 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1 - F'] 
df_classificados3 = df_classificadoss.loc[df_classificadoss['SEMESTRE']=='2021.1'] 
#Divisão das abas da base de classsificados

df_financeiras1 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1 EAD']
df_financeiras2 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1 - F'] 
df_financeiras3 = df_financeirass.loc[df_financeirass['SEMESTRE']=='2021.1'] 
#Divisão das abas da base de Financeiras

"""# OUTPUT DE DADOS"""

classificados = pd.ExcelWriter('classificados.xlsx')
df_classificados1.to_excel(classificados, sheet_name = 'EAD',index=False)
df_classificados2.to_excel(classificados, sheet_name = 'FLEX',index=False)
df_classificados3.to_excel(classificados, sheet_name = 'PRESENCIAL',index=False)
classificados.save()

financeiras = pd.ExcelWriter('financeiras.xlsx')
df_financeiras1.to_excel(financeiras, sheet_name = 'EAD',index=False)
df_financeiras2.to_excel(financeiras, sheet_name = 'FLEX',index=False)
df_financeiras3.to_excel(financeiras, sheet_name = 'PRESENCIAL',index=False)
financeiras.save()

desistentes = pd.ExcelWriter('desistentes.xlsx')
df_desistentes.to_excel(desistentes, sheet_name = 'desistentes',index=False)
desistentes.save()

te = pd.ExcelWriter('te.xlsx')
df_te.to_excel(te, sheet_name = 'te',index=False)
te.save()

#onteminter = pd.ExcelWriter('onteminter.xlsx')
#df_onteminter.to_excel(onteminter, sheet_name = 'onteminter',index=False)
#onteminter.save()

geralinter = pd.ExcelWriter('geralinter.xlsx')
df_basegeralinter.to_excel(geralinter, sheet_name = 'geralinter',index=False)
geralinter.save()

acad = pd.ExcelWriter('academicas.xlsx')
df_acad.to_excel(acad, sheet_name = 'academicas',index=False)
acad.save()

"""# Relatórios"""

serie = pd.Series(df_basegeralinter["SITUACAO"])
serie.value_counts()
