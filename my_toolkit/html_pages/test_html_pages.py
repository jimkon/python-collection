import unittest
from unittest.mock import patch, mock_open

import html_pages


class TestHtml(unittest.TestCase):
    @patch("html_pages._TEMPLATE_DIR", "template_dir")
    def test__read_template(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            self.assertEqual(html_pages._read_template('test_template'), "data")
        mock_file.assert_called_with('template_dir\\test_template.html', 'r')


class TestHTMLBuilder(unittest.TestCase):
    def test_builder(self):
        builder = html_pages.HTMLBuilder("random_text [replace1] [replace2] [replace1] [replace3]")
        builder.replace('replace1', 'value1')
        builder.replace('replace2', 'value2')
        builder.replace('replace3', 'value3')

        html = builder.html()
        expected_html = "random_text value1 value2 value1 value3"
        self.assertEqual(html, expected_html)


class TestHTMLPage(unittest.TestCase):
    def test_page_builder(self):
        page = html_pages.HTMLPage()

        page.add_element('test1')
        page.add_element('test2')
        page.add_element('test3')

        html = page.html()
        expected_html = "\n<div>test1</div>\n<div>test2</div>\n<div>test3</div>"

        self.assertEqual(html, expected_html)


class TestTemplateHTMLBuilder(unittest.TestCase):
    def test_from_template_file(self):
        with patch("builtins.open", mock_open(read_data="template_file_html")) as mock_file:
            builder = html_pages.TemplateHTMLBuilder("test_template")
            self.assertEqual(builder.html(), "template_file_html")


class TestImageHTML(unittest.TestCase):
    @patch.object(html_pages.ImageHTML, '_bytes_to_utf8', return_value='_bytes_to_utf8')
    def test_no_size(self, mock_conv):
        img_html = html_pages.ImageHTML(b"test_bytes").html()
        mock_conv.assert_called_with(b"test_bytes")
        self.assertEqual(img_html, '<img src="data:image/gif;base64, _bytes_to_utf8" >')

    @patch.object(html_pages.ImageHTML, '_bytes_to_utf8', return_value='_bytes_to_utf8')
    def test_height(self, mock_conv):
        img_html = html_pages.ImageHTML(b"test_bytes", height=200).html()
        mock_conv.assert_called_with(b"test_bytes")
        self.assertEqual(img_html, '<img src="data:image/gif;base64, _bytes_to_utf8" height="200">')

    @patch.object(html_pages.ImageHTML, '_bytes_to_utf8', return_value='_bytes_to_utf8')
    def test_width(self, mock_conv):
        img_html = html_pages.ImageHTML(b"test_bytes", width=200).html()
        mock_conv.assert_called_with(b"test_bytes")
        self.assertEqual(img_html, '<img src="data:image/gif;base64, _bytes_to_utf8" width="200">')


class TestSimpleTableHTML(unittest.TestCase):
    def test_table(self):
        import pandas as pd

        test_df = pd.DataFrame(data={'a': [1, 2, 3, 4],
                                     'b': [1, 10, 100, 1000],
                                     'c': ['aa', 'ab', 'ac', 'ad'],
                                     'tags': [[], [], [], []]})

        test_str = html_pages.SimpleHTMLTable(test_df, 'test_title').html()

        expected_str = """<h1>test_title</h1>
<table>
    <thead>
        <tr><tr><th>a</th><th>b</th><th>c</th><th>tags</th></tr></tr>
    </thead>
    <tbody>
    <tr><td>1</td><td>1</td><td>aa</td><td>[]</td></tr>
    <tr><td>2</td><td>10</td><td>ab</td><td>[]</td></tr>
    <tr><td>3</td><td>100</td><td>ac</td><td>[]</td></tr>
    <tr><td>4</td><td>1000</td><td>ad</td><td>[]</td></tr>
    
    </tbody>
</table>"""
        self.assertEqual(test_str, expected_str)


if __name__ == '__main__':
    unittest.main()

