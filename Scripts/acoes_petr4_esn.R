#getwd()
# setwd("C:\\Users\\Fabô\\Documents\\UniRV\\2026-1\\Bancas TFC e orientações")

# Leitura de argumentos de linha de comando para automação
args <- commandArgs(trailingOnly = TRUE)
tipo_win   <- if (length(args) >= 1) args[1] else "Normal"
tipo_w     <- if (length(args) >= 2) args[2] else "Normal"
num_itera  <- if (length(args) >= 3) as.integer(args[3]) else 10000L
num_run    <- if (length(args) >= 4) args[4] else "1"
output_dir <- if (length(args) >= 5) args[5] else "."

# Definição dinâmica dos nomes dos arquivos de saída
sufixo          <- paste0("com_factor ", num_itera, "_", num_run, ".csv")
arq_esn         <- file.path(output_dir, paste0("Dados PETR4 ESN_mae_otim40x60 ", sufixo))
arq_bestSol_fit <- file.path(output_dir, paste0("Dados PETR4 bestSol melhores_fitness mae_otim40x60 ", sufixo))
arq_win         <- file.path(output_dir, paste0("Dados PETR4 Win ESN_mae_otim40X60 ", sufixo))
arq_w           <- file.path(output_dir, paste0("Dados PETR4 W reservatório ESN_mae_otim40X60 ", sufixo))
arq_wout        <- file.path(output_dir, paste0("Dados PETR4 Wout ESN_mae_otim40X60 ", sufixo))
arq_resumo      <- file.path(output_dir, paste0("Dados PETR4 resumo fitness ESN_mae_otim40X60 ", sufixo))
arq_bestSol     <- file.path(output_dir, paste0("Dados PETR4 bestSol mae_otim40x60 ", sufixo))

library(ggplot2)               #Plota os gráficos
library(PerformanceAnalytics)  #Assimetria e curtose
library(GA)                    #Algoritmo genético
library(pracma)                #Tic e Toc (demarcadores de tempo de execução)
library(fitdistrplus)
library(MASS)
library(PearsonDS)
library(StockDistFit)          #ged_fit
library(fGarch)                #rged


#Para fins de simplificação serão considerados apenas os valores de fechamento das ações
data_fac <- as.matrix(read.csv2("data/PETR4_close com factor_2000-2020.txt",header=F)) #5198 sem factor
data_fac = as.numeric(data_fac)
#data = as.matrix(read.csv2('PETR4_close_2000-2020.txt',header=F))       #5198 sem factor
#data = as.numeric(data)
#data
#length(data)
#View(data)                    # 5198 entradas
#summary(data)
#describe(data)

#TAMANHOS TREINO, VALIDAÇÃO E TESTE
#treino   = 3118                #60% 
#valida   = 1040                #20% 
#teste    = 1040                #20% 
treino   = 2600                #50% 
valida   = 1299                #25% 
teste    = 1299                #25% 


#treino = data(1:treino)
#treino_fac = data(1:treino)
#treino_valida    = data[1:(treino+valida)]                                      #Sem factor
treino_valida = data_fac[1:(treino+valida)]                                     #Com factor
#head(treino_valida[1:treino])
#tail(treino_valida[1:treino])
#treino_valida[3117]
#treino_valida
#length(treino_valida)         #4158

#treina_testa  = c(data[1:treino],data[(valida+1):(treino+valida+teste)])        #Sem factor e sem factor
#treina_testa  = c(data_fac[1:treino],data_fac[(valida+1):(treino+valida+teste)])#Com factor e com factor                       
#treina_testa  = c(data_fac[1:treino],data[(valida+1):(treino+valida+teste)])    #Com factor e sem factor
#tail(treina_testa[1:treino])
#treina_testa[3117]
#treina_testa
#length(treina_testa)          #4158

#train             = data[1:treino]                                               #Sem factor
#train             = data_fac[1:treino]                                           #Com factor                               
#plot(train,   type="l")
#train_media       = mean(train)

#validate          = data[(treino+1):(treino+valida)]                             #Sem factor
#validate          = data_fac[(treino+1):(treino+valida)]                         #Com factor
#plot(validate,type="l")
#valid_media       = mean(validate)

