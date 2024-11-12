import nbformat
from nbformat.v4 import new_notebook
import os
import pandas as pd
import nbconvert

# List of notebook paths to combine
DOCS_DIR = "docs/memoria"

# Get all the files in the docs directory and order them by their section number
notebook_files = [file for file in os.listdir(DOCS_DIR) if file.endswith(".ipynb")]
notebook_files_df = pd.DataFrame(
    {
        "file" : notebook_files,
        "order_str" : pd.Series(notebook_files).str.split("-").str[0]
    }
)
notebook_files_df["order"] =  pd.to_numeric(notebook_files_df["order_str"])
notebook_files_df = notebook_files_df.sort_values(by="order")
print(notebook_files_df)

# Create a new notebook
combined_notebook = new_notebook()

# Load each notebook and add its cells to the combined notebook
for notebook_file in notebook_files_df["file"].values:
    notebook_path = DOCS_DIR + "/" + notebook_file
    print(notebook_path)
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)
        combined_notebook.cells.extend(notebook.cells)

# Save the combined notebook
with open("docs/memoria.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(combined_notebook, f)
    print("Memoria combinada guardada en docs/memoria.ipynb")
    
    # Export the combined notebook to HTML
    html_exporter = nbconvert.HTMLExporter()
    html_data, resources = html_exporter.from_notebook_node(combined_notebook)

    # Save the HTML file
    with open("docs/memoria.html", "w", encoding="utf-8") as f:
        f.write(html_data)
    print("Memoria HTML guardada en docs/memoria.html")


