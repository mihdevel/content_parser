from optparse import OptionParser
from bs4 import BeautifulSoup
from urllib.request import urlopen



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
    self.content_text = {}
    response = urlopen(url)
    html = response.read()
    parsed_html = BeautifulSoup(html)
    self.content_text['h1'] = (parsed_html.body.find('h1'))
    self.content_text['p'] = (parsed_html.body.find_all('p'))
    
  def return_content_text(self):
    return self.content_text



class FormatingContentText:
  def __init__(self):
    self.max_line_size = 80
    self.word_transferring = True
    self.allocation_captions_and_paragrapf = True



class Main:
  args_command_line = GetArgs()
  url = args_command_line.get_url()
  obj_get_content_text = GetContentText(url)
  content_text = obj_get_content_text.return_content_text()
  
  
  
  # print(content_text)
  


if __name__ == '__main__':
    Main()