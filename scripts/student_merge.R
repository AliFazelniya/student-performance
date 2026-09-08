raw_dir <- file.path("data", "raw")  # Defines the folder containing the original CSV files
mat_path <- file.path(raw_dir, "student-mat.csv")  # Builds the path to the math dataset
por_path <- file.path(raw_dir, "student-por.csv")  # Builds the path to the Portuguese dataset

d1=read.table(mat_path,sep=";",header=TRUE)  # Loads the math dataset with semicolon delimiters
d2=read.table(por_path,sep=";",header=TRUE)  # Loads the Portuguese dataset with semicolon delimiters

d3=merge(d1,d2,by=c("school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"))  # Combines records present in both datasets on shared demographic keys
print(nrow(d3))  # Reports the number of students present in the merged dataset
