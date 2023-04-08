class NodeUtils:
    #  __metaclass__ = ABCMeta


    def serialize_relationships(self, nodes):
        serialized_nodes = []
        for node in nodes:
            # serialize node
            serialized_node = node.serialize

            serialized_nodes.append(serialized_node)

        return serialized_nodes
