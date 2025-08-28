import re
def hard_block(message):
    m = message.lower()
    # Block obvious scam keywords or suspicious shortlinks
    if 'free money' in m or 'claim now' in m or 'congratulations you have won' in m:
        return 'scam_phrase'
    # shortlink patterns
    if re.search(r'(bit\.ly|tinyurl|t\.co|goo\.gl|tiny\.cc)', m):
        return 'shortlink_untrusted'
    # many digits and urgent words
    if re.search(r'(urgent|immediately|act now)', m) and len(re.findall(r'\d', m))>6:
        return 'urgent_digits'
    return None
