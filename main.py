from rich.panel import Panel
from rich.prompt import Prompt
from rich import print

from home import home_screen
from storage import load_data, save_data

data = load_data()
users = data["users"]
current_user = None

def signup():
    print("\n[bold green]📝 ثبت نام[/bold green]")
    email = Prompt.ask("ایمیل")
    username = Prompt.ask("نام کاربری")
    password = Prompt.ask("رمز عبور", password=True)

    for user in users.values():
        if user["email"] == email:
            print("[red]!این ایمیل قبلاً ثبت شده[/red]")
            return None

    if username in users:
        print("[red]!این نام کاربری قبلاً گرفته شده[/red]")
        return None

    users[username] = {
        "email": email,
        "username": username,
        "password": password,
        "bio": "",
        "followers": [],
        "following": [],
        "posts": [],
        "saved_posts": [],
        "follow_requests": [],
        "blocked_users": [],
        "is_private": False,
        "stories": []
    }

    save_data(data)
    print(f"[green]ثبت نام با موفقیت انجام شد! خوش آمدی، [bold]{username}[/bold][/green]")
    return users[username]

def login():
    print("\n[bold cyan]ورود به حساب کاربری[/bold cyan]")
    username = Prompt.ask("نام کاربری")
    password = Prompt.ask("رمز عبور", password=True)

    user = users.get(username)

    if not user:
        print("[red]!کاربری با این نام وجود ندارد[/red]")
        return None

    if user["password"] != password:
        print("[red]!رمز عبور نادرست است[/red]")
        return None

    print(f"[green]خوش آمدی، [bold]{username}[/bold]![/green]")
    return user

def welcome_screen():
    print(Panel.fit("[bold cyan]به اینستاگرام ترمینالی خوش آمدید![/bold cyan]"))
    print("1. ثبت‌نام")
    print("2. ورود")
    print("3. خروج")

def main():
    global current_user

    while True:
        welcome_screen()
        choice = Prompt.ask("\n[bold yellow]انتخاب شما[/bold yellow]", choices=["1", "2", "3"])

        if choice == "1":
            user = signup()
            if user:
                current_user = user
                break
        elif choice == "2":
            user = login()
            if user:
                current_user = user
                break
        elif choice == "3":
            print("\n[bold red]خروج از برنامه...[/bold red]")
            return

    home_screen(current_user)

if __name__ == "__main__":
    main()