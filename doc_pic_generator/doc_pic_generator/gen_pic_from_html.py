import subprocess
import os.path
from glob import glob

OUTPUT_DIR = '../../data/png'
WIDTH = 595
HEIGHT = 842

INPUT_DIR = '../../data/html'

for html_file_path in glob(INPUT_DIR + '/*.html'):
    html_name = os.path.basename(html_file_path)

    html_path_for_webkit2png = 'file:///{}'.format(os.path.abspath(html_file_path))

    subprocess.call(["webkit2png",
      html_path_for_webkit2png,
      '--clipped', '--clipwidth={}'.format(WIDTH), '--clipheight={}'.format(HEIGHT),
      '--dir={}'.format(OUTPUT_DIR),
      '--filename={}.png'.format(html_name)
    ])
    print ('converted {} to png'.format(html_path_for_webkit2png))