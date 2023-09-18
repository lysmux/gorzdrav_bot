from jinja2 import Environment, select_autoescape, PackageLoader

env = Environment(
    loader=PackageLoader("bot", "answer_templates"),
    autoescape=select_autoescape(["html"])
)


def render_template(name: str, **kwargs):
    template = env.get_template(name)
    return template.render(**kwargs)
