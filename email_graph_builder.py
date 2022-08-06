import re
from urllib.parse import urlparse
from urllib.request import urlopen

import networkx as nx
import validators
from bs4 import BeautifulSoup

EMAIL_PATTERN = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"


def extract_domain(url: str) -> str:
    return urlparse(url).netloc


class EmailGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_email_nodes_for_page(self, page, page_url: str) -> None:
        try:
            decoded = page.decode('utf8')
        except UnicodeDecodeError:
            print('Error decoding page')
            return

        self.add_email_nodes_for_str(decoded, page_url)

    def add_email_nodes_for_str(self, string: str, url: str) -> None:
        for line in string.splitlines():
            for email in re.findall(EMAIL_PATTERN, line):
                self.graph.add_node(email, kind='email')
                self.graph.add_edge(url, email)
                print(email + ' email added')

    def handle_page(self, page_url: str, depth: int = 3, width: int = 20) -> None:
        if depth == 0:
            return

        if self.graph.has_node(page_url):
            return

        domain = extract_domain(page_url)
        if not self.graph.has_node(domain):
            self.graph.add_node(domain, kind='domain')
            print(domain + ' domain added')

        self.graph.add_node(page_url, kind='url')
        self.graph.add_edge(domain, page_url)
        print(page_url + ' url added')

        try:
            page = urlopen(page_url, timeout=5).read()
        except:
            print('Error fetching page')
            return

        self.add_email_nodes_for_page(page, page_url)

        # advance recursively for all pointed pages
        soup = BeautifulSoup(page)
        i = 0
        for link in soup.findAll('a'):
            href = link.get('href')
            if href is not None and validators.url(href):
                if i >= width:
                    return
                self.handle_page(href, depth - 1, width)
                i += 1
