Olá, estou de volta. Agora precisamos implementar algumas condições referente à variável "assinatura\_fechados" para o Parceiro Indique.

Devemos levar em consideração o tipo de plano para o cálculo que fazemos de acordo com o negócio. Se um dos negócios for "Plano 15%" o valor que deve ser apresentado no segundo gráfico referente a variavel "assintatura\_fechados" sendo 15% do valor da assinatura total e ele deve ser apresentado apenas no mês de Mar/2026. Se o plano daquele negócio for "Plano 20%" o valor para aquele negócio deve ser de 50% do valor total da assinatura também apenas no mês de Mar/2026 e se plano for "Plano 25%" o valor deve ser de 50% do valor total da assinatura em Mar/2026 e 50% do valor total da assinatura em Mar/2027. Resumindo:

Plano 15% = 15% do valor da assinatura em Mar/2026

Plano 20% = 50% do valor da assinatura em Mar/2026

Plano 25% = 50% do valor da assinatura em Mar/2026 e Mar/2027



========================================================================



Preciso que você faça o calculo de valor de assinatura por deal sendo que:



**valor assinatura = kWh Contratado \* 1,1150643 \* (1 - Plano)**



Preciso que essa equação seja calculada por deal fechado e armazenada em uma variável. Com isso feito preciso agora que no segundo gráfico seja apresentado o valor dessa assinatura com o seguinte efeito de acordo com o plano de cada deal:

Plano 15% = 15% do valor da assinatura em Mar/2026

Plano 20% = 50% do valor da assinatura em Mar/2026

Plano 25% = 50% do valor da assinatura em Mar/2026 e Mar/2027



Por exemplo, existe um cliente em que o resultado de assinatura de um de seus dois negócios foi de 1000, sendo que um de seus planos é "Plano 20%" e o outro é "Plano 25%". O gráfico a ser apresentado referente a essas informações é:



Mar/2026: 50%(Plano 25%) de 1000 = 500 + 50%(Plano 20%) de 1000 = 500

Mar/2027: 50%(Plano 25%) de 1000 = 500



Lembrando que esse parametro deve ser implementado apenas para Finders Indique e se refere ao segundo gráfico.



Agora preciso ajustar o parceiro Plus. Vamos levar com consideração as mesmas variáveis que usamos para estruturar a lógica o Indique, mas os parametros referente aos planos vai ser o seguinte:

Plano 15% = 25% do valor da assinatura em Abr/2026

Plano 85% = 85% do valor da assinatura em Abr/2026

Plano 25% = 85% do valor da assinatura em Abr/2026 e Abr/2027


**Lista de tipos de Finder**

