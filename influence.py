import networkx as nx
import numpy as np
import random

# 计算节点集的影响力
def influence_computation_IC(seed):
    influence = 0
    if len(seed) == 0: # 种子为0 直接返回0 -> 无影响力
        return influence

    for i in range(R):
        result_list = []
        result_list.extend(seed)

        # 保存**的状态
        checked = np.zeros(g.number_of_nodes()) 
        for node in result_list:
            checked[node] = 1

        # 当前节点不为空，进行影响
        while len(result_list) != 0:
            influence += 1
            current_node = result_list.pop(0)
            for nbr in g.neighbors(current_node): # 得到当前节点的邻居节点
                if checked[nbr] == 0:
                    wt = g.get_edge_data(current_node, nbr)
                    if random.uniform(0,1) < wt['weight']:
                        checked[nbr] = 1
                        result_list.append(nbr)

    return influence/R

if __name__ == "__main__":
    k = 5 # 影响力最大的几个点，这里设置为三个点
    R = 10000 # 传播过程 一般 10000次
    seed = []
    node_list = []
    
    g = nx.read_graphml('') # 空手道俱乐部

    for edge in g.edges:
        g.add_edge(edge[0], edge[1], weight=random.uniform(0,1)) # 权值为(0,1)
    
    for i in range(k):
        f = np.zeros(g.number_of_nodes())
        state = np.zeros(g.number_of_nodes())
        for v in seed:
            state[v] = 1
        for v in g.nodes:
            node_list.extend(seed)
            if state[v] == 0:
                node_list.append(v)
                f[v] = influence_computation_IC(node_list) - influence_computation_IC(seed)  
            node_list.clear()
        print(f)
        seed.append(f.argmax()) 
    print(seed)

