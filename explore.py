from rich import print
from rich.prompt import Prompt
from storage import save_data


def search_user(current_user):
    username = Prompt.ask("🔍 نام کاربری مورد نظر:")
    
    if user["is_private"] and current_user["username"] not in user["followers"]:
        if current_user["username"] not in user.get("follow_requests", []):
            user.setdefault("follow_requests", []).append(current_user["username"])
            save_data(data)
            print("[yellow]درخواست دنبال کردن ارسال شد[/yellow]")
        else:
            print("[cyan]درخواست قبلاً ارسال شده[/cyan]")

        
    if username not in users:
        print("[red]❌ کاربر یافت نشد[/red]")
        return

    target = users[username]

    if username in current_user["blocked_users"] or current_user["username"] in target["blocked_users"]:
        print("[red]⛔️ شما اجازه مشاهده این پروفایل را ندارید[/red]")
        return

    print(f"\n[bold blue]📄 پروفایل {username}[/bold blue]")
    print(f"📝 بیو: {target['bio'] if target['bio'] else 'ندارد'}")
    print(f"👥 دنبال کننده: {len(target['followers'])} | دنبال‌شونده: {len(target['following'])}")
    print(f"📸 تعداد پست: {len(target['posts'])}")
    print(f"🔐 نوع حساب: {'خصوصی' if target['is_private'] else 'عمومی'}")

    if current_user["username"] == username:
        print("[green]این حساب خودت هست[/green]")
        return

    if current_user["username"] in target["followers"]:
        choice = Prompt.ask("✅ آنفالو کنی؟ (y/n)", choices=["y", "n"])
        if choice == "y":
            target["followers"].remove(current_user["username"])
            current_user["following"].remove(username)
            save_data({"users": users, "posts": []})
            print("[yellow]❎ آنفالو شد[/yellow]")
    else:
        if target["is_private"]:
            user.setdefault("follow_requests", []).append(current_user["username"])
            save_data(data)
            print("[cyan]📩 درخواست دنبال کردن ارسال شد[/cyan]")
        else:
            target["followers"].append(current_user["username"])
            current_user["following"].append(username)
            save_data({"users": users, "posts": []})
            print("[green]✅ دنبال شد![/green]")

    block_choice = Prompt.ask("⛔️ مسدود/رفع مسدود کنی؟ (y/n)", choices=["y", "n"])
    if block_choice == "y":
        if username in current_user["blocked_users"]:
            current_user["blocked_users"].remove(username)
            print("[green]✅ رفع مسدود شد[/green]")
        else:
            current_user["blocked_users"].append(username)
            print("[red]🚫 کاربر مسدود شد[/red]")
        save_data({"users": users, "posts": []})