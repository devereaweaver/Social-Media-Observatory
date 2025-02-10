# Upload Telegram handles
from dash import html, dcc, Input, Output, State, dash_table, no_update
import dash
import base64
import pandas as pd
import io
import re
from content.config import handles_queue
from content.utilities.mq_ch2 import send_data_to_queue

# Define the page layout with any desired components
layout = html.Div(
    [
        html.Div(
            [
                # Add upload component
                dcc.Upload(
                    id="drag-and-drop",
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
                    multiple=False,  # only allow one upload at a time
                ),
            ]
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
@dash.callback(
    Output("drag-and-drop-feedback", "children"),
    Input("drag-and-drop", "filename"),
    Input("drag-and-drop", "contents"),
)
def preview_file(filename: str, contents: list):
    """
    Provide a preview of the file the investigators selected for upload.
    Will alter the 'drag-and-drop-feedback' element
    """
    # CSV file validation check
    if filename is None:
        return None
    if filename[filename.rfind(".") :] != ".csv":
        return html.P("Please upload at CSV", style={"color": "red"})

    # Attempt to upload contents of CSV into a pandas DataFrame
    # contents is a base64 encoded binary string, we need to split the content type
    # along with the encoded string first
    content_type, content_b64_string = contents.split(",")

    # next, we'll need to decode the encoded string
    content_decoded_string = base64.b64decode(content_b64_string)

    # now, we can place the decoded CSV contents into a dataframe
    df = pd.read_csv(io.StringIO(content_decoded_string.decode("utf-8")))

    # validate the 'handle' column exists and is properly formatted in the csv
    if "handle" not in list(df):
        return html.P(
            "Please include a column of handles entitled 'handle'",
            style={"color": "red"},
        )

    # Attempt to sanitize the data:
    # 1. Drop null rows
    df = df.loc[df["handle"].notnull(), :]

    # Convert to all lowercase (case doesn't mattter for our use-case)
    df["handle"] = df["handle"].apply(lambda x: x.lower())

    # De-duplicate
    df.drop_duplicates("handle", inplace=True)

    # Check if there are any rows left
    if df.empty:
        return html.P(
            "Please include at least one handle in the 'handle' column",
            style={"color": "red"},
        )

    # Check if handles contain illegal characters. Do a regex match
    # for each row in the 'handle' column
    for i in df.index:
        if re.match(r"^\w+$", df.loc[i, "handle"]) is None:
            return html.P(
                f"""Illegal characters
                           detected in row {i + 2} of spreadsheet:
                           {df.loc[i, 'handle']}""",
                style={"color": "red"},
            )

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


@dash.callback(
    Output("seed-list-name-feedback", "children"), Input("seed-list-name", "value")
)
def validate_seed_list_name(seed_list_name: str):
    """
    Provides secondary validation for the seed list name. Once this validation
    check is passed, an upload button will be rendered to allow the data to be
    send to the backend logic for processing.
    """
    if not seed_list_name:
        return dash.no_update

    # Validate the seed list name characters are correct
    if re.match(r"^\w+$", seed_list_name) is None:
        return html.P(
            f"""Use only alphanumeric characters or underscores""",
            style={"color": "red"},
        )

    # Ensure seed list name is less than 64 characters
    if len(seed_list_name) > 64:
        return html.P(f"""Use <=64 chars""", style={"color": "red"})

    # Render the upload button if all validation is correct
    return html.Div(
        [
            html.Button(
                "Upload to server", id="upload-button", n_clicks=0, disabled=False
            ),
            html.Div(id="upload-feedback"),
        ]
    )


# TODO: Create a component that allows the user to upload the file and submit the
# desired seed-list name to the RabbitMQ pipeline.
# Note: In a production implementation of this, we'd want to also hande any potentially
# dangerous strings for the database and also to limit the length of each string.
# In the case of a valid seed list name and CSV file, the callback should return an upload
# button using the html.Button() component.
# When the user clicks the button, we'll send the handles to the backend via RabbitMQ.
@dash.callback(
    Output("upload-button", "n_clicks"),  # change the n_clicks property
    Output("upload-feedback", "children"),  # change the visual layout after clicking
    Input("upload-button", "n_clicks"),  # listen for a change in the n_clicks property
    State(
        "seed-data", "data"
    ),  # Pass data value from seed-data component (cached handles)
    State(
        "seed-list-name", "value"
    ),  # Pass the value property from the seed-list-name component (seed list name)
)
def upload_file(want_upload: int, seed_data: list[dict], seed_list_name: str):
    """
    upload_file callback trigged when a user clicks the upload button after selecting a valid
    CSV file and a valid seed list name. It creates the messages that get sent to the handles_queue
    using RabbitMQ which will then be read in by the producer.py code and Telegram handle information
    fetched via the Telegram API.
    """
    if want_upload == 0:
        return no_update, no_update

    # Load data from cache (the handles that we cached earlier) into dataframe
    df = pd.DataFrame.from_records(seed_data)

    # Define messages to send to queue (this will be sent to RabbitMQ)
    # Construct a list of key-value pairs from the list of handles and proposed
    # seed list name
    messages = [
        {"handles": [handle], "seed_list": seed_list_name.lower()}
        for handle in list(df["handle"])
    ]

    # Publish messages to queue which the get_channel_info.py backend logic is subscribed
    send_data_to_queue(messages, handles_queue)

    # Successful upload will return note and reset n_clicks property to 0
    # This can be seen in the decorator, the first Output is n_clicks property
    # and the second output is the children property where we render the following
    # html
    return 0, html.P(
        f"Seed list '{seed_list_name}' submitted for data collection!",
        style={"color": "lime"},
    )
