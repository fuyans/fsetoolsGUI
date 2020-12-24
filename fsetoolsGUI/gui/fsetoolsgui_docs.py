import webbrowser
from os.path import join

from fsetoolsGUI import __root_dir__, logger


class App:
    app_name_short = 'Documentation'
    app_name_long = 'Documentation'

    url = join(__root_dir__, 'docs', 'html', 'index.html')

    def __init__(self, *args, **kwargs):
        pass

    def show(self):
        logger.info(f'Opening docs url, {self.url}')
        webbrowser.open(self.url)


if __name__ == '__main__':
    App()
