from django import template

from main.content_models import localized_message_hash

register = template.Library()


def _norm_text(raw: str) -> str:
    return " ".join((raw or "").replace("\u00a0", " ").split())


@register.simple_tag(takes_context=True)
def tx(context, ru_source: str) -> str:
    key = localized_message_hash(ru_source)
    bag = context.get("L10") or {}
    return bag.get(key, ru_source.strip())


class _TrimTxNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        inner = "".join(self.nodelist.render(context)).strip()
        canon = _norm_text(inner)
        key = localized_message_hash(canon)
        bag = context.get("L10") or {}
        return bag.get(key, inner)


@register.tag(name="txtrim")
def txtrim(parser, token):
    nodelist = parser.parse(("endtxtrim",))
    parser.delete_first_token()
    return _TrimTxNode(nodelist)
