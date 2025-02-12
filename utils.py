
import yaml

def load_yaml_config(file_path):
    """Load a YAML configuration file."""
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

def df_to_html(
        df,
        output_file="output.html",
        url_column="link",
        title_column="title",
        highlight_column="is_seed"
        ):
    """
    Converts a Pandas DataFrame to an HTML file with hyperlinks.

    :param df: Pandas DataFrame containing the data
    :param url_column: The column name containing URLs
    :param output_file: The output HTML file name
    """
    # Ensure required columns exist
    if url_column not in df.columns:
        raise ValueError(f"Column '{url_column}' not found in DataFrame")
    if title_column not in df.columns:
        raise ValueError(f"Column '{title_column}' not found in DataFrame")
    if highlight_column not in df.columns:
        raise ValueError(f"Column '{highlight_column}' not found in DataFrame")


    # Convert URLs to clickable links with titles as text
    df[title_column] = df.apply(lambda row: f'<a href="{row[url_column]}" target="_blank">{row[title_column]}</a>', axis=1)
    df = df.drop(url_column, axis=1)

    # Convert DataFrame to HTML with row highlighting
    def highlight_row(row):
        return 'background-color: orange;' if str(row[highlight_column]).lower() == 'true' else ''

    styled_table = df.style.apply(lambda row: [highlight_row(row)] * len(row), axis=1).to_html(escape=False)

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Table</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
        <h2>Data Table with Hyperlinks</h2>
        """ + styled_table + """
        </body>
        </html>
        """)

    print(f"HTML file '{output_file}' has been created successfully.")

# Example usage
# data = {
#     "Name": ["Google", "OpenAI", "GitHub"],
#     "Website": ["https://www.google.com", "https://www.openai.com", "https://www.github.com"]
# }
# df = pd.DataFrame(data)
# df_to_html(df, "Website")

