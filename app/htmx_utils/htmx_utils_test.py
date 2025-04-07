from table_builder import TableBuilder

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

    

