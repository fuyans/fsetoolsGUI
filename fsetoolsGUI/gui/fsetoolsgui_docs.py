import os
import subprocess
import sys
import webbrowser

from fsetoolsGUI import __root_dir__, logger


class App:
    app_name_short = 'Documentation'
    app_name_long = 'Documentation'

    url = os.path.join(__root_dir__, 'docs', 'html', 'index.html')

    def __init__(self, *args, **kwargs):
        pass

    def show(self):
        logger.info(f'Opening docs url: {self.url}')
        try:
            if sys.platform == 'darwin':
                # webbrowser does not work in the latest MAC OS update, Big Sur. Fall back to subprocess.Popen to open url. 29/12/2020
                subprocess.Popen(['open', self.url])
            else:
                webbrowser.open(self.url)

        except Exception as e:
            logger.info(f'Failed to open docs url, {e}')


if __name__ == '__main__':
    App()
