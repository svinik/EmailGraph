# Email Graph

Email Graph is a web crawler that will search the web for valid e-mail
addresses that can later be used for various purposes.

It will also answer the question `what are the most important URLs per domain (top 5)?`

The graph will be written to a file graph.pkl, and the top urls will be written to top_urls.pkl.

The graph will be a kind of Tri-partite graph, where one side is the domains, the second side is the urls and the third side is the emails. Each domain has an edge to all his urls. Each url has an edge to all his linked urls. Each url has an edge to all the emails appearing in its content.

A url importance is calculated by how many emails are reachable from it.

## Install
```commandline
pip install -r requirements.txt
```

## Run
```commandline
python main.py urls.txt depth <graph.pkl> 
```
* `urls.txt` - A file with valid urls to crawl. One url per line.

* `depth` - the depth of the crawler search, i.e. the largest size of urls path

* `graph.pkl` - optional pickle file for the graph, if specified the graph will not be crawled

## Output
* `graph.pkl` - pickle of the representation graph

* `top_urls.txt` - a text file mapping each domain to its top 5 urls

## Limitations

* Due to performance issues the number of linked urls for a certain url is limited to 20.

* The growth in number of urls is exponential, a higher number than 3 might take a long time.

* Some urls will cause some errors while parsing them (Forbidden, timeout, unicode) the crawler will skip such pages.