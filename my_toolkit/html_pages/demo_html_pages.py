import pandas as pd

import html_pages

page = html_pages.HTMLPage()

page.add_element("<title>Demo title</title>")
page.add_element("<h1>Demo header</h1>")

tabs = html_pages.TabsHTML()
tabs.add_tab("Tab 1", "Example text")
tabs.add_tab("Tab 2", html_pages.SimpleHTMLTable(
    pd.DataFrame(data={'c1': [1, 2, 3, 4], 'c2': [4, 3, 2, 1], 'c3': [2, 1, 3, 4]})))


sub_tabs = html_pages.TabsHTML()
sub_tabs.add_tab("Sub tab 1", "Sub tab 1")
sub_tabs.add_tab("Sub tab 2", "Sub tab 2")
tabs.add_tab("Tab 3", html_pages.HTMLPage().add_element("<h2>Sub tabs</h2>").add_element(sub_tabs))

page.add_element(tabs)

with open('demo_page.html', 'w') as f:
    f.write(page.html())
