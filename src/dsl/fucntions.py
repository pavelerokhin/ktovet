import re


def parse_max_threads(dsl_code):
    pattern = r'!max-threads\((\d+)\)'
    match = re.search(pattern, dsl_code)
    if match:
        max_threads = int(match.group(1))
        return max_threads
    else:
        # Handle parsing error
        return None


def parse_url(dsl_code):
    pattern = r'url\((.*?)\)'
    match = re.search(pattern, dsl_code)
    if match:
        url = match.group(1)
        return url
    else:
        # Handle parsing error
        return None


def parse_find_all(dsl_code):
    pattern = r'find-all\((.*?)\) -> \$([\w]+)'
    match = re.search(pattern, dsl_code)
    if match:
        selector = match.group(1)
        variable = match.group(2)
        return selector, variable
    else:
        # Handle parsing error
        return None, None


def parse_shuffle(dsl_code):
    pattern = r'shuffle\(\$([\w]+)\)'
    match = re.search(pattern, dsl_code)
    if match:
        variable = match.group(1)
        return variable
    else:
        # Handle parsing error
        return None


def parse_in_new_window(dsl_code):
    pattern = r'in new window (.*?)\n\s+find\((.*?)\) -> \$([\w]+)\n\s+find\((.*?)\) -> \$([\w]+)'
    match = re.search(pattern, dsl_code, re.DOTALL)
    if match:
        url = match.group(1)
        title_selector = match.group(2)
        title_variable = match.group(3)
        text_selector = match.group(4)
        text_variable = match.group(5)
        return url, title_selector, title_variable, text_selector, text_variable
    else:
        # Handle parsing error
        return None, None, None, None, None


# Example usage
dsl_snippet = """
!max-threads(10)
url(https://meduza.io/)
find-all(.article .Link-root) -> $links
shuffle($links)
in new window url($links)
  find(h1) -> $title
  find(.GeneralMaterial-article) -> $text
"""

max_threads = parse_max_threads(dsl_snippet)
url = parse_url(dsl_snippet)
selector, variable = parse_find_all(dsl_snippet)
shuffled_variable = parse_shuffle(dsl_snippet)
new_window_url, title_selector, title_variable, text_selector, text_variable = parse_in_new_window(dsl_snippet)

print(f"Max Threads: {max_threads}")
print(f"URL: {url}")
print(f"Find All Selector: {selector}, Variable: {variable}")
print(f"Shuffled Variable: {shuffled_variable}")
print(f"New Window URL: {new_window_url}")
print(f"Title Selector: {title_selector}, Variable: {title_variable}")
print(f"Text Selector: {text_selector}, Variable: {text_variable}")