#test              = data[(treino+valida+1):(treino+valida+teste)]                #Sem factor
#test              = data_fac[(treino+valida+1):(treino+valida+teste)]            #Com factor
#plot(test,    type="l")
#test_media        = mean(test)

#ajuste=fitdist(train,"cauchy")                                                   #pode trocar "norm" por "gamma", "weibull" ou "lnorm"
#coef(ajuste)                                                                     #location=47.02474,    scale=10.24399  apresenta os critérios de informação e tb a função de verossimilhança. 

#ajuste=fitdistr(dados,"norm")                                                    #pode trocar "norm" por "gamma", "weibull" ou "lnorm"
#coef(ajuste)                                                                     # apresenta os critérios de informação e tb a função de verossimilhança.

#ged_fit(train)                                                                   # mean=47.4000008, sd=24.9533557, nu=0.8952071

#summary(data)
summary(data_fac)
#skewness(data,method="moment")                #assimetria = 1.618189 (fortemente assimétrica>0.5)
skewness(data_fac,method="moment")                #assimetria = 1.618189 (fortemente assimétrica>0.5)
#kurtosis(data,method="excess")                #curtose    = 3.204829 (leptocúrtica>0)
kurtosis(data_fac,method="excess")                #curtose    = 3.204829 (leptocúrtica>0)
#hist(data, breaks = (c(1, 5.831, 10.662, 15.493, 20.324, 25.155, 29.986, 34.817, 39.648, 44.479, 49.31, 54.141, 58.972, 63.803, 68.634, 73.465, 78.296, 83.127)),xlab = "Closing price with factor of PETR4 stock" ,main = "Histogram of daily closing price with factor \n of PETR4 stock between 2000 and 2020")

# Criar o gráfico PDF diretamente na pasta de destino de forma limpa
pdf_file <- file.path(output_dir, paste0(basename(output_dir), ".pdf"))
pdf(pdf_file, width=10, height=7)

par(mfrow=c(1,2))
#hist(data, ylim=c(0,1200), breaks = (c(8.589, 18.672, 28.755, 38.838, 48.921, 59.004, 69.087, 79.17, 89.253, 99.336, 109.419, 119.502, 129.585, 139.668, 149.751, 159.834, 169.917, 180)),xlab = "Closing price of PETR4 stock (R$)" ,main = "(a)")
hist(data_fac, ylim=c(0,1200), xlab = "Closing price with factor of PETR4 stock (R$)" ,main = "(b)")
#boxplot(data,ylim=c(0,185),ylab = "Closing price of PETR4 stock (R$)",main="(a)") #com outliers
boxplot(data_fac,ylim=c(0,185),ylab = "Closing price with factor of PETR4 stock (R$)",main="(b)") #com outliers
par(mfrow=c(1,1))

#par(mfrow=c(1,2))
#data_date = as.matrix(read.csv2('PETR4_close_2000-2020_com data.csv',header=F))                #5191 sem factor
#data_date_1 = as.Date(data_date[2:5198,1])
#data_date_1
#length(data_date_1)
#data_date_2 = as.numeric(data_date[2:5198,2])     
#data_date_2
#plot(data_date_1,data_date_2,xlab="Date",ylab="Raw data (R$)",type="l",main="Daily closing price of PETR4 stock \n between 2000 and 2020 \n (raw data/without factor)")

#data_date_fac = as.matrix(read.csv2('PETR4_close com factor_2000-2020_com data.csv',header=F))
#data_date_fac
#data_date_fac1 = as.Date(data_date_fac[2:5198,1])        
#data_date_fac1
#data_date_fac2 = as.numeric(data_date_fac[2:5198,2])     
#data_date_fac2
#plot(data_date_fac1,data_date_fac2,xlab="Date",ylab="Data with factor (R$)",type="l",main="Daily closing price of PETR4 stock \n between 2000 and 2020 \n (Data with factor applied)")


#par(mfrow=c(1,3))
#plot(data_date_1[1:treino],data[1:treino],ylim = c(5,180), xlab="Date",ylab="Closing price of PETR4 stock without factor (R$)",type="l",main="Training data")
#plot(data_date_1[(treino+1):(treino+valida)],data[(treino+1):(treino+valida)],ylim = c(5,180),xlab="Date",ylab="Closing price of PETR4 stock without factor (R$)",type="l",main="Validation data")
#plot(data_date_1[(treino+valida+1):5198],data[(treino+valida+1):5198],ylim = c(5,180),xlab="Date",ylab="Closing price of PETR4 stock without factor (R$)",type="l",main="Test data")

