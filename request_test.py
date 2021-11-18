import requests

# Main url
URL = "https://im-fine-backend.herokuapp.com/api"

def main():
    token, id = login()
    check_user_type(token, id)
    # user_list(token)


def login():
    # Login credentials
    username = "aqel"
    password = "username1"

    # Request data
    data = {"username" : username,
            "password" : password}

    # Make the request
    r = requests.post(url = URL + "/auth/login/", data = data)

    print(r.status_code)
    print(r.json())

    return r.json()["key"], r.json()["user_id"]


def user_list(token):
    headers = {"Authorization": f"Token {token}"}
    r = requests.get(url = URL + "/users", headers = headers)
    print(r.text)


def check_user_type(token, id):
    headers = {"Authorization": f"Token {token}"}
    r = requests.get(url = f"{URL}/users/{id}", headers = headers)
    print(r.json()["userType"])


if __name__ == "__main__":
    main()