import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import itertools

class MarkovChain:
    """
    Create a markov chain with 4 nodes, the weights on edge = 1/p, with p equals
    to the in node. Initialise transition matrix with random weights and find
    the stable transition matrix over a number of iteration. 
    """
    def __init__(self, nodes=None, edges=None):
        self.nodes = [0, 1, 2, 3]
        self.edges = np.asarray([[1,1,1,0],
                                 [1,0,0,1],
                                 [1,0,0,1],
                                 [0,1,1,1],
                                 ])
        self.state = np.random.normal(size=4)
        self.transit = np.asarray([[1/3, 1/3, 1/3, 0],
                                   [1/2, 0, 0, 1/2],
                                   [1/2, 0, 0, 1/2],
                                   [0, 1/3, 1/3, 1/3],
                                   ]) 

    def update(self):
        self.state = self.transit @ self.state

    def edges2tuple(self):
        l = np.where(self.edges==1)
        return [(x[0].tolist(), x[1].tolist()) for x in zip(l[0],l[1])]


def anime(n):
    mc.update()
    states = [np.round(i,3) for i in mc.state]
    #print(states)
    text = [str(np.round(i,3)) for i in mc.state]
    for k,v in enumerate(states):
        container[k].set_height(v)
    ax1.set_title(f"frame {n} : State")
    leg.get_texts()[0].set_text(text[0])
    leg.get_texts()[1].set_text(text[1])
    leg.get_texts()[2].set_text(text[2])
    leg.get_texts()[3].set_text(text[3])


if __name__ == '__main__':
    print('Animate Markov Chain with 4 nodes')
    mc = MarkovChain()

    # Create a gragh
    G = nx.MultiDiGraph()
    edge_list = mc.edges2tuple()
    edge_labels = {k: np.round(mc.transit[k[0],k[1]].tolist(),3) for k in edge_list}
    for i, (u,v) in enumerate(edge_list):
        G.add_edge(u,v, w=round(i/3, 2))
    pos = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)} 
    labels = {i:k for i, k in enumerate(['A','B','C','D'])}

    fig, (ax0,ax1) = plt.subplots(1,2)

    # Plot the graph
    ax0.set_title("Plot markov chain")
    nx.draw_networkx_nodes(G, pos, ax=ax0)
    connectionstyle = [f"arc3, rad={r}" for r in itertools.accumulate([0.15]*2)]
    nx.draw_networkx_edges(G, pos, ax=ax0, connectionstyle=connectionstyle)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 connectionstyle=connectionstyle,
                                 font_color="blue", ax=ax0)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax0)

    # Plot the state (initial state)
    ax1.set_title("State")
    ax1.set_yticks([0.0])
    ax1.set_ylim(-1.0,1.0)
 
    states = [np.round(i,3) for i in mc.state]
    text = [str(np.round(i,3)) for i in mc.state]
    container = ax1.bar(['A', 'B','C','D'], states, label=text)
    (left,right) = ax1.get_xlim()
    ax1.hlines(0.0, left,right, colors = "r", linestyles='dotted')
    leg = ax1.legend(title="states")

    # Animation
    anim = animation.FuncAnimation(fig, func=anime, frames=25, repeat=False,
                                   interval=200)
    #plt.show() 
    #anim.save('MarkovChain.mp4', writer="ffmpeg")
    anim.save('MarkovChain.gif', writer="ffmpeg")
     

