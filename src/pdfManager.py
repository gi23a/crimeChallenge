from pypdf import PdfReader
from datetime import datetime
import re




#read pdf 
def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n"  
    
    return text 

def assign_pdf_data(path):

    pdfdata = {
        "Dates": "",
        "Descript": "",
        "DayOfWeek": "",
        "PdDistrict": "",
        "Resolution": "",
        "Latitude (Y)": "",
        "Longitude (X)": "",
        "Address": "",

    }
    text = read_pdf(path)
    
    lines = text.splitlines()
    current_field = None

    for line in lines:
        #if next line have : then new field if not then append to the curr line 
        if ':' in line:
            field, value = line.split(":", 1)
            field = field.strip()
            value = value.strip()
            if field == "Date & Time":
                pdfdata["Dates"] = value
                pdfdata["DayOfWeek"] = extract_dayOfWeek(value)
            elif field == "Incident Location":
                pdfdata["Address"] = value
            elif field == "Coordinates":
                coordinates = value.strip("()").split(',')
                pdfdata["Latitude (Y)"] = coordinates[0].strip()
                pdfdata["Longitude (X)"] = coordinates[1].strip()
            elif field == "Detailed Description":
                pdfdata["Descript"] = value
            elif field == "Resolution":
                pdfdata["Resolution"] = value
            elif field == "Police District":
                pdfdata["PdDistrict"] = value
            current_field = field  
        else:
            if current_field == "Detailed Description":
                pdfdata["Descript"] += " " + line.strip() 
    print(pdfdata)
    return pdfdata



def extract_dayOfWeek(date_string):
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return date.strftime("%A")  
    except ValueError:
        return "Couldn't add dayOfWeek" 

def assign_severity(category):
    return severityDic.get(category, "Unk")






