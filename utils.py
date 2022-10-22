
import json
import statistics

# helper function to create hyperlinked text for html
def create_anchor(link_data):
    """Helper function to generate anchored html from link data.

    Args:
        link_data ([dict]): A row of data as dict

    Returns:
        [list]: Same data with hyperlink
    """
    title = link_data["title"]
    url = link_data["link"]
    hyperlink = '<a href=' + url + ' target="_blank">' + title + '</a>'

    other_data = [
        link_data["final_score"],
        link_data["author"],
        link_data["views"],
        link_data["likes"],
        ' '.join(link_data["keywords"])
        ]
    res = [hyperlink] + other_data
    return res

# To get score from the scored list (with anchored title).
# This is to enable sorting of the list containing data.
def get_score(row):
    return row[1]

# To create html table from data and write to filename
def write_to_html(target_folder, filename, sorted_list):
    table = "<table>\n"
    # Create the table's column headers
    header = ['Title', 'Score', 'Author', 'Views', 'Likes', 'Keywords']
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

def get_author_counts_dict(path_to_author_counts_dict="author_counts.json"):
    try:
        with open(path_to_author_counts_dict, 'r') as fp:
            author_counts_dict = json.load(fp)
        return author_counts_dict
    except Exception:
        return {}

def normalize_dictionary(dictionary):
    factor=1.0/sum(dictionary.values())
    normalised_dictionary = {k: v*factor for k, v in dictionary.items()}
    return normalised_dictionary

def get_median_of_frontier(frontier):
    all_scores = [tuple[0] for tuple in frontier]
    return statistics.median(all_scores)
