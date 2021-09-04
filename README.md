# imdbsoup

Get credits for people on IMDb, using Beautiful Soup.

## install

```bash
pip install -r requirements.txt
```

## usage

First, grab the IMDb name identifier from the webpage URL. This starts with `nm#######`:

E.g. https://www.imdb.com/name/nm1297015/ -> `nm1297015`

Pass the name identifier to the CLI:

```
$ python -i main.py nm1297015
Retrieved credits for Emma Stone.
>>> person
<IMDb entry: Emma Stone (218 total credits)>
>>> person.name
'Emma Stone'
>>> person.total_credits
218 
>>> person.credits.keys()
dict_keys(['Actress', 'Producer', 'Soundtrack', 'Self', 'Archive footage'])
>>> person.credits['Actress']['n_credits']
51  
>>> person.credits['Actress']['credits'][8]
{'year': '2019', 'title': 'Zombieland: Double Tap', 'description': 'Wichita'}
>>>
```