00 - AT - 3R Renovável
00 - AT - Allvar Engenharia
00 - AT - América Energia
00 - AT - André Lins
00 - AT - Antônio Moreira
00 - AT - Assessoria Terra
00 - AT - Assis
00 - AT - Auto Paraná
00 - AT - Base Energia
00 - AT - Bruno Santos
00 - AT - Carlos Eduardo
00 - AT - Ceos Energia
00 - AT - Clarke
00 - AT - Claudio
00 - AT - Compesa
00 - AT - Confidence Energy
00 - AT - Dilson Manzoni
00 - AT - DL Industria
00 - AT - Douglas
00 - AT - Dupla Consultoria
00 - AT - E5 Solar
00 - AT - Eduardo Lima
00 - AT - Empório Energia
00 - AT - Energy Brasil (Thiago)
00 - AT - Enex
00 - AT - Engie
00 - AT - Fator Energy
00 - AT - Futtura Energia
00 - AT - Garth Harding
00 - AT - Gonçalves Melo
00 - AT - Hugo Gonçalves
00 - AT - Inter Energia (Marcos)
00 - AT - Jonas Santos
00 - AT - Leonardo
00 - AT - Leonardo Coimbra
00 - AT - Lucas Muller
00 - AT - Marcelo (XP)
00 - AT - Mariana Correia
00 - AT - Mariana Moraes
00 - AT - Matheus
00 - AT - Matheus Lage (CML)
00 - AT - McPar Engenharia
00 - AT - Merx
00 - AT - Minato Brasil
00 - AT - Mosair Timóteo
00 - AT - Ney Coelho
00 - AT - Nilmaer Souza
00 - AT - Origo Energia
00 - AT - Pacto Consultoria
00 - AT - Paulin Martins
00 - AT - Petronio Silva - Ceara
00 - AT - Pontes Consultoria
00 - AT - Priscila Moura
00 - AT - Protton
00 - AT - Real Gestão
00 - AT - Rediandro
00 - AT - Reduza Energia
00 - AT - Rodrigo Emídio
00 - AT - Roger Santos
00 - AT - Rota Solar
00 - AT - Sion
00 - AT - Smart Energia
00 - AT - Solener (J.Rubens)
00 - AT - Solver
00 - AT - Spirit
00 - AT - Thierry Volpi
00 - AT - Tradener
00 - AT - Trifase
00 - AT - Vando
00 - AT - Vargas Dias
00 - AT - Victor Hunka
00 - AT - Vinicius
00 - AT - Virgilio
01 - Interno - Barbara Araujo (ex-funcionário)
01 - Interno - David Barmak
01 - Interno - Dbios (ex-funcionário)
01 - Interno - GoData (ex-funcionário)
01 - Interno - Gustavo Lemos (ex-funcionário)
01 - Interno - Indicação dos sócios (Sem Finder)
01 - Interno - Jessica Silva
01 - Interno - Kido (ex-funcionário)
01 - Interno - Leandro Mantovani (ex-funcionário)
01 - Interno - Luciano Borges
01 - Interno - Luiz Baldner
01 - Interno - Mari Canuto (ex-funcionário)
01 - Interno - Nayara Pimenta (ex-funcionário)
01 - Interno - PaP - Antônio
01 - Interno - PaP - Denilson Conceição Ribeiro
01 - Interno - PaP - Diego Amaral Bispo
01 - Interno - PaP - Diogo Beirão
01 - Interno - PaP - Elivania Dias
01 - Interno - PaP - Felipe Viana Sousa
01 - Interno - PaP - Giovane Santos
01 - Interno - PaP - Leandro Santos Araujo
01 - Interno - PaP - Lyon
01 - Interno - PaP - Mikael Santos
01 - Interno - PaP - Roberto Leão
01 - Interno - PaP - Victor Hugo
01 - Interno - Priscila Mesquita (ex-funcionário)
01 - Interno - Sabrina Rodrigues (ex-funcionário)
01 - Interno - SDR Arianny Ferreira (ex-funcionário)
01 - Interno - SDR Gustavo Nogueira (ex-funcionário)
01 - Interno - SDR Luana Rodrigues (ex-funcionário)
01 - Interno - Valeria (ex-funcionário)
02 - Indique - AASA ASSOCIAÇÃO DOS AGENTES DE SAÚDE DO ESTADO DA BAHIA
02 - Indique - AS SERVICOS DE TECNOLOGIA LTDA (Adriano)
02 - Indique - BAHIA TACOGRAFO LTDA (Pablo Ricardo da Silva Leal)
02 - Indique - Cacai Leal
02 - Indique - CONECTFIBRA (Adriano)
02 - Indique - E-ELETRICA ENGENHARIA LTDA
02 - Indique - ELA Com. Representação Ltda
02 - Indique - ISISNET FIBER
02 - Indique - JAIR DE ALMEIDA SILVA (Jair)
02 - Indique - Jorge Bianchi
02 - Indique - JORGE BIANCHI (Jorge Bianchi)
02 - Indique - LUCIANO VIANA DOS SANTOS REPRESENTAÇÕES
02 - Indique - MAYCON DE JESUS SANTOS (VIRTUALNET)
02 - Indique - Michel Sleiman
02 - Indique - Milton Netomilto_Cond Princesa do Sertão FSA
02 - Indique - P J DOS SANTOS REPRESENTAÇÕES
02 - Indique - W3I CONECTE LTDA-ME (Ivanildo)
03 - Plus - EDUARDO PERES DA SILVA (Eduardo)
03 - Plus - Enerx - Viktor
03 - Plus - EPSOL ENERGIA SOLAR (Eduardo)
03 - Plus - LUIZ MEDRADO
03 - Plus - MONTTEREY (Bruno Ribeiro)
03 - Plus - Silvia Gentil
03 - Plus - Sirlene Macrosol
03 - Plus - Vanessa Adorno
03 - Plus - VIP AIR ADVISOR CONSULTORIA LTDA
04 - Gold - DSC E ALMEIDA PASSOS TAMBORES E METAIS LTDA (Denise)
04 - Gold - Eduardo Barbalho Cardoso
04 - Gold - Eduardo Reis
04 - Gold - Genildo SETEX (ACEFS)
04 - Gold - GF CAPITAL, INVESTIMENTOS E ASSESSORIA LTDA (Anderson Velloso)
04 - Gold - Ingrid e Lais (Ambiental) (Ingrid Abreu)
04 - Gold - JOSE VICTOR MEDEIROS CARNEIRO BRAGA
04 - Gold - JOSÉ VICTOR MEDEIROS CARNEIRO BRAGA
04 - Gold - Julio Cesar
04 - Gold - MARCUS VINICIUS LIMA LOBO (Marcus)
04 - Gold - MAURICIO (Mauricio Viana)
04 - Gold - MAURÍCIO VIANA
04 - Gold - Rafael Aguiar
04 - Gold - Roberto Pimentel
04 - Gold - Sindicato do Comércio de Feira de Santana (Marco Antonio Santana da Silva)
04 - Gold - TILSON FREIRE DA SILVA (Tilson)
04 - Gold - VANESSA MARQUES GONCALVES SERVICOS ADMINISTRATIVOS LTDA
05 - Exsat - LM SATELITE SERVICOS E REPRESENTACOES COMERCIAIS LTDA (Miguel)
06 - Parceiro Exsat - ACTEC - (Álvaro Rios)
06 - Parceiro Exsat - Ailton Barreto
06 - Parceiro Exsat - ALAN LEMOS
06 - Parceiro Exsat - ANIVALDO CERQUEIRA
06 - Parceiro Exsat - Antonio Fernandes Barros
06 - Parceiro Exsat - BILLTECH SEGURANCA ELETRONICA
06 - Parceiro Exsat - BONFIM TORQUATO COMERCIO (João Victor)
06 - Parceiro Exsat - Carine
06 - Parceiro Exsat - CLERIO ROCHA SOUSA (Clerio rocha sousa)
06 - Parceiro Exsat - DAIANE DAMASCENO DANTAS (Jairo Dantas)
06 - Parceiro Exsat - DSL SOLAR LTDA (Dalmo Ferreira Lopes)
06 - Parceiro Exsat - E JOVITA DOS SANTOS (Roberlan)
06 - Parceiro Exsat - ELISIO (PARCEIRO FORTE - ACOMPANHADO PELO LUIZ) (Elisio)
06 - Parceiro Exsat - ELMO SENA DE FREITAS
06 - Parceiro Exsat - EMBAVIG (Marcia Regina Pires de Sousa)
06 - Parceiro Exsat - EVANDRO VIEIRA OLIVEIRA (Evandro Vieira Oliveira)
06 - Parceiro Exsat - FC TELECOMUNICAÇÕES E SEGURANÇA ELETRONICA (FLÁVIO DA SILVA)
06 - Parceiro Exsat - FRANKLIN JOSE ALVES DE SOUZA (Franklin e Francis)
06 - Parceiro Exsat - GENTILTECH SEGURAÇÃO ELETRÔNICA
06 - Parceiro Exsat - Gilmar
06 - Parceiro Exsat - GM SEGURANÇA ELETRÔNICA (Gilson Almeida Santos)
06 - Parceiro Exsat - GUARDIANSEG
06 - Parceiro Exsat - GUARDIANTEC SEGURANÇA ELETRÔNICA
06 - Parceiro Exsat - HB SOLUCOES INSTALACOES INDUSTRIAIS LTDA (Herbert Silva)
06 - Parceiro Exsat - HELP SEGURANÇA ELETRÔNICA (Tiago)
06 - Parceiro Exsat - HELPTECH SERVIÇOS EM TI (Warley Lima Barbosa)
06 - Parceiro Exsat - J H ZORGETZ ENERGIA SOLAR E SEGURANCA ELETRONICA LIMITADA (João Hugo Pereira Zorgetz)
06 - Parceiro Exsat - J P O BARROS SERVIÇOS DE USINAGEM (Juan Pablo Oliveira Barros)
06 - Parceiro Exsat - JC CONSTRUÇÕES E REFORMAS LTDA (Jorge Rodrigues Santos)
06 - Parceiro Exsat - JIM SOLUCOES TECNOLOGICAS LTDA (Marivaldo)
06 - Parceiro Exsat - JOSE ANDERSON CAMPOS ARAUJO
06 - Parceiro Exsat - José Claudio Santos Silva
06 - Parceiro Exsat - JPL- Osvaldo
06 - Parceiro Exsat - JSD - Josiel
06 - Parceiro Exsat - JÚNIOR DE JESUS PINHEIRO
06 - Parceiro Exsat - KALIAN ANDRADE
06 - Parceiro Exsat - KALIANE ALVES ROCHA (Kaliane Alves Rocha)
06 - Parceiro Exsat - LAC CONSTRUTEC CONSTRUTORA LTDA (Luiz)
06 - Parceiro Exsat - LORENA AMARAL (Lorena Amaral)
06 - Parceiro Exsat - Luan Jardim Santos
06 - Parceiro Exsat - Marcelo Rozario
06 - Parceiro Exsat - MARIA DE FATIMA FERREIRA BECKMAN (Willian Beckman)
06 - Parceiro Exsat - MARIANO E DIMITRI GERACAO DE ENERGI (Claudio)
06 - Parceiro Exsat - MELO TELECOM (ndrei Marques de Oliveira)
06 - Parceiro Exsat - MENESES OLIVEIRA COM SER REP EIRELE (oyan Meneses dos Santos)
06 - Parceiro Exsat - MERCIA REGINA RODRIGUES ALVES (Lazaro Ferraz Lemos)
06 - Parceiro Exsat - MMLC CONERCIO DE MADEIRA LTDA (arcio da Silva Santos)
06 - Parceiro Exsat - MOMÓ TECNEWS ENERGIA SOLAR (Hermógenes de Sousa Evangelista)
06 - Parceiro Exsat - MOSCOSO SERVIÇOS DE ENGENHARIA ELETRÔNICA LTDA (Gustavo)
06 - Parceiro Exsat - MTC TELECOMUNICAÇÕES (Thiago Almeida Paixao)
06 - Parceiro Exsat - NUNNES CFTV E SERVIÇOS (Alex Nunes)
06 - Parceiro Exsat - PAULO HENRIQUE DE ALMEIDA SOUSA (Lívio Senna Freitas)
06 - Parceiro Exsat - PRECAVE COMERCIO E SERVICO LTDA (Fabiane)
06 - Parceiro Exsat - PROTECTION SISTEMAS DE SEGURANÇA LTDA (odrigo Cerqueira Lavigne Weyll)
06 - Parceiro Exsat - R JOVITA DOS SANTOS (Roberlan)
06 - Parceiro Exsat - Rafael Ferreira
06 - Parceiro Exsat - REINALDO BRAZ SANTANA (Reinaldo Braz Santana)
06 - Parceiro Exsat - RENAN QUEIROZ (Renan Queiroz Santos)
06 - Parceiro Exsat - RICARDO CARDOSO DOS SANTOS (icardo Cardoso dos Santos)
06 - Parceiro Exsat - ROGERIRO MOTA (Rogeriro Mota)
06 - Parceiro Exsat - RONIVALDO ARAUJO DA SILVA (Ronivaldo Araujo da silva)
06 - Parceiro Exsat - RS SEGURANÇA ELETRÔNICA LTDA (Evandro Régis Schettini)
06 - Parceiro Exsat - SEG COMERCIO DE EQUIPAMENTOS DE COMUNICAÇÃO LTDA (anilo Alves de Oliveira)
06 - Parceiro Exsat - SIGAON (Jânio Santos Dantas)
06 - Parceiro Exsat - SILVA SILVA COMERCIO E SERVICOS DE INFORMATICA LTDA (Uelington Silva Pereira)
06 - Parceiro Exsat - SUDOESTE MÓVEIS (Rogério Silva Fontes)
06 - Parceiro Exsat - SUNECOLOGY - TECNOLOGIAS E SOLUCOES EM ENERGIA SOLAR (Vivaldo)
06 - Parceiro Exsat - TECNOAGIL TELECOMUNICAÇÕES E SISTEMAS DE SEGURANÇA (Leandro Almeida Santos)
06 - Parceiro Exsat - THARSIEL JACKSON DE JESUS MENEZES (Tharsiel Jackson de jesus menezes)
06 - Parceiro Exsat - TIAGO MACHADO (Tiago Machado Ferreira)
07 - Marketing - Eventos promovidos
07 - Marketing - Google/Site
07 - Marketing - Redes Sociais
07 - Marketing - Rádio
08 - Provedor - Enerx- Viktor
08 - Provedor - Evaldo Rodrigues
08 - Provedor - Linknet
08 - Provedor - MONTTEREY (Bruno Ribeiro)
08 - Provedor - PLANOWEB NETWORK SERVIÇO E COMERCIO LTDA
08 - Provedor - Rogério Chimidt
08 - Provedor - Rummenig Liborio
09 - Provedor MSM - MSM INCUBADORA E CONSULTORIA LTDA (Mychel)
10 - Ademário - A&C CONSULTORIA E PROJETOS LTDA (Ademário Afonso)
11 - Parceiro Ademário - Ademário
11 - Parceiro Ademário - Parceiro Clean Land Bionergy LTDA (Daniele)
11 - Parceiro Ademário - PRESERV CONSULTORIA AMBIENTAL LTDA (Ernane)
12 - Sandro - GL AUTOMAÇÃO E ENERGIA SOLAR LTDA (Sandro)
13 - Parceiro Sandro - Álvaro
14 - Parceiro Exsat GMIX - DFV Energia LTDA (Luciano da Silva Santos)
15 - Comercial interno (Porta a Porta)
16 - Indique Personalizado - STEPHANIE AGUIAR SILVA (Lucas Ação Service)
17 - EXATTA & GF CAPITAL
18 - Mater Dei - Hospital
19 - Recorrente - Inpasa
20 - Parceiro PaP - YURE DA SILVA SANTOS
20 - Parceiro PaP - LAZARO ARIEL LOPES
21 - Parceiro CDL - JOAO
21 - Parceiro CDL - IRAILDES
06 - Parceiro Exsat - Alessandra da Exsat
22- Parceiro Televit - JCSFibra (sergio)
06 - Parceiro Exsat - Vigiai Tecnologia (Caio Cesar de Magalhaes)
01 - Interno - Henrique Michelini
02 - Indique - INVESTPLEN/MARIO CERQUEIRA
20 - Parceiro PaP- Ricardo dos Santos Barbosa
08 - Provedor - Gmix/Sigaon


