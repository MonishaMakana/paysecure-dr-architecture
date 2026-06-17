import os
import markdown

root = os.path.dirname(os.path.abspath(__file__))
runbook_dir = os.path.join(root, 'RUNBOOKS')
output_dir = os.path.join(root, 'docs', 'runbooks')
os.makedirs(output_dir, exist_ok=True)
md = markdown.Markdown(extensions=['fenced_code', 'tables'])

for name in os.listdir(runbook_dir):
    if name.endswith('.md'):
        source_path = os.path.join(runbook_dir, name)
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        html_body = md.reset().convert(content)
        title = content.splitlines()[0].lstrip('# ').strip() if content else 'Runbook'
        target_name = name.replace('.md', '.html')
        target_path = os.path.join(output_dir, target_name)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(
                '<!doctype html>\n'
                '<html lang="en">\n'
                '  <head>\n'
                '    <meta charset="utf-8" />\n'
                '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
                f'    <title>{title}</title>\n'
                '    <link rel="stylesheet" href="/styles.css" />\n'
                '  </head>\n'
                '  <body>\n'
                '    <main>\n'
                f'{html_body}\n'
                '    </main>\n'
                '  </body>\n'
                '</html>\n'
            )
        print('generated:', target_path)
