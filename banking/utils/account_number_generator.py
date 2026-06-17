def generate_account_number(id, first_name, last_name, CIN):
    bank_code = "DGB"

    # "DGB-01-FL-XXXXX"
    return "{}{}{}{}{}".format( str(bank_code), str(id), str(first_name)[0].upper(), str(last_name)[0].upper(), CIN)
