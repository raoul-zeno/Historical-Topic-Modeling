import pandas as pd
import pprint as pp
import os
import xml.etree.ElementTree as ET

xml_directory = r"#################"

data = []

def extract_text(text_element):
    text_content = []

    def recursive_extract(text_elem):
        if text_elem.text:
            text_content.append(text_elem.text)
        for child in text_elem:
            recursive_extract(child)
            if child.tail:
                text_content.append(child.tail)

    recursive_extract(text_element)
    
    return " ".join(text_content)


for file_name in os.listdir(xml_directory):
    if file_name.endswith(".xml"):
        file_path = os.path.join(xml_directory, file_name)


        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {"ns0":"http://www.tei-c.org/ns/1.0"}

        main_title = root.findtext('.//ns0:title[@type="main"]', namespaces=ns)
        sub_title = root.findtext('.//ns0:title[@type="sub"]', namespaces=ns)
        volume_title = root.findtext('.//ns0:title[@type="volume"]', namespaces=ns)
        class_main = root.findtext(".//ns0:classCode[@scheme='https://www.deutschestextarchiv.de/doku/klassifikation#dwds1main']", namespaces=ns)
        class_sub = root.findtext(".//ns0:classCode[@scheme='https://www.deutschestextarchiv.de/doku/klassifikation#dwds1sub']", namespaces=ns)
        author_surname = root.findtext(".//ns0:surname", namespaces=ns)
        author_forename = root.findtext(".//ns0:forename", namespaces=ns)
        author = f"{author_surname}, {author_forename}"
        publication_date_str = root.findtext(".//ns0:sourceDesc/ns0:biblFull/ns0:publicationStmt/ns0:date[@type='publication']", namespaces=ns)
        language = root.findtext(".//ns0:language", namespaces=ns)
        text_element = root.find(".//ns0:text", namespaces=ns)
        plain_text = extract_text(text_element)

        data.append({
            "main_title": main_title,
            "sub_title": sub_title,
            "volume_title": volume_title,
            "author": author,
            "publication_date": publication_date_str,
            "class_main": class_main,
            "class_sub": class_sub,
            "language": language,
            "text": plain_text
        })

df = pd.DataFrame(data)

df.to_csv("output_csv_definitive", index=False, encoding="utf-8")

print("Created a csv-file!")



