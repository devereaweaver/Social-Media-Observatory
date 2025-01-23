# Upload Telegram handles 
from dash import html , dcc

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
        )
    ]
)