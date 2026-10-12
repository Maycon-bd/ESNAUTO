invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
.libPaths(c("Scripts/results/bibliometria_ambiente/R-library", "C:/Users/User/AppData/Local/R/win-library/4.6", "Scripts/results/diebold_mariano/ambiente/R-library", .libPaths()))
library(ggplot2)
out <- "reports/qa_monografia_bibliometria/figuras"
dir.create(out, recursive=TRUE, showWarnings=FALSE)
theme_word <- theme_minimal(base_size=10, base_family="sans") + theme(panel.grid.major.y=element_blank(), panel.grid.minor=element_blank(), axis.text=element_text(color="#172832"), plot.margin=margin(5,12,5,5))
barplot_word <- function(labels, counts, filename, height, denom=NULL, limit=NULL) {
 d <- data.frame(label=factor(labels,levels=rev(labels)), n=counts)
 d$value <- if(is.null(denom)) as.character(counts) else chartr(".",",",sprintf("%d (%.1f%%)",counts,100*counts/denom))
 p <- ggplot(d,aes(n,label))+geom_col(fill="#24627A",width=.7)+geom_text(aes(label=value),hjust=-.1,size=3.1)+scale_x_continuous(limits=c(0,if(is.null(limit)) max(counts)+1.2 else limit),expand=c(0,0),breaks=scales::breaks_width(if(max(counts)>15)5 else 2))+labs(x="Número de estudos",y=NULL)+theme_word
 ggsave(file.path(out,filename),p,width=6.3,height=height,dpi=300,bg="white")
}
barplot_word(c("P1  Inicialização dos pesos","P2  Otimização de hiperparâmetros","P3  Pré-processamento","P4  Comparação com Deep Learning","P5  Mercado e ativo"),c(16,16,31,21,30),"01.png",2.7,34,40)
v <- jsonlite::fromJSON("reports/bibliometria_reconstrucao/validacao_bibliometrix.json")
f <- v$frequencias[v$frequencias$documentos>=2,]
barplot_word(f$termo,f$documentos,"02.png",4.3)
t <- jsonlite::fromJSON("reports/bibliometria_reconstrucao/expressoes_titulos.json")$frequencias
t <- t[t$documentos>=2,]
barplot_word(t$expressao,t$documentos,"04.png",5.2)
N <- as.matrix(readRDS("reports/bibliometria_reconstrucao/matriz_coocorrencia.rds"))
freq <- sort(diag(N),decreasing=TRUE)
sel <- names(freq)[freq>=2]
A <- N[sel,sel]; diag(A)<-0
g <- igraph::graph_from_adjacency_matrix(A,mode="undirected",weighted=TRUE,diag=FALSE)
set.seed(20261012)
L <- igraph::norm_coords(igraph::layout_with_fr(g),xmin=-1,xmax=1,ymin=-1,ymax=1)
c <- igraph::membership(igraph::cluster_walktrap(g))
d <- data.frame(name=igraph::V(g)$name,x=L[,1],y=L[,2],n=as.numeric(freq[igraph::V(g)$name]),group=factor(c),label=tolower(igraph::V(g)$name))
e <- igraph::as_data_frame(g,what="edges")
e$x <- d$x[match(e$from,d$name)]; e$y <- d$y[match(e$from,d$name)]
e$xend <- d$x[match(e$to,d$name)]; e$yend <- d$y[match(e$to,d$name)]
p <- ggplot()+geom_segment(data=e,aes(x=x,y=y,xend=xend,yend=yend,linewidth=weight),color="#A7B8C2",alpha=.7)+geom_point(data=d,aes(x=x,y=y,size=n,fill=group),shape=21,color="white",stroke=.6)+ggrepel::geom_text_repel(data=d,aes(x=x,y=y,label=label),size=3.15,seed=20261012,box.padding=.55,point.padding=.7,max.overlaps=Inf,min.segment.length=0,segment.color="#A0ADB5",max.time=10)+scale_size_area(max_size=11)+scale_fill_manual(values=c("#24627A","#AF653E","#4D7C4F","#74609B","#735A48"))+scale_linewidth_continuous(range=c(.4,1.3))+coord_equal(xlim=c(-1.55,1.55),ylim=c(-1.4,1.4),clip="off")+theme_void()+theme(legend.position="none",plot.margin=margin(14,18,14,18))
ggsave(file.path(out,"03.png"),p,width=6.3,height=5.0,dpi=300,bg="white")
stopifnot(nrow(d)==14,nrow(e)==33)
cat("Quatro figuras preparadas para inserção em 16 cm.\n")
