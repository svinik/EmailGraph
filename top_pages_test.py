import unittest

from top_pages import *


class TopPagesTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TopPagesTest, self).__init__(*args, **kwargs)

    def setUp(self):
        self.graph = nx.DiGraph()
        self.graph.add_node('foo', kind='domain')
        self.graph.add_node('bar', kind='url')
        self.graph.add_node('doo', kind='url')
        self.graph.add_node('foo@bar.com', kind='email')
        self.graph.add_node('goo@bar.com', kind='email')
        nx.add_path(self.graph, ['foo', 'bar', 'foo@bar.com'])
        nx.add_path(self.graph, ['foo', 'bar', 'goo@bar.com'])
        nx.add_path(self.graph, ['foo', 'doo', 'goo@bar.com'])

        self.graph.add_node('moo', kind='domain')
        self.graph.add_node('noo', kind='url')
        self.graph.add_node('moo@noo.com', kind='email')
        nx.add_path(self.graph, ['moo', 'noo', 'moo@noo.com'])

    def test_calc_page_weight_should_return_correct_weight(self):
        paths = dict(nx.all_pairs_shortest_path(self.graph))
        kinds = nx.get_node_attributes(self.graph, "kind")

        weight = calc_page_weight('bar', paths, kinds)
        self.assertEqual(weight, 2)

    def test_calc_page_weight_should_raise_exception_on_illegal_url(self):
        paths = dict(nx.all_pairs_shortest_path(self.graph))
        kinds = nx.get_node_attributes(self.graph, "kind")

        with self.assertRaises(ValueError):
            calc_page_weight('illegal node', paths, kinds)

    def test_get_top_k_pages_for_domain_return_correct_pages(self):
        paths = dict(nx.all_pairs_shortest_path(self.graph))
        kinds = nx.get_node_attributes(self.graph, "kind")

        top_pages = get_top_k_pages_for_domain(1, paths, 'foo', self.graph, kinds)
        self.assertEqual(top_pages, ['bar'])

    def test_get_top_k_pages_for_domain_with_k_gt_n_should_return_all_pages(self):
        paths = dict(nx.all_pairs_shortest_path(self.graph))
        kinds = nx.get_node_attributes(self.graph, "kind")

        top_pages = get_top_k_pages_for_domain(3, paths, 'foo', self.graph, kinds)
        self.assertEqual(top_pages, ['bar', 'doo'])

    def test_get_top_k_pages_should_return_correct_pages_for_domain(self):
        top_pages = get_top_k_pages(1, self.graph)
        self.assertEqual(top_pages, {'foo': ['bar'], 'moo': ['noo']})


if __name__ == '__main__':
    unittest.main()
