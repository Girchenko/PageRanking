import networkx as nx


class Graph:
    def __init__(self, data):
        self.nodes_num = data[0]
        self.nodes = data[1]
        self.edges = data[2]
        self.designed_graph = ""
        self.plot_params = ""
        self.ranks_labels = []
        self.page_ranks = ""

    @staticmethod
    def set_start_rank(nodes_num):
        rank = float(1 / nodes_num)
        res = []
        for i in range(nodes_num):
            res.append(rank)
        return res

    @staticmethod
    def labels_config(nodes):
        labels = dict()
        for i in range(len(nodes)):
            labels[nodes[i]] = nodes[i]
        return labels

    def view_ranks(self, p, rank):
        s_plot = p[0]
        nodes = p[1]
        pos = p[2]
        for txt in self.ranks_labels:
            txt.set_visible(False)
        self.ranks_labels = []
        for i in range(len(nodes)):
            x, y = pos[nodes[i]]
            current_rank = s_plot.text(x, y + 0.1, s=round(rank[i], 3), bbox=dict(facecolor='white', alpha=1),
                                       horizontalalignment='center')
            self.ranks_labels.append(current_rank)

    @staticmethod
    def get_matrix(gr):
        graph_nodes = list(gr.nodes)
        matrix = list()
        num_of_successors = list()
        for i in range(gr.number_of_nodes()):
            num_of_successors.append(len(list(gr.neighbors(graph_nodes[i]))))
        for i in range(gr.number_of_nodes()):
            m_row = list()
            for j in range(gr.number_of_nodes()):
                if gr.has_successor(graph_nodes[j], graph_nodes[i]):
                    m_row.append(1 / num_of_successors[j])
                else:
                    m_row.append(0)
            matrix.append(m_row)
        return matrix

    def graph_build(self, s_plot):
        n_num = self.nodes_num
        n = self.nodes
        e = self.edges
        g = nx.DiGraph()
        g.add_nodes_from(n)
        g.add_edges_from(e)
        start_ranks = self.set_start_rank(n_num)
        labels = self.labels_config(n)
        pos = nx.spring_layout(g)
        self.plot_params = [s_plot, n, pos]
        self.view_ranks(self.plot_params, start_ranks)
        nx.draw(g, pos, ax=s_plot, arrows=True, alpha=0.8)
        nx.draw_networkx_labels(g, pos, labels, font_size=12, ax=s_plot)
        self.designed_graph = g
        self.page_ranks = start_ranks
