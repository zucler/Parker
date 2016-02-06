import re
from html.parser import HTMLParser

from parker.classes.core.utils import Utils


class CoreParser(HTMLParser):
    """Generic HTML parser class"""

    def __init__(self, section_split_tag=""):
        """Initialize a generic HTML parser."""
        HTMLParser.__init__(self)
        self.__pageContent = {}
        self.__sectionContent = []
        self.__searchBy = ""
        self.__elementName = ""
        self.__className = ""
        self.__elementID = ""
        self.__sectionSplitTag = section_split_tag
        self.__sectionName = ""
        self.__newSectionStarted = False
        self.__inSearchedElement = False

    def get_data_by_class_name(self, element_name, class_name, html, element_id=""):
        """Iterate through all tags in HTML and return content of the first one that has a matching class name.

        Args:
                element_name (str): Tag name to search for
                class_name (str): Class of the tag to search for
                html (str): HTML code to be searched
                element_id (str): OPTIONAL Element ID of the class to search for

        Returns:
                Returns content of the tag with given tag and class names. If tag is not found, returns empty string
        """
        self.__searchBy = "class"
        self.__elementName = element_name
        self.__className = class_name
        if element_id:
            self.__elementID = element_id

        self.feed(html)
        return self.__pageContent

    def is_searched_element(self, tag, attrs):
        """ Check if current tag is the element we are searching for

        Args:
            tag (str): HTML tag
            attrs: HTML tag attributes

        Returns:

        """
        if self.__searchBy == "class":
            if tag == self.__elementName and ('class', self.__className) in attrs:
                if not self.__elementID or ('id', self.__elementID):
                    return True

            return False

    def handle_starttag(self, tag, attrs):
        """Reads opening tag of an HTML element.

        Args:
                tag (str): Tag name
                attrs (dict): Tag attributes
        """
        if self.is_searched_element(tag, attrs):
            self.__inSearchedElement = True

        if self.__inSearchedElement and tag == self.__sectionSplitTag:
            self.__newSectionStarted = True

    def handle_data(self, data):
        """Reads content of an HTML element.

        Args:
                data (str): Raw text data enclosed in the tag
        """
        if self.__inSearchedElement:
            if self.__newSectionStarted:
                if self.__sectionContent:
                    self.__pageContent[self.__sectionName] = self.__sectionContent
                    self.__sectionContent = []  # Resetting section content
                self.__newSectionStarted = False
                self.__sectionName = data.strip()
            else:
                self.__sectionContent.append(data.strip())

    def handle_endtag(self, tag):
        """Reads closing tag of an HTML element.

        Args:
                tag (str): Tag name
        """
        if self.__inSearchedElement and tag == self.__elementName:
            self.__inSearchedElement = False
            self.__pageContent[self.__sectionName] = self.__sectionContent
