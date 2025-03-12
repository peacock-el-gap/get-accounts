# Get Accounts from MF API

## Glossary
* **MF** = Ministerstwo Finansów = Polish Ministry of Finance
* **NIP** = Numer Identyfikacji Podatkowej = Polish TAX ID
* **NRB** = Numer Rachunku Bankowego = Polish standard for account numbers

## Get Accounts

1. Input data (NIP + account number) is provided in an Excel file.
2. Ensure that the following values are correctly set:
   - `DIR_NAME`
   - `INPUT_FILE_NAME`
   - `INPUT_SHEET_NAME`
   - `OUTPUT_FILE_NAME`
   - `OUTPUT_SHEET_NAME`
3. Run the script.
4. Check the results in the output file.

### Prerequisites
To run the script, you need to:
1. Install Python (tested with Python 3.13).
2. *(Optional but recommended)* Activate a virtual environment.
3. Install dependencies using: `pip install -r requirements.txt`.

## MF API
Documentation available only in Polish.

Official website: [MF API Documentation](https://www.gov.pl/web/kas/api-wykazu-podatnikow-vat)

### API Usage Limitations

|PL|EN|
|-|-|
|Korzystanie z API jest limitowane. Przy wykorzystaniu metody „search” możesz złożyć 10 zapytań o maksymalnie 30 podmiotów jednocześnie, natomiast przy wykorzystaniu metody „check” możesz zapytać o 1 podmiot. Po wyczerpaniu tego limitu dostęp do API jest blokowany do godziny 0:00.|The use of the API is limited. Using the "search" method, you can make 10 requests for up to 30 entities at the same time, while using the "check" method you can query 1 entity. Once this limit is reached, access to the API is blocked until 0:00.|

There is a discussion about API limitations here: [Forum Discussion](https://4programmers.net/Forum/PHP/333944-biala_lista_numerow_kont?p=1655673#id1655673)

|PL|EN|
|-|-|
|Wg. oficjalnych danych te limity są, mi się kilka razy udało do nich dobić. Urban legend głosi, że te limity zostały znacząco zwiększone, ale oficjalnego komunikatu w tej sprawie nie widziałem.|According to official figures, these limits exist; I have managed to reach them several times. Urban legends say that these limits have been significantly increased, but I have not seen an official announcement on this.|

### Summary
There is no official way to access the API without usage limitations.

## Alternative Verification Method
The Ministry of Finance allows unlimited verification of NIP (tax ID) and account number pairs using a so-called "flat file." This file is published daily and contains SHA-512 hashes for TIN/account pairs.

### Additional Information
- [Flat File Information](https://www.podatki.gov.pl/vat/bezpieczna-transakcja/wykaz-podatnikow-vat/plik-plaski/)
- [Technical Specification (PDF)](https://www.podatki.gov.pl/media/5745/specyfikacja-techniczna-pliku-plaskiego_20200826.pdf)

Documentation is available only in Polish.

### Limitations of This Method
This approach **only verifies** whether a specific NIP/account pair is valid (i.e., represents a valid VAT taxpayer and a valid business account).

⚠️ **It does not provide account numbers for a given NIP. It only allows verification.**

