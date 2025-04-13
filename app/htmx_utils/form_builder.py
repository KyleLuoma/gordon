from enum import Enum
from typing import Union

class InputType(Enum):
        BUTTON = "button"
        CHECKBOX = "checkbox"
        COLOR = "color"
        DATE = "date"
        DATETIME_LOCAL = "datetime-local"
        EMAIL = "email"
        FILE = "file"
        HIDDEN = "hidden"
        IMAGE = "image"
        MONTH = "month"
        NUMBER = "number"
        PASSWORD = "password"
        RADIO = "radio"
        RANGE = "range"
        RESET = "reset"
        SEARCH = "search"
        SUBMIT = "submit"
        TEL = "tel"
        TEXT = "text"
        TIME = "time"
        URL = "url"
        WEEK = "week"


class LabelElement:
    
    def __init__(
            self, 
            for_attr: str, 
            label_text: str,
            css_class: str = None,
            custom_attributes: dict = None,
            linebreaks: int = 0
            ):
        self.for_attr = for_attr
        self.label_text = label_text
        self.css_class = css_class
        self.custom_attributes = custom_attributes
        self.linebreaks = linebreaks

    def __str__(self) -> str:
        attributes = [f'for="{self.for_attr}"']
        if self.css_class:
            attributes.append(f'class="{self.css_class}"')
        if self.custom_attributes:
            for k in self.custom_attributes.keys():
                attributes.append(f'{k}="{self.custom_attributes[k]}"')
                
        label = f'<label {" ".join(attributes)}>{self.label_text}</label>'
        if self.linebreaks > 0:
            for i in range(self.linebreaks):
                label += "<br>"
        return label
    

class InputElement:

    def __init__(
              self, 
              type: InputType, 
              id: str = None, 
              name: str = None, 
              value = None,
              css_class = None,
              custom_attributes: dict = None
              ):
        self.type = type
        self.id = id
        self.name = name
        self.value = value
        self.css_class = css_class
        self.custom_attributes = custom_attributes

    def __str__(self) -> str:
        attributes = []
        if self.type:
            attributes.append(f'type="{self.type.value}"')
        if self.id:
            attributes.append(f'id="{self.id}"')
        if self.name:
            attributes.append(f'name="{self.name}"')
        if self.value:
            attributes.append(f'value="{self.value}"')
        if self.css_class:
            attributes.append(f'class="{self.css_class}"')
        if self.custom_attributes:
            for k in self.custom_attributes.keys():
                attributes.append(f'{k}="{self.custom_attributes[k]}"')

        return f'<input {" ".join(attributes)}>'



class FormBuilder:

    def __init__(
            self,
            include_form_tags: bool = True,
            method: str = None
            ):
        self.form_items = []
        self.include_form_tags = include_form_tags

    def add_element(self, element: Union[InputElement, LabelElement]):
        self.form_items.append(element)

    def _render_form(self) -> str:
        if self.include_form_tags:
            form = "<form>\n    "
        else: 
            form = ""
        form += "\n    ".join(str(item) for item in self.form_items)
        if self.include_form_tags:
            form += "\n</form>"
        return form

    def __str__(self) -> str:
        return self._render_form()