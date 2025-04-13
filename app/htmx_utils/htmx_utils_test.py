from table_builder import TableBuilder
from form_builder import (
    FormBuilder,
    LabelElement,
    InputElement,
    InputType
    )

class TestHtmxUtils:

    def test_table_builder_render_table_random_table_id(self):
        html = TableBuilder._render_table(
            column_header=["A"],
            rows=[["1"], ["2"]],
            table_id=True
        )
        print(html)
        assert "table id=\"table-" in html

    def test_table_builder_render_table_set_table_id(self):
        html = TableBuilder._render_table(
            column_header=["A"],
            rows=[["1"], ["2"]],
            table_id="test-table-id"
        )
        print(html)
        assert "table id=\"test-table-id" in html

    def test_table_builder_render_table_add_class(self):
        html = TableBuilder._render_table(
            column_header=["A"],
            rows=[["1"], ["2"]],
            table_id="test-table-id",
            element_classes={"table": "test-class"}
        )
        print(html)
        assert 'class="test-class"' in html

    def test_table_builder_column_wise_dict_to_html_table(self):
        html = TableBuilder.column_wise_dict_to_html_table({
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 30, 35],
            "City": ["New York", "Los Angeles", "Chicago"]
        })
        assert html == """
<table>
    <thead>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
    </thead>
    <tbody>
        <tr><td>Alice</td><td>25</td><td>New York</td></tr>
        <tr><td>Bob</td><td>30</td><td>Los Angeles</td></tr>
        <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
    </tbody>
</table>"""

    def test_table_builder_row_wise_dict_list_to_html_table(self):
        html = TableBuilder.row_wise_dict_list_to_html_table([
                {"Name": "Alice", "Age": 25, "City": "New York"},
                {"Name": "Bob", "Age": 30, "City": "Los Angeles"},
                {"Name": "Charlie", "Age": 35, "City": "Chicago"}
            ])
        print(html)
        assert html == """
<table>
    <thead>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
    </thead>
    <tbody>
        <tr><td>Alice</td><td>25</td><td>New York</td></tr>
        <tr><td>Bob</td><td>30</td><td>Los Angeles</td></tr>
        <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
    </tbody>
</table>"""

    def test_form_builder_label_element_str(self):
        le = LabelElement(
            for_attr="test1", 
            label_text="This is a label", 
            css_class="lb1",
            custom_attributes={"c1": "a1"}
        )
        print(le)
        assert str(le) == """<label for="test1" class="lb1" c1="a1">This is a label</label>"""
    
    def test_form_builder_add_input_and_label(self):
        fb = FormBuilder()
        fb.add_element(LabelElement(for_attr="input1", label_text="Enter Name:"))
        fb.add_element(InputElement(type=InputType.TEXT, id="input1", name="name", value="", css_class="text-input"))
        form_html = str(fb)
        print(form_html)
        assert form_html == """<form>
    <label for="input1">Enter Name:</label>
    <input type="text" id="input1" name="name" class="text-input">
</form>"""

    def test_form_builder_add_multiple_elements(self):
        fb = FormBuilder()
        fb.add_element(LabelElement(for_attr="email", label_text="Email:"))
        fb.add_element(InputElement(type=InputType.EMAIL, id="email", name="email", value="", css_class="email-input"))
        fb.add_element(LabelElement(for_attr="password", label_text="Password:"))
        fb.add_element(InputElement(type=InputType.PASSWORD, id="password", name="password", value="", css_class="password-input"))
        form_html = str(fb)
        print(form_html)
        assert form_html == """<form>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" class="email-input">
    <label for="password">Password:</label>
    <input type="password" id="password" name="password" class="password-input">
</form>"""

    def test_form_builder_with_custom_attributes(self):
        fb = FormBuilder()
        fb.add_element(LabelElement(for_attr="username", label_text="Username:", custom_attributes={"data-test": "label"}))
        fb.add_element(InputElement(type=InputType.TEXT, id="username", name="username", value="", css_class="username-input", custom_attributes={"data-test": "input"}))
        form_html = str(fb)
        print(form_html)
        assert form_html == """<form>
    <label for="username" data-test="label">Username:</label>
    <input type="text" id="username" name="username" class="username-input" data-test="input">
</form>"""
