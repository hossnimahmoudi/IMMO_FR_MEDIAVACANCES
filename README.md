## How to launch a spider
 - Create a virtualEnv Python2.7 
 - Install all libraries that exists in the file `requirements.txt`
 - Launch `SELOGER_MEDIAVACANCE.py`
 - Drop all duplicated rows based on field ID_CLIENT

<hr>

## Follow this steps

- Install libraries in VirtualEnv
```
pip install -r requirements.txt
pip install iso3166
sudo apt-get install gocr
```

- Launch a spider `SELOGER_MEDIAVACANCE.py` in Screen
``` 
scrapy crawl name_of_spider -o name_file_csv.csv
```

- Drop duplicate
```
sort -u -k3,3 -t";" name_file_csv.csv > file_without_dup.csv
```