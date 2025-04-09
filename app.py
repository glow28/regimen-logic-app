import streamlit as st
from graphviz import Digraph
import tempfile
from PIL import Image

def generate_graphviz_diagram(logic_string):
    tokens = logic_string.strip().split()
    drug_labels = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    graph = Digraph(format='png')
    graph.attr(rankdir='TB', size='10')

    graph.node('ROOT', 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='white', fontname='Helvetica')

    regimen_count = 0
    node_count = 0

    def new_node_id():
        nonlocal node_count
        node_count += 1
        return f"N{node_count}"

    i = 0
    # Handle pre-OR regimen (before first OR)
    if tokens[0] != 'OR':
        regimen_count += 1
        reg_node = f"R{regimen_count}"
        graph.node(reg_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
        graph.edge('ROOT', reg_node, label='component')

        if tokens[0] == 'AND':
            # Flat AND
            for _ in range(2):
                comp_node = new_node_id()
                label = next(drug_labels)
                graph.node(comp_node, f'component: {label}', shape='box')
                graph.edge(reg_node, comp_node)
            i = 1
        elif tokens[0] == 'or':
            # Nested OR inside ALL
            nested = new_node_id()
            graph.node(nested, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
            graph.edge(reg_node, nested, label='component')

            or_count = 1
            while i + or_count < len(tokens) and tokens[i + or_count] == 'or':
                or_count += 1
            for _ in range(or_count + 1):
                comp_node = new_node_id()
                label = next(drug_labels)
                graph.node(comp_node, f'component: {label}', shape='box')
                graph.edge(nested, comp_node)
            i += or_count
        elif tokens[0] == 'AND':
            # Already handled above
            pass
        else:
            # Single component
            comp_node = new_node_id()
            label = next(drug_labels)
            graph.node(comp_node, f'component: {label}', shape='box')
            graph.edge(reg_node, comp_node)
            i += 1

    while i < len(tokens):
        token = tokens[i]

        if token == 'OR':
            regimen_count += 1
            reg_node = f"R{regimen_count}"
            graph.node(reg_node, 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='#1E3A8A', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')
            comp_node = new_node_id()
            label = next(drug_labels)
            graph.node(comp_node, f'component: {label}', shape='box')
            graph.edge(reg_node, comp_node)
            i += 1

        elif token == 'AND':
            regimen_count += 1
            reg_node = f"R{regimen_count}"
            graph.node(reg_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')

            # Count following lowercase ors
            or_count = 0
            j = i + 1
            while j < len(tokens) and tokens[j] == 'or':
                or_count += 1
                j += 1

            if or_count > 0:
                # One flat component
                comp_node = new_node_id()
                label = next(drug_labels)
                graph.node(comp_node, f'component: {label}', shape='box')
                graph.edge(reg_node, comp_node)

                # Nested OR
                nested = new_node_id()
                graph.node(nested, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
                graph.edge(reg_node, nested, label='component')

                for _ in range(or_count + 1):
                    comp_node = new_node_id()
                    label = next(drug_labels)
                    graph.node(comp_node, f'component: {label}', shape='box')
                    graph.edge(nested, comp_node)
                i += or_count + 1
            else:
                # Flat AND block
                for _ in range(2):
                    comp_node = new_node_id()
                    label = next(drug_labels)
                    graph.node(comp_node, f'component: {label}', shape='box')
                    graph.edge(reg_node, comp_node)
                i += 1
        else:
            i += 1

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    graph.render(tmpfile.name, format='png', cleanup=True)
    return tmpfile.name + ".png"


# Streamlit UI
st.title("💊 Regimen Logic Visualiser")
logic_input = st.text_input("Enter logic string:", value="or AND OR OR OR OR and")

if logic_input:
    path = generate_graphviz_diagram(logic_input)
    st.image(Image.open(path), caption="Generated Diagram")
