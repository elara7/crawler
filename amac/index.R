# part 1

# url
addr1 <- "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.1406895170965674&page="
addr2 <- "&size=20"
i <- 1:872-1
addr <- paste(addr1,i,addr2,sep = "")

library(httr)

# header
header <- c("gs.amac.org.cn",
            "XMLHttpRequest",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "application/json",
            "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html"
)
names(header) <- c("Host" , "X-Requested-With" , "User-Agent" , "Content-Type" , "Referer")


# get first data

data <- NULL # init

d <- NULL # init

# get json
d <- POST(url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.1406895170965674&page=0&size=20", 
          add_headers(header),
          body = "{}",
          encode = "json"
)
d_content <- content(d)$content
oritable <- as.data.frame(t(unlist(d_content[[1]])))
tname <- names(oritable)
table <- oritable

# get all data

for (i in 1:length(addr)){
  
  d <- NULL # init
  
  # get json
  d <- POST(url = addr[i], 
            add_headers(header),
            body = "{}",
            encode = "json"
  )
  d_content <- content(d)$content
  # convert data
  for (j in 1:length(d_content)){
    temp <- as.data.frame(t(unlist(d_content[[j]])))
    table <- merge(table,temp,all = T,sort = F)
  }
  print(i)
}

# convert time

table$establishDate <- strptime(as.Date(as.POSIXlt(as.numeric(as.character(table$establishDate))/1000, origin="1970-01-01")), "%Y-%m-%d")
table$registerDate <- strptime(as.Date(as.POSIXlt(as.numeric(as.character(table$registerDate))/1000, origin="1970-01-01")), "%Y-%m-%d")

# data output
write.csv(table,file = "table.csv")
