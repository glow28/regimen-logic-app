from graphviz import Digraph
import streamlit as st
import tempfile
import os

st.set_page_config(layout="centered")
st.title("🧠 Regimen Logic Visualiser")
st.markdown("Version 4.0 — handles **nested AND/or**, flat logic, and **single OR components (pink)**.")

logic_string = st.text_input("Enter regimen logic (e.g. 'AND or OR OR')", "AND or OR OR OR or AND OR or AND")

if st.button("Generate Diagram"):
    tokens = logic_string.strip().split()
    drug_labels = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    graph = Digraph(format='png')
    graph.attr(rankdir='TB', size='10')
    graph.node('ROOT', 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='white', fontname='Helvetica')

    regimen_count = 0
    node_counter = [0]

    def new_node_id():
        node_counter[0] += 1
        return f"N{node_counter[0]}"

    def add_component_block(parent_node, label):
        comp_node = new_node_id()
        graph.node(comp_node, f'component: {label}', shape='box')
        graph.edge(parent_node, comp_node)

    def add_flat_group(parent_node, keyword, count=2):
        flat_node = new_node_id()
        if keyword == 'and':
            group_label = f"Regimen selection: all ({keyword})"
            fill = '#B91C1C'
        elif keyword == 'or' and count == 2:
            group_label = f"Regimen selection: exactly-one ({keyword})"
            fill = '#EC4899'  # pink
        else:
            group_label = f"Regimen selection: exactly-one ({keyword})"
            fill = '#FACC15'
        graph.node(flat_node, group_label, shape='box', style='filled', fillcolor=fill)
        graph.edge(parent_node, flat_node, label='component')
        for _ in range(count):
            add_component_block(flat_node, next(drug_labels))

    def add_nested_and_or(parent_node, position='start', count=2):
        and_node = new_node_id()
        graph.node(and_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
        graph.edge(parent_node, and_node, label='component')

        if position == 'start':
            add_component_block(and_node, next(drug_labels))
            nested_or = new_node_id()
            graph.node(nested_or, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
            graph.edge(and_node, nested_or, label='component')
            for _ in range(count):
                add_component_block(nested_or, next(drug_labels))
        elif position == 'end':
            nested_or = new_node_id()
            graph.node(nested_or, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
            graph.edge(and_node, nested_or, label='component')
            for _ in range(count):
                add_component_block(nested_or, next(drug_labels))
            add_component_block(and_node, next(drug_labels))

    def parse_regimen(start_idx):
        end_idx = start_idx
        while end_idx < len(tokens) and tokens[end_idx] != 'OR':
            end_idx += 1
        segment = tokens[start_idx:end_idx]
        has_and = 'AND' in segment
        has_or = 'or' in segment

        reg_node = f"R{start_idx}"
        regimen_label = 'Regimen selection: exactly-one (OR)'
        graph.node(reg_node, regimen_label, shape='box', style='filled', fillcolor='#1E3A8A', fontcolor='white')
        graph.edge('ROOT', reg_node, label='component')

        if has_and and has_or:
            if segment.index('AND') < segment.index('or'):
                add_nested_and_or(reg_node, position='start', count=segment.count('or') + 1)
            else:
                add_nested_and_or(reg_node, position='end', count=segment.count('or') + 1)
        elif all(t == 'or' for t in segment):
            add_flat_group(reg_node, 'or', len(segment) + 1)
        elif all(t == 'and' for t in segment):
            add_flat_group(reg_node, 'and', len(segment) + 1)
        elif len(segment) == 1 and segment[0] in ['or', 'and']:
            add_flat_group(reg_node, segment[0], 2)
        else:
            add_flat_group(reg_node, 'or', 1)

        return end_idx, end_idx

    i = 0

    # ✅ Fix: Add placeholder if first token is OR (means implicit regimen before it)
    if tokens and tokens[0] == 'OR':
        parse_regimen(0)

    while i < len(tokens):
        if tokens[i] == 'OR':
            i += 1
        i, _ = parse_regimen(i)

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = os.path.join(tmpdirname, 'regimen_logic')
        graph.render(output_path, format='png', cleanup=True)
        st.image(output_path + '.png', caption="Regimen Logic Diagram")



