from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from users.models import UserExtended

SVG_SIZE = 100
BACKGROUND_COLORS = [
    '#F3F4F6',
    '#E0F2FE',
    '#ECFCCB',
    '#FEF3C7',
    '#FCE7F3',
    '#EDE9FE',
]
TEXT_COLORS = [
    '#2563EB',
    '#059669',
    '#DC2626',
    '#7C3AED',
    '#EA580C',
    '#0F172A',
]


def generate_initials(user: 'UserExtended') -> str:
    parts = []

    if user.first_name:
        parts.append(user.first_name[0])

    if user.last_name:
        parts.append(user.last_name[0])

    if not parts and user.username:
        parts.append(user.username[0])

    if not parts and user.email:
        parts.append(user.email[0])

    return ''.join(parts).upper()[:2] or 'U'


def generate_avatar_svg(user: 'UserExtended') -> str:
    bg_color = random.choice(BACKGROUND_COLORS)
    text_color = random.choice(TEXT_COLORS)

    initials = generate_initials(user)

    # Увеличенные размеры шрифта
    font_size = 56 if len(initials) == 1 else 44

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{SVG_SIZE}"
         height="{SVG_SIZE}"
         viewBox="0 0 {SVG_SIZE} {SVG_SIZE}">

        <rect
            width="{SVG_SIZE}"
            height="{SVG_SIZE}"
            rx="16"
            fill="{bg_color}"
        />

        <text
            x="50%"
            y="54%"
            dominant-baseline="middle"
            text-anchor="middle"
            font-family="Arial, Helvetica, sans-serif"
            font-size="{font_size}"
            font-weight="900"
            letter-spacing="-2"
            fill="{text_color}">
            {initials}
        </text>
    </svg>
    """.strip()
