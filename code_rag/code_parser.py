from tree_sitter import Language, Parser
import os
from graphviz import Digraph

def build_py_language():
    Language.build_library(
        # 存储生成的语言库的路径
        'build/my-languages.so',
        # 包含语法的仓库路径
        ['vendor/tree-sitter-python']
    )

# 检查语言库是否存在，如果不存在则构建
if not os.path.exists('build/my-languages.so'):
    build_py_language()

# 加载Tree-sitter Python语言库
PY_LANGUAGE = Language('build/my-languages.so', 'python')

def parse_python_file(file_path):
    parser = Parser()
    parser.set_language(PY_LANGUAGE)

    with open(file_path, 'r') as file:
        code = file.read()

    tree = parser.parse(bytes(code, 'utf8'))
    return tree

def traverse_tree(node, level=0):
    result = '  ' * level + f"{node.type}: {node.text.decode('utf8')}\n"
    for child in node.children:
        result += traverse_tree(child, level + 1)
    return result

def create_ast_graph(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph(comment='Abstract Syntax Tree')
        graph.attr(rankdir='TB')

    node_id = str(id(node))
    label = f"{node.type}\n{node.text.decode('utf8')[:20]}"
    graph.node(node_id, label)

    if parent:
        graph.edge(str(id(parent)), node_id)

    for child in node.children:
        create_ast_graph(child, graph, node)

    return graph

def process_python_files(directory, output_file, graph_output_dir):
    with open(output_file, 'w') as out_file:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    out_file.write(f"Processing file: {file_path}\n")
                    tree = parse_python_file(file_path)
                    out_file.write(traverse_tree(tree.root_node))
                    out_file.write("\n\n")

                    # 生成图形
                    graph = create_ast_graph(tree.root_node)
                    graph_file = os.path.join(graph_output_dir, f"{os.path.basename(file_path)}.png")
                    graph.render(graph_file, format='png', cleanup=True)
                    print(f"AST graph for {file_path} has been saved to {graph_file}")

if __name__ == "__main__":
    # 指定要解析的Python项目目录
    project_directory = '/Users/mac/Desktop/gpt_test/auto_coder_test'
    output_file = 'ast_output.txt'
    graph_output_dir = 'ast_graphs'
    
    if not os.path.exists(graph_output_dir):
        os.makedirs(graph_output_dir)
    
    process_python_files(project_directory, output_file, graph_output_dir)
    print(f"AST analysis has been written to {output_file}")
    print(f"AST graphs have been saved in {graph_output_dir}")