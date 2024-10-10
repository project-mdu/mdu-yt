from typing import List, Dict, Union

def process_unicode_text(text: str) -> Dict[str, Union[str, int]]:
    """
    Process a Unicode string and return information about it.
    
    Args:
        text (str): The input Unicode string to process.
    
    Returns:
        Dict[str, Union[str, int]]: A dictionary containing information about the processed text.
    """
    return {
        "original": text,
        "length": len(text),
        "bytes": len(text.encode('utf-8')),
        "reversed": text[::-1]
    }

def combine_unicode_strings(strings: List[str]) -> str:
    """
    Combine a list of Unicode strings into a single string.
    
    Args:
        strings (List[str]): A list of Unicode strings to combine.
    
    Returns:
        str: The combined Unicode string.
    """
    return " ".join(strings)

if __name__ == "__main__":
    # Test with various Unicode strings
    test_strings: List[str] = [
        "Hello, World!",  # Basic Latin
        "こんにちは、世界！",  # Japanese
        "Здравствуй, мир!",  # Russian
        "🌍🌎🌏",  # Emoji (Earth globes)
        "àáâãäåæç",  # Latin-1 Supplement
    ]
    
    for string in test_strings:
        result = process_unicode_text(string)
        print(f"Original: {result['original']}")
        print(f"Length: {result['length']}")
        print(f"Bytes: {result['bytes']}")
        print(f"Reversed: {result['reversed']}")
        print()
    
    combined = combine_unicode_strings(test_strings)
    print("Combined string:")
    print(combined)
    print(f"Combined length: {len(combined)}")
    print(f"Combined bytes: {len(combined.encode('utf-8'))}")