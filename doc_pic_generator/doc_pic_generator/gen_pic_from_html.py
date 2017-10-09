import subprocess
import os.path
from glob import glob
import numpy as np

CURRENT_DIR = os.path.dirname(__file__)

OUTPUT_DIR = os.path.join(CURRENT_DIR, '../../data/png')
WIDTH = 595
HEIGHT = 842

INPUT_DIR = os.path.join(CURRENT_DIR, '../../data/html')

SELECTED_TEMPLATES = ['doc_template_01', 'doc_template_02', 'doc_template_03', 'doc_template_04']

GENERATE_MODE = ['train', 'validate', 'test']

split_ratio = {
  'train': .6,
  'validate': .2,
  'test': .2,
}

for html_file_path in sum([glob(INPUT_DIR + '/{}.*.html'.format(template)) for template in SELECTED_TEMPLATES], []):
    html_name = os.path.basename(html_file_path)
    doc_template_name = html_name.split('.')[0]

    html_path_for_webkit2png = 'file:///{}'.format(os.path.abspath(html_file_path))
    mode = GENERATE_MODE[np.random.choice(len(GENERATE_MODE), p=list(split_ratio.values()))]
    subprocess.call(["webkit2png",
      html_path_for_webkit2png,
      '--clipped', '--clipwidth={}'.format(WIDTH), '--clipheight={}'.format(HEIGHT),
      '--dir={}'.format(os.path.join(OUTPUT_DIR, mode, doc_template_name)),
      '--filename={}.png'.format(html_name),
      '--scale=1'
    ])
    print('converted {} to png'.format(html_path_for_webkit2png))
