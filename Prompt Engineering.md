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







