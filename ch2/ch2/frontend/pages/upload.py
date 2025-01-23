# Upload Telegram handles 
from dash import html , dcc, Input, Output, State, dash_table, no_update
import dash

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
            multiple=False,
        ),
        html.Div(id="drag-and-drop-feedback"),
    ]
)

@dash.callback(Output("drag-and-drop-feedback", "children"),
               Input('drag-and-drop', 'filename'),
               Input('drag-and-drop', 'contents'))
def preview_file(my_filename: str, my_contents: list):
    """
    Provide a preview of the file the investigators selected for upload. 
    Will alter the 'drag-and-drop-feedback' element
    """
    pass