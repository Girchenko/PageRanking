class GraphConfig:

    @staticmethod
    def read_from_file(filename):
        try:
            with open(filename, 'r') as f_in:
                read_data = f_in.read()
            f_in.close()
        except FileNotFoundError:
            f_in = open(filename, 'w')
            read_data = ''
            f_in.close()
        return read_data

    @staticmethod
    def data_to_fields(file_data):
        lines = file_data.split("\n")
        nodes_num = int(lines[0])
        eps = int(lines[1])
        nodes_text = ""
        for i in range(2, nodes_num + 2):
            nodes_text += str(lines[i]) + "\n"
        edges_text = ""
        for i in range(nodes_num + 2, len(lines)):
            edges_text += str(lines[i]) + "\n"
        return [str(nodes_num), nodes_text, edges_text, str(eps)]

    @staticmethod
    def data_proceed(nodes_n, nodes, edges):
        nodes = nodes.split("\n")
        edges = edges.split("\n")
        nodes_list = list()
        for i in range(nodes_n):
            nodes_list.append(nodes[i])
        edges_list = list()
        for i in range(len(edges)):
            ed = edges[i].split(" ")
            if len(ed) > 1:
                edge = (ed[0], ed[1])
                edges_list.append(edge)
        res = [nodes_n, nodes_list, edges_list]
        return res
