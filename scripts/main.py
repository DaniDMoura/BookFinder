from .auth import Authentication

def run():
    auth = Authentication()
    auth.authentication_sign_in_window()
    
if __name__ == "__main__":
    run()
