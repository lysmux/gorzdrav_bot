from jinja2 import Environment, PackageLoader

jinja_env = Environment(
    loader=PackageLoader("src.bot", "answer_templates"),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True
)


def render_template(name: str, **kwargs):
    template = jinja_env.get_template(name)
    return template.render(**kwargs)
