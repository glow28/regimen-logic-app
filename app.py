
from graphviz import Digraph
import streamlit as st

st.markdown("🧠 **Updated Parser: Capital OR block awareness + nesting logic + plus-one**")

def generate_graphviz_diagram(logic_string):
    tokens = logic_string.strip().split()
    drug_labels = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    graph = Digraph(format='png')
    graph.attr(rankdir='TB', size='10')

    graph.node('ROOT', 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='white', fontname='Helvetica')

    node_counter = 0
    def new_node_id():
        nonlocal node_counter
        node_counter += 1
        return f"N{node_counter}"

    # Split on capital OR into potential regimen blocks
    chunks = []
    temp = []
    for token in tokens:
        if token == 'OR':
            chunks.append(temp)
            temp = []
        else:
            temp.append(token)
    if temp:
        chunks.append(temp)

    for idx, chunk in enumerate(chunks):
        reg_node = f"R{idx+1}"
        # Parse each chunk depending on its structure
        if not chunk:
            continue

        if 'AND' in chunk:
            graph.node(reg_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')
            i = 0
            while i < len(chunk):
                if chunk[i] == 'AND':
                    # Detect how many ors follow
                    or_count = 0
                    j = i + 1
                    while j < len(chunk) and chunk[j] == 'or':
                        or_count += 1
                        j += 1

                    if or_count > 0:
                        # flat component + nested or
                        flat = new_node_id()
                        graph.node(flat, f'component: {next(drug_labels)}', shape='box')
                        graph.edge(reg_node, flat)

                        nested_or = new_node_id()
                        graph.node(nested_or, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
                        graph.edge(reg_node, nested_or, label='component')
                        for _ in range(or_count + 1):
                            cid = new_node_id()
                            graph.node(cid, f'component: {next(drug_labels)}', shape='box')
                            graph.edge(nested_or, cid)
                        i += or_count + 1
                    else:
                        for _ in range(2):
                            cid = new_node_id()
                            graph.node(cid, f'component: {next(drug_labels)}', shape='box')
                            graph.edge(reg_node, cid)
                        i += 1
                else:
                    i += 1

        elif 'and' in chunk:
            and_count = chunk.count('and')
            graph.node(reg_node, 'Regimen selection: all (and)', shape='box', style='filled', fillcolor='#B91C1C', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')
            for _ in range(and_count + 1):
                cid = new_node_id()
                graph.node(cid, f'component: {next(drug_labels)}', shape='box')
                graph.edge(reg_node, cid)

        elif 'or' in chunk:
            or_count = chunk.count('or')
            graph.node(reg_node, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
            graph.edge('ROOT', reg_node, label='component')
            for _ in range(or_count + 1):
                cid = new_node_id()
                graph.node(cid, f'component: {next(drug_labels)}', shape='box')
                graph.edge(reg_node, cid)

        else:
            # Single flat drug
            graph.node(reg_node, 'component', shape='box')
            graph.edge('ROOT', reg_node, label='component')

    output_path = '/tmp/kg_dynamic_logic_diagram'
    graph.render(output_path, format='png', cleanup=False)
    return f'{output_path}.png'

# --- Streamlit UI ---
st.title("Regimen Logic Diagram Generator")
logic_input = st.text_input("Enter logic string:", value="or AND or or OR OR and")
if logic_input:
    image_path = generate_graphviz_diagram(logic_input)
    st.image(image_path)
