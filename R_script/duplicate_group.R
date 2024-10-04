library(dplyr)

# Assuming your data is in a dataframe called 'df'
bYearList <- c("1970", "1971", "1972", "1973", "1974", "1975",
               "1976", "1977", "1978", "1979", "1980", "1981",
               "1982", "1983", "1984", "1985", "1986", "1987",
               "1988", "1989", "1990", "1991", "1992", "1993",
               "1994", "1995", "1996", "1997", "1998", "1999",
               "2000", "2001", "2002", "2003", "2004", "2005",
               "2006", "2007", "2008", "2009", "2010", "2011",
               "2012", "2013", "2014", "2015")

combined_data <- read.csv("~/Documents/user-segment/user_segment/combined_data.csv", 
                          header = TRUE,
                          stringsAsFactors = FALSE)


non_empty_births <- combined_data  %>%
filter(!is.na(birth) & length(birth) > 0 & birth != "")
print(non_empty_births)

# Group by email and combine events
result <- combined_data %>%
  group_by(email) %>%
  summarise(
    event = paste(unique(na.omit(event)), collapse = ", "),
    # Change all list-based columns to use paste(unique(...)
    name = paste(unique(na.omit(name)), collapse = ", "),
    mobile = paste(unique(na.omit(mobile)), collapse = ", "),
    email = paste(unique(na.omit(email)), collapse = ", "),
    #age = paste(unique(na.omit(age)), collapse = ", "),
    #title = paste(unique(na.omit(title)), collapse = ", "),
    gender = paste(unique(na.omit(gender)), unique(na.omit(title)), collapse = ", "),
    birth_year = paste(bYearList[unique(na.omit(byear))],unique(na.omit(birth)),unique(na.omit(age)), collapse = ", "),
    bmonth = paste(unique(na.omit(bmonth)), collapse = ", "),
    work = paste(unique(na.omit(work)), collapse = ", "),
    marriage = paste(unique(na.omit(marriage)), collapse = ", "),
    #birth = paste(unique(na.omit(birth[0:3])), collapse = ", ")
  ) %>%
  ungroup()


#non_empty_births <- result %>%
  #filter(!is.na(birth_year) & length(birth_year) > 0 & birth_year != "")

# Display the result
#print(non_empty_births)
print(result)

write.csv(result, "~/Documents/user-segment/user_segment/result.csv", row.names = FALSE)
