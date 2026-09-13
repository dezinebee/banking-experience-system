"""Shared site navigation: one sidebar + one topbar for every page.
Used by build-docs.py (docs pages) and apply-shell.py (showcase, journey, gallery)."""
import html

STRAT = [
 ("Strategy","strategy/00-README.md","strategy-overview","Phase 01 overview"),
 ("Strategy","strategy/01-vision.md","strategy-vision","Vision"),
 ("Strategy","strategy/02-design-principles.md","strategy-principles","Design principles"),
 ("Strategy","strategy/03-target-users.md","strategy-users","Target users"),
 ("Strategy","strategy/04-uae-context.md","strategy-uae","UAE context"),
 ("Strategy","strategy/05-regulatory-considerations.md","strategy-regulatory","Regulatory considerations"),
 ("Strategy","strategy/06-reference-analysis.md","strategy-references","Reference analysis"),
 ("Strategy","strategy/07-experience-architecture.md","strategy-architecture","Experience architecture"),
 ("Strategy","strategy/08-system-taxonomy.md","strategy-taxonomy","System taxonomy"),
]
SYS = [
 ("Getting started","system/00-README.md","overview","System overview"),
 ("Foundations","system/01-foundations-color.md","color","Color"),
 ("Foundations","system/02-foundations-typography.md","typography","Typography"),
 ("Foundations","system/03-foundations-spacing-layout.md","spacing-layout","Spacing & layout"),
 ("Foundations","system/04-foundations-iconography.md","iconography","Iconography"),
 ("Foundations","system/05-foundations-motion.md","motion","Motion"),
 ("Architecture","system/06-token-architecture.md","tokens","Token architecture"),
 ("Architecture","system/07-financial-semantics.md","financial-semantics","Financial semantics"),
 ("Core components","system/08-core-actions.md","actions","Actions"),
 ("Core components","system/09-core-inputs.md","inputs","Inputs & forms"),
 ("Core components","system/10-core-navigation.md","navigation","Navigation"),
 ("Core components","system/11-core-containers.md","containers","Containers"),
 ("Core components","system/12-core-feedback.md","feedback","Feedback & status"),
 ("Financial components","system/13-financial-money.md","money","Money"),
 ("Financial components","system/14-financial-accounts.md","accounts","Accounts"),
 ("Financial components","system/15-financial-transactions.md","transactions","Transactions"),
 ("Financial components","system/16-financial-payments-transfers.md","payments-transfers","Payments & transfers"),
 ("Financial components","system/17-financial-cards.md","cards","Cards"),
 ("Financial components","system/18-financial-lending.md","lending","Lending & financing"),
 ("Financial components","system/19-financial-investments.md","investments","Investments"),
 ("Financial components","system/20-financial-identity-security.md","identity-security","Identity & security"),
 ("Financial components","system/21-financial-consent-privacy.md","consent-privacy","Consent & privacy"),
 ("Patterns","system/22-patterns-input.md","patterns-input","Asking users for…"),
 ("Patterns","system/23-patterns-confirmation.md","patterns-confirmation","Review & confirmation"),
 ("Patterns","system/24-patterns-status-disclosure.md","patterns-status","Status & disclosure"),
 ("Patterns","system/25-patterns-safety.md","patterns-safety","Fraud, errors & recovery"),
 ("Cross-cutting systems","system/26-data-visualization.md","data-viz","Data visualization"),
 ("Cross-cutting systems","system/27-content-notifications-errors.md","content-errors","Content & errors"),
 ("Cross-cutting systems","system/28-accessibility-architecture.md","accessibility","Accessibility"),
 ("Cross-cutting systems","system/29-localization-rtl.md","localization-rtl","Localization & RTL"),
 ("Cross-cutting systems","system/30-multibrand-theming.md","theming","Multi-brand & theming"),
]
GALLERY = [
 ("index","Install & overview"),("actions","Actions & feedback"),("forms","Forms & inputs"),
 ("money","Money & accounts"),("transactions","Transactions"),("patterns","Composed patterns"),
 ("advanced","Advanced & charts"),
]
ORDER = SYS + STRAT
MDMAP = {f.split("/")[-1]: slug for (g, f, slug, l) in STRAT + SYS}

def _a(href, label, on):
    cls = ' class="on"' if on else ''
    return f'<a href="{href}"{cls}>{html.escape(label)}</a>'

def build_sidenav(prefix, active=None):
    """active: docs slug, or 'showcase' / 'journey' / 'brand-proof' / 'gallery:<slug>' / None."""
    out = ['<div class="grp">Start</div>',
           _a(f"{prefix}index.html", "Home", False),
           _a(f"{prefix}showcase.html", "Live showcase", active == "showcase"),
           _a(f"{prefix}journey-remittance.html", "Remittance journey", active == "journey"),
           _a(f"{prefix}brand-proof.html", "Brand proof", active == "brand-proof"),
           _a(f"{prefix}pages/status.html", "Status & verification", active == "status"),
           _a(f"{prefix}pages/figma-build-spec.html", "Figma library spec", active == "figma-build-spec"),
           '<div class="grp">Live components</div>']
    for slug, label in GALLERY:
        out.append(_a(f"{prefix}components/{slug}.html", label, active == f"gallery:{slug}"))
    cur = None
    for grp, f, slug, label in ORDER:
        if grp != cur:
            out.append(f'<div class="grp">{html.escape(grp)}</div>'); cur = grp
        out.append(_a(f"{prefix}pages/{slug}.html", label, active == slug))
    return "\n".join(out)

def build_status_banner(prefix):
    """Site-wide honesty strip. Every automated gate in this repo is a machine
    gate; none of the four human protocols in docs/testing/ has been run. That
    fact belongs on the page, not only in STATUS.md."""
    return (
        '<div class="statusbar" role="note">'
        '<strong>Draft — not yet human-verified.</strong> '
        'Every gate passing here is automated. No screen-reader, Arabic native-speaker '
        'or usability testing has been carried out yet, and all Arabic UI copy is '
        'machine-drafted. '
        f'<a href="{prefix}pages/status.html">What has and hasn\'t been verified</a>'
        '</div>'
    )


def build_topbar(prefix, section=None):
    """section: 'docs' / 'components' / 'journey' / 'showcase' / None (home)."""
    def pill(href, label, on):
        return f'  <a class="pill{" on" if on else ""}" href="{href}">{label}</a>'
    return "\n".join([
        '<div class="topbar">',
        '  <button class="menu-btn" onclick="document.querySelector(\'nav.side\').classList.toggle(\'open\')">Menu</button>',
        f'  <a href="{prefix}index.html" style="display:flex;align-items:center;gap:10px"><span class="sq">BES</span><span class="name">Banking Experience System</span></a>',
        '  <div class="spacer"></div>',
        pill(f"{prefix}pages/overview.html", "Docs", section == "docs"),
        pill(f"{prefix}components/index.html", "Components", section == "components"),
        pill(f"{prefix}journey-remittance.html", "Journey", section == "journey"),
        pill(f"{prefix}showcase.html", "Showcase", section == "showcase"),
    ])