#plot(data_date_fac1[1:treino],data_fac[1:treino],ylim = c(0,85),xlab="Date",ylab="Data with factor (R$)",type="l",main="Training data")
#plot(data_date_fac1[(treino+1):(treino+valida)],data_fac[(treino+1):(treino+valida)],ylim = c(0,85),xlab="Date",ylab="Data with factor (R$)",type="l",main="Validation data")
#plot(data_date_fac1[(treino+valida+1):5198],data_fac[(treino+valida+1):5198],ylim = c(0,85),xlab="Date",ylab="Data with factor (R$)",type="l",main="Test data")


#par(mfrow=c(1,2))
#plot(data,xlab="Time (days)",ylab="Raw data (R$)",type="l",main="Daily closing price of PETR4 stock \n between 2000 and 2020 \n (raw data/without factor)")
#plot(data_fac,xlab="Time (days)",ylab="Data with factor (R$)",yaxis = c(),type="l",main="Daily closing price of PETR4 stock \n between 2000 and 2020 \n (data with factor applied)")
#plot(data_date_1,data,ylim=c(0,200),xlab="Date (a)",ylab="Raw data (R$)",type="l")#,main="Daily closing price of PETR4 stock \n between 2000 and 2020")
#plot(data_date_fac1,data_fac,ylim=c(0,200),xlab="Date (b)",ylab="Data with factor (R$)",type="l")#,main="Daily closing price of PETR4 stock \n between 2000 and 2020")

#data_plot_train = data[1:treino]
#qplot(x = 1:treino , y = data_plot_train, geom = 'line') + geom_line(color = 'darkblue') + 
#  labs(x = 'Training days' , y = 'Price (R$)' , title = "Daily closing price of PETR4 stock between 2000 and 2020") + geom_hline(yintercept = mean(data_plot_train) , color = 'red')

#data_plot_test = treina_testa[3119:4159]                           
#qplot(x = 3119:4159 , y = data_plot_test, geom = 'line') + geom_line(color = 'darkblue') + 
#  labs(x = 'Test days' , y = 'Price (R$)' , title = "Raw daily closing price of PETR4 stock test series") + geom_hline(yintercept = mean(data_plot_test) , color = 'red')

#data_plot_test = data[3119:4679]
#qplot(x = 3119:4679 , y = data_plot_test, geom = 'line') + geom_line(color = 'darkblue') + 
#  labs(x = 'Test days' , y = 'Price (R$)' , title = "Daily closing price of PETR4 stock between 2000 and 2020") + geom_hline(yintercept = mean(data_plot_test) , color = 'red')

#data_plot_valid = data[4679:5198]
#qplot(x = 4679:5198 , y = data_plot_valid, geom = 'line') + geom_line(color = 'darkblue') + 
#  labs(x = 'Test days' , y = 'Price (R$)' , title = "Daily closing price of PETR4 stock between 2000 and 2020") + geom_hline(yintercept = mean(data_plot_valid) , color = 'red')


