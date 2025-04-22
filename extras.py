from rich import print
from rich.panel import Panel

def show_tagged_posts(current_user, posts):
    username = current_user["username"]
    tagged = []

    for post in posts:
        for _, comment in post["comments"]:
            if f"@{username}" in comment:
                tagged.append(post)
                break

    if not tagged:
        print("[yellow]🤷‍♀️ هیچ پستی که در آن تگ شده باشی پیدا نشد[/yellow]")
        return

    print(f"[bold magenta]📌 پست‌هایی که در کامنت تگ شده‌ای:[/bold magenta]")
    for i, post in enumerate(tagged):
        panel = Panel.fit(
            f"[bold]{post['username']}[/bold] - [italic]{post['caption']}[/italic]\n❤️ {len(post['likes'])}  💬 {len(post['comments'])}",
            title=f"Tagged Post #{i + 1}"
        )
        print(panel)