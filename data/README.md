# Data

```
Data
|-- RE
|   |-- 2018_n2c2
|       |-- examples.csv
|       |-- test_200.csv
|   |-- GAD
|       |-- examples.csv
|       |-- test_200.csv
|-- NER
|   |-- 2018_n2c2
|       |-- examples.csv
|       |-- test_200.csv
|   |-- NCBI_Disease
|       |-- examples.csv
|       |-- test_200.csv

```

The data were download from [[FedNLP Repo]](https://github.com/PL97/FedNLP), the examples (in `examples.csv`) for few-shot prompting (i.e., in-context learning) in each dataset were sampled randomly from the training dataset. The test set (in `test_200.csv`) is sampled randomly from the complete test set.