monitora <- function(obj){
  # plot(obj) # Desativado para evitar gerar PDFs gigantescos de giga-bytes no loop
  #ggplot(y = c(obj@summary[,1],obj@summary[,2],obj@summary[,6]), geom = 'line') 
  #plot(type="l",cbind(obj@summary[,1],obj@summary[,2],obj@summary[,6]))
  #conta = conta + 1L
  if (old_obj < obj@summary[[obj@iter]]){
     #linha_fitness = cbind(obj@iter,obj@summary[[obj@iter]],old_obj)
     #write.table(linha_fitness,file = "Dados PETR4 melhores_fitness ESN_mae_otim40X60 sem_factor 10000_1.csv", append = T, col.names = F, sep = "\t", eol = "\n")
     
     a_monit   = sum(obj@bestSol[[obj@iter]][1:17] * 2^(rev(seq(along=obj@bestSol[[obj@iter]][1:17])) - 1))/131071
     #a_monit   = binary2decimal(obj@bestSol[[obj@iter]][1:17])/131071
     if (a_monit == 0) {a_monit=7.62939453125e-6}

     sr_monit  = sum(obj@bestSol[[obj@iter]][18:34] * 2^(rev(seq(along=obj@bestSol[[obj@iter]][18:34])) - 1))/131071
     #sr_monit  = binary2decimal(obj@bestSol[[obj@iter]][18:34])/131071
     if (sr_monit == 0) {sr_monit=7.62939453125e-6}
     
     iL_monit  = sum(obj@bestSol[[obj@iter]][35:41] * 2^(rev(seq(along=obj@bestSol[[obj@iter]][35:41])) - 1))
     #iL_monit  = binary2decimal(obj@bestSol[[obj@iter]][35:41])
     iL_monit  = iL_monit+2
     
     tr_monit  = sum(obj@bestSol[[obj@iter]][42:46] * 2^(rev(seq(along=obj@bestSol[[obj@iter]][42:46])) - 1))
     #tr_monit  = binary2decimal(alg_gen@bestSol[[i]][42:46])
     tr_monit  = tr_monit+2
     
     reg_monit = sum(obj@bestSol[[obj@iter]][47:55] * 2^(rev(seq(along=obj@bestSol[[obj@iter]][47:55])) - 1))/511
     #reg_monit = binary2decimal(alg_gen@bestSol[[obj@iter]][47:55])/511
     reg_monit = (reg_monit + 1e-4)*(1e-4 - 1e-6)
     
     linha_bestSol = cbind(obj@iter,a_monit,sr_monit,iL_monit,tr_monit,reg_monit,obj@summary[[obj@iter]])
     write.table(linha_bestSol,file = arq_bestSol_fit, append = T, row.names = F, col.names = F, sep = "\t", eol = "\n")     
     
     old_obj  <<- obj@summary[[obj@iter]]
    }
  #sumario[[obj@iter]] <<- obj@summary[[obj@iter]]   #Primeiro valor do sumário (melhor)
  #sumario[[obj@iter]] <<- obj@summary[[obj@iter]][]
  #sumario[[obj@iter]] <<- c(obj@summary[obj@iter,]) #Todos valores do sumário
  sumario[[obj@iter]] <<- c(obj@summary[[obj@iter,1]],obj@summary[[obj@iter,2]],obj@summary[[obj@iter,6]])   #Todos específicos do sumário
}

inSize = outSize = 1


#f <- function(i, j, k){
f <- function(cromossoma=c()){

   #Geração dos cromossomos e das populações dos hiperparâmetros a serem otimizados
   #a_GA             = binary2decimal(cromossoma[1:17])                 #real
   #a_GA             = a_GA/131072                                      #taxa de vazão
   a_GA             = sum(cromossoma[1:17] * 2^(rev(seq(along=cromossoma[1:17])) - 1))/131071
   if (a_GA == 0)    {a_GA=7.62939453125e-6}
   
   #sr_GA            = binary2decimal(cromossoma[18:34])                #real
   #sr_GA            = sr_GA/131071                                     #raio espectral
   sr_GA            = sum(cromossoma[18:34] * 2^(rev(seq(along=cromossoma[18:34])) - 1))/131071
   if (sr_GA == 0)   {sr_GA=7.62939453125e-6}
   
   #initLen_GA        = binary2decimal(cromossoma[35:41])               #int
   initLen_GA       = sum(cromossoma[35:41] * 2^(rev(seq(along=cromossoma[35:41])) - 1))
   initLen_GA       = initLen_GA+2                                     #valores iniciais desconsiderados
   
   #tam_reservoir_GA = binary2decimal(cromossoma[42:46])                   #int
   tam_reservoir_GA = sum(cromossoma[42:46] * 2^(rev(seq(along=cromossoma[42:46])) - 1))
   tam_reservoir_GA = tam_reservoir_GA+2                               #tamanho do reservatório
   
   #reg_GA           = binary2decimal(cromossoma[24:24])/100000000      #real
   #reg_GA           = binary2decimal(cromossoma[47:55])/511            #coeficiente de regularização da regressão
   reg_GA           = sum(cromossoma[47:55] * 2^(rev(seq(along=cromossoma[47:55])) - 1))/511
   reg_GA           = (reg_GA + 1e-4)*(1e-4 - 1e-6)
   if (reg_GA == 0) {reg_GA=1e-9}      
   
   #ESN a partir daqui (configurado dinamicamente pela automação)
   if (tipo_win == "Normal") {
     Win_GA = matrix(rnorm(tam_reservoir_GA*(1+inSize), mean = -0.08, sd = 1), tam_reservoir_GA)
     distr_Win_GA = "Normal média=0, desvio padrão=1"
   } else if (tipo_win == "Uniforme") {
     Win_GA = matrix(runif(tam_reservoir_GA*(1+inSize), -1.0, 1.0), tam_reservoir_GA)
     distr_Win_GA = "Uniforme limite_inf=-1, limite_sup=1"
   } else if (tipo_win == "GED") {
     Win_GA = matrix(rged(tam_reservoir_GA*(1+inSize), mean = 14.573152, sd = 8.032086, nu = 7.686645), tam_reservoir_GA)
     distr_Win_GA = "GED mean=14.573152, sd=8.032086, nu=7.686645"
   } else {
     Win_GA = matrix(rnorm(tam_reservoir_GA*(1+inSize), mean = -0.08, sd = 1), tam_reservoir_GA)
     distr_Win_GA = "Normal média=0, desvio padrão=1"
   }
   
   if (tipo_w == "Normal") {
     W_GA = matrix(rnorm(tam_reservoir_GA*tam_reservoir_GA, mean = -0.08, sd = 1), tam_reservoir_GA)
     distr_W_GA = "Normal média=0, desvio padrão=1"
   } else if (tipo_w == "Uniforme") {
     W_GA = matrix(runif(tam_reservoir_GA*tam_reservoir_GA, -1, 1), tam_reservoir_GA)
     distr_W_GA = "Uniforme limite_inf=-1, limite_sup=1"
   } else {
     W_GA = matrix(rnorm(tam_reservoir_GA*tam_reservoir_GA, mean = -0.08, sd = 1), tam_reservoir_GA)
     distr_W_GA = "Normal média=0, desvio padrão=1"
   }
   
   rhoW_GA = abs(eigen(W_GA,only.values=TRUE)$values[1])                  #Autovalores da matriz W
   W_GA = sr_GA * W_GA / rhoW_GA
   
   X = matrix(0,1+inSize+tam_reservoir_GA,treino-initLen_GA)
   Yt = matrix(treino_valida[(initLen_GA+2):(treino+1)],1)
   x = rep(0,tam_reservoir_GA)                                         #Preenche o vetor x (do tamanho do reservatório) com 0
   
   for (t in 1:treino){
     u = treino_valida[t]
     x = (1-a_GA)*x + a_GA*tanh( Win_GA %*% rbind(1,u) + W_GA %*% x )         #tanh é a função de ativação
     if (t > initLen_GA)
       X[,t-initLen_GA] = rbind(1,u,x)
   }
   X_T = t(X)
   Wout_GA = Yt %*% X_T %*% solve( X %*% X_T + reg_GA*diag(1+inSize+tam_reservoir_GA))
   
   #Prevendo os dados de validação
   Y = matrix(0,outSize,valida)
   u = treino_valida[treino+1]
   
   for (t in 1:valida){
     x = (1-a_GA)*x + a_GA*tanh( Win_GA %*% rbind(1,u) + W_GA %*% x )
     y = Wout_GA %*% rbind(1,u,x)
     Y[,t] = y
     u = treino_valida[treino+t+1]
   }
   
   #Prevendo os dados de treino
   Ytr = matrix(0,outSize,treino)
   u   = treino_valida[1]
   
   for (j in 1:treino) {
     x = (1-a_GA)*x + a_GA*tanh( Win_GA %*% rbind(1,u) + W_GA %*% x )
     y = Wout_GA %*% rbind(1,u,x)
     Ytr[,j] = y
     u = treino_valida[j+1]                               #corrigido [j+1] a partir desta versão
   }
   
#CÁLCULO DE ERROS PARA OTIMIZAÇÃO   
   rmse_treino_GA = sqrt(mean((    treino_valida[2:treino] - Ytr[outSize,1:(treino-1)])^2))
   rmse_valida_GA = sqrt(mean((    treino_valida[(treino+2):(treino+valida)]-Y[outSize,1:(valida-1)])^2))
   mae_treino_GA  =      mean(abs( treino_valida[2:treino] - Ytr[outSize,1:(treino-1)]))
   mae_valida_GA  =      mean(abs( treino_valida[(treino+2):(treino+valida)]-Y[outSize,1:(valida-1)]))
   
#Fitness = erro de treinamento * 0.4 e erro de validação * 0.6
   #otimiza            = (-rmse_treino_GA*0.4 - rmse_valida_GA*0.6)
   otimiza            = (-mae_treino_GA*0.4 - mae_valida_GA*0.6)
   contar           <<- contar + 1L
   old_otim_backup  <<- old_otim
   old_rmse_backup  <<- old_rmse
   Win_GA_t         <<- t(Win_GA)
   W_GA_t           <<- t(W_GA)
   Wout_GA_t        <<- t(Wout_GA)
   if (old_otim < otimiza){
      linha_entrada      = cbind(contar,Win_GA_t, distr_Win_GA)
      write.table(linha_entrada,     file = arq_win, append = T, col.names = F, sep = "\t", eol = "\n")
      linha_reservatorio = cbind(contar,W_GA_t, distr_W_GA)
      write.table(linha_reservatorio,file = arq_w, append = T, col.names = F, sep = "\t", eol = "\n")
      linha_saida        = cbind(contar,Wout_GA_t)
      write.table(linha_saida,       file = arq_wout, append = T, col.names = F, sep = "\t", eol = "\n")
      old_otim         <<- otimiza
     }

   linha_ESN   = cbind(contar,a_GA,sr_GA,initLen_GA,tam_reservoir_GA,reg_GA,mae_treino_GA,mae_valida_GA,otimiza,old_otim_backup,rmse_treino_GA,rmse_valida_GA,rmse_treino_GA*0.4+rmse_valida_GA*0.6)
   write.table(linha_ESN,         file = arq_esn, append = T, col.names = F, sep = "\t", eol = "\n")
  
   return(otimiza)
}

