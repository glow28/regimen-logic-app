import streamlit as st
from graphviz import Digraph
import tempfile
import os

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

            or_count = 0
            j = i + 1
            while j < len(tokens) and tokens[j] == 'or':
                or_count += 1
                j += 1

            if or_count > 0:
                comp_node = new_node_id()
                label = next(drug_labels)
                graph.node(comp_node, f'component: {label}', shape='box')
                graph.edge(reg_node, comp_node)

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
                for _ in range(2):
                    comp_node = new_node_id()
                    label = next(drug_labels)
                    graph.node(comp_node, f'component: {label}', shape='box')
                    graph.edge(reg_node, comp_node, label='component')
                i += 1
        else:
            i += 1

    if tokens and tokens[-1] == 'OR':
        regimen_count += 1
        reg_node = f"R{regimen_count}"
        graph.node(reg_node, 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='#1E3A8A', fontcolor='white')
        graph.edge('ROOT', reg_node, label='component')
        comp_node = new_node_id()
        label = next(drug_labels)
        graph.node(comp_node, f'component: {label}', shape='box')
        graph.edge(reg_node, comp_node)

    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, "graph")
    graph.render(path, format='png', cleanup=True)
    return f"{path}.png"

# ---- Streamlit App UI ----
st.set_page_config(page_title="Regimen Logic Visualiser", layout="centered")
st.title("🧠 Regimen Logic Visualiser")
st.markdown("Enter a logic string like `OR OR AND or or`, and it will generate the structure diagram.")

logic_input = st.text_input("Enter logic string:", value="OR OR OR AND or or")

if logic_input:
    image_path = generate_graphviz_diagram(logic_input)
    st.image(image_path, caption="Generated Diagram", use_column_width=True)
