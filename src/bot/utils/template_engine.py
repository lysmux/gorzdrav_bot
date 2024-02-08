from jinja2 import Environment, PackageLoader

jinja_env = Environment(
    loader=PackageLoader("src.bot.multimedia", "templates"),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True
)


def render_template(name: str, **kwargs) -> str:
    template = jinja_env.get_template(name)
    return template.render(**kwargs)