#Criação dos arquivos que vão gravar a ESN
linha_ESN          = cbind("Parâmetro","Contar","a","sr","initLen","tam_reservoir","reg","MAE_treino40%","MAE_valida60%","Otimiza","old_Otimiza","RMSE_treino","RMSE_valida","RMSE_t0.4+RMSE_v0.6")
write.table(linha_ESN,file     = arq_esn, append = F, row.names = F, col.names = F, sep = "\t", eol = "\n")
linha_bestSol      = cbind("Época","a","sr","iL","tr","reg","Fitness")
write.table(linha_bestSol,file = arq_bestSol_fit, append = F, row.names = F, col.names = F, sep = "\t", eol = "\n")     
linha_entrada      = cbind("Época","Win","Distribuição")
write.table(linha_entrada,file = arq_win, append = F, col.names = F, sep = "\t", eol = "\n")
linha_reservatorio = cbind("Época","W","Distribuição")
write.table(linha_reservatorio,file = arq_w, append = F, col.names = F, sep = "\t", eol = "\n")
linha_saida        = cbind("Época","Wout")
write.table(linha_saida,file = arq_wout, append = F, col.names = F, sep = "\t", eol = "\n")
#linha_fitness = cbind("Época","Fitness","old_fitness")
#write.table(linha_fitness,file  = "Dados PETR4 melhor_fitness ESN_mae_otim40X60 brutos 7500_1.csv", append = F, col.names = F, sep = "\t", eol = "\n")

#Inicialização das variáveis
old_obj  <- -Inf
old_otim <- -Inf
old_rmse <-  Inf
old_mae   =  Inf
conta    <- contar <- 0L
rmse_treino = mae_treino = rmse_valida = mae_valida = otimiza = 0
itera     = num_itera      #Número de épocas máximo
sumario  <- vector("list", length = itera)
#semente   = 1716

#Algoritmo Genético (chama as funções de fitness e monitoramento, a qual gera o gráfico)
tic()         #Início da medição do tempo
alg_gen <- ga("binary", fitness=function(x) f(x), nBits = 59, popSize = 10, pcrossover = 0.8, population = gabin_Population,
              selection = gabin_tourSelection, crossover = gabin_spCrossover, mutation = gabin_raMutation, run=3500, #máximo de iterações sem melhora para abortar
              pmutation=0.1, elitism = 1, parallel = F, maxiter= itera,      #n de gerações
              keepBest = T,  monitor=monitora, optim = F)                #o keepBest salva os melhores individuos de cada geração
