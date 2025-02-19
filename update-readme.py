import os
import re
from datetime import datetime
import glob

def extract_title_from_tex(tex_file):
    """Extract title from LaTeX file."""
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for \title{...} pattern
            title_match = re.search(r'\\title{([^}]*)}', content)
            if title_match:
                title = title_match.group(1)
                # Check if title contains multiple words
                if len(title.split()) > 1:
                    return title
    except Exception as e:
        print(f"Error reading {tex_file}: {e}")
    return None

def get_earliest_file_date(folder):
    """Get the earliest file creation date in the folder."""
    earliest_date = datetime.now()
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_date = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_date < earliest_date:
                    earliest_date = file_date
            except Exception as e:
                print(f"Error getting date for {file_path}: {e}")
    return earliest_date

def update_readme():
    """Update README.md with paper titles and PDF links."""
    papers = []
    whitepaper = None
    
    # Process each top-level directory
    for folder in [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]:
        # Find TEX files
        tex_files = glob.glob(os.path.join(folder, '*.tex'))
        # Find PDF files
        pdf_files = glob.glob(os.path.join(folder, '*.pdf'))
        
        if tex_files and pdf_files:
            title = extract_title_from_tex(tex_files[0])
            if not title:
                continue  # Skip if no multi-word title found
            
            earliest_date = get_earliest_file_date(folder)
            
            paper_info = {
                'title': title,
                'pdf_path': pdf_files[0],
                'date': earliest_date
            }
            
            # Check if this is the whitepaper
            if 'whitepaper' in folder.lower() or 'whitepaper' in title.lower():
                whitepaper = paper_info
            else:
                papers.append(paper_info)
    
    # Sort papers by date (newest first)
    papers.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate README content
    readme_content = "# Saito Papers\n\n"
    readme_content += "This is a collection of academic papers related to Saito research and development. "
    readme_content += "The papers are listed in chronological order, with the most recent first.\n\n"
    
    # Add whitepaper section
    readme_content += "## Saito Whitepaper\n\n"
    if whitepaper:
        relative_path = whitepaper['pdf_path'].replace('\\', '/')
        readme_content += f"- [{whitepaper['title']}]({relative_path})\n\n"
    
    # Add other papers section
    readme_content += "## Mechanism Design and Economics\n\n"
    for paper in papers:
        relative_path = paper['pdf_path'].replace('\\', '/')
        readme_content += f"- [{paper['title']}]({relative_path})\n"
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()