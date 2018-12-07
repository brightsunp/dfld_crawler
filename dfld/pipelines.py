# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, re, csv


class HtmlCleanPipeline(object):
    '''
    数据清洗：title、content
    '''
    def __init__(self):
        pass

    def process_item(self, item, spider):
        item['title'] = self._process_title(item['title'])
        item['content'] = self._process_content(item['content'])
        return item

    def _process_title(self, title):
        # 去除标题中的空字符
        return ''.join(title.split())

    def _process_content(self, content):
        re_blank = re.compile('[,\s]*')  # 空白字符（空格、tab、换行）、英文逗号
        re_script = re.compile('<script[^>]*>.*?</script>', re.I)  # script标签
        re_style = re.compile('<style[^>]*>.*?</style>', re.I)  # style标签
        re_comment = re.compile('<!--.*?-->')  # HTML注释
        re_tag = re.compile('<[^>]*>')  # HTML标签
        re_entity = re.compile('&[#\w\d]*?;')  # HTML实体

        for ptn in [re_blank, re_script, re_style, re_comment, re_tag, re_entity]:
            content = ptn.sub('', content)
        return content


class CsvWritePipeline(object):
    '''
    结果存储：.csv文件，每一行的数据是[url, title, content]
    '''
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.result_dir = os.path.join(cur_dir, '..', 'result')
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def process_item(self, item, spider):
        file_name = os.path.join(self.result_dir, 'dfld.csv')
        with open(file_name, 'a+', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow([item['url'], item['title'], item['content']])
        return item
