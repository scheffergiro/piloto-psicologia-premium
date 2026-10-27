"""Shared contact URL and authorized reference SVGs; no copied client information."""
from html import escape
from urllib.parse import quote

WHATSAPP_ICON = '<svg class="button-icon whatsapp-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 2.9L3 21Z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></svg>'
PHONE_ICON = '<svg class="button-icon phone-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7.2 3.5 10 8.2 7.9 10a15.4 15.4 0 0 0 6.1 6.1l1.8-2.1 4.7 2.8-.7 2.7c-.2.7-.8 1.2-1.5 1.2C10 20.1 3.9 14 3.3 5.7c-.1-.7.4-1.3 1.2-1.5l2.7-.7Z"></path></svg>'
FLOAT_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="37" height="36" viewBox="0 0 37 36" fill="none" aria-hidden="true" focusable="false"><circle cx="18.4989" cy="17.5429" r="17.0226" fill="#48D134" stroke="#269A15"></circle><path d="M25.5489 10.4528C24.632 9.52688 23.5399 8.79274 22.3364 8.29314C21.1329 7.79354 19.842 7.53846 18.5389 7.54278C13.0789 7.54278 8.62889 11.9928 8.62889 17.4528C8.62889 19.2028 9.08889 20.9028 9.94889 22.4028L8.54889 27.5428L13.7989 26.1628C15.2489 26.9528 16.8789 27.3728 18.5389 27.3728C23.9989 27.3728 28.4489 22.9228 28.4489 17.4628C28.4489 14.8128 27.4189 12.3228 25.5489 10.4528ZM18.5389 25.6928C17.0589 25.6928 15.6089 25.2928 14.3389 24.5428L14.0389 24.3628L10.9189 25.1828L11.7489 22.1428L11.5489 21.8328C10.7264 20.5198 10.2898 19.0021 10.2889 17.4528C10.2889 12.9128 13.9889 9.21278 18.5289 9.21278C20.7289 9.21278 22.7989 10.0728 24.3489 11.6328C25.1165 12.3966 25.7248 13.3053 26.1385 14.3061C26.5522 15.3069 26.7631 16.3799 26.7589 17.4628C26.7789 22.0028 23.0789 25.6928 18.5389 25.6928ZM23.0589 19.5328C22.8089 19.4128 21.5889 18.8128 21.3689 18.7228C21.1389 18.6428 20.9789 18.6028 20.8089 18.8428C20.6389 19.0928 20.1689 19.6528 20.0289 19.8128C19.8889 19.9828 19.7389 20.0028 19.4889 19.8728C19.2389 19.7528 18.4389 19.4828 17.4989 18.6428C16.7589 17.9828 16.2689 17.1728 16.1189 16.9228C15.9789 16.6728 16.0989 16.5428 16.2289 16.4128C16.3389 16.3028 16.4789 16.1228 16.5989 15.9828C16.7189 15.8428 16.7689 15.7328 16.8489 15.5728C16.9289 15.4028 16.8889 15.2628 16.8289 15.1428C16.7689 15.0228 16.2689 13.8028 16.0689 13.3028C15.8689 12.8228 15.6589 12.8828 15.5089 12.8728H15.0289C14.8589 12.8728 14.5989 12.9328 14.3689 13.1828C14.1489 13.4328 13.5089 14.0328 13.5089 15.2528C13.5089 16.4728 14.3989 17.6528 14.5189 17.8128C14.6389 17.9828 16.2689 20.4828 18.7489 21.5528C19.3389 21.8128 19.7989 21.9628 20.1589 22.0728C20.7489 22.2628 21.2889 22.2328 21.7189 22.1728C22.1989 22.1028 23.1889 21.5728 23.3889 20.9928C23.5989 20.4128 23.5989 19.9228 23.5289 19.8128C23.4589 19.7028 23.3089 19.6528 23.0589 19.5328Z" fill="white"></path></svg>'

def whatsapp_url(home):
    config = home['whatsapp']
    if not config['number']:
        return None
    return 'https://wa.me/' + config['number'] + '?text=' + quote(config['message'], safe='')


def contact_link(home, label, *, icon=WHATSAPP_ICON, classes='button', icon_after=False):
    url = whatsapp_url(home)
    # An unconfirmed number must never become a guessed link.
    url = home['cta_url'] or url
    href = escape(url or '#contato', quote=True)
    external = ' target="_blank" rel="noopener noreferrer"' if url and not url.startswith('#') else ''
    visible = label if url else home['fallback_cta']
    if not whatsapp_url(home): icon = '<svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
    label_html = '<span>' + escape(visible) + '</span>'
    inner = label_html + icon if icon_after else icon + label_html
    return f'<a class="{classes}" href="{href}"{external}>{inner}</a>'


def floating_link(home):
    url = whatsapp_url(home)
    if url is None:
        return ''
    return ('<a class="whatsapp-float" id="whatsapp" href="' + escape(url, quote=True) +
            '" target="_blank" rel="noopener noreferrer" aria-label="' + escape(home['floating_label']+' pelo WhatsApp (abre em nova aba)', quote=True) + '">' +
            '<span class="whatsapp-tooltip" aria-hidden="true">' + escape(home['floating_label']) + '</span>' + FLOAT_ICON + '</a>')
