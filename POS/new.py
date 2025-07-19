from num2words import num2words

def amount_in_words(amount):
    # Split amount into whole and decimal parts
    whole_part = int(round(amount,2))
    decimal_part = int(round((amount - whole_part) * 100))
    
    # Convert each part to words
    whole_part_words = num2words(whole_part, lang='en')
    decimal_part_words = num2words(decimal_part, lang='en')
    
    # Combine with custom currency terms
    return f"{whole_part_words.capitalize()} Qathery Riyals and {decimal_part_words.capitalize()} Dirhams"


print(amount_in_words(89.10976))