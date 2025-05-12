import graphviz
import neat

def draw_net(config, genome, view=False, node_names=None, filename=None, show_disabled=True, prune_unused=False, node_colors=None, fmt='png'):
    dot = graphviz.Digraph(format=fmt, node_attr={'style': 'filled', 'shape': 'circle',
                                                   'fontsize': '12', 'height': '0.2', 'width': '0.2'})

    inputs = set(config.genome_config.input_keys)
    outputs = set(config.genome_config.output_keys)

    for k in inputs:
        name = node_names.get(k, str(k)) if node_names else str(k)
        dot.node(name, fillcolor='#2ecc71')

    for k in outputs:
        name = node_names.get(k, str(k)) if node_names else str(k)
        dot.node(name, fillcolor='#e74c3c')

    for k in genome.nodes:
        if k in inputs or k in outputs:
            continue
        name = node_names.get(k, str(k)) if node_names else str(k)
        dot.node(name, fillcolor='#3498db')

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            input_node = node_names.get(cg.key[0], str(cg.key[0])) if node_names else str(cg.key[0])
            output_node = node_names.get(cg.key[1], str(cg.key[1])) if node_names else str(cg.key[1])

            color = 'green' if cg.weight > 0 else 'red'
            style = 'solid' if cg.enabled else 'dotted'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(input_node, output_node, color=color, style=style, penwidth=width)

    if filename:
        dot.render(filename, view=view)
    else:
        dot.render('network.gv', view=view)
