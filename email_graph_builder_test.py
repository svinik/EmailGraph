import unittest
from unittest.mock import MagicMock, ANY

from email_graph_builder import EmailGraphBuilder
import networkx as nx


class EmailGraphBuilderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(EmailGraphBuilderTest, self).__init__(*args, **kwargs)

    def setUp(self):
        self.builder = EmailGraphBuilder()

    def test_add_email_nodes_for_str_should_add_all_emails(self):
        string = 'bla bla bla foo@bar.com ha ha ha\n bar@goo.co.il'
        self.builder.graph.add_node('foo', kind='url')
        self.builder.add_email_nodes_for_str(string, 'foo')
        self.assertTrue(self.builder.graph.has_node('foo@bar.com'))
        self.assertTrue(self.builder.graph.has_node('bar@goo.co.il'))

        kinds = nx.get_node_attributes(self.builder.graph, "kind")
        self.assertTrue(kinds['foo@bar.com'] == 'email')

    def test_add_email_nodes_for_str_should_connect_url_to_email(self):
        string = 'bla bla bla foo@bar.com ha ha ha\n bar@goo.co.il'
        self.builder.graph.add_node('foo', kind='url')
        self.builder.add_email_nodes_for_str(string, 'foo')
        self.assertTrue(self.builder.graph.has_edge('foo', 'foo@bar.com'))

    def test_handle_page_with_depth_0_should_return(self):
        self.builder.handle_page('some.url.com', depth=0)
        self.assertEqual(0, self.builder.graph.number_of_nodes())

    def test_handle_page_should_add_domain(self):
        self.builder.handle_page('http://www.some-url.com/bla', depth=1)
        domain = 'www.some-url.com'
        self.assertTrue(self.builder.graph.has_node(domain))

        kinds = nx.get_node_attributes(self.builder.graph, "kind")
        self.assertEqual('domain', kinds[domain])

    def test_handle_page_should_add_url(self):
        url = 'http://www.some-url.com/bla'
        self.builder.handle_page(url, depth=1)
        self.assertTrue(self.builder.graph.has_node(url))

        kinds = nx.get_node_attributes(self.builder.graph, "kind")
        self.assertEqual('url', kinds[url])

    def test_handle_page_should_add_edge_between_domain_and_url(self):
        url = 'http://www.some-url.com/bla'
        domain = 'www.some-url.com'

        self.builder.handle_page(url, depth=1)
        self.assertTrue(self.builder.graph.has_edge(domain, url))

    def test_handle_page_should_add_all_page_emails(self):
        url = 'https://www.york.ac.uk/teaching/cws/wws/webpage1.html'
        self.builder.add_email_nodes_for_page = MagicMock()
        self.builder.handle_page(url, depth=1)
        self.builder.add_email_nodes_for_page.assert_called_once_with(ANY, url)

    def test_handle_page_should_add_linked_pages(self):
        url = 'https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple.html'
        linked_url = 'http://www.yahoo.com/'

        self.builder.add_email_nodes_for_page = MagicMock()
        self.builder.handle_page(url, depth=2)
        self.builder.add_email_nodes_for_page.assert_called_with(ANY, linked_url)


if __name__ == '__main__':
    unittest.main()
