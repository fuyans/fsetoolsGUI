import base64
import os
import os.path as path
import re

import markdown2

import fsetoolsGUI.gui


def md2md_embedded_img(fp_md: str):
    with open(fp_md, 'r') as f:
        md = f.read()

    for ref_img in re.findall(r'!\[.+\]\(.+\)', md):
        # get full file path
        fp_img = re.search(r'\((.+)\)', ref_img).group(1)
        fp_img = path.realpath(path.join(path.dirname(fp_md), *path.split(fp_img)))

        # read image and encode to base64
        with open(fp_img, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')

        # make embedded image url
        img_html_embedded = f"<img src='data:image/png;base64,{img_base64}' width=790>"

        # replace ref img with embedded img
        md = md.replace(ref_img, img_html_embedded)

    return md


def md2html(fp_or_md: str):
    """Converts markdown file or string to html.

    :param fp_or_md: file path or markdown raw string.
    :return:
    """

    # parse markdown raw from file or `fp_or_md`
    if path.isfile(fp_or_md):
        with open(fp_or_md, 'r') as f:
            doc_md = f.read()
    else:
        doc_md = fp_or_md

    # conversion using `markdown2`
    return markdown2.markdown(doc_md, extras=['tables', 'fenced-code-blocks'])


if __name__ == '__main__':
    # get file path

    fp_md_list = list()

    for dirpath, dirnames, filenames in os.walk(path.join(path.dirname(fsetoolsGUI.__root_dir__), 'docs')):
        for fn in filenames:
            if fn.endswith('.md'):
                fp_md_list.append(path.join(dirpath, fn))

    html: str = None

    for fp_md in fp_md_list:
        html = md2html(md2md_embedded_img(fp_md))
        css = f"<style type='text/css'>{fsetoolsGUI.gui.md_css}</style>"
        with open(path.join(fsetoolsGUI.__root_dir__, 'gui', 'docs', path.basename(fp_md).replace('.md', '')),
                  'w+') as f:
            f.write(css + html)
