from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from storage import save_data, load_data
from explore import search_user
from extras import show_tagged_posts
from profile import show_profile


data = load_data()
users = data["users"]
posts = data["posts"]
messages = data.setdefault("messages", {})
groups = data.setdefault("groups", {})

def home_screen(current_user):
    while True:
        print("\n[bold cyan]صفحه اصلی[/bold cyan]")
        print("1. مشاهده پست ها")
        print("2. افزودن پست")
        print("3. ارسال پیام")
        print("4. خروج از حساب")
        print("5. جستجوی کاربران")
        print("6. پست هایی که تگ شده ام")
        print("7. انتشار استوری جدید")
        print("8. مشاهده استوری های کاربران دنبال شده")
        print("9. ایجاد گروه")
        print("10. پیام به گروه")
        print("11. مشاهده چت گروهی")
        print("12. مدیریت درخواست های دنبال کردن")
        print("13. بخش صفحه کاربری (پروفایل)")


        choice = Prompt.ask("انتخاب شما", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])

        if choice == "1":
            show_posts(current_user)
        elif choice == "2":
            add_post(current_user)
        elif choice == "3":
            send_message(current_user)
        elif choice == "4":
            print("[bold red]خروج از حساب...[/bold red]")
            break
        elif choice == "5":
            search_user(current_user)
        elif choice == "6":
            show_tagged_posts(current_user, posts)
        elif choice == "7":
            add_story(current_user)
        elif choice == "8":
            view_stories(current_user)
        elif choice == "9":
            create_group(current_user)
        elif choice == "10":
            send_group_message(current_user)
        elif choice == "11":
            view_group_chat(current_user)
        elif choice == "12":
            manage_follow_requests(current_user)
        elif choice == "12":
            show_profile(current_user)

def show_posts(current_user):
    if not posts:
        print("[yellow]!هیچ پستی هنوز وجود ندارد[/yellow]")
        return

    print("\n[bold magenta]📸 پست ها[/bold magenta]")
    for i, post in enumerate(posts):
        panel = Panel.fit(
            f"[bold]{post['username']}[/bold]\n\n[italic]{post['caption']}[/italic]\n\n❤️ {len(post['likes'])} 💬 {len(post['comments'])}",
            title=f"پست #{i + 1}"
        )
        print(panel)

        print("\nانتخاب عملیات:")
        print("l: لایک | c: کامنت | s: ذخیره | sh: اشتراک گذاری | n: هیچکدام")
        action = Prompt.ask("انتخاب کن", choices=["l", "c", "s", "sh", "n"], default="n")

        if action == "l":
            if current_user["username"] not in post["likes"]:
                post["likes"].append(current_user["username"])
                print("[green]❤️ لایک شد![/green]")
            else:
                print("[yellow]قبلاً لایک کرده ای[/yellow]")
        elif action == "c":
            comment = Prompt.ask("متن کامنت:")
            post["comments"].append((current_user["username"], comment))
            print("[green]💬 کامنت ثبت شد[/green]")
        elif action == "s":
            current_user["saved_posts"].append(post)
            print("[blue]🔖 پست ذخیره شد[/blue]")
        elif action == "sh":
            receiver = Prompt.ask("اشتراک گذاری با چه کاربری؟")
            print(f"[green]📨 پست با موفقیت برای {receiver} ارسال شد [/green]")

        save_data(data)

def add_post(current_user):
    caption = Prompt.ask("📝 متن پست:")
    new_post = {
        "username": current_user["username"],
        "caption": caption,
        "likes": [],
        "comments": []
    }
    posts.append(new_post)
    current_user["posts"].append(new_post)
    save_data(data)
    print("[green]✅ پست با موفقیت منتشر شد![/green]")

def send_message(current_user):
    receiver = Prompt.ask("نام کاربری گیرنده:")
    if receiver not in users:
        print("[red]کاربر مورد نظر یافت نشد[/red]")
        return
    message = Prompt.ask("✉️ پیام شما:")
    print(f"[bold green]پیام به {receiver} ارسال شد[/bold green] (صرفاً نمایشی، ذخیره نمی‌شود فعلاً)")
        
def add_story(current_user):
    story_text = Prompt.ask("📝 متن استوری:")
    story = {
        "text": story_text,
        "likes": []
    }
    current_user["stories"].append(story)
    save_data(data)
    print("[green]✅ استوری با موفقیت منتشر شد![/green]")

def view_stories(current_user):
    found = False
    print("\n[bold cyan] استوری های کاربران دنبال شده:[/bold cyan]")
    for username in current_user["following"]:
        if username in users:
            friend = users[username]
            if friend.get("stories"):
                found = True
                print(f"\n[bold magenta]{username}[/bold magenta]:")
                for story in friend["stories"]:
                    print(f"📖 {story['text']}")
                    print(f"❤️ {len(story['likes'])} لایک")

                    like = Prompt.ask("لایک می‌کنی؟ (y/n)", choices=["y", "n"], default="n")
                    if like == "y":
                        if current_user["username"] not in story["likes"]:
                            story["likes"].append(current_user["username"])
                            print("[green]❤️ لایک شد[/green]")
                        else:
                            print("[yellow]قبلاً لایک کرده‌ای[/yellow]")
    if not found:
        print("[yellow]هیچ استوری فعالی وجود ندارد[/yellow]")
    save_data(data)
    
def create_group(current_user):
    name = Prompt.ask("نام گروه:")
    members = [current_user["username"]]
    while True:
        member = Prompt.ask("کاربر دیگر (یا n برای توقف):")
        if member == "n":
            break
        if member in users:
            members.append(member)
        else:
            print("[red]کاربر یافت نشد[/red]")
    groups[name] = {
        "members": members,
        "messages": []
    }
    save_data(data)
    print(f"[green]✅ گروه {name} ساخته شد[/green]")
    
def send_group_message(current_user):
    name = Prompt.ask("نام گروه:")
    group = groups.get(name)
    if not group or current_user["username"] not in group["members"]:
        print("[red]دسترسی ندارید[/red]")
        return
    text = Prompt.ask("💬 پیام شما:")
    msg = {"sender": current_user["username"], "text": text}
    group["messages"].append(msg)
    save_data(data)
    print("[green]✅ پیام در گروه ارسال شد[/green]")
    
def view_group_chat(current_user):
    name = Prompt.ask("نام گروه:")
    group = groups.get(name)
    if not group or current_user["username"] not in group["members"]:
        print("[red]دسترسی ندارید[/red]")
        return
    print(f"\n[bold cyan]💬 چت گروهی: {name}[/bold cyan]")
    for m in group["messages"]:
        print(f"[bold]{m['sender']}:[/bold] {m['text']}")

def manage_follow_requests(current_user):
    requests = current_user.get("follow_requests", [])
    if not requests:
        print("[yellow]درخواستی وجود ندارد[/yellow]")
        return

    print("[bold cyan]درخواست های دنبال کردن:[/bold cyan]")
    for username in requests[:]:
        print(f"درخواست از: {username}")
        action = Prompt.ask("تایید یا رد؟ (a: تایید / r: رد)", choices=["a", "r"])
        if action == "a":
            current_user["followers"].append(username)
            users[username]["following"].append(current_user["username"])
            print(f"[green]✅ {username} اکنون دنبال کننده شماست[/green]")
        else:
            print(f"[red]❌ درخواست {username} رد شد[/red]")
        requests.remove(username)

    current_user["follow_requests"] = requests
    save_data(data)
