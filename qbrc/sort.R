# Rscript sort.R
# install.packages("tictoc")
library("tictoc")

selectSort <- function(numbers) {
   for(i in 1:(length(numbers) - 1)) {
      minIndex = i
      for(j in (i+1):length(numbers)) {
         if(numbers[j] < numbers[minIndex]) {
	    minIndex = j
	 }
      }
      temp <- numbers[i]
      numbers[i] <- numbers[minIndex]
      numbers[minIndex] <- temp
   }
   return(numbers)
}

checkSorted <- function(numbers) {
   for(i in 1:(length(numbers) - 1)) {
      if(numbers[i] > numbers[i+1]) {
         return(FALSE)
      }
   }
   return(TRUE)
}

max_num <- 20000

numbers <- (max_num-1):0

print("sorting starts.")
tic()

numbers <- selectSort(numbers)
# numbers <- sort(numbers)

print("sorting ends.")
toc()

passed <- checkSorted(numbers)
if(passed) {
   print("Correctly sorted.")
} else {
   print("Error: numbers are not sorted.")
}

