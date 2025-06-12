import re
import csv
from bs4 import BeautifulSoup

MANUAL_COUNTRY_MAP = {
    "Czech Republic": "cz", "North Korea": "kp", "South Korea": "kr", "Taiwan": "tw",
    "United Kingdom": "gb", "Turkey": "tr", "Slovakia": "sk", "Russia": "ru",
    "Moldova": "md", "Bolivia": "bo", "Iran": "ir", "Venezuela": "ve",
    "Vietnam": "vn", "United States": "us", "Czechia": "cz"
}

def get_country_code(country_name):
    """Gets the 2-letter ISO code for a country name."""
    if country_name in MANUAL_COUNTRY_MAP:
        return MANUAL_COUNTRY_MAP[country_name]
    try:
        import pycountry
        return pycountry.countries.lookup(country_name).alpha_2.lower()
    except (LookupError, ModuleNotFoundError):
        print(f"Could not find code for: {country_name}")
        return None

def get_color_class(referendum_law, threshold):
    """Determines the CSS class based on the coloring rules."""
    if referendum_law == 'No':
        return 'no-referendum'
    
    threshold_str = str(threshold).lower()
    if 'no standing requirement' in threshold_str:
        return 'historic-no-threshold'
    if 'none' in threshold_str:
        return 'no-threshold'
        
    if 'n/a' in threshold_str or threshold_str == '-':
        return 'no-spec-threshold'

    if 'double majority' in threshold_str:
        return 'threshold-high'

    match = re.search(r'(\d+)', threshold_str)
    if match:
        percent = int(match.group(1))
        if percent <= 25: return 'threshold-low'
        if percent < 40: return 'threshold-mid'
        if percent < 50: return 'threshold-mid-high'
        return 'threshold-high'
            
    return 'no-spec-threshold'

def clean_wikitext(text):
    """Removes common wikitext markup."""
    text = re.sub(r'<ref>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', text)
    text = re.sub(r'\[\[(.*?)\]\]', r'\1', text)
    text = re.sub(r'\{\{.*?\}\}', '', text)
    text = text.replace('<br />', ' ').strip()
    return text

def parse_wikitable(wikitext):
    """Parses the wikitext to extract country data."""
    countries = []
    table_rows = wikitext.split('|-')
    
    for row in table_rows:
        if not row.strip() or row.startswith('!'):
            continue

        columns = row.strip().split('||')
        if len(columns) < 4:
            continue
            
        country_col = columns[0]
        country_match = re.search(r'\[\[(.*?)\]\]', country_col)
        country_name = country_match.group(1).split('|')[-1] if country_match else 'N/A'

        law_col = columns[1]
        if 'Yes check.svg' in law_col:
            referendum_law = 'Yes'
        elif 'X mark.svg' in law_col:
            referendum_law = 'No'
        else:
            referendum_law = 'Unclear'
        
        if country_name == 'Czech Republic' and 'No on state level' in law_col:
            referendum_law = 'No'

        threshold_col = columns[3]
        threshold = clean_wikitext(threshold_col)

        countries.append({'name': country_name, 'law': referendum_law, 'threshold': threshold})

    return countries

def main():
    """Main function to generate the colored map."""
    try:
        with open('Wikipedia data', 'r', encoding='utf-8') as f:
            wikitext = f.read()
    except FileNotFoundError:
        print("Error: 'Wikipedia data' file not found.")
        return

    country_data = parse_wikitable(wikitext)
    
    with open('BlankMap-World.svg', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Referendum Turnout Threshold by Country"

    css_styles = """
    .no-referendum { fill: #ff0000 !important; }
    .no-spec-threshold { fill: #4F4F4F !important; }
    .no-threshold { fill: #008F00 !important; }
    .historic-no-threshold { fill: #90ee90 !important; }
    .threshold-low { fill: #add8e6 !important; }
    .threshold-mid { fill: #4682b4 !important; }
    .threshold-mid-high { fill: #1e90ff !important; }
    .threshold-high { fill: #0000cd !important; }
    """
    
    style_tag = soup.find('style')
    if style_tag:
        style_tag.string = css_styles + style_tag.string
    else:
        new_style_tag = soup.new_tag('style', id='style_css_sheet', type='text/css')
        new_style_tag.string = css_styles
        soup.svg.insert(0, new_style_tag)

    all_paths = soup.find_all('path')
    for country in country_data:
        code = get_country_code(country['name'])
        if not code:
            continue
            
        color_class = get_color_class(country['law'], country['threshold'])
        
        # Find all paths that have this country's code in their class list
        country_paths = [p for p in all_paths if f' {code} ' in f" {' '.join(p.get('class', []))} "]

        if not country_paths:
            # Fallback for elements where the ID is the code
            element = soup.find(id=code)
            if element:
                if element.name == 'path':
                    country_paths = [element]
                elif element.name == 'g':
                    country_paths = element.find_all('path')

        if not country_paths:
            print(f"Warning: Could not find any SVG paths for {country['name']} ({code})")
            continue

        for path in country_paths:
            classes = path.get('class', [])
            if isinstance(classes, str):
                classes = classes.split(' ')
            if color_class not in classes:
                classes.append(color_class)
                path['class'] = classes

    with open('Referendum_map_colored.svg', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("Map generated: Referendum_map_colored.svg")

if __name__ == "__main__":
    main() 