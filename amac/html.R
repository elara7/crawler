# part 2 

# url
load("part2.RData")
addh <- "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/"
index <- as.character(tableurl)
addr_html <- paste(addh,index,sep = "")


library(XML)

data_html <- data.frame()

j=0
for (i in 1:length(index)){

parsed_doc <- htmlParse(file = addr_html[i],encoding = "UTF-8")

data_html[i,1] <- index[i]
data_html[i,2] <- managername[i]
# people
#/html/body/div/div[2]/div/table/tbody/tr[13]/td[2]

data_html[i,3] <- xpathSApply(parsed_doc,"/html/body/div/div[2]/div/table/tbody/tr[13]/td[2]", fun = xmlValue)

# product1
#/html/body/div/div[2]/div/table/tbody/tr[25]/td[2]

data_html[i,4] <- length(xpathSApply(parsed_doc,"/html/body/div/div[2]/div/table/tbody/tr[25]/td[2]//a"))

# product2
#/html/body/div/div[2]/div/table/tbody/tr[26]/td[2]

data_html[i,5] <- length(xpathSApply(parsed_doc,"/html/body/div/div[2]/div/table/tbody/tr[26]/td[2]//a"))
print(i)

j=j+1
if (j >=2000 ){
  save(data_html,file = paste("data_html",i,".RData",sep = ""))
  j=0
}

}
names(data_html) <- c("url","managername","staff","before","after")
write.csv(data_html,file = "data_html.csv")
