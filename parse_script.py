import ast
import json
import argparse
import os

def extract_chat_data(source_path, output_path):
    """
    Parses a Python script to extract chat data stored in a specific structure
    and saves it as a JSON file.

    Args:
        source_path (str): The path to the source Python script.
        output_path (str): The path to save the output JSON file.
    """
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Source file not found at {source_path}")
        return

    tree = ast.parse(source_code)
    chat_data = []

    # Find the top-level 'contents' assignment node first
    contents_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == 'contents' for t in node.targets):
                contents_node = node
                break

    # Process the found node
    if contents_node and isinstance(contents_node.value, ast.List):
        for element in contents_node.value.elts:
            # Each element is a types.Content(...) call
            if isinstance(element, ast.Call):
                role = ''
                parts_text = []
                for keyword in element.keywords:
                    if keyword.arg == 'role':
                        if isinstance(keyword.value, ast.Constant):
                            role = keyword.value.value
                    elif keyword.arg == 'parts':
                        if isinstance(keyword.value, ast.List):
                            for part_call in keyword.value.elts:
                                # Each part is a types.Part.from_text(...) call
                                if isinstance(part_call, ast.Call):
                                    for part_kw in part_call.keywords:
                                        if part_kw.arg == 'text':
                                            if isinstance(part_kw.value, ast.Constant):
                                                parts_text.append(part_kw.value.value)
                
                # Relaxed condition: only require a role to include the entry.
                # This prevents skipping entries with empty parts.
                if role:
                    chat_data.append({
                        'role': role,
                        'parts': [{'text': text} for text in parts_text]
                    })
    
    if not chat_data:
        print("Could not find or parse the 'contents' data structure in the script.")
        return

    # Write the extracted data to a JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully extracted data to {output_path}")
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse a Python script to extract Gemini chat data.")
    parser.add_argument('source_file', type=str, help='The path to the source Python script.')
    parser.add_argument('-o', '--output_file', type=str, help='The path to save the output JSON file. Defaults to the source file name with a .json extension.')
    
    args = parser.parse_args()
    
    source_path = args.source_file
    output_path = args.output_file
    
    if not output_path:
        base_name = os.path.splitext(source_path)[0]
        output_path = f"{base_name}.json"
        
    extract_chat_data(source_path, output_path)
