import re

class ExecutionNode:
    def __init__(self, action, arguments=None, children=None):
        self.action = action
        self.arguments = arguments
        self.children = children if children else []

def parse_max_threads(dsl_code):
    pattern = r'!max-threads\((\d+)\)'
    match = re.search(pattern, dsl_code)
    if match:
        max_threads = int(match.group(1))
        return ExecutionNode('max_threads', max_threads)
    else:
        return None

def parse_sql(dsl_code):
    pattern = r'!sql\((.*?)\)'
    match = re.search(pattern, dsl_code)
    if match:
        db_marker = match.group(1)
        return ExecutionNode('sql', db_marker)
    else:
        return None

def parse_folder(dsl_code):
    pattern = r'!folder\((.*?)\)'
    match = re.search(pattern, dsl_code)
    if match:
        folder_path = match.group(1)
        return ExecutionNode('folder', folder_path)
    else:
        return None

def parse_in_new_window(dsl_code):
    pattern = r'in new window url\((.*?)\)(.*?)close window'
    match = re.search(pattern, dsl_code, re.DOTALL)
    if match:
        url = match.group(1)
        inner_code = match.group(2)
        children = parse_execution_tree(inner_code)
        return ExecutionNode('in_new_window', url, children)
    else:
        return None

def parse_find_all(dsl_code):
    pattern = r'find-all\((.*?)\) -> \$([\w]+)'
    match = re.search(pattern, dsl_code)
    if match:
        selector = match.group(1)
        variable = match.group(2)
        return ExecutionNode('find_all', (selector, variable))
    else:
        return None

def parse_shuffle(dsl_code):
    pattern = r'shuffle\(\$([\w]+)\)'
    match = re.search(pattern, dsl_code)
    if match:
        variable = match.group(1)
        return ExecutionNode('shuffle', variable)
    else:
        return None

def parse_find(dsl_code):
    pattern = r'find\((.*?)\) -> \$([\w]+)'
    match = re.search(pattern, dsl_code)
    if match:
        selector = match.group(1)
        variable = match.group(2)
        return ExecutionNode('find', (selector, variable))
    else:
        return None

def parse_save_sql(dsl_code):
    pattern = r'save-sql\((.*?), \[(.*?)\]\)'
    match = re.search(pattern, dsl_code)
    if match:
        db_marker = match.group(1)
        variables = [var.strip() for var in match.group(2).split(',')]
        return ExecutionNode('save_sql', (db_marker, variables))
    else:
        return None

def parse_save_folder(dsl_code):
    pattern = r'save-folder\(\$([\w]+)\)'
    match = re.search(pattern, dsl_code)
    if match:
        variable = match.group(1)
        return ExecutionNode('save_folder', variable)
    else:
        return None

def parse_execution_tree(dsl_code):
    execution_tree = []

    for line in dsl_code.split('\n'):
        line = line.strip()
        if line.startswith('!'):
            node = None
            if line.startswith('!max-threads'):
                node = parse_max_threads(line)
            elif line.startswith('!sql'):
                node = parse_sql(line)
            elif line.startswith('!folder'):
                node = parse_folder(line)
            execution_tree.append(node)
        elif line.startswith('in new window'):
            node = parse_in_new_window(line)
            execution_tree.append(node)
        elif line.startswith('find-all'):
            node = parse_find_all(line)
            execution_tree[-1].children.append(node)
        elif line.startswith('shuffle'):
            node = parse_shuffle(line)
            execution_tree[-1].children.append(node)
        elif line.startswith('find'):
            node = parse_find(line)
            execution_tree[-1].children.append(node)
        elif line.startswith('save-sql'):
            node = parse_save_sql(line)
            execution_tree[-1].children.append(node)
        elif line.startswith('save-folder'):
            node = parse_save_folder(line)
            execution_tree[-1].children.append(node)

    return execution_tree

# Example usage
dsl_snippet = '''!max-threads(10)
!sql(news.db)
!folder(./news)


in new window url(https://meduza.io/)
find-all(.article .Link-root) -> $links
shuffle($links)
close window
in new window url($links)
  find(h1) -> $title
  find(.GeneralMaterial-article) -> $text
  find-all(.GeneralMaterial-article img) -> $images
  close window
  save-sql(news.db, [title, text])
  save-folder($images)'''

execution_tree = parse_execution_tree(dsl_snippet)

def print_execution_tree(node, indent=''):
    print(indent + node.action, node.arguments)
    for child in node.children:
        print_execution_tree(child, indent + '  ')

print_execution_tree(execution_tree[0])  # Start from the root node
