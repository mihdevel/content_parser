from optparse import OptionParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
from textwrap import wrap
import re
import os
from config import max_size_line, allocation_captions_and_paragrapf, name_file_from_url_format


class GetArgs:
  def __init__(self):
    # Получение аргументов коммандной строки
    parser_opt = OptionParser()
    parser_opt.add_option('-u', '--url')
    (self.options, args) = parser_opt.parse_args()
    
  def get_url(self):
    return self.options.url



class GetContentText:
  def __init__(self, url):
    # Получение html
    response = urlopen(url)
    html = response.read()
    parsed_html = BeautifulSoup(html, features = "html.parser")

    self.caption_article = parsed_html.body.find('h1').text

    self.main_text_article = []
    
    for paragrapf in parsed_html.body.find_all('p'):
      paragrapf = str(paragrapf).replace('<p>', '')
      
      if allocation_captions_and_paragrapf:
        paragrapf = str(paragrapf).replace('</p>', '\n')
      else:
        paragrapf = str(paragrapf).replace('</p>', '')

      self.main_text_article.append(paragrapf)


  def get_caption_article(self):
    return self.caption_article
   
    
  def get_main_text_article(self):
    return self.main_text_article



class FormatingContentText:
  # Форматирование контента
  def __init__(self, max_size_line):
    self.max_size_line = max_size_line
   
    
  def split_string(self, text):
    # Разбиение длинной строки на короткие
    if len(text) > self.max_size_line:
      text = wrap(text, self.max_size_line)

    return text
  
  
  def url_reformat(self, text):
    pattern_link = '<a.*href\=\"(?P<url>.*?)\".*>(?P<text>.*)</a>'
    while re.search(pattern_link, text):
      text = re.sub(pattern_link, ' \g<text> [\g<url>]', text)
      
    return text

  

class TextToFile:
  def __init__(self, name_file_from_url_format, url, default_file_name):
    if name_file_from_url_format:
      pattern_url = '/(https?:\/\/)?(?P<new_url>([\da-z\.-]+)\.(?P<file_name>[a-z\.]{2,6})([\/\w \.-]*)*\/?)'
      str_url_reformat = re.search(pattern_url, url).group('new_url')
      
      url_structure = str_url_reformat.split('/')
      for folder in url_structure[:-1]:
        try:
          os.mkdir(folder)
          os.chdir(folder)
        except FileExistsError:
          os.chdir(folder)
      
      self.file_name = url_structure.pop()
      
      if not self.file_name:
        self.file_name = default_file_name
      else:
        self.file_name.split('.')
        self.file_name = self.file_name[0] + '.txt'
    else:
      self.file_name = default_file_name
  
  
  def writing(self, text):
    with open(self.file_name, 'a') as file:
      
      if type(text) == list:
        for line in text: file.write(line.strip() + '\n')
      
      else:
        file.write(text + '\n\n')



class Main:
  args_command_line = GetArgs()
  url = args_command_line.get_url()

  process = GetContentText(url)
  caption_article = process.get_caption_article()
  main_text_article = process.get_main_text_article()
  
  format_text = FormatingContentText(max_size_line)
  file_obj = TextToFile(name_file_from_url_format, url, default_file_name='article.txt')

  # Форматирование и запись заголовка
  caption_article = format_text.split_string(caption_article)
  file_obj.writing(caption_article)

  text =''

  # Форматирование и запись основного текста
  for line in main_text_article:
    text += format_text.url_reformat(str(line))+ '\n'
  
  text = format_text.split_string(text)
  file_obj.writing(text)


if __name__ == '__main__':
    Main()