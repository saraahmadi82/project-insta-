from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from storage import save_data

def show_profile(current_user):
    while True:
        print("\n[bold cyan]👤 پروفایل من[/bold cyan]")
        print("1. نمایش اطلاعات")
        print("2. ویرایش نام یا بیو")
        print("3. نمایش پست‌های من")
        print("4. تنظیمات حریم خصوصی")
        print("5. کاربران مسدودشده")
        print("6. بازگشت")
        print("7. پست‌های ذخیره‌شده")

        choice = Prompt.ask("انتخاب شما", choices=["1", "2", "3", "4", "5", "6", "7"])

        if choice == "1":
            show_info(current_user)
        elif choice == "2":
            edit_profile(current_user)
        elif choice == "3":
            show_my_posts(current_user)
        elif choice == "4":
            toggle_privacy(current_user)
        elif choice == "5":
            show_blocked(current_user)
        elif choice == "6":
            break
        elif choice == "7":
            show_saved(current_user)

def show_info(user):
    print(f"\n[bold blue]📄 اطلاعات حساب:[/bold blue]")
    print(f"🆔 نام کاربری: {user['username']}")
    print(f"📧 ایمیل: {user['email']}")
    print(f"📝 بیو: {user['bio'] if user['bio'] else 'ندارد'}")
    print(f"👥 دنبال‌کننده: {len(user['followers'])} | دنبال‌شونده: {len(user['following'])}")
    print(f"🔐 نوع حساب: {'خصوصی' if user['is_private'] else 'عمومی'}")

def edit_profile(user):
    new_name = Prompt.ask("📝 نام جدید", default=user["username"])
    new_bio = Prompt.ask("📖 بیو جدید", default=user["bio"])
    user["username"] = new_name
    user["bio"] = new_bio
    save_data({"users": users, "posts": []})
    print("[green]✅ پروفایل بروزرسانی شد[/green]")

def show_my_posts(user):
    if not user["posts"]:
        print("[yellow]📭 شما هنوز پستی نگذاشته‌اید[/yellow]")
        return

    for i, post in enumerate(user["posts"]):
        panel = Panel.fit(
            f"[italic]{post['caption']}[/italic]\n\n❤️ {len(post['likes'])}  💬 {len(post['comments'])}",
            title=f"پست #{i + 1}"
        )
        print(panel)

def toggle_privacy(user):
    current = "خصوصی" if user["is_private"] else "عمومی"
    print(f"🔐 وضعیت فعلی حساب: {current}")
    choice = Prompt.ask("تغییر دهید؟ (y/n)", choices=["y", "n"])
    if choice == "y":
        user["is_private"] = not user["is_private"]
        save_data({"users": users, "posts": []})
        print(f"[cyan]✅ وضعیت جدید: {'خصوصی' if user['is_private'] else 'عمومی'}[/cyan]")

def show_blocked(user):
    if not user["blocked_users"]:
        print("[green]📗 لیست مسدودها خالی است[/green]")
        return

    print("[bold red]⛔️ کاربران مسدودشده:[/bold red]")
    for blocked in user["blocked_users"]:
        print(f"- {blocked}")

    choice = Prompt.ask("رفع مسدود؟ (y/n)", choices=["y", "n"])
    if choice == "y":
        target = Prompt.ask("نام کاربری برای رفع مسدودی:")
        if target in user["blocked_users"]:
            user["blocked_users"].remove(target)
            save_data({"users": users, "posts": []})
            print("[green]✅ رفع مسدود شد[/green]")

def show_saved(user):
    if not user["saved_posts"]:
        print("[yellow]🔖 هنوز هیچ پستی ذخیره نشده[/yellow]")
        return

    print("[bold blue]📥 پست‌های ذخیره‌شده:[/bold blue]")
    for i, post in enumerate(user["saved_posts"]):
        panel = Panel.fit(
            f"[bold]{post['username']}[/bold] - [italic]{post['caption']}[/italic]\n❤️ {len(post['likes'])}  💬 {len(post['comments'])}",
            title=f"Saved #{i + 1}"
        )
        print(panel)