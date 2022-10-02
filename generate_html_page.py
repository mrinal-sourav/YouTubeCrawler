
#%%
from pathlib import Path

def find_repo(path):
    "Find repository root from the path's parents"
    for path in Path(path).parents:
        # Check whether "path/.git" exists and is a directory
        git_dir = path / ".git"
        if git_dir.is_dir():
            return path

# Find the repo root where the script is
find_repo("./music/english/Friction Imagine Dragons Audio YouTube.html")


# To create html table from data and write to filename
def write_to_html2(filename, sorted_list):
    table = "<table>\n"
    # Create the table's column headers
    header = ['Title', 'Score', 'Author', 'Views', 'Likes']
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

    # Create the table's row data
    for row in sorted_list:
        table += "  <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(column)
        table += "  </tr>\n"

    table += "</table>"

    with open(target_folder+filename, "w") as f:
        f.writelines(table)