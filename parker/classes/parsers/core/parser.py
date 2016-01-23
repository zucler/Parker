import re
from html.parser import HTMLParser


class CoreParser(HTMLParser):
    """Generic HTML parser class"""

    def __init__(self):
        """Initialize a generic HTML parser."""
        HTMLParser.__init__(self)
        self.__content = ""
        self.__elementName = ""
        self.__className = ""
        self.__inSearchedElement = False
        self.__headerOpen = False

    def get_data_by_class_name(self, element_name, class_name, html):
        """Iterate through all tags in HTML and return content of the first one that has a matching class name.

        Args:
                element_name (str): Tag name to search for
                class_name (str): Class of the tag to search for
                html (str): HTML code to be searched

        Returns:
                Returns content of the tag with given tag and class names. If tag is not found, returns empty string
        """
        self.__elementName = element_name
        self.__className = class_name
        self.feed(html)
        return self.__content

    def handle_starttag(self, tag, attrs):
        """Reads opening tag of an HTML element.

        Args:
                tag (str): Tag name
                attrs (dict): Tag attributes
        """
        if tag == self.__elementName and ('class', self.__className) in attrs:
            self.__inSearchedElement = True

        if self.__inSearchedElement and tag == "h3":
            self.__content += "\n<" + tag + ">"
            self.__headerOpen = True

    def handle_data(self, data):
        """Reads content of an HTML element.

        Args:
                data (str): Raw text data enclosed in the tag
        """
        if self.__inSearchedElement:
            if not self.__headerOpen:
                self.__content += "\n"
                self.__content += data
            else:
                self.__content += data

    def handle_endtag(self, tag):
        """Reads closing tag of an HTML element.

        Args:
                tag (str): Tag name
        """
        if tag == self.__elementName:
            self.__inSearchedElement = False

        if self.__inSearchedElement and tag == "h3":
            self.__content += "</" + tag + ">"
            self.__headerOpen = False

    def get_prices_information(self, html):
        print("Am I here?!")
        """Process html code to build and return a parking rates object

        Args:
                html (str): Parking page html that includes parking info

        Returns:
                Returns Rates object that contain parking rates information
        """
        pass

    def split_rates_by_sections(self, start_tag, html):
        """Splits html by pattern into a dictionary of sub sections

        Args:
            start_tag (str): Opening HTML tag for a section (e.g. <h3>)
            html (str): HTML to be breakdown

        Returns:
            Returns dictionary where key is section header and value is section content
        """
        sections_dict = {}
        end_tag = start_tag[:1] + "/" + start_tag[1:]
        pattern = re.escape(start_tag) + ".+" + re.escape(end_tag)
        section_names = re.findall(pattern, html)
        rates_list = re.split(pattern, html)
        i = 0
        for key in section_names:
            key = key.lstrip(start_tag)
            key = key.rstrip(end_tag)
            if not rates_list[i]:  # ignoring empty lines
                i += 1

            sections_dict[key] = rates_list[i]
            i += 1

        return sections_dict
