from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader("bot", "answer_templates"),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True
)


def render_template(name: str, **kwargs):
    template = env.get_template(name)
    return template.render(**kwargs)
