import win32com.client
import os
import sys

def convert_doc_to_docx(doc_path):
    abs_path = os.path.abspath(doc_path)
    if not os.path.exists(abs_path):
        print(f"Error: File {abs_path} not found")
        return None
    
    docx_path = abs_path + "x"
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        doc = word.Documents.Open(abs_path)
        # wdFormatXMLDocument = 12
        doc.SaveAs2(docx_path, FileFormat=12)
        doc.Close()
        print(f"Successfully converted {doc_path} to {os.path.basename(docx_path)}")
        return docx_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        word.Quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_doc_to_docx(sys.argv[1])
    else:
        print("Usage: python convert.py <file.doc>")