toc()         #Fim da medição do tempo
beep()        #Sinal sonoro de aviso de fim

# Plotar o gráfico final do Algoritmo Genético (curva evolutiva completa em uma única página)
plot(alg_gen)

#sumario
#View(sumario)
#old_obj
#par(mfrow=c(1,1))
#View(alg_gen)
#alg_gen@summary
#alg_gen@fitness[1, ]
#plot(alg_gen@solution[1, ])


#Trocar pela maior época obtida no gráfico (definido dinamicamente)
itera   = alg_gen@iter

#Finalização dos arquivos que gravaram a ESN
linha_ESN          = cbind("Parâmetro","Contar","a","sr","initLen","tam_reservoir","reg","MAE_treino40%","MAE_valida60%","Otimiza","old_Otimiza","RMSE_treino","RMSE_valida","RMSE_t0.4+RMSE_v0.6")
write.table(linha_ESN,file     = arq_esn, append = T, row.names = F, col.names = F, sep = "\t", eol = "\n")

linha_bestSol      = cbind("Época","a","sr","iL","tr","reg","Fitness")
write.table(linha_bestSol,file = arq_bestSol_fit, append = T, row.names = F, col.names = F, sep = "\t", eol = "\n")     

linha_entrada      = cbind("Época","Win","Distribuição")
write.table(linha_entrada,file = arq_win, append = T, col.names = F, sep = "\t", eol = "\n")
linha_reservatorio = cbind("Época","W","Distribuição")
write.table(linha_reservatorio,file = arq_w, append = T, col.names = F, sep = "\t", eol = "\n")
linha_saida        = cbind("Época","Wout")
write.table(linha_saida,file = arq_wout, append = T, col.names = F, sep = "\t", eol = "\n")

linha_resumo       = cbind("Melhor_Fitness","Fitness_médio","Fitness_mínimo")
write.table(linha_resumo,file  = arq_resumo, append = F, col.names = F, sep = "\t", eol = "\n")
linha_resumo       = cbind(sumario)
write.table(linha_resumo,file  = arq_resumo, append = T, col.names = F, sep = "\t", eol = "\n")
linha_resumo       = cbind("Melhor_Fitness","Fitness_médio","Fitness_mínimo")
write.table(linha_resumo,file  = arq_resumo, append = T, col.names = F, sep = "\t", eol = "\n")

linha_bestSol      = cbind("Época","a","sr","iL","tr","reg")
write.table(linha_bestSol,file = arq_bestSol, append = F, row.names = F, col.names = F, sep = "\t", eol = "\n")
for (i in 1:itera) {
    resulta_a      = binary2decimal(alg_gen@bestSol[[i]][1:17])/131071
    if (resulta_a == 0) {resulta_a=7.62939453125e-6}
    resulta_sr     = binary2decimal(alg_gen@bestSol[[i]][18:34])/131071
    if (resulta_sr == 0) {resulta_sr=7.62939453125e-6}
    resulta_iL     = binary2decimal(alg_gen@bestSol[[i]][35:41])
    resulta_iL     = resulta_iL+2
    #if (resulta_iL == 0) {resulta_iL=2}
    resulta_tr     = binary2decimal(alg_gen@bestSol[[i]][42:46])
    resulta_tr     = resulta_tr+2
    resulta_reg    = binary2decimal(alg_gen@bestSol[[i]][47:55])/511
    resulta_reg    = (resulta_reg + 1e-4)*(1e-4 - 1e-6)

    linha_bestSol  = cbind(i,resulta_a,resulta_sr,resulta_iL,resulta_tr,resulta_reg)
    write.table(linha_bestSol,file = arq_bestSol, append = T, row.names = F, col.names = F, sep = "\t", eol = "\n")
}
linha_bestSol = cbind("Época","a","sr","iL","tr","reg")
write.table(linha_bestSol,file = arq_bestSol, append = T, row.names = F, col.names = F, sep = "\t", eol = "\n")

# Fechar o dispositivo de PDF salvando os gráficos gerados de forma íntegra
dev.off()
