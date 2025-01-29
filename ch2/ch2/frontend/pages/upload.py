# Upload Telegram handles 
from dash import html , dcc, Input, Output, State, dash_table, no_update, dash_table
import dash
import base64
import pandas as pd
import io
import re

# Define the page layout with any desired components
layout = html.Div(
    [
        # Add upload component
        dcc.Upload(
            id = "drag-and-drop",
            children=html.Div(
                [
                    f"Drag and drop your CSV here, or ",
                    html.A("click here to browse your file system"),
                ]
            ),
            style={
            "width": "99%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",           
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
            },
            multiple=False,   # only allow one upload at a time
        ),
        html.Div(id="drag-and-drop-feedback"),
    ]
)

# Since this is event-driven programming, we need to subscribe a Dash callback
# to listen for the desired event (upload event here)
# Here, we're listening for changes in two possible properties. They are both on the
# drag-and-drop component and the callback will trigger if there is a change to either
# its filename component or its contents component. 
# The two inputs have corresponding variable names in the function.
# The function output will change the children property of the drag-and-drop-feedback
# component. 
@dash.callback(Output("drag-and-drop-feedback", "children"),
               Input('drag-and-drop', 'filename'),
               Input('drag-and-drop', 'contents'))
def preview_file(filename: str, contents: list):
    """
    Provide a preview of the file the investigators selected for upload. 
    Will alter the 'drag-and-drop-feedback' element
    """
    # CSV file validation check
    if filename is None:
        return None
    if filename[filename.rfind('.'):] != '.csv':
        return html.P('Please upload at CSV', style={'color': 'red'})

    # Attempt to upload contents of CSV into a pandas DataFrame
    # contents is a base64 encoded binary string, we need to split the content type
    # along with the encoded string first
    content_type, content_b64_string = contents.split(',')

    # next, we'll need to decode the encoded string
    content_decoded_string = base64.b64decode(content_b64_string)

    # now, we can place the decoded CSV contents into a dataframe
    df = pd.read_csv(io.StringIO(content_decoded_string.decode('utf-8')))

    # validate the 'handle' column exists and is properly formatted in the csv
    if 'handle' not in list(df):
        return html.P("Please include a column of handles entitled 'handle'",
                      style={'color': 'red'})

    # Attempt to sanitize the data:
    # 1. Drop null rows 
    df = df.loc[df['handle'].notnull(),:]

    # Convert to all lowercase (case doesn't mattter for our use-case)
    df['handle'] = df['handle'].apply(lambda x: x.lower())

    # De-duplicate
    df.drop_duplicates('handle', inplace=True)

    # Check if there are any rows left
    if df.empty:
        return html.P(
            "Please include at least one handle in the 'handle' column",
            style={'color': 'red'},
        )
    
    # Check if handles contain illegal characters. Do a regex match 
    # for each row in the 'handle' column
    for i in df.index:
        if re.match('^\w+$', df.loc[i, 'handle']) is None:
            return html.P(f"""Illegal characters
                           detected in row {i + 2} of spreadsheet:
                           {df.loc[i, 'handle']}""",
                           style={'color': 'red'})

    # If everything checks out, we'll confirm with a preview, cache what's loaded up
    # and then promprt the user to supply a seed list name. We'll return several components
    # wrapped in a Div hta will define what the children of the output component will be
    return html.Div(
        [
            # Create a table
            dash_table.DataTable(
                data=df.to_dict("records"),  # convert dataframe to appropriate format
                columns=[{"name": i, "id": i} for i in list(df)],
                style_cell={"textAlign": "left"},
                page_current=0,
                page_size=10,
            ),
            html.Div(
                [
                # Create an input field for the seed list name
                html.H4(
                    children="Enter seed list name (case-insensitive):",
                    style={"color": "blue"},
                ),
                dcc.Input(
                    id="seed-list-name",
                    type="text",
                    placeholder="No special characters!", 
                    disabled=False,
                    debounce=False,
                    value=filename.rstrip(".csv").lower(),
                ),
                html.Div(id="seed-list-name-feedback"),
                ]
            ), 
            dcc.Store(id="seed-data", data=df.to_dict("records")),
        ]
    )