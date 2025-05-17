#!/usr/bin/env python3

# Requires:
# pip3 install Jinja2

import os
from jinja2 import Environment, FileSystemLoader, exceptions

# --- Configuration ---
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.'
TEMPLATE_EXTENSIONS = ('.html')
GLOBAL_CONTEXT = {
    # 'something': 'Example'
}
# ---------------------

def render_template_to_file(template_name, env, context):
  template = env.get_template(template_name)
  rendered_output = template.render(context)
  output_file_path = os.path.join(OUTPUT_DIR, template_name)

  # Ensure the output directory exists
  os.makedirs(OUTPUT_DIR, exist_ok=True)

  with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(rendered_output)

  print(f"Successfully rendered '{template_name}' to '{output_file_path}'")


def main():
  env = Environment(
          loader=FileSystemLoader(TEMPLATE_DIR),
          trim_blocks=False,
          lstrip_blocks=False
        )

  for root, _, files in os.walk(TEMPLATE_DIR):
    for file in files:
      relative_path = os.path.relpath(os.path.join(root, file), TEMPLATE_DIR)

      if relative_path.lower().endswith(TEMPLATE_EXTENSIONS):
        current_context = GLOBAL_CONTEXT.copy()
        render_template_to_file(relative_path, env, current_context)
      else:
        print(f"Skipping file: '{relative_path}'")


if __name__ == "__main__":
  main()
