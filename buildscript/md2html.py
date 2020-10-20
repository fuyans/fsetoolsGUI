import base64
import io
import os
import os.path as path
import re

import markdown2
from PIL import Image

import fsetoolsGUI.gui


def md2md_embedded_img(fp_md: str):
    with open(fp_md, 'r') as f:
        md = f.read()

    for ref_img in re.findall(r'!\[.+?\]\(.+?\)', md):
        # get full file path
        fp_img = re.search(r'\((.+)\)', ref_img).group(1)
        fp_img = path.realpath(path.join(path.dirname(fp_md), *path.split(fp_img)))

        try:
            img = Image.open(fp_img)
        except FileNotFoundError:
            print('Missing file ', fp_img)
        # img_width, img_height = img.size
        # img_width, img_height = 635, (img_height * 635 / img_width)
        # img = img.resize((img_width, int(img_height)), resample=Image.LANCZOS)

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='png')

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        # make embedded image url
        img_html_embedded = f"<img width='{635}' src='data:image/png;base64,{img_base64}'>"

        # replace ref img with embedded img
        md = md.replace(ref_img, img_html_embedded)

    return md


def md2html(fp_or_md: str):
    """Converts markdown file or string to html.

    :param fp_or_md: file path or markdown raw string.
    :return:
    """

    # parse markdown raw from file or `fp_or_md`
    try:
        with open(fp_or_md, 'r') as f:
            doc_md = f.read()
    except Exception as e:
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

    html = None

    for i, fp_md in enumerate(fp_md_list):
        print(fp_md, f' ({i+1}/{len(fp_md_list)})')
        html = md2html(md2md_embedded_img(fp_md))
        css = f"<style type='text/css'>{fsetoolsGUI.gui.md_css}</style>"
        fp_html = path.join(fsetoolsGUI.__root_dir__, 'gui', 'docs', path.basename(fp_md).replace('.md', '.html'))
        with open(fp_html, 'w+') as f:
            f.write(css + html)
