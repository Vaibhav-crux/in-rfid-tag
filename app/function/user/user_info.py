def get_current_user():
    """Reads the current user name from a file."""
    try:
        with open('app/file/currentUser.txt', 'r') as file:
            user_name = file.read().strip()
            return user_name
    except FileNotFoundError:
        return "Unknown User"
