from optparse import OptionParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
from textwrap import wrap
import re



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
    for p in parsed_html.body.find('p'):
      self.main_text_article.append(p)
    

  def get_caption_article(self):
    return self.caption_article
   
    
  def get_main_text_article(self):
    return self.main_text_article



class FormatingContentText:
  # Форматирование контента
  def __init__(self):
    self.max_size_line = 80
    self.word_transferring = True
    self.allocation_captions_and_paragrapf = True
   
    
  def split_string(self, text):
      # Разбиение длинной строки на короткие
      if self.word_transferring == True and len(text) > self.max_size_line:
        text = wrap(text.text, self.max_size_line)
      return text



class FileWriting:
  def __init__(self, text):
    with open('article.txt', 'a') as file:
      
      if type(text) == list:
        for line in text: file.write(line.strip() + '\n')
      
      else:
        file.write(text + '\n')



class Main:
  args_command_line = GetArgs()
  url = args_command_line.get_url()

  process = GetContentText(url)
  caption_article = process.get_caption_article()
  main_text_article = process.get_main_text_article()
  
  format_text = FormatingContentText()

  # Форматирование и запись заголовка
  if format_text.allocation_captions_and_paragrapf == True:
    caption_article = format_text.split_string(caption_article)
  FileWriting(caption_article)

  # Форматирование и запись основного текста
  for text in main_text_article:
    text = format_text.split_string(text)
    # FileWriting(text)



if __name__ == '__main__':
    Main()