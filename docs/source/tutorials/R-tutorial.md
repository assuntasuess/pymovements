How to use pymovements in R:

Install the R-package **reticulate** for interoperability between Python and R.
```{r echo=T, message=FALSE, results='hold'}
 install.packages("reticulate")
```

Load the package.
```{r, echo=T,results='hold', message=T}
library(reticulate)
```

Install pymovements, if you haven't yet.
```{r echo=T, message=TRUE, results='hold'}
py_install("pymovements")
```

Import pymovements.
```{r, echo=T,results='hold', message=T}
#import module
pm <- import("pymovements")
```

Now pymovements should appear under values in your environment

Access functions and data within python modules and classes via the $ operator

To test, you can proceed with the "Working with Datasets" tutorial, for example download the ToyDataset
```{r, echo=T,results='hold', message=T}
dataset = pm$datasets$ToyDataset(root='testdata', download=TRUE)
```



### Related handy functions:

Load a python shell in R.
```{r, echo=T,results='hold', message=T}
#repl_python()
```


Information about the version of Python currently being used by reticulate
```{r, echo=F,results='hold', message=T}
#py_config()
```