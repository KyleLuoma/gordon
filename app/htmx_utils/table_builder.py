import json
import random
from typing import Union

class TableBuilder:

    @staticmethod
    def _render_table(
        column_header: list[str],
        rows: list[list],
        table_id: Union[str, bool] = None,
        thead_id: Union[str, bool] = None,
        tbody_id: Union[str, bool] = None,
        row_ids: Union[list, bool] = None,
        element_classes: dict[str, Union[str, list]] = None
    ) -> str:
        if table_id == True:
            table_id = f"table-{random.randint(1000, 99999999)}"
        if thead_id == True:
            thead_id = f"thead-{random.randint(1000, 99999999)}"
        if tbody_id == True:
            tbody_id = f"tbody-{random.randint(1000, 99999999)}"
        if type(row_ids) == list:
            assert(len(row_ids) == len(rows))
        elif row_ids == True:
            row_ids = [f"trow-{random.randint(1000, 99999999)}" for i in range(0, len(rows))]
        html_rows = []
        for row in rows:
            assert len(row) == len(column_header)
            html_rows.append("".join([f"<td>{str(val)}</td>" for val in row]))
        head = "".join([f"<th>{c}</th>" for c in column_header])
        if row_ids == None:
            body = ("\n        ".join(f"<tr>{row}</tr>" for row in html_rows))
        else:
            body = ("\n        ".join(f"<tr id={id}>{row}</tr>" for id, row in zip(row_ids, html_rows)))
        html = f"""
<table{f' id="{table_id}"' if table_id != None else ''}>
    <thead{f' id="{thead_id}"' if thead_id != None else ''}>
        <tr>{head}</tr>
    </thead>
    <tbody{f' id="{tbody_id}"' if tbody_id != None else ''}>
        {body}
    </tbody>
</table>"""
        if element_classes:
            for cls in element_classes:
                if f"<{cls}" not in html:
                    continue
                if type(element_classes[cls]) == list:
                    class_val = " ".join(element_classes[cls])
                else:
                    class_val = element_classes[cls]
                html = html.replace(f"<{cls}", f'<{cls} class="{class_val}"')
        return html

    @staticmethod
    def column_wise_dict_to_html_table(
        table_dict: dict[str, list],
        table_id: Union[str, bool] = None,
        thead_id: Union[str, bool] = None,
        tbody_id: Union[str, bool] = None,
        row_ids: Union[list, bool] = None,
        element_classes: dict = None
        ) -> str:
        """
        Converts a dictionary with column-wise data into an HTML table.
        Args:
            table_dict (dict): A dictionary where keys are column names (str) and values are lists 
                         containing the ordered contents of the columns. All lists must be of 
                         the same length.
        Returns:
            str: An HTML string representing the table.
        Example:
            Input:
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Age": [25, 30, 35],
                "City": ["New York", "Los Angeles", "Chicago"]
            }
            Output:
            <table>
                <thead>
                    <tr><th>Name</th><th>Age</th><th>City</th></tr>
                </thead>
                <tbody>
                    <tr><td>Alice</td><td>25</td><td>New York</td></tr>
                    <tr><td>Bob</td><td>30</td><td>Los Angeles</td></tr>
                    <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
                </tbody>
            </table>
        """
        col_length = len(table_dict[list(table_dict.keys())[0]])
        for k in table_dict.keys():
            assert len(table_dict[k]) == col_length
        columns = list(table_dict.keys())
        rows = [[table_dict[c][i] for c in columns] for i in range(0, col_length)]
        return TableBuilder._render_table(
            column_header=columns, 
            rows=rows,
            table_id=table_id,
            thead_id=thead_id,
            tbody_id=tbody_id,
            row_ids=row_ids,
            element_classes=element_classes
            )


    def row_wise_dict_list_to_html_table(
            dict_list: list[dict[str, object]],
            table_id: Union[str, bool] = None,
            thead_id: Union[str, bool] = None,
            tbody_id: Union[str, bool] = None,
            row_ids: Union[list, bool] = None,
            element_classes: dict = None
            ) -> str:
        """
        Converts a list with row-wise data as dicts with column names as keys into an HTML table.
        Args:
            dict_list (list): A list of dicts where each dict represents a row in the table.
            dict keys represent column names, and must be consistent for all rows.
            Dict values are treated as atomic (non-iterable), and iterables will be
            stringified, which may cause formatting issues.
        Returns:
            str: An HTML string representing the table.
        Example:
            Input:
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Age": [25, 30, 35],
                "City": ["New York", "Los Angeles", "Chicago"]
            }
            Output:
            <table>
                <thead>
                    <tr><th>Name</th><th>Age</th><th>City</th></tr>
                </thead>
                <tbody>
                    <tr><td>Alice</td><td>25</td><td>New York</td></tr>
                    <tr><td>Bob</td><td>30</td><td>Los Angeles</td></tr>
                    <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
                </tbody>
            </table>
        """
        keys = list(dict_list[0].keys())
        rows = []
        for row in dict_list:
            assert len(row.keys()) == len(keys)
            assert set(keys) == set(row.keys())
            rows.append([row[k] for k in row.keys()])
        return TableBuilder._render_table(
            column_header=keys, 
            rows=rows,
            table_id=table_id,
            thead_id=thead_id,
            tbody_id=tbody_id,
            row_ids=row_ids,
            element_classes=element_classes
            )