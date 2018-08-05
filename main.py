from optparse import OptionParser
from bs4 import BeautifulSoup
from urllib.request import urlopen



class GetArgs():
  def __init__(self):
    # Получение аргументов коммандной строки
    parser_opt = OptionParser()
    parser_opt.add_option('-u', '--url')
    (self.options, args) = parser_opt.parse_args()
    
  def get_url(self):
    return self.options.url



class GetContentText():
  def __init__(self):
    # Получение html
    response = urlopen(options.url)
    html = response.read()
    parsed_html = BeautifulSoup(html)
    print(parsed_html)
    # print(parsed_html.body.find('div', attrs={'class': 'toc'}))




class FormatContentText():
  def __init__(self):
    self.max_line_size = 80
    self.word_transferring = True
    self.allocation_captions_and_paragrapf = True



# class OutputNameFormatThroughUrl():
#
#   def get_folders_and_name_file(self, url):
#     pass
#
#   def create_folders_and_text_file(self, dict):
#     pass





class Main():
  args_command_line = GetArgs()
  url = args_command_line.get_url()
  print(url)
  



if __name__ == '__main__':
    Main()