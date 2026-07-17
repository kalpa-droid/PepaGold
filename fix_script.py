with open("generate_blog.py", "r") as f:
    code = f.read()

# Revert doubled curly braces since we won't use .format()
code = code.replace("{{", "{").replace("}}", "}")

# Replace the formatting logic
old_logic = """        content = html_template.format(
            title=page["title"],
            description=page["description"],
            h1=page["h1"]
        )"""

new_logic = """        content = html_template.replace("{title}", page["title"]).replace("{description}", page["description"]).replace("{h1}", page["h1"])"""

code = code.replace(old_logic, new_logic)

with open("generate_blog.py", "w") as f:
    f.write(code)
