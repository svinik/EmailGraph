import sys
import json
import pickle

from email_graph_builder import EmailGraphBuilder
from top_pages import get_top_k_pages

if __name__ == '__main__':
    assert len(sys.argv) >= 3

    builder = EmailGraphBuilder()
    depth = int(sys.argv[2])

    print("----- Start building graph -----")
    with open(sys.argv[1]) as file:
        for url in file:
            builder.handle_page(url.strip(), depth=depth)

    with open('graph.pkl', 'wb') as handle:
        pickle.dump(builder.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("----- Finished building graph -----")

    top_pages = get_top_k_pages(k=5, graph=builder.graph)

    with open('top_urls.txt', 'w+') as top_urls_file:
        top_urls_file.write(json.dumps(top_pages))
