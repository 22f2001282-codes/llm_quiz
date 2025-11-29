import requests, pdfplumber
from io import BytesIO

def download_and_sum_pdf_value_column(pdf_url: str, page_index: int = 1):
    # downloads pdf and sums numeric values from a table column named 'value' on page_index
    r = requests.get(pdf_url, timeout=30)
    r.raise_for_status()
    with pdfplumber.open(BytesIO(r.content)) as pdf:
        if page_index >= len(pdf.pages):
            raise ValueError("page_index out of range")
        page = pdf.pages[page_index]
        table = page.extract_table()
        if not table or len(table) < 2:
            raise ValueError("no usable table found on page")
        headers = table[0]
        # find 'value' column case-insensitive
        idx = None
        for i, h in enumerate(headers):
            if h and h.strip().lower() == 'value':
                idx = i
                break
        if idx is None:
            raise ValueError("'value' column not found in table headers: " + str(headers))
        total = 0.0
        for row in table[1:]:
            cell = row[idx]
            if cell is None:
                continue
            # remove common thousand separators
            cleaned = cell.replace(',', '').strip()
            try:
                total += float(cleaned)
            except:
                # ignore parse errors for now
                continue
        return total
