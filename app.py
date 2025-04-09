from graphviz import Digraph
import streamlit as st

st.markdown("🔪 **Version: Full nested + plus-one logic (OR and AND)**")

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

    # Special case: logic starts with 'or AND'
    if len(tokens) >= 2 and tokens[0] == 'or' and tokens[1] == 'AND':
        regimen_count += 1
        reg_node = f"R{regimen_count}"
        graph.node(reg_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
        graph.edge('ROOT', reg_node, label='component')

        # Flat component
        comp_node = new_node_id()
        graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
        graph.edge(reg_node, comp_node, label='component')

        # Nested OR
        nested_or = new_node_id()
        graph.node(nested_or, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
        graph.edge(reg_node, nested_or, label='component')
        for _ in range(2):
            comp_node = new_node_id()
            graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
            graph.edge(nested_or, comp_node)

        i = 2

    while i < len(tokens):
        token = tokens[i]

        if token == 'OR':
            # Count how many in a row (plus-one logic)
            or_count = 1
            while i + or_count < len(tokens) and tokens[i + or_count] == 'OR':
                or_count += 1

            regimen_count += 1
            reg_node = f"R{regimen_count}"
            graph.node(reg_node, 'Regimen selection: exactly-one (OR)', shape='box', style='filled', fillcolor='#1E3A8A', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')

            for _ in range(or_count + 1):  # n ORs = n+1 components
                comp_node = new_node_id()
                graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
                graph.edge(reg_node, comp_node)

            i += or_count

        elif token == 'AND':
            regimen_count += 1
            reg_node = f"R{regimen_count}"
            graph.node(reg_node, 'Regimen selection: all (AND)', shape='box', style='filled', fillcolor='#8B0000', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')

            # Count small ors for nested block
            or_count = 0
            j = i + 1
            while j < len(tokens) and tokens[j] == 'or':
                or_count += 1
                j += 1

            if or_count > 0:
                # Flat component + nested OR block
                comp_node = new_node_id()
                graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
                graph.edge(reg_node, comp_node)

                nested = new_node_id()
                graph.node(nested, 'Regimen selection: exactly-one (or)', shape='box', style='filled', fillcolor='#FACC15')
                graph.edge(reg_node, nested, label='component')

                for _ in range(or_count + 1):
                    comp_node = new_node_id()
                    graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
                    graph.edge(nested, comp_node)

                i += or_count + 1
            else:
                for _ in range(2):
                    comp_node = new_node_id()
                    graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
                    graph.edge(reg_node, comp_node)
                i += 1

        elif token == 'and':
            and_count = 1
            while i + and_count < len(tokens) and tokens[i + and_count] == 'and':
                and_count += 1

            regimen_count += 1
            reg_node = f"R{regimen_count}"
            graph.node(reg_node, 'Regimen selection: all (and)', shape='box', style='filled', fillcolor='#B91C1C', fontcolor='white')
            graph.edge('ROOT', reg_node, label='component')

            for _ in range(and_count + 1):
                comp_node = new_node_id()
                graph.node(comp_node, f'component: {next(drug_labels)}', shape='box')
                graph.edge(reg_node, comp_node)

            i += and_count
        else:
            i += 1

    output_path = '/tmp/kg_dynamic_logic_diagram'
    graph.render(output_path, format='png', cleanup=False)
    return f'{output_path}.png'

# --- Streamlit UI ---
st.title("Regimen Logic Diagram Generator")
logic_input = st.text_input("Enter logic string:", value="or or AND or")
if logic_input:
    image_path = generate_graphviz_diagram(logic_input)
    st.image(image_path)



