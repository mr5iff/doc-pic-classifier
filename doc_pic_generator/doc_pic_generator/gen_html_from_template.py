#!/usr/bin/env/python

from jinja2 import Environment, FileSystemLoader
import os.path
from faker import Faker
import time
import logging

CURRENT_DIR = os.path.dirname(__file__)

# for faking data
fake = Faker()

TEMPLATE_DIR = os.path.join(CURRENT_DIR, '../templates')
OUTPUT_DIR = os.path.join(CURRENT_DIR, '../../data/html')
test_template_names = ['doc_template_01.html', 'doc_template_02.html', 'doc_template_03.html', 'doc_template_04.html']


class DocPicGenerator(object):
    def __init__(self, template_dir, output_dir, data_generator=None):
        self.TEMPLATE_DIR = template_dir
        self.OUTPUT_DIR = output_dir
        if data_generator is None:
            data_generator = lambda param=None: {'name': fake.name(), 'address': fake.address(), 'paragraph': fake.text()}
        self.data_generator = data_generator

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
        return [self.data_generator() for _ in range(count)]

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

    def output_htmls(self, template_names, count=10):
        fake_data_list = self.gen_fake_data(count)
        if not isinstance(template_names, list):
            template_names = [template_names]
        for template_name in template_names:
            for i, data in enumerate(fake_data_list):
                output_file_name = self._html_name(template_name=template_name, idx=i)
                self.output_html(template_name=template_name, output_file_name=output_file_name, data=data)


if __name__ == '__main__':
    docPicGen = DocPicGenerator(template_dir=TEMPLATE_DIR, output_dir=OUTPUT_DIR)
    docPicGen.output_htmls(template_names=test_template_names, count=150)
