"""과정 사이트 훅 — 강사만 아는 주소를 mkdocs.yml 한 곳(extra.course_links)에서 쪽마다 채운다.

쪽에서 쓰는 법(마크다운 안의 원시 HTML 한 줄):

    <span data-tf-link="open_chat">오픈채팅 들어가기</span>
    <span data-tf-link="team_form" data-tf-empty="당일 화면에서 안내">팀 제출 폼</span>

- 값이 http(s)://… 이면 → 새 탭 링크 `<a class="tf-link">오픈채팅 들어가기</a>`
- 값이 글자(예: 강의장 이름)면 → 그 글자
- 값이 비었거나 키가 없으면 → 중립 문구 '첫날 안내'(또는 data-tf-empty의 글)

값을 넣고 main에 push하면 다음 배포부터 모든 쪽이 바뀐다. 빌드는 깨지지 않는다(모르는 키도 '첫날 안내').
"""
from __future__ import annotations

import html
import logging
import re

log = logging.getLogger("mkdocs.hooks.course_links")

_SPAN = re.compile(
    r'<span\b(?P<attrs>[^>]*?\bdata-tf-link="(?P<key>[A-Za-z0-9_-]+)"[^>]*)>(?P<text>.*?)</span>',
    re.S,
)
_EMPTY = re.compile(r'\bdata-tf-empty="(?P<v>[^"]*)"')
_URL = re.compile(r"^(https?://|mailto:)", re.I)
DEFAULT_EMPTY = "첫날 안내"


def _links(config) -> dict:
    extra = config.get("extra") or {}
    links = extra.get("course_links") or {}
    return links if isinstance(links, dict) else {}


def render(html_text: str, links: dict, page_name: str = "") -> str:
    def repl(m: re.Match) -> str:
        key, attrs, text = m.group("key"), m.group("attrs"), m.group("text").strip()
        value = str(links.get(key) or "").strip()
        if key not in links:
            log.info("course_links: '%s'에 모르는 키 '%s' — 중립 문구로 둡니다", page_name, key)
        if not value:
            e = _EMPTY.search(attrs)
            fallback = html.escape(e.group("v")) if e and e.group("v") else DEFAULT_EMPTY
            return (f'<span class="tf-link tf-link--pending" data-tf-link-key="{key}" '
                    f'title="주소는 강사가 수업 중에 안내합니다">{fallback}</span>')
        if _URL.match(value):
            label = text or "열기"
            return (f'<a class="tf-link" data-tf-link-key="{key}" href="{html.escape(value, quote=True)}" '
                    f'target="_blank" rel="noopener">{label}</a>')
        return f'<span class="tf-link tf-link--text" data-tf-link-key="{key}">{html.escape(value)}</span>'

    return _SPAN.sub(repl, html_text)


def on_page_content(html_text, page, config, files):  # noqa: D401 — MkDocs 훅 이름
    if "data-tf-link=" not in html_text:
        return html_text
    return render(html_text, _links(config), getattr(getattr(page, "file", None), "src_uri", ""))
