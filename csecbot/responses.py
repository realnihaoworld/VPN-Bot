# handles the command !generate, creates a private key, then returns it

def handle_response(message) -> str:
    # processes the message
    p_message = message.lower()

    if p_message == '?generate':
        # TODO: generate private key
        private_key = "temp"
        return private_key

