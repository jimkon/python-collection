import abc
import base64
import os
import tempfile
import matplotlib.pyplot as plt

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def _read_template(template_name):
    filename = os.path.join(_TEMPLATE_DIR, template_name+'.html')
    with open(filename, 'r') as f:
        return f.read()


class HTMLObject(abc.ABC):
    @abc.abstractmethod
    def html(self) -> str:
        return None

    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.html())


class HTMLBuilder(HTMLObject):
    def __init__(self, template_str):
        self._html_str = template_str

    def replace(self, this, with_that):
        self._html_str = self._html_str.replace(f"[{this}]", with_that)

    def html(self):
        return self._html_str


class HTMLPage(HTMLBuilder):
    def __init__(self):
        super().__init__('')

    def add_element(self, element):
        self._html_str = f"{self._html_str}\n<div>{element.html()}</div>"
        return self


class TemplateHTMLBuilder(HTMLBuilder):
    def __init__(self, template_name):
        template_html = _read_template(template_name)
        super().__init__(template_html)


class ImageHTML(TemplateHTMLBuilder):
    def __init__(self, img_bytes, width=None, height=None):
        super().__init__('image')
        self.replace('image', self._bytes_to_utf8(img_bytes))

        if height:
            self.replace('height', f'height="{height}"')
        else:
            self.replace('height', '')

        if width:
            self.replace('width', f'width="{width}"')
        else:
            self.replace('width', '')

    @staticmethod
    def _bytes_to_utf8(_bytes):
        return base64.b64encode(_bytes).decode("utf-8")

    @staticmethod
    def from_image_file(image_path):
        with open(image_path, "rb") as image_file:
            return ImageHTML(image_file.read())

    @staticmethod
    def from_matplotlib():
        tmp_file = tempfile.NamedTemporaryFile(suffix='_image.png', delete=False)
        plt.savefig(tmp_file.name)

        image_html = ImageHTML.from_image_file(tmp_file.name)

        tmp_file.close()
        os.unlink(tmp_file.name)

        return image_html


class TabsHTML(TemplateHTMLBuilder):
    def __init__(self):
        super().__init__('tabs')
        self._add_default_id = True

    def _add_button(self, label):
        default_id = "id=\"defaultOpen\"" if self._add_default_id else ""
        self._add_default_id = False
        to_add = f"<button class=\"tablinks\" onclick=\"openCity(event, '{label}')\" {default_id}>{label}</button>\n\t[button]"
        self.replace('button', to_add)

    def _add_div(self, label, html_content):
        to_add = f"<div id=\"{label}\" class=\"tabcontent\">\n{html_content}\n</div>\n[div_tab]"
        self.replace('div_tab', to_add)

    def add_tab(self, label, html_content):
        self._add_button(label)
        self._add_div(label, html_content.html())
        return self

    def html(self):
        self.replace("button", '')
        self.replace("div_tab", '')
        return self._html_str

