#!/usr/bin/env/python

from jinja2 import Environment, FileSystemLoader
import os.path
from faker import Faker
import time
import logging


TEMPLATE_DIR = '../templates'
OUTPUT_DIR = '../../data/html'
test_template_name = 'doc_template_01.html'


class DocPicGenerator(object):
    def __init__(self, template_dir, output_dir):
        self.TEMPLATE_DIR = template_dir
        self.OUTPUT_DIR = output_dir
        self._fake = Faker()

    def _gen_doc_html(self, template_name, data={}):
        # Create the jinja2 environment.
        # Notice the use of trim_blocks, which greatly helps control whitespace.
        j2_env = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR),
                             trim_blocks=True)
        html_text = j2_env.get_template(template_name).render(
            data=data
        )
        return html_text

    def gen_fake_data(self, count=10):
        fake = self._fake
        return [{'name': fake.name(), 'address': fake.address()} for _ in range(count)]

    def _html_name(self, template_name, idx=''):
        """generate the html file name"""
        timestamp = str(int(time.time()))
        tokens = template_name.split('.')
        final_tokens = (tokens[:-1] + [str(timestamp), str(idx), tokens[-1]])
        return '.'.join(final_tokens)

    def output_html(self, template_name, output_file_name, data={}):
        html_text = self._gen_doc_html(template_name=template_name, data=data)
        with open(os.path.join(self.OUTPUT_DIR, output_file_name), 'w') as fp:
            fp.write(html_text)
            logging.info('output_file_name {} created'.format(output_file_name))

    def output_htmls(self, template_name, count=10):
        fake_data_list = self.gen_fake_data(count)
        for i, data in enumerate(fake_data_list):
            output_file_name = self._html_name(template_name, idx=i)
            self.output_html(template_name, output_file_name=output_file_name, data=data)


if __name__ == '__main__':
    docPicGen = DocPicGenerator(template_dir=TEMPLATE_DIR, output_dir=OUTPUT_DIR)
    docPicGen.output_htmls(template_name=test_template_name, count=10)
