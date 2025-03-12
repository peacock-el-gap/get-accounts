import datetime
import pandas as pd
import requests
import time

DIR_NAME = "."

INPUT_FILE_NAME = "input_data.xlsx"
INPUT_FILE_WITH_PATH = DIR_NAME + "/" + INPUT_FILE_NAME
INPUT_SHEET_NAME = "input_data"

OUTPUT_FILE_NAME = "output_data.xlsx"
OUTPUT_FILE_WITH_PATH = DIR_NAME + "/" + OUTPUT_FILE_NAME
OUTPUT_SHEET_NAME = "output_data"

PL = "2521"
CURRENT_DATE = datetime.date.today().strftime("%Y-%m-%d")
BASE_URL = "https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}"


# NRB Validation Function
# NRB = Numer Rachunku Bankowego = Polish standard for bank account numbers
def validate_nrb(account):
    if len(account) != 26 or not account.isdigit():
        return "# NRB account must be exactly 26 digits"
        # return False

    account = account + PL
    account = account[2:] + account[0:2]
    result = int(account) % 97

    if result == 1:
        return_message = "Valid NRB"
    else:
        return_message = f"# Invalid NRB, result = {result}, should be 1"

    return return_message


# NIP validation function
# NIP = Numer Identyfikacji Podatkowej = Polish TAX ID
def validate_nip(nip):
    if len(nip) != 10 or not nip.isdigit():
        return "# NIP must be exactly 10 digits"

    # Weights for first 9 digits
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    # Modulo 11 check
    checksum = sum(int(nip[i]) * weights[i] for i in range(9)) % 11

    # Last digit must match the checksum
    return checksum == int(nip[9])


# Function to request data for a given NIP
def fetch_nip_data(nip):
    time.sleep(0.3)
    url = BASE_URL.format(nip=nip, date=CURRENT_DATE)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return response.json()


# Function to extract accountNumbers from API response
def extract_account_numbers(api_response):
    if isinstance(api_response, dict):
        try:
            return api_response["result"]["subject"].get("accountNumbers", [])
        except KeyError:
            return []
        except AttributeError:
            return []
    return "# API response is None or an error string"


# Function to extract error message from response, if exists
def extract_error_message(api_response):
    if isinstance(api_response, dict):
        try:
            return api_response["message"]
        except Exception as e:
            try:
                if api_response["result"]["subject"] is None:
                    return "Nie figuruje w rejestrze VAT"
            except Exception as e:
                return "# N/A"
    return "# N/A"


if __name__ == "__main__":

    # Read input data
    df = pd.read_excel(
        INPUT_FILE_WITH_PATH,
        sheet_name=INPUT_SHEET_NAME,
        dtype={"invoicing_detail_tax_id": str, "bank_account": str},
    )

    # Clean input data
    df["tax_id_cleaned"] = df["invoicing_detail_tax_id"].apply(
        lambda text: "".join(filter(str.isdigit, text))
    )
    df["bank_account_cleaned"] = df["bank_account"].apply(
        lambda text: "".join(filter(str.isdigit, text))
    )

    # Validate input data
    df["is_tax_id_cleaned_valid"] = df["tax_id_cleaned"].apply(validate_nip)
    df["is_bank_account_cleaned_valid_NRB"] = df["bank_account_cleaned"].apply(
        validate_nrb
    )

    # Get data from API
    df["response_from_API"] = df["tax_id_cleaned"].apply(fetch_nip_data)

    # Extract accounts
    df["accounts_from_API"] = df["response_from_API"].apply(extract_account_numbers)

    # Extract error if exists
    df["error_message"] = df["response_from_API"].apply(extract_error_message)

    # print(df[["invoicing_detail_tax_id", "bank_account", "accounts_from_API", "error_message"]].head(100))

    # Save result to file
    df.to_excel(OUTPUT_FILE_WITH_PATH, sheet_name=OUTPUT_SHEET_NAME, index=False)
    print(f"See file \"{OUTPUT_FILE_WITH_PATH}\" for results.")
