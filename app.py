import base64
import json
from xml.etree.ElementTree import Element, SubElement, tostring

import cairosvg


class SVGGenerator:
    def __init__(self, height: int = 16, width: int = 16, color: str = "000000") -> None:
        self.height = height
        self.width = width
        self.color = color

        self.svg = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            height=str(self.height),
            width=str(self.width),
        )

    def circle(self) -> Element:
        SubElement(
            self.svg,
            "circle",
            cx=str(self.width / 2),
            cy=str(self.height / 2),
            r=str(self.height / 2),
            fill=f"#{self.color}",
        )
        return self.svg

    def square(self) -> Element:
        SubElement(
            self.svg,
            "rect",
            fill=f"#{self.color}",
            width=str(self.width),
            height=str(self.height),
        )
        return self.svg

    def triangle(self) -> Element:
        SubElement(
            self.svg,
            "polygon",
            points=f"{self.height / 2},0 {self.height},{self.width} 0,{self.width}",
            fill=f"#{self.color}",
        )
        return self.svg


def lambda_handler(event: dict, context: dict) -> dict:
    parameters = event["queryStringParameters"]
    shape = parameters.get("shape", None)
    size = parameters.get("size", None)
    color = parameters.get("color", None)

    width, height = map(int, size.split("x"))
    generator = SVGGenerator(height, width, color)

    if shape == "circle":
        svg = generator.circle()
    elif shape == "square":
        svg = generator.square()
    elif shape == "triangle":
        svg = generator.triangle()
    else:
        return {"statusCode": 400, "body": json.dumps("Shape not supported.")}

    drawing = cairosvg.svg2png(
        bytestring=tostring(svg), output_width=width, output_height=height
    )

    return {
        "statusCode": 200,
        "headers": {
            "Accept": "*/*",
            "Content-Type": "image/png",
        },
        "body": base64.b64encode(drawing).decode("utf-8"),
        "isBase64Encoded": True,
    }


if __name__ == "__main__":
    response = lambda_handler(
        {
            "pathParameters": {
                "shape": "circle",
                "size": "64x64",
                "color": "FF375F",
            }
        },
        None,
    )
    print(f"<img src=\"data:image/png;base64,{response['body']}\" />")
