from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTCurve, LTFigure, LTTextContainer

texte_extrait: list[str] = list()
fonts: set[str] = set()
curve_colors: set[tuple[float, ...]] = set()


def process(element) -> None:
    if isinstance(element, LTFigure):
        for part in element:
            process(part)  # récursion
    elif isinstance(element, LTTextContainer):
        for text_line in element:
            texte_extrait.append(text_line.get_text().strip())
            for char in text_line:
                if isinstance(char, LTChar):
                    fonts.add(char.fontname)
    elif isinstance(element, LTCurve):
        curve_colors.add(element.stroking_color)


for page_layout in extract_pages("Plan-Metro.1607863858.pdf"):
    for i, element in enumerate(page_layout):
        process(element)

print(fonts)
print(curve_colors)
print(texte_extrait[:80])