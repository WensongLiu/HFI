class User:
    public_user_ID = ''
    user_name = ''
    public_client_ID = ''
    admin = None

    def __init__(self, public_user_ID, user_name, public_client_ID, admin):
        self.public_user_ID = public_user_ID
        self.user_name = user_name
        self.public_client_ID = public_client_ID
        self.admin = admin