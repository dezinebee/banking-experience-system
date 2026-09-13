# Live examples embedded into documentation pages, keyed by page slug.
# Each value is a demo body (goes inside <div class="demo bes">…</div>);
# the build wraps it with the section shell and auto-extracts the code view.
# Markup uses only bes.css classes + tokens — the same code users copy.

DEMOS = {}

DEMOS["color"] = """
<div class="demo-row">
  <span class="bes-badge" data-bes-state="completed"></span>
  <span class="bes-badge" data-bes-state="pending"></span>
  <span class="bes-badge" data-bes-state="failed"></span>
  <span class="bes-badge" data-bes-state="blocked"></span>
  <span class="bes-badge" data-bes-state="reversed"></span>
  <span class="bes-badge bes-badge--neutral">Neutral (generic UI status)</span>
</div>
<div class="demo-row" style="margin-top:16px">
  <bdi class="bes-amount bes-amount--sm">−AED 89.50</bdi>
  <bdi class="bes-amount bes-amount--sm bes-amount--credit">+AED 12,500.00</bdi>
  <bdi class="bes-amount bes-amount--sm bes-amount--negative">−AED 320.00 overdrawn</bdi>
</div>
"""

DEMOS["typography"] = """
<div class="demo-stack">
  <div style="font-size:var(--bes-type-h1-size);line-height:var(--bes-type-h1-line);font-weight:var(--bes-type-h1-weight)">Send money abroad</div>
  <div style="font-size:var(--bes-type-body-size);line-height:var(--bes-type-body-line);max-width:60ch">Your transfer usually arrives within one hour. We'll notify you at every step.</div>
  <bdi class="bes-amount bes-amount--hero"><span class="cur">AED</span> 25,000<span class="dec">.00</span></bdi>
  <div class="demo-row">
    <bdi class="bes-amount bes-amount--sm">−AED 1,250.50</bdi>
    <bdi class="bes-amount bes-amount--sm bes-amount--credit">+AED 12,500.00</bdi>
    <bdi class="bes-amount bes-amount--meta">≈ ₹250,800.00 · estimated</bdi>
  </div>
</div>
"""

DEMOS["actions"] = """
<div class="demo-row">
  <button class="bes-btn bes-btn--primary">Send <bdi class="bes-amount">AED 5,000.00</bdi></button>
  <button class="bes-btn bes-btn--secondary">Back</button>
  <button class="bes-btn bes-btn--ghost">View Key Facts (PDF)</button>
  <button class="bes-btn bes-btn--destructive">Cancel transfer</button>
  <button class="bes-btn bes-btn--primary bes-btn--loading">Sending…</button>
  <button class="bes-btn bes-btn--primary" disabled>Continue</button>
</div>
"""

DEMOS["inputs"] = """
<div class="demo-stack">
  <div class="bes-field">
    <label class="bes-label" for="d-iban">Recipient IBAN</label>
    <input class="bes-input bes-input--ltr" id="d-iban" spellcheck="false" aria-invalid="true" aria-describedby="d-iban-e" value="AE07 0331 2345">
    <div class="bes-error-msg" id="d-iban-e">This IBAN doesn't look right — UAE IBANs have 23 characters starting with AE. Paste it with or without spaces.</div>
  </div>
  <div class="bes-field">
    <label class="bes-label" for="d-amt">Amount</label>
    <div class="bes-currency">
      <span class="code" aria-hidden="true">AED</span>
      <input class="bes-input" id="d-amt" inputmode="decimal" value="5,000" data-bes-currency data-max="25000" data-currency="AED" data-left-msg="Leaves {x} available" data-over-msg="That's {x} more than your available balance">
    </div>
    <div class="bes-context-line">Leaves AED 20,000.00 available</div>
  </div>
  <label class="bes-check">
    <input type="checkbox">
    <span>I accept the <a href="#">Key Facts Statement (PDF)</a><span class="desc">Version 3.2 · required to continue</span></span>
  </label>
  <label class="bes-switch">
    <input type="checkbox" checked>
    <span class="track" aria-hidden="true"></span>
    <span>International payments <span class="state">On</span></span>
  </label>
</div>
"""

DEMOS["navigation"] = """
<div class="demo-stack" style="max-width:560px">
  <div>
    <div class="bes-tabs" role="tablist" aria-label="Account sections">
      <button class="bes-tab" role="tab" aria-selected="true" aria-controls="dp-1" id="dt-1">Transactions</button>
      <button class="bes-tab" role="tab" aria-selected="false" aria-controls="dp-2" id="dt-2" tabindex="-1">Details</button>
      <button class="bes-tab" role="tab" aria-selected="false" aria-controls="dp-3" id="dt-3" tabindex="-1">Statements</button>
    </div>
    <div id="dp-1" role="tabpanel" aria-labelledby="dt-1" style="padding:12px 2px;font-size:14px;color:var(--bes-text-secondary)">214 transactions this quarter.</div>
    <div id="dp-2" role="tabpanel" aria-labelledby="dt-2" hidden style="padding:12px 2px;font-size:14px;color:var(--bes-text-secondary)">IBAN, SWIFT and account facts.</div>
    <div id="dp-3" role="tabpanel" aria-labelledby="dt-3" hidden style="padding:12px 2px;font-size:14px;color:var(--bes-text-secondary)">Monthly statements, PDF and CSV.</div>
  </div>
  <div class="bes-stepper" aria-label="Progress: step 2 of 4">
    <span class="bes-step bes-step--done"><span class="n">✓</span> Amount</span>
    <span class="bes-step-bar"></span>
    <span class="bes-step bes-step--current"><span class="n">2</span> Recipient</span>
    <span class="bes-step-bar"></span>
    <span class="bes-step"><span class="n">3</span> Review</span>
    <span class="bes-step-bar"></span>
    <span class="bes-step"><span class="n">4</span> Done</span>
  </div>
</div>
"""

DEMOS["containers"] = """
<div class="demo-row" style="align-items:flex-start">
  <div class="bes-card" style="max-width:300px">
    <div style="font-weight:600;margin-bottom:4px">Card container</div>
    <div style="font-size:13.5px;color:var(--bes-text-secondary)">One concept per card. Dense surfaces prefer flat sections with dividers.</div>
  </div>
  <button class="bes-btn bes-btn--secondary" data-bes-open="doc-modal">Open confirm dialog</button>
</div>
<div class="bes-scrim" id="doc-modal" role="dialog" aria-modal="true" aria-labelledby="doc-m-t">
  <div class="bes-modal">
    <h3 id="doc-m-t">Remove beneficiary Rajesh Kumar?</h3>
    <p>You'll need to add them again to send money — and new payees may have a 24-hour holding period.</p>
    <div class="actions">
      <button class="bes-btn bes-btn--secondary" data-bes-close="doc-modal">Keep beneficiary</button>
      <button class="bes-btn bes-btn--destructive-solid" data-bes-close="doc-modal">Remove beneficiary</button>
    </div>
  </div>
</div>
"""

DEMOS["feedback"] = """
<div class="demo-stack" style="max-width:560px">
  <div class="bes-alert bes-alert--error" role="alert">
    <div><b>We couldn't complete this transfer.</b>
    Your bank declined the transaction. No money was deducted from your account.
    <div class="actions"><a href="#">Try again</a><a href="#">Contact support</a></div></div>
  </div>
  <div class="bes-alert bes-alert--info" role="status">
    <div><b>We're checking your transfer status.</b> Your money is safe — we'll confirm within 30 minutes.</div>
  </div>
  <div class="demo-row" style="flex-wrap:wrap;gap:8px">
    <span class="bes-badge" data-bes-state="draft"></span>
    <span class="bes-badge" data-bes-state="review"></span>
    <span class="bes-badge" data-bes-state="authentication"></span>
    <span class="bes-badge" data-bes-state="processing"></span>
    <span class="bes-badge" data-bes-state="pending"></span>
    <span class="bes-badge" data-bes-state="completed"></span>
    <span class="bes-badge" data-bes-state="failed"></span>
    <span class="bes-badge" data-bes-state="unknown"></span>
    <span class="bes-badge" data-bes-state="blocked"></span>
    <span class="bes-badge" data-bes-state="reversed"></span>
    <span class="bes-badge" data-bes-state="refunded"></span>
    <span class="bes-badge" data-bes-state="disputed"></span>
    <span class="bes-badge" data-bes-state="cancelled"></span>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0;max-width:60ch">
    All 13 canonical states (doc 07 §4). The markup names only the state —
    <code>data-bes-state="unknown"</code> — and colour, glyph and label all come from one
    registry, so two screens cannot drift. <strong>Completed and Refunded share green;
    Processing, Pending and Checking status share teal.</strong> That is deliberate: they are
    related states, and what tells them apart is the glyph and the word, never the colour alone.
  </p>
  <div class="demo-row">
    <button class="bes-btn bes-btn--secondary bes-btn--sm" data-bes-toast="IBAN copied">Show toast</button>
  </div>
</div>
"""

RESULT_STATES = """
<div class="demo-stack" style="max-width:420px">
  <div class="bes-card bes-result" data-bes-state="unknown">
    <div class="ic"></div><h3></h3>
    <p class="money-state"></p>
    <div class="demo-row" style="justify-content:center;margin-top:14px">
      <button class="bes-btn bes-btn--secondary bes-btn--sm">Notify me</button>
      <button class="bes-btn bes-btn--secondary bes-btn--sm">Contact support</button>
      <button class="bes-btn bes-btn--primary bes-btn--sm" data-bes-retry>Try again</button>
    </div>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:0;max-width:60ch">
    The markup above <em>includes</em> a &ldquo;Try again&rdquo; button. It is not rendered:
    the binder removes any <code>[data-bes-retry]</code> from a state whose registry entry
    says <code>allowsRetry: false</code>. A rail that has gone quiet may still be holding a
    successful transfer, so retry is a double-send — and a missing button is the smaller
    failure. Only a confirmed <code>failed</code> keeps it.
  </p>
  <div class="bes-card bes-result" data-bes-state="blocked">
    <div class="ic"></div><h3></h3>
    <p class="money-state">Your money is held while we complete the checks.</p>
  </div>
  <div class="bes-card bes-result" data-bes-state="refunded">
    <div class="ic"></div><h3></h3>
    <p class="money-state">AED 149.00 returned to Current account &bull;&bull;4521 on 29 August.</p>
  </div>
</div>
"""

DEMOS["financial-semantics"] = """
<div class="demo-stack" style="max-width:560px">
  <div class="demo-row">
    <span class="bes-badge bes-badge--neutral">Draft</span>
    <span class="bes-badge bes-badge--info">Processing</span>
    <span class="bes-badge bes-badge--pending">Pending</span>
    <span class="bes-badge bes-badge--success">Completed</span>
    <span class="bes-badge bes-badge--error">Failed</span>
    <span class="bes-badge bes-badge--info">Checking status</span>
    <span class="bes-badge bes-badge--warning">Additional checks</span>
    <span class="bes-badge bes-badge--reversed">Reversed</span>
  </div>
  <div class="bes-alert bes-alert--info" role="status">
    <div><b>We're checking your transfer status.</b> Your money is safe — no amount will be deducted twice. We'll confirm within 30 minutes. <span style="font-weight:600">(UNKNOWN is a designed state — never shown as "failed".)</span></div>
  </div>
</div>
""" + RESULT_STATES

DEMOS["money"] = """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">You send</span><span class="v"><bdi class="bes-amount">AED 10,000.00</bdi></span></div>
    <div class="bes-row bes-row--rate"><span>Exchange rate</span><span><bdi class="bes-amount">1 AED = ₹25.0800</bdi> · <span class="bes-lock">locked 4:59</span></span></div>
    <div class="sep"></div>
    <div class="bes-row"><span class="k">Transfer fee</span><span class="v"><bdi class="bes-amount">AED 15.00</bdi></span></div>
    <div class="bes-row"><span class="k">FX margin <button class="bes-whyfee" type="button">why?</button></span><span class="v"><bdi class="bes-amount">AED 20.00</bdi></span></div>
    <div class="bes-row"><span class="k">VAT on fees (5%)</span><span class="v"><bdi class="bes-amount">AED 1.75</bdi></span></div>
  </div>
  <div class="bes-total"><span class="k">Total you pay</span><span class="v"><bdi class="bes-amount">AED 10,036.75</bdi></span></div>
  <div class="bes-row" style="padding-top:10px"><span class="k">Recipient gets</span><span class="v" style="color:var(--bes-financial-income)"><bdi class="bes-amount">₹250,800.00</bdi> · exact</span></div>
</div>
"""

DEMOS["accounts"] = """
<div class="bes-card bes-acct" style="max-width:400px">
  <div class="row1">
    <div>
      <div class="name">Current account</div>
      <div class="meta"><bdi class="bes-amount">••4521</bdi> · Personal</div>
    </div>
    <button class="bes-iconbtn" aria-label="Hide balance" data-bes-mask="doc-bal" aria-pressed="false">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M2 10s3-5.5 8-5.5S18 10 18 10s-3 5.5-8 5.5S2 10 2 10z" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="2.4" stroke="currentColor" stroke-width="1.5"/></svg>
    </button>
  </div>
  <bdi class="bes-amount bes-amount--lg" id="doc-bal"><span class="cur">AED</span> 25,000.00</bdi>
  <div class="sub">Available · <bdi class="bes-amount">AED 500.00</bdi> reserved</div>
  <div class="actions">
    <button class="bes-btn bes-btn--primary bes-btn--sm">Send</button>
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Details</button>
  </div>
</div>
"""

DEMOS["transactions"] = """
<div class="bes-list" style="max-width:560px">
  <div class="bes-list-head">Pending</div>
  <div class="bes-item">
    <span class="main"><span class="t">Priya Kumar</span><br><span class="s">Transfer · AED → INR</span></span>
    <span class="trail"><bdi class="bes-amount bes-amount--sm">−AED 10,036.75</bdi><span class="bes-badge bes-badge--pending">Pending</span></span>
  </div>
  <div class="bes-list-head">Today</div>
  <div class="bes-item">
    <span class="main"><span class="t">Carrefour</span><br><span class="s">Groceries · Card ••8834 · 19:42</span></span>
    <span class="trail"><bdi class="bes-amount bes-amount--sm">−AED 89.50</bdi></span>
  </div>
  <div class="bes-item">
    <span class="main"><span class="t">Salary — Al Noor Trading LLC</span><br><span class="s">Incoming transfer · 09:00</span></span>
    <span class="trail"><bdi class="bes-amount bes-amount--sm bes-amount--credit">+AED 18,500.00</bdi></span>
  </div>
  <div class="bes-item">
    <span class="main"><span class="t">Noon.com</span><br><span class="s"><bdi class="bes-amount bes-amount--struck">AED 320.00</bdi> · Declined — over daily limit</span></span>
    <span class="trail"><span class="bes-badge bes-badge--error">Declined</span></span>
  </div>
</div>
"""

DEMOS["payments-transfers"] = """
<div class="demo-stack" style="max-width:480px">
  <div class="bes-card">
    <div class="bes-cop bes-cop--close">
      <span class="ic"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5L15 14H1L8 1.5z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M8 6v3.2M8 11.4v.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span>
      <div><b>Did you mean "Priya Kumar Nair"?</b><p>The name you entered is close, but not exact. Check with the recipient before sending.</p>
      <div class="demo-row" style="margin-top:12px"><button class="bes-btn bes-btn--primary bes-btn--sm">Use this name</button><button class="bes-btn bes-btn--secondary bes-btn--sm">Check with recipient</button></div></div>
    </div>
  </div>
  <div class="bes-card">
    <ul class="bes-timeline">
      <li class="done"><span class="dot">✓</span><span><span class="t">Sent from your account</span><br><span class="s">Today 14:32</span></span></li>
      <li class="current"><span class="dot">●</span><span><span class="t">With recipient bank</span><br><span class="s">Usually within 1 hour · expected by 15:30</span></span></li>
      <li><span class="dot">○</span><span><span class="t">Delivered to Priya Kumar</span><br><span class="s">We'll notify you</span></span></li>
    </ul>
  </div>
</div>
"""

DEMOS["cards"] = """
<div class="bes-card" style="max-width:420px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
    <div style="font-weight:600">Debit card <bdi class="bes-amount">••8834</bdi></div>
    <span class="bes-badge bes-badge--info">Frozen</span>
  </div>
  <label class="bes-switch" style="margin-bottom:10px">
    <input type="checkbox" checked>
    <span class="track" aria-hidden="true"></span>
    <span>Freeze card <span class="state">On — blocks new payments, ATM and online</span></span>
  </label>
  <label class="bes-switch" style="margin-bottom:10px">
    <input type="checkbox">
    <span class="track" aria-hidden="true"></span>
    <span>Online payments <span class="state">Off</span></span>
  </label>
  <label class="bes-switch">
    <input type="checkbox" checked>
    <span class="track" aria-hidden="true"></span>
    <span>Contactless <span class="state">On</span></span>
  </label>
  <div class="bes-limit" style="margin-top:16px">
    <div style="font-size:13.5px;font-weight:600;margin-bottom:6px">Daily spend limit</div>
    <div class="bes-progress bes-progress--warn"><div class="fill" style="inline-size:82%"></div></div>
    <div class="figures"><span class="used"><bdi class="bes-amount">AED 2,460.00</bdi> used</span><span>of <bdi class="bes-amount">AED 3,000.00</bdi></span></div>
  </div>
</div>
"""

DEMOS["lending"] = """
<div class="bes-card" style="max-width:440px;border-radius:8px">
  <span style="display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--bes-text-secondary);border:1px solid var(--bes-border-strong);border-radius:4px;padding:3px 8px;margin-bottom:12px">Personal financing · Fixed rate</span>
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Amount</span><span class="v"><bdi class="bes-amount">AED 100,000.00</bdi></span></div>
    <div class="bes-row"><span class="k">Term</span><span class="v">48 months</span></div>
    <div class="bes-row"><span class="k">Rate (reducing)</span><span class="v"><bdi class="bes-amount">5.99%</bdi></span></div>
    <div class="bes-row"><span class="k">Monthly payment</span><span class="v"><bdi class="bes-amount">AED 2,348.00</bdi></span></div>
    <div class="bes-row"><span class="k">Total repayment</span><span class="v"><bdi class="bes-amount">AED 112,704.00</bdi></span></div>
    <div class="bes-row"><span class="k">Processing fee</span><span class="v"><bdi class="bes-amount">AED 1,050.00</bdi></span></div>
  </div>
  <div class="bes-alert bes-alert--warning" style="margin-block-start:12px">
    <div>Missing payments can affect your credit record and future borrowing.</div>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 6px">You can cancel within 5 business days of signing.</p>
  <a href="#" style="font-size:14px;font-weight:500">Key Facts Statement (PDF)</a>
</div>
"""

DEMOS["identity-security"] = """
<div class="demo-stack" style="max-width:560px">
  <div class="bes-alert bes-alert--warning">
    <div><b>Are you on a call with someone guiding you through this payment?</b>
    Banks never ask you to move money to a "safe account". If someone is pressuring you, hang up — genuine payees will understand a short wait.
    <div class="actions"><a href="#">No, continue</a><a href="#">Yes — pause and get help</a></div></div>
  </div>
  <div class="bes-card" style="display:flex;justify-content:space-between;align-items:center;gap:12px">
    <div>
      <div style="font-weight:600;font-size:15px">iPhone 15 Pro · Dubai</div>
      <div style="font-size:13px;color:var(--bes-text-secondary)">This device · Last active now</div>
    </div>
    <span class="bes-badge bes-badge--success">Trusted</span>
  </div>
  <div class="bes-card" style="display:flex;justify-content:space-between;align-items:center;gap:12px">
    <div>
      <div style="font-weight:600;font-size:15px">Chrome on Windows · Sharjah</div>
      <div style="font-size:13px;color:var(--bes-text-secondary)">First seen today 11:02</div>
    </div>
    <div class="demo-row"><span class="bes-badge bes-badge--warning">New</span>
    <button class="bes-btn bes-btn--destructive bes-btn--sm">Sign out</button></div>
  </div>
</div>
"""

DEMOS["consent-privacy"] = """
<div class="bes-card" style="max-width:440px">
  <div style="display:flex;gap:12px;align-items:center;margin-bottom:14px">
    <span style="inline-size:40px;block-size:40px;border-radius:10px;background:var(--bes-transaction-reversedTint);color:var(--bes-transaction-reversed);display:grid;place-items:center;font-weight:700">AF</span>
    <div>
      <div style="font-weight:600">ABC Finance</div>
      <div style="font-size:12.5px;color:var(--bes-status-success);font-weight:600">✓ Licensed provider · verified today</div>
    </div>
  </div>
  <p style="margin:0 0 8px;font-size:14.5px;font-weight:500">wants to access:</p>
  <div class="bes-rows">
    <div class="bes-row"><span class="k">✓ Account information</span></div>
    <div class="bes-row"><span class="k">✓ Balance</span></div>
    <div class="bes-row"><span class="k">✓ Transaction history (12 months)</span></div>
  </div>
  <div style="font-size:13.5px;color:var(--bes-text-secondary);line-height:1.7;border-block-start:1px solid var(--bes-border-default);padding-block-start:10px;margin-top:6px">
    Purpose: <b style="color:var(--bes-text-primary)">Personal financial management</b><br>
    Access until: <b style="color:var(--bes-text-primary)">30 September 2026</b><br>
    Stop this anytime in Settings → Data sharing.
  </div>
  <div class="demo-row" style="margin-top:14px">
    <button class="bes-btn bes-btn--primary" style="flex:1">Allow access</button>
    <button class="bes-btn bes-btn--secondary" style="flex:1">Cancel</button>
  </div>
</div>
"""

DEMOS["patterns-confirmation"] = """
<div class="bes-card" style="max-width:440px">
  <h3 style="margin:0 0 14px;font-size:18px;font-weight:600">Check and confirm</h3>
  <div class="bes-rows">
    <div class="bes-row"><span class="k">To</span><span class="v">Priya Kumar · <bdi class="bes-amount">ICICI ••4102</bdi> <a href="#" style="font-size:13px">Change</a></span></div>
    <div class="bes-row"><span class="k">You send</span><span class="v"><bdi class="bes-amount">AED 10,000.00</bdi></span></div>
    <div class="sep"></div>
    <div class="bes-row"><span class="k">All fees + VAT</span><span class="v"><bdi class="bes-amount">AED 36.75</bdi></span></div>
  </div>
  <div class="bes-total"><span class="k">Total you pay</span><span class="v"><bdi class="bes-amount">AED 10,036.75</bdi></span></div>
  <p class="bes-consequence">We'll send AED 10,036.75 from your current account now. International transfers can't be cancelled once sent.</p>
  <button class="bes-btn bes-btn--primary bes-btn--lg">Send <bdi class="bes-amount">AED 10,036.75</bdi></button>
</div>
"""

DEMOS["patterns-safety"] = """
<div class="bes-card" style="max-width:460px">
  <div style="font-size:17px;font-weight:600;margin-bottom:6px">We noticed unusual activity</div>
  <bdi class="bes-amount bes-amount--md">AED 18,500.00</bdi>
  <div style="font-size:13.5px;color:var(--bes-text-secondary);margin:2px 0 14px">International transfer · Dubai → India · today 15:47</div>
  <div style="font-size:14.5px;font-weight:500;margin-bottom:12px">Did you make this transfer?</div>
  <div class="demo-row">
    <button class="bes-btn bes-btn--secondary" style="flex:1">Yes, it was me</button>
    <button class="bes-btn bes-btn--primary" style="flex:1">No, secure my account</button>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:12px 0 0">We'll hold this transfer for up to 2 hours awaiting your reply, then cancel it for safety.</p>
</div>
"""

# ---- extended coverage: every system doc page carries a visual ----

DEMOS["overview"] = """
<div class="demo-stack">
  <div class="demo-row">
    <button class="bes-btn bes-btn--primary">Send <bdi class="bes-amount">AED 5,000.00</bdi></button>
    <span class="bes-badge bes-badge--pending">Pending</span>
    <span class="bes-badge bes-badge--success">Completed</span>
    <span class="bes-badge bes-badge--info">Checking status</span>
    <bdi class="bes-amount bes-amount--md">−AED 1,250.50</bdi>
  </div>
  <div class="bes-alert bes-alert--info" role="status">
    <div><b>This documentation is live.</b> Most pages open with a working example built from the coded library — the same markup you can copy. Full interactive sets: <a href="../components/index.html">component gallery</a> · <a href="../journey-remittance.html">remittance journey</a>.</div>
  </div>
</div>
"""

DEMOS["spacing-layout"] = """
<div class="demo-stack" style="max-width:560px">
  <div>
    <div style="font-size:13px;font-weight:600;margin-bottom:8px">The 4px scale</div>
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div style="inline-size:24px;block-size:4px;background:var(--bes-action-primary);border-radius:2px" title="4"></div>
      <div style="inline-size:24px;block-size:8px;background:var(--bes-action-primary);border-radius:2px" title="8"></div>
      <div style="inline-size:24px;block-size:16px;background:var(--bes-action-primary);border-radius:2px" title="16"></div>
      <div style="inline-size:24px;block-size:24px;background:var(--bes-action-primary);border-radius:2px" title="24"></div>
      <div style="inline-size:24px;block-size:32px;background:var(--bes-action-primary);border-radius:2px" title="32"></div>
      <div style="inline-size:24px;block-size:48px;background:var(--bes-action-primary);border-radius:2px" title="48"></div>
      <div style="inline-size:24px;block-size:64px;background:var(--bes-action-primary);border-radius:2px" title="64"></div>
    </div>
    <div style="display:flex;gap:8px;font-size:11px;color:var(--bes-text-secondary);margin-top:4px"><span style="inline-size:24px;text-align:center">4</span><span style="inline-size:24px;text-align:center">8</span><span style="inline-size:24px;text-align:center">16</span><span style="inline-size:24px;text-align:center">24</span><span style="inline-size:24px;text-align:center">32</span><span style="inline-size:24px;text-align:center">48</span><span style="inline-size:24px;text-align:center">64</span></div>
  </div>
  <div>
    <div style="font-size:13px;font-weight:600;margin-bottom:8px">Density modes — same list row, three modes</div>
    <div class="bes-list">
      <div class="bes-item" style="min-block-size:64px"><span class="main"><span class="t">Comfortable · 64px rows</span><br><span class="s">Consumer onboarding, elderly contexts</span></span><span class="trail"><bdi class="bes-amount bes-amount--sm">−AED 89.50</bdi></span></div>
      <div class="bes-item" style="min-block-size:56px"><span class="main"><span class="t">Standard · 56px rows</span><br><span class="s">Retail default</span></span><span class="trail"><bdi class="bes-amount bes-amount--sm">−AED 89.50</bdi></span></div>
      <div class="bes-item" style="min-block-size:44px;padding-block:6px"><span class="main"><span class="t">Compact · 44px rows</span><br><span class="s">SME &amp; treasury</span></span><span class="trail"><bdi class="bes-amount bes-amount--sm">−AED 89.50</bdi></span></div>
    </div>
  </div>
</div>
"""

DEMOS["iconography"] = """
<div class="demo-stack" style="max-width:560px">
  <div>
    <div style="font-size:13px;font-weight:600;margin-bottom:10px">Mirrors in RTL (directional semantics) — try the toggle</div>
    <div class="demo-row" style="font-size:0;gap:16px" id="icon-mirror-row">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><path d="M15 5l-6 7 6 7" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/><title>back</title></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><path d="M4 12h14M14 6l6 6-6 6" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/><title>send / next</title></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><path d="M4 8h12M12 4l4 4-4 4M20 16H8m4 4l-4-4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><title>transfer</title></svg>
    </div>
    <div style="font-size:13px;font-weight:600;margin:16px 0 10px">Never mirrors (universal semantics)</div>
    <div class="demo-row" style="gap:16px">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.6"/><path d="M12 7.5V12l3 2.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><title>clock</title></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-status-success)"><path d="M5 12.5L10 17.5 19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><title>check</title></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><path d="M12 3l7.5 3.4v4.2c0 4.2-2.9 7.2-7.5 8.9-4.6-1.7-7.5-4.7-7.5-8.9V6.4L12 3z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><title>shield</title></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="color:var(--bes-text-primary)"><rect x="4" y="4" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="13.5" y="4" width="3" height="3" stroke="currentColor" stroke-width="1.5"/><rect x="4" y="13.5" width="3" height="3" stroke="currentColor" stroke-width="1.5"/><path d="M14 13.5h6M14 17h3m3 0h.01M14 20.5h6" stroke="currentColor" stroke-width="1.5"/><title>QR</title></svg>
    </div>
  </div>
  <button class="bes-btn bes-btn--secondary bes-btn--sm" style="align-self:flex-start"
    onclick="var d=this.closest('.demo');var r=d.getAttribute('dir')==='rtl'?'ltr':'rtl';d.setAttribute('dir',r);document.getElementById('icon-mirror-row').style.transform=r==='rtl'?'scaleX(-1)':'none'">
    Toggle direction on this demo</button>
</div>
"""

DEMOS["motion"] = """
<div class="demo-stack" style="max-width:520px">
  <div class="demo-row">
    <button class="bes-btn bes-btn--primary" onclick="var b=this;b.classList.add('bes-btn--loading');setTimeout(function(){b.classList.remove('bes-btn--loading');BES.toast('Transfer sent')},1600)">Press me — loading → confirm</button>
    <button class="bes-btn bes-btn--secondary" data-bes-toast="Preference saved">Toast (motion.standard)</button>
  </div>
  <div class="demo-row" style="align-items:center">
    <div class="bes-skel" style="inline-size:180px;block-size:16px"></div>
    <span style="font-size:13px;color:var(--bes-text-secondary)">Skeleton pulse — static under prefers-reduced-motion</span>
  </div>
  <div class="bes-alert bes-alert--info"><div>No count-up animations on real balances, no shakes on errors, no entrance animation on fraud interruptions — motion is information, not decoration.</div></div>
</div>
"""

DEMOS["tokens"] = """
<div class="demo-stack" style="max-width:560px">
  <div style="font-size:13px;font-weight:600;margin-bottom:2px">Semantic tokens resolving live (they change with this page's theme)</div>
  <div class="demo-row">
    <span class="chip" style="display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bes-border-default);border-radius:999px;padding:6px 12px;font-size:13px"><span style="inline-size:12px;block-size:12px;border-radius:3px;background:var(--bes-action-primary)"></span><code>--bes-action-primary</code></span>
    <span class="chip" style="display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bes-border-default);border-radius:999px;padding:6px 12px;font-size:13px"><span style="inline-size:12px;block-size:12px;border-radius:3px;background:var(--bes-financial-income)"></span><code>--bes-financial-income</code></span>
    <span class="chip" style="display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bes-border-default);border-radius:999px;padding:6px 12px;font-size:13px"><span style="inline-size:12px;block-size:12px;border-radius:3px;background:var(--bes-transaction-pending)"></span><code>--bes-transaction-pending</code></span>
    <span class="chip" style="display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bes-border-default);border-radius:999px;padding:6px 12px;font-size:13px"><span style="inline-size:12px;block-size:12px;border-radius:3px;background:var(--bes-surface-tertiary);border:1px solid var(--bes-border-strong)"></span><code>--bes-surface-tertiary</code></span>
  </div>
  <div style="font-size:13px;font-weight:600;margin:8px 0 2px">One component, two brands — same behavior, token values swapped</div>
  <div class="demo-row">
    <button class="bes-btn bes-btn--primary">Send <bdi class="bes-amount">AED 5,000.00</bdi></button>
    <span style="--bes-action-primary:#0F6974;--bes-action-primaryHover:#0B525B"><button class="bes-btn bes-btn--primary">Send <bdi class="bes-amount">AED 5,000.00</bdi></button></span>
    <span style="--bes-action-primary:#5A3DA0;--bes-action-primaryHover:#46307C"><button class="bes-btn bes-btn--primary">Send <bdi class="bes-amount">AED 5,000.00</bdi></button></span>
  </div>
</div>
"""

DEMOS["investments"] = """
<div class="demo-stack" style="max-width:560px">
  <div class="demo-row" style="align-items:flex-start">
    <div class="bes-risk bes-risk--low" style="flex:1;min-inline-size:240px">
      <span class="lvl">Risk level 2 of 7 — Low</span>
      <div class="scale"><span class="on"></span><span class="on"></span><span></span><span></span><span></span><span></span><span></span></div>
      <span class="meaning">Value moves a little; you could get back less than you invest.</span>
    </div>
    <div>
      <div style="font-size:13px;color:var(--bes-text-secondary)">Portfolio · 1M</div>
      <bdi class="bes-amount bes-amount--md">AED 48,320.00</bdi><br>
      <span class="bes-delta bes-delta--up">▲ +AED 1,120.00 (2.4%) <span class="tf">vs July</span></span>
    </div>
  </div>
  <div class="bes-chart" data-bes-chart='{"type":"donut","data":[{"label":"UAE equities","value":19300},{"label":"Global ETFs","value":14500},{"label":"Sukuk","value":9600},{"label":"Cash","value":4920}],"opts":{"center":"AED 48.3K","centerSub":"Allocation","label":"Asset allocation, total 48,320 dirhams","colLabel":"Class","colValue":"AED"}}'></div>
</div>
"""

DEMOS["data-viz"] = """
<div class="demo-stack">
  <div class="grid2" style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
    <div>
      <div style="font-size:13px;font-weight:600;margin-bottom:6px">Spending breakdown — August</div>
      <div class="bes-chart" data-bes-chart='{"type":"donut","data":[{"label":"Groceries","value":2340},{"label":"Dining","value":1240},{"label":"Transport","value":860},{"label":"Utilities","value":1590},{"label":"Other","value":2890}],"opts":{"center":"AED 8.9K","centerSub":"August","label":"Spending by category, August","colLabel":"Category","colValue":"AED"}}'></div>
    </div>
    <div>
      <div style="font-size:13px;font-weight:600;margin-bottom:6px">Balance trend — 6 months</div>
      <div class="bes-chart" data-bes-chart='{"type":"line","data":[{"label":"Mar","value":21000},{"label":"Apr","value":19400},{"label":"May","value":24100},{"label":"Jun","value":22800},{"label":"Jul","value":26500},{"label":"Aug","value":25000}],"opts":{"label":"Balance trend over six months","colLabel":"Month","colValue":"AED"}}'></div>
    </div>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:4px 0 0">Every chart ships a "View as table" equivalent (expand under each) — data is never conveyed by color alone.</p>
</div>
"""

DEMOS["patterns-input"] = """
<div class="demo-stack" style="max-width:440px">
  <div class="bes-field">
    <label class="bes-label" for="pd-phone">Mobile number</label>
    <div style="display:flex;gap:8px">
      <div class="bes-select" style="inline-size:110px"><select aria-label="Country code"><option>+971</option><option>+91</option><option>+92</option><option>+63</option></select></div>
      <input class="bes-input bes-input--ltr" id="pd-phone" inputmode="tel" placeholder="50 123 4567" style="flex:1">
    </div>
    <div class="bes-help">UAE mobile numbers have 9 digits after +971 — spaces and dashes are fine.</div>
  </div>
  <div class="bes-field" style="margin-bottom:0">
    <label class="bes-label" for="pd-pob">Purpose of transfer</label>
    <div class="bes-select"><select id="pd-pob"><option>Family support</option><option>Savings</option><option>Rent</option><option>Education fees</option><option>Medical</option></select></div>
    <div class="bes-help">Required for international transfers — plain-language options, codes stay internal.</div>
  </div>
</div>
"""

DEMOS["patterns-status"] = """
<div class="demo-stack" style="max-width:480px">
  <div class="bes-banner" style="border-radius:10px;border:1px solid var(--bes-border-default)">
    <svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.4"/><path d="M8 7.4v3.2M8 5v.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    Balances from other banks are delayed — showing data from 14:32.
  </div>
  <div class="bes-card">
    <div style="font-size:13.5px;font-weight:600;margin-bottom:6px">Card holds — release dates stated</div>
    <div class="bes-rows">
      <div class="bes-row"><span class="k">Rove Hotels (pre-auth)</span><span class="v"><bdi class="bes-amount">AED 350.00</bdi> · <span style="color:var(--bes-text-secondary);font-weight:400">releases by 8 Sep</span></span></div>
      <div class="bes-row"><span class="k">ADNOC (fuel pre-auth)</span><span class="v"><bdi class="bes-amount">AED 150.00</bdi> · <span style="color:var(--bes-text-secondary);font-weight:400">releases by 2 Sep</span></span></div>
    </div>
  </div>
  <div class="bes-limit">
    <div style="font-size:13.5px;font-weight:600;margin-bottom:6px">Dining budget — August</div>
    <div class="bes-progress bes-progress--warn"><div class="fill" style="inline-size:84%"></div></div>
    <div class="figures"><span class="used"><bdi class="bes-amount">AED 1,240.00</bdi> spent</span><span><bdi class="bes-amount">AED 240.00</bdi> left</span></div>
  </div>
</div>
"""

DEMOS["content-errors"] = """
<div class="demo-stack" style="max-width:520px">
  <div class="bes-list">
    <div class="bes-notif bes-notif--security">
      <span class="ic"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5l5.5 2v4c0 3.2-2.3 5.6-5.5 7-3.2-1.4-5.5-3.8-5.5-7v-4l5.5-2z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg></span>
      <span style="flex:1"><span class="t">New device signed in — Chrome on Windows, Sharjah</span><br><span class="s">Was this you? Review your devices.</span></span>
      <span class="when">11:02</span>
    </div>
    <div class="bes-notif">
      <span class="ic"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2v8m0 0L5 7m3 3l3-3M3 13h10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <span style="flex:1"><span class="t">Salary received — <bdi class="bes-amount">+AED 18,500.00</bdi></span><br><span class="s">Al Noor Trading LLC · Current account ••4521</span></span>
      <span class="when">09:00</span>
    </div>
  </div>
  <div class="bes-alert bes-alert--error" role="alert">
    <div><b>We couldn't complete this transfer.</b> Your bank declined the transaction. No money was deducted from your account.
    <div class="actions"><a href="#">Try again</a><a href="#">Contact support</a></div></div>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:0">Security notifications are visually distinct from transaction notices and never mix with marketing. Every error answers: what · why · what happened to the money · what next.</p>
</div>
"""

DEMOS["accessibility"] = """
<div class="demo-stack" style="max-width:520px">
  <div class="demo-row">
    <button class="bes-btn bes-btn--primary" style="outline:2px solid var(--bes-border-focus);outline-offset:2px">Focused state — always visible</button>
    <span class="bes-badge bes-badge--success"><svg class="ic" viewBox="0 0 12 12" fill="none"><path d="M2.5 6.5L5 9l4.5-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Icon + label, never color alone</span>
  </div>
  <div class="demo-row" style="align-items:center">
    <button class="bes-iconbtn bes-iconbtn--bordered" aria-label="44 by 44 pixel minimum target" style="outline:1px dashed var(--bes-border-input);outline-offset:2px">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="8" cy="8" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <span style="font-size:13px;color:var(--bes-text-secondary)">44×44 minimum touch target (dashed = hit area), preserved in compact density on touch</span>
  </div>
  <div class="bes-alert bes-alert--success"><div><b>Verified by machine, then by people.</b> Contrast: 60/60 token pairings pass (see docs/audits/). Structure: 50 files, 0 static errors. Screen readers, Arabic review and usability follow the protocols in docs/testing/.</div></div>
</div>
"""

DEMOS["localization-rtl"] = """
<div class="demo-stack" style="max-width:520px">
  <div class="bes-card" id="bidi-demo" dir="rtl" lang="ar">
    <p style="margin:0 0 10px;font-size:15px">أرسلت <bdi class="bes-amount">AED 10,036.75</bdi> إلى بريا كومار على الحساب <bdi class="bes-amount">AE07 0331 2345 6789 0123 456</bdi> بسعر <bdi class="bes-amount">1 AED = ₹25.0800</bdi> — المرجع <bdi class="bes-amount">BES-K8P2QX</bdi>.</p>
    <div class="bes-rows"><div class="bes-row"><span class="k">الإجمالي المدفوع</span><span class="v"><bdi class="bes-amount">AED 10,036.75</bdi></span></div></div>
  </div>
  <button class="bes-btn bes-btn--secondary bes-btn--sm" style="align-self:flex-start"
    onclick="var d=document.getElementById('bidi-demo');var r=d.getAttribute('dir')==='rtl'?'ltr':'rtl';d.setAttribute('dir',r);d.setAttribute('lang',r==='rtl'?'ar':'en')">
    Flip this card LTR ⇄ RTL</button>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:0">The amount, IBAN, rate and reference are bidi-isolated LTR runs — flip direction and they hold together instead of scrambling. This is the defect the isolation architecture removes.</p>
</div>
"""

DEMOS["theming"] = """
<div class="demo-stack" style="max-width:560px">
  <div style="font-size:13px;font-weight:600">One core, three brands — only token values change; behavior, disclosure and states are locked</div>
  <div class="demo-row" style="align-items:stretch">
    <div class="bes-card" style="flex:1;min-inline-size:150px">
      <div style="font-size:12px;color:var(--bes-text-secondary);margin-bottom:8px">Default</div>
      <button class="bes-btn bes-btn--primary bes-btn--sm" style="inline-size:100%">Send money</button>
      <div style="margin-top:8px"><span class="bes-badge bes-badge--pending">Pending</span></div>
    </div>
    <div class="bes-card" style="flex:1;min-inline-size:150px;--bes-action-primary:#0F6974;--bes-action-primaryHover:#0B525B;--bes-radius-md:4px">
      <div style="font-size:12px;color:var(--bes-text-secondary);margin-bottom:8px">Islamic window · sharp preset</div>
      <button class="bes-btn bes-btn--primary bes-btn--sm" style="inline-size:100%">Send money</button>
      <div style="margin-top:8px"><span class="bes-badge bes-badge--pending">Pending</span></div>
    </div>
    <div class="bes-card" style="flex:1;min-inline-size:150px;--bes-action-primary:#5A3DA0;--bes-action-primaryHover:#46307C;--bes-radius-md:14px">
      <div style="font-size:12px;color:var(--bes-text-secondary);margin-bottom:8px">Youth brand · soft preset</div>
      <button class="bes-btn bes-btn--primary bes-btn--sm" style="inline-size:100%">Send money</button>
      <div style="margin-top:8px"><span class="bes-badge bes-badge--pending">Pending</span></div>
    </div>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:0">Note what did NOT change: the pending badge (financial semantics are brand-invariant), the label, the states. Themes are validated against the contrast contract before acceptance.</p>
</div>
"""
SECTIONS = {}

# =====================================================================
# SECTIONS: full per-family component coverage, appended after the spec
# =====================================================================

SECTIONS["actions"] = [
("Icon buttons", """
<div class="demo-row">
  <button class="bes-iconbtn" aria-label="Copy IBAN" data-bes-copy="AE070331234567890123456" data-bes-copied="IBAN copied">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="6" y="6" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 6V4.5A1.5 1.5 0 0 0 10.5 3H4.5A1.5 1.5 0 0 0 3 4.5v6A1.5 1.5 0 0 0 4.5 12H6" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <button class="bes-iconbtn bes-iconbtn--bordered" aria-label="Search">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="8" cy="8" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
  </button>
  <button class="bes-iconbtn" aria-label="Hide balance" aria-pressed="true">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M2 10s3-5.5 8-5.5S18 10 18 10s-3 5.5-8 5.5S2 10 2 10z" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="2.4" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <span style="font-size:13px;color:var(--bes-text-secondary)">Tap the copy icon — it toasts. Learned glyphs only; 44×44 targets.</span>
</div>
"""),
("Action menu", """
<div class="demo-row" style="align-items:flex-start">
  <ul class="bes-menu" style="list-style:none">
    <li><button type="button">Download receipt</button></li>
    <li><button type="button">Repeat transfer</button></li>
    <li><button type="button">Add note</button></li>
    <li class="sep" role="separator"></li>
    <li class="destructive"><button type="button">Report a problem</button></li>
  </ul>
  <span style="font-size:13px;color:var(--bes-text-secondary);max-width:280px">Destructive items last and separated. Critical actions never live only in an overflow.</span>
</div>
"""),
("Button group — approval pair", """
<div class="demo-row">
  <button class="bes-btn bes-btn--primary">Approve</button>
  <button class="bes-btn bes-btn--destructive">Reject</button>
  <span style="font-size:13px;color:var(--bes-text-secondary)">Affirmative at inline-start (mirrors in RTL); solid red reserved for the confirm step.</span>
</div>
"""),
]

SECTIONS["inputs"] = [
("Select & Combobox", """
<div class="demo-row" style="align-items:flex-start">
  <div class="bes-field" style="inline-size:220px;margin-bottom:0">
    <label class="bes-label" for="si-per">Statement period</label>
    <div class="bes-select"><select id="si-per"><option>August 2026</option><option>July 2026</option><option>June 2026</option></select></div>
  </div>
  <div class="bes-field" style="inline-size:300px;margin-bottom:0">
    <label class="bes-label" for="si-bank">Recipient's bank (type to filter)</label>
    <div class="bes-combo">
      <input class="bes-input" id="si-bank" role="combobox" aria-expanded="false" aria-autocomplete="list" autocomplete="off" placeholder="Search by name or code">
      <ul class="bes-combo-list" hidden>
        <li data-value="enbd" data-label="Emirates NBD">Emirates NBD <span class="s">EBILAEAD</span></li>
        <li data-value="fab" data-label="First Abu Dhabi Bank">First Abu Dhabi Bank <span class="s">NBADAEAA</span></li>
        <li data-value="icici" data-label="ICICI Bank (India)">ICICI Bank (India) <span class="s">ICICINBB</span></li>
        <li class="empty" hidden>No bank found — check the SWIFT code</li>
      </ul>
      <span class="bes-combo-count" aria-live="polite"></span>
    </div>
  </div>
</div>
"""),
("Date picker — processing-day aware", """
<div class="bes-datepicker" data-bes-datepicker data-disabled-days="0" data-disabled-note="Transfers don't process on Sundays — we'll send the next business day."></div>
"""),
("PIN & code entry", """
<div class="demo-row" style="align-items:flex-start;gap:32px">
  <div><p class="bes-label" style="margin:0 0 8px">App PIN (no paste)</p>
    <div class="bes-pin">
      <input aria-label="PIN digit 1" type="password"><input aria-label="PIN digit 2" type="password">
      <input aria-label="PIN digit 3" type="password"><input aria-label="PIN digit 4" type="password">
    </div>
  </div>
  <div><p class="bes-label" style="margin:0 0 8px">Verification code (paste allowed)</p>
    <div class="bes-pin bes-pin--code">
      <input aria-label="Code digit 1"><input aria-label="Code digit 2"><input aria-label="Code digit 3">
      <input aria-label="Code digit 4"><input aria-label="Code digit 5"><input aria-label="Code digit 6">
    </div>
  </div>
</div>
"""),
("File upload & character count", """
<div class="demo-stack" style="max-width:460px">
  <div class="bes-upload">
    <button class="bes-btn bes-btn--secondary bes-btn--sm" type="button">Upload trade license</button>
    <div class="hint">PDF or photo · max 10 MB</div>
  </div>
  <div class="bes-file">
    <span class="n">trade-license-2026.pdf</span>
    <span class="meta">1.2 MB · <span style="color:var(--bes-status-success);font-weight:600">Verified</span></span>
  </div>
  <div class="bes-field" style="margin-bottom:0">
    <label class="bes-label" for="si-ref">Payment reference <span class="opt">(optional)</span></label>
    <input class="bes-input" id="si-ref" maxlength="35" value="Rent September">
    <div class="bes-charcount" data-bes-charcount="si-ref"></div>
  </div>
</div>
"""),
("Radio group as option cards", """
<div class="demo-stack" style="max-width:420px" role="radiogroup" aria-label="Payout method">
  <label class="bes-check" style="border:1px solid var(--bes-border-input);border-radius:12px;padding:13px 14px">
    <input type="radio" name="si-payout" checked>
    <span><b>Bank transfer</b><span class="desc">Fee AED 15.00 · within 1 hour</span></span>
  </label>
  <label class="bes-check" style="border:1px solid var(--bes-border-input);border-radius:12px;padding:13px 14px">
    <input type="radio" name="si-payout">
    <span><b>Cash pickup</b><span class="desc">Fee AED 20.00 · minutes · 2,400 locations</span></span>
  </label>
</div>
"""),
]

SECTIONS["navigation"] = [
("Breadcrumb & pagination", """
<div class="demo-stack">
  <nav aria-label="Breadcrumb"><ol class="bes-breadcrumb">
    <li><a href="#">Payments</a></li><li><a href="#">Bulk payments</a></li><li><a href="#">July payroll</a></li><li aria-current="page">Payment 41 of 60</li>
  </ol></nav>
  <div class="bes-pagination">
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Previous</button>
    <span class="range"><bdi class="bes-amount">41–60</bdi> of <bdi class="bes-amount">214</bdi></span>
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Next</button>
  </div>
</div>
"""),
("Segmented control", """
<div class="demo-row">
  <div class="bes-seg" role="group" aria-label="View as">
    <button aria-pressed="true">List</button><button aria-pressed="false">Chart</button>
  </div>
  <div class="bes-seg" role="group" aria-label="Currency display">
    <button aria-pressed="true">AED</button><button aria-pressed="false">USD</button>
  </div>
</div>
"""),
("Bottom navigation (mobile pattern)", """
<div style="max-width:390px;border:1px solid var(--bes-border-default);border-radius:14px;overflow:hidden">
  <div style="display:flex;background:var(--bes-surface-primary);border-block-start:1px solid var(--bes-border-default)">
    <span style="flex:1;text-align:center;padding:10px 0 12px;color:var(--bes-action-primary);font-size:11px;font-weight:600">●<br>Home</span>
    <span style="flex:1;text-align:center;padding:10px 0 12px;color:var(--bes-text-secondary);font-size:11px;font-weight:500">○<br>Payments</span>
    <span style="flex:1;text-align:center;padding:10px 0 12px;color:var(--bes-text-secondary);font-size:11px;font-weight:500">○<br>Cards</span>
    <span style="flex:1;text-align:center;padding:10px 0 12px;color:var(--bes-text-secondary);font-size:11px;font-weight:500;position:relative">○<br>Approvals<span class="bes-badge bes-badge--error" style="position:absolute;inset-block-start:4px;inset-inline-end:14px;padding:1px 6px;font-size:10px">3</span></span>
    <span style="flex:1;text-align:center;padding:10px 0 12px;color:var(--bes-text-secondary);font-size:11px;font-weight:500">○<br>Profile</span>
  </div>
</div>
<p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0">Labels always visible; badges included in the accessible name; order mirrors in RTL.</p>
"""),
("Session bar — timeout warning", """
<div class="bes-banner" style="border-radius:10px;border:1px solid var(--bes-border-default);justify-content:space-between">
  <span>You'll be signed out in <bdi class="bes-amount">0:59</bdi></span>
  <button class="bes-btn bes-btn--primary bes-btn--sm">Stay signed in</button>
</div>
<p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0">Appears at T-60s; expiry never silently discards a payment draft — it's restored after re-auth.</p>
"""),
]

SECTIONS["containers"] = [
("List & data table", """
<div class="demo-stack">
  <div class="bes-list" style="max-width:460px">
    <button class="bes-item" type="button">
      <span class="main"><span class="t">Statements</span><br><span class="s">Monthly PDF and CSV</span></span>
      <span class="trail" style="color:var(--bes-text-disabled)">›</span>
    </button>
    <button class="bes-item" type="button">
      <span class="main"><span class="t">Limits</span><br><span class="s">Daily transfer AED 50,000</span></span>
      <span class="trail" style="color:var(--bes-text-disabled)">›</span>
    </button>
  </div>
  <div class="bes-table-wrap">
    <table class="bes-table" data-bes-sortable>
      <thead><tr><th data-sort="text">Payee</th><th class="num" data-sort="num">Amount (AED)</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Gulf Star Trading LLC</td><td class="num">250,000.00</td><td><span class="bes-badge bes-badge--warning">Awaiting approval</span></td></tr>
        <tr><td>DEWA</td><td class="num">843.50</td><td><span class="bes-badge bes-badge--success">Completed</span></td></tr>
        <tr><td>Etisalat</td><td class="num">399.00</td><td><span class="bes-badge bes-badge--success">Completed</span></td></tr>
      </tbody>
    </table>
  </div>
</div>
"""),
("Accordion — elaborates, never hides obligations", """
<div class="bes-accordion" style="max-width:460px">
  <details><summary>Why this fee?</summary><div class="body">The transfer fee covers processing through the international payment network. Full <a href="#">schedule of charges (PDF)</a>.</div></details>
  <details><summary>When does the money arrive?</summary><div class="body">Transfers to India usually arrive within 1 hour. Same-day cut-off is 22:00 UAE time.</div></details>
</div>
"""),
("Drawer", """
<button class="bes-btn bes-btn--secondary" data-bes-drawer-open="dc-drawer">Open transaction drawer</button>
<div class="bes-drawer-scrim" id="dc-drawer-scrim"></div>
<aside class="bes-drawer" id="dc-drawer" role="dialog" aria-labelledby="dc-dr-t">
  <div class="head"><h3 id="dc-dr-t">Carrefour · <bdi class="bes-amount">−AED 89.50</bdi></h3>
  <button class="bes-iconbtn" data-bes-drawer-close="dc-drawer" aria-label="Close">✕</button></div>
  <div class="body">
    <div class="bes-rows">
      <div class="bes-row"><span class="k">Status</span><span class="v"><span class="bes-badge bes-badge--success">Completed</span></span></div>
      <div class="bes-row"><span class="k">Card</span><span class="v"><bdi class="bes-amount">••8834</bdi> · Contactless</span></div>
      <div class="bes-row"><span class="k">Reference</span><span class="v"><bdi class="bes-amount">TXN-88213-AE</bdi></span></div>
    </div>
  </div>
</aside>
"""),
("Tooltip & popover", """
<div class="demo-row">
  <span class="bes-pop">
    <button class="bes-iconbtn bes-iconbtn--bordered" aria-label="Copy IBAN">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="6" y="6" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 6V4.5A1.5 1.5 0 0 0 10.5 3H4.5A1.5 1.5 0 0 0 3 4.5v6A1.5 1.5 0 0 0 4.5 12H6" stroke="currentColor" stroke-width="1.5"/></svg>
    </button>
    <span class="tip" role="tooltip">Copy IBAN</span>
  </span>
  <span style="font-size:13px;color:var(--bes-text-secondary)">Hover or focus the button — tooltips name icon-only controls, never carry unique information.</span>
</div>
"""),
]

SECTIONS["feedback"] = [
("Banner tiers", """
<div class="demo-stack" style="max-width:560px">
  <div class="bes-banner bes-banner--security" style="border-radius:10px;border:1px solid var(--bes-border-default)">
    <svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5l5.5 2v4c0 3.2-2.3 5.6-5.5 7-3.2-1.4-5.5-3.8-5.5-7v-4l5.5-2z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
    We'll never ask for your password or card PIN. <a href="#" style="font-weight:600">Spot the scams</a>
  </div>
  <div class="bes-banner" style="border-radius:10px;border:1px solid var(--bes-border-default)">
    <svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.4"/><path d="M8 7.4v3.2M8 5v.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    Scheduled maintenance Fri 02:00–04:00 — cards keep working.
  </div>
</div>
<p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0">One banner at a time; security &gt; degraded &gt; regulatory &gt; system. Marketing never uses this channel.</p>
"""),
("Progress, skeleton & spinner", """
<div class="demo-stack" style="max-width:420px">
  <div>
    <div style="font-size:13px;font-weight:600;margin-bottom:6px">Profile completeness — determinate only when real</div>
    <div class="bes-progress"><div class="fill" style="inline-size:80%"></div></div>
    <div style="font-size:12.5px;color:var(--bes-text-secondary);margin-top:4px">80% complete</div>
  </div>
  <div class="demo-row" style="align-items:center">
    <div class="bes-skel" style="inline-size:160px;block-size:14px"></div>
    <div class="bes-skel" style="inline-size:80px;block-size:24px"></div>
    <button class="bes-btn bes-btn--secondary bes-btn--sm bes-btn--loading">Checking…</button>
  </div>
</div>
"""),
("Empty & error states", """
<div class="demo-row" style="align-items:stretch">
  <div class="bes-card bes-empty" style="inline-size:280px">
    <div class="t">No beneficiaries yet</div>
    <div class="s">Add someone to send money to — it takes a minute.</div>
    <button class="bes-btn bes-btn--primary bes-btn--sm">Add beneficiary</button>
  </div>
  <div class="bes-card bes-empty" style="inline-size:280px">
    <div class="t">We can't load transactions right now</div>
    <div class="s">Your money is safe. Showing balances from 14:32.</div>
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Try again</button>
  </div>
</div>
"""),
]

SECTIONS["money"] = [
("Amount pair & FX rate with lock", """
<div class="demo-stack" style="max-width:420px">
  <div>
    <bdi class="bes-amount bes-amount--md">USD 500.00</bdi>
    <div class="bes-amount--meta bes-amount" style="display:block">≈ AED 1,836.50 at 1 USD = 3.6730</div>
  </div>
  <div class="bes-row bes-row--rate" style="display:flex;justify-content:space-between">
    <span>Exchange rate</span>
    <span><bdi class="bes-amount">1 AED = ₹25.0800</bdi> · <span class="bes-ratelock" data-bes-countdown="90" data-prefix="locked " data-expired-text="rate expired"><span class="t"></span></span></span>
  </div>
  <p style="font-size:13px;color:var(--bes-text-secondary);margin:0">The lock counts down live (warns at 60s, then expires). Expiry always produces an explicit re-quote — never silent re-pricing.</p>
</div>
"""),
("Masked balance", """
<div class="demo-row">
  <bdi class="bes-amount bes-amount--lg" id="dm-bal"><span class="cur">AED</span> 25,000.00</bdi>
  <button class="bes-iconbtn" aria-label="Hide balance" data-bes-mask="dm-bal" aria-pressed="false">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M2 10s3-5.5 8-5.5S18 10 18 10s-3 5.5-8 5.5S2 10 2 10z" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="2.4" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <span style="font-size:13px;color:var(--bes-text-secondary)">Masked values never reach the accessibility tree as bullets.</span>
</div>
"""),
("Amount delta", """
<div class="demo-row">
  <span class="bes-delta bes-delta--up">▲ +AED 1,200.00 (4.8%) <span class="tf">vs July</span></span>
  <span class="bes-delta bes-delta--down">▼ −2.1% <span class="tf">1M</span></span>
  <span class="bes-delta bes-delta--flat">No change <span class="tf">this week</span></span>
</div>
<p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0">Green/red only on investment performance; spending deltas stay neutral — spending more isn't morally red.</p>
"""),
("Limit indicator", """
<div class="bes-limit" style="max-width:420px">
  <div style="font-size:13.5px;font-weight:600;margin-bottom:6px">Daily transfer limit</div>
  <div class="bes-progress bes-progress--warn"><div class="fill" style="inline-size:82%"></div></div>
  <div class="figures"><span class="used"><bdi class="bes-amount">AED 41,000.00</bdi> used</span><span>of <bdi class="bes-amount">AED 50,000.00</bdi></span></div>
  <div class="reset">Resets at midnight · discovered at amount entry, never at the failure step</div>
</div>
"""),
]

SECTIONS["accounts"] = [
("Balance set — the full truth", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k" style="color:var(--bes-text-primary);font-weight:600">Available balance</span><span class="v"><bdi class="bes-amount bes-amount--md">AED 23,750.00</bdi></span></div>
    <div class="bes-row"><span class="k">Current balance</span><span class="v"><bdi class="bes-amount">AED 25,000.00</bdi></span></div>
    <div class="bes-row"><span class="k">Pending out</span><span class="v"><bdi class="bes-amount">−AED 750.00</bdi> <span style="color:var(--bes-text-secondary);font-weight:400">(2)</span></span></div>
    <div class="bes-row"><span class="k">Card holds</span><span class="v" style="color:var(--bes-financial-reserved)"><bdi class="bes-amount">−AED 500.00</bdi></span></div>
  </div>
  <a href="#" style="font-size:13.5px;font-weight:500">Why is my available balance different?</a>
</div>
"""),
("Account selector", """
<div class="bes-field" style="max-width:380px;margin-bottom:0">
  <label class="bes-label" for="da-src">From account</label>
  <div class="bes-select"><select id="da-src">
    <option>Current account ••4521 — AED 23,750.00 available</option>
    <option>Savings ••8102 — AED 46,200.00 available</option>
    <option disabled>Joint account ••3377 — AED 120.00 (not enough for this transfer)</option>
  </select></div>
  <div class="bes-help">Options always show name, masked number and available balance.</div>
</div>
"""),
("IBAN display with copy", """
<div class="demo-row">
  <bdi class="bes-amount" style="font-size:15px;font-weight:600;letter-spacing:.04em">AE07 0331 2345 6789 0123 456</bdi>
  <button class="bes-iconbtn" aria-label="Copy IBAN" data-bes-copy="AE070331234567890123456" data-bes-copied="IBAN copied">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="6" y="6" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 6V4.5A1.5 1.5 0 0 0 10.5 3H4.5A1.5 1.5 0 0 0 3 4.5v6A1.5 1.5 0 0 0 4.5 12H6" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <span style="font-size:13px;color:var(--bes-text-secondary)">Displays grouped; copies unspaced; always an LTR run — flip a doc-demo direction and it holds.</span>
</div>
"""),
("Spaces / goal card", """
<div class="bes-card bes-goal" style="max-width:380px">
  <div class="head"><span class="name">🏠 Rent — September</span><span class="bes-badge bes-badge--success">On track</span></div>
  <div class="bes-progress"><div class="fill" style="inline-size:65%"></div></div>
  <div class="figs"><b><bdi class="bes-amount">AED 6,500.00</bdi></b> of <bdi class="bes-amount">AED 10,000.00</bdi> · saves <bdi class="bes-amount">AED 500.00</bdi> every payday</div>
  <div class="demo-row" style="margin-top:12px">
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Add money</button>
    <button class="bes-btn bes-btn--ghost bes-btn--sm">Withdraw</button>
  </div>
</div>
"""),
]

SECTIONS["transactions"] = [
("Transaction table — sortable, treasury density", """
<div class="bes-table-wrap">
  <table class="bes-table" data-bes-sortable>
    <thead><tr><th data-sort="text">Date</th><th>Counterparty</th><th>Reference</th><th class="num" data-sort="num">Debit</th><th class="num" data-sort="num">Credit</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>30 Aug</td><td>Gulf Star Trading LLC</td><td><bdi class="bes-amount">INV-2026-0841</bdi></td><td class="num">250,000.00</td><td class="num">—</td><td><span class="bes-badge bes-badge--warning">Awaiting approval</span></td></tr>
      <tr><td>29 Aug</td><td>DEWA</td><td><bdi class="bes-amount">CON-99231</bdi></td><td class="num">843.50</td><td class="num">—</td><td><span class="bes-badge bes-badge--success">Completed</span></td></tr>
      <tr><td>28 Aug</td><td>Falcon Media FZ</td><td><bdi class="bes-amount">RCP-1187</bdi></td><td class="num">—</td><td class="num">42,000.00</td><td><span class="bes-badge bes-badge--success">Completed</span></td></tr>
    </tbody>
  </table>
</div>
"""),
("Transaction timeline", """
<div class="bes-card" style="max-width:420px">
  <ul class="bes-timeline">
    <li class="done"><span class="dot">✓</span><span><span class="t">Sent from your account</span><br><span class="s">Today 14:32</span></span></li>
    <li class="done"><span class="dot">✓</span><span><span class="t">Converted AED → INR</span><br><span class="s">rate ₹25.0800 locked</span></span></li>
    <li class="current"><span class="dot">●</span><span><span class="t">With recipient bank</span><br><span class="s">Usually within 1 hour · expected by 15:30</span></span></li>
    <li><span class="dot">○</span><span><span class="t">Delivered to Priya Kumar</span><br><span class="s">We'll notify you</span></span></li>
  </ul>
</div>
"""),
("Receipt — immutable, printable proof", """
<div class="bes-receipt" style="max-width:420px">
  <div class="head"><span class="title">Payment receipt</span><span class="bes-badge bes-badge--success">Completed</span></div>
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Reference</span><span class="v"><bdi class="bes-amount">BES-K8P2QX</bdi></span></div>
    <div class="bes-row"><span class="k">Recipient</span><span class="v">Priya Kumar · ICICI <bdi class="bes-amount">••4102</bdi></span></div>
    <div class="bes-row"><span class="k">Amount sent</span><span class="v"><bdi class="bes-amount">AED 10,000.00</bdi></span></div>
    <div class="bes-row"><span class="k">Fees + VAT</span><span class="v"><bdi class="bes-amount">AED 36.75</bdi></span></div>
  </div>
  <div class="bes-total"><span class="k">Total paid</span><span class="v"><bdi class="bes-amount">AED 10,036.75</bdi></span></div>
</div>
"""),
("Filter chips", """
<div class="demo-row">
  <button class="bes-chip" aria-pressed="true">Last 90 days ✕</button>
  <button class="bes-chip" aria-pressed="true">Card ••8834 ✕</button>
  <button class="bes-chip" aria-pressed="false">+ Amount range</button>
  <span style="font-size:13px;color:var(--bes-text-secondary)">214 → 38 transactions · <a href="#">Clear all</a></span>
</div>
"""),
]

SECTIONS["payments-transfers"] = [
("Payment method selector", """
<div class="demo-stack" style="max-width:440px" role="radiogroup" aria-label="Delivery method">
  <label class="bes-check" style="border:1px solid var(--bes-action-primary);outline:1.5px solid var(--bes-action-primary);border-radius:12px;padding:13px 14px">
    <input type="radio" name="dp-method" checked>
    <span><b>Bank account</b><span class="desc">Fee AED 15.00 · within 1 hour · IBAN required</span></span>
  </label>
  <label class="bes-check" style="border:1px solid var(--bes-border-input);border-radius:12px;padding:13px 14px">
    <input type="radio" name="dp-method">
    <span><b>Wallet (GCash)</b><span class="desc">Fee AED 12.00 · minutes · mobile number required</span></span>
  </label>
  <label class="bes-check" style="border:1px solid var(--bes-border-input);border-radius:12px;padding:13px 14px">
    <input type="radio" name="dp-method">
    <span><b>Cash pickup</b><span class="desc">Fee AED 20.00 · minutes · 2,400 locations</span></span>
  </label>
</div>
"""),
("Result screens — success and the honest UNKNOWN", """
<div class="demo-row" style="align-items:stretch">
  <div class="bes-card bes-result bes-result--completed" style="inline-size:260px;padding-block:20px">
    <div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M5 13l4.5 4.5L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
    <h2 style="font-size:18px">Transfer sent</h2>
    <p class="money-state"><bdi class="bes-amount">AED 10,036.75</bdi> on its way · within 1 hour</p>
  </div>
  <div class="bes-card bes-result bes-result--unknown" style="inline-size:260px;padding-block:20px">
    <div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 10.5v5M12 7v.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
    <h2 style="font-size:18px">We're checking your transfer status</h2>
    <p class="money-state"><b>Your money is safe</b> — we'll confirm within 30 minutes. Never shown as "failed".</p>
  </div>
</div>
"""),
("Request-to-pay", """
<div class="bes-card" style="max-width:400px">
  <div style="display:flex;gap:12px;align-items:center;margin-bottom:10px">
    <span style="inline-size:38px;block-size:38px;border-radius:50%;background:var(--bes-surface-tertiary);display:grid;place-items:center;font-weight:600;color:var(--bes-text-secondary)">AS</span>
    <div><b>Anil Sharma</b> <span style="font-size:12px;color:var(--bes-status-success);font-weight:600">✓ registered name</span><br>
    <span style="font-size:13px;color:var(--bes-text-secondary)">requests <bdi class="bes-amount" style="font-weight:600">AED 425.00</bdi> · "Dinner split"</span></div>
  </div>
  <div class="demo-row">
    <button class="bes-btn bes-btn--primary bes-btn--sm">Review &amp; pay</button>
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Decline</button>
    <button class="bes-btn bes-btn--ghost bes-btn--sm">Report</button>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:10px 0 0">Never one-tap pay from a notification — always through the review contract. Expires 2 Sep.</p>
</div>
"""),
("Bill payment tile", """
<div class="bes-card" style="max-width:400px;display:flex;justify-content:space-between;gap:12px;align-items:center">
  <div>
    <b>DEWA — Marina flat</b><br>
    <span style="font-size:13px;color:var(--bes-text-secondary)">Due 3 Sep · autopay on, cap <bdi class="bes-amount">AED 1,500.00</bdi></span>
  </div>
  <div style="text-align:end">
    <bdi class="bes-amount bes-amount--md">AED 843.50</bdi><br>
    <span class="bes-badge bes-badge--warning">Due in 3 days</span>
  </div>
</div>
"""),
("Scheduled / recurring summary", """
<div class="bes-card" style="max-width:420px;display:flex;justify-content:space-between;gap:12px;align-items:center">
  <div>
    <b>↻ <bdi class="bes-amount">AED 2,000.00</bdi> to Priya Kumar</b><br>
    <span style="font-size:13px;color:var(--bes-text-secondary)">25th of every month · next: 25 Sep · if funds are short we retry next day and notify you</span>
  </div>
  <div class="demo-row"><button class="bes-btn bes-btn--secondary bes-btn--sm">Pause</button><button class="bes-btn bes-btn--ghost bes-btn--sm">Edit</button></div>
</div>
"""),
]

SECTIONS["cards"] = [
("Card art — virtual, co-badged, frozen", """
<div class="demo-row" style="align-items:flex-start">
  <div class="bes-cardart bes-cardart--virtual">
    <div class="bank">AL NOOR BANK</div>
    <div class="pan">•••• •••• •••• 8834</div>
    <div class="row"><span class="holder">S. KUMAR</span><span class="schemes">JAYWAN · INTL</span></div>
  </div>
  <div class="bes-cardart bes-cardart--frozen">
    <div class="bank">AL NOOR BANK</div>
    <div class="pan">•••• •••• •••• 4521</div>
    <div class="row"><span class="holder">S. KUMAR</span><span class="schemes">JAYWAN · INTL</span></div>
  </div>
</div>
"""),
("Details reveal — step-up gated", """
<div class="bes-card" style="max-width:400px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Card number</span><span class="v"><bdi class="bes-amount">5312 7789 0021 8834</bdi> <button class="bes-whyfee" type="button" data-bes-copy="5312778900218834" data-bes-copied="Card number copied">copy</button></span></div>
    <div class="bes-row"><span class="k">Expiry</span><span class="v"><bdi class="bes-amount">09/29</bdi></span></div>
    <div class="bes-row"><span class="k">CVV</span><span class="v"><bdi class="bes-amount">•••</bdi> <button class="bes-whyfee" type="button">reveal</button></span></div>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:8px 0 0">Auto-masks after 60s · clipboard clears after 90s · every reveal is notification-logged.</p>
</div>
"""),
("Dispute triage — the fraud fork acts first", """
<div class="demo-stack" style="max-width:440px" role="radiogroup" aria-label="What's wrong with this payment?">
  <label class="bes-check"><input type="radio" name="dcard-disp"><span><b>I don't recognize this</b><span class="desc">→ fraud path: freeze offered immediately, questions after</span></span></label>
  <label class="bes-check"><input type="radio" name="dcard-disp"><span><b>Charged twice</b><span class="desc">→ dispute case with evidence upload</span></span></label>
  <label class="bes-check"><input type="radio" name="dcard-disp"><span><b>Subscription I cancelled</b><span class="desc">→ merchant dispute + block future charges</span></span></label>
</div>
"""),
("Replacement — reason drives consequence", """
<div class="bes-alert bes-alert--warning" style="max-width:460px">
  <div><b>Lost or stolen?</b> Your current card stops working immediately and can't be reactivated. Your card number changes — we'll list merchants that charged this card so you can update subscriptions. Replacement arrives in 3–5 days; your virtual card keeps working.</div>
</div>
"""),
]

SECTIONS["lending"] = [
("Payment calculator", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Amount</span><span class="v"><bdi class="bes-amount">AED 100,000.00</bdi></span></div>
    <div class="bes-row"><span class="k">Term</span><span class="v">48 months</span></div>
  </div>
  <div class="bes-total"><span class="k">Monthly payment</span><span class="v"><bdi class="bes-amount">≈ AED 2,348.00</bdi></span></div>
  <div class="bes-rows" style="margin-top:6px">
    <div class="bes-row"><span class="k">Total you pay for this financing</span><span class="v"><bdi class="bes-amount">AED 12,704.00</bdi></span></div>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:8px 0 0">Estimated — your personal rate may differ. Total cost never hides behind a tap.</p>
</div>
"""),
("Profit rate display (Islamic dimension)", """
<div class="bes-card" style="max-width:440px">
  <span style="display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--bes-text-secondary);border:1px solid var(--bes-border-strong);border-radius:4px;padding:3px 8px;margin-bottom:10px">Mudarabah savings</span>
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Profit-sharing ratio</span><span class="v">You receive 70% of pool profit</span></div>
    <div class="bes-row"><span class="k">Distribution</span><span class="v">Monthly</span></div>
    <div class="bes-row"><span class="k">Last distribution (indicative)</span><span class="v"><bdi class="bes-amount">3.85%</bdi> p.a. equivalent</span></div>
  </div>
  <div class="bes-alert bes-alert--info" style="margin-top:10px"><div>This is Mudarabah: the bank invests your deposit per Shari'ah and shares the profit. Rates are indicative, not guaranteed. <a href="#">Structure certificate</a></div></div>
</div>
"""),
("Repayment schedule", """
<div class="bes-table-wrap" style="max-width:520px">
  <table class="bes-table bes-schedule">
    <thead><tr><th>#</th><th>Date</th><th class="num">Payment</th><th class="num">Principal</th><th class="num">Profit</th><th>Status</th></tr></thead>
    <tbody>
      <tr class="paid"><td>13</td><td>1 Aug</td><td class="num">2,348.00</td><td class="num">1,905.20</td><td class="num">442.80</td><td><span class="bes-badge bes-badge--success">Paid</span></td></tr>
      <tr class="due"><td>14</td><td>1 Sep</td><td class="num">2,348.00</td><td class="num">1,914.70</td><td class="num">433.30</td><td><span class="bes-badge bes-badge--warning">Due in 1 day</span></td></tr>
      <tr><td>15</td><td>1 Oct</td><td class="num">2,348.00</td><td class="num">1,924.30</td><td class="num">423.70</td><td><span class="bes-badge bes-badge--neutral">Upcoming</span></td></tr>
    </tbody>
  </table>
</div>
"""),
("Early settlement — both numbers, no selling", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Settle today</span><span class="v"><bdi class="bes-amount">AED 81,032.00</bdi> <span style="color:var(--bes-text-secondary);font-weight:400">(incl. 1% fee)</span></span></div>
    <div class="bes-row"><span class="k">Continue 34 months</span><span class="v"><bdi class="bes-amount">AED 84,528.00</bdi> total</span></div>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:8px 0 0">Quote valid until 6 Sep. The component shows both paths — it doesn't sell either.</p>
</div>
"""),
("Overdue state — factual, hardship path always present", """
<div class="bes-alert bes-alert--error" style="max-width:460px">
  <div><b><bdi class="bes-amount">AED 2,348.00</bdi> overdue by 6 days.</b>
  A late fee of AED 105 was applied. Continued non-payment can affect your credit record.
  <div class="actions"><a href="#">Pay now</a><a href="#">Struggling to pay? See your options</a></div></div>
</div>
"""),
]

SECTIONS["investments"] = [
("Holding items", """
<div class="bes-list" style="max-width:520px">
  <button class="bes-item" type="button">
    <span class="main"><span class="t">Emaar Properties · EMAAR</span><br><span class="s">200 shares · avg <bdi class="bes-amount">AED 8.40</bdi></span></span>
    <span class="trail"><bdi class="bes-amount bes-amount--sm">AED 1,840.00</bdi><span class="bes-delta bes-delta--up" style="font-size:12px">▲ 2.1% 1M</span></span>
  </button>
  <button class="bes-item" type="button">
    <span class="main"><span class="t">Global Sukuk Fund</span><br><span class="s">NAV as of 28 Aug · <span class="bes-badge bes-badge--success" style="padding:2px 8px;font-size:11px">Shari'ah certified</span></span></span>
    <span class="trail"><bdi class="bes-amount bes-amount--sm">AED 9,600.00</bdi><span class="bes-delta bes-delta--down" style="font-size:12px">▼ 0.4% 1M</span></span>
  </button>
</div>
"""),
("Order ticket — consequence before execution", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Buy</span><span class="v">Emaar Properties · market order</span></div>
    <div class="bes-row"><span class="k">Amount</span><span class="v"><bdi class="bes-amount">≈ AED 5,000.00</bdi> <span style="color:var(--bes-text-secondary);font-weight:400">(~595 shares)</span></span></div>
    <div class="bes-row"><span class="k">Commission</span><span class="v"><bdi class="bes-amount">AED 12.50</bdi></span></div>
    <div class="bes-row bes-row--rate"><span>Indicative price</span><span><bdi class="bes-amount">AED 8.41</bdi> · final at execution</span></div>
  </div>
  <p class="bes-consequence">Market orders execute at the best available price, which may differ from what you see. They can't be cancelled once executed.</p>
  <button class="bes-btn bes-btn--primary bes-btn--lg">Buy ~<bdi class="bes-amount">AED 5,000.00</bdi> of Emaar</button>
</div>
"""),
("Term deposit — no silent auto-renewal", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">Fixed deposit</span><span class="v"><bdi class="bes-amount">AED 50,000.00</bdi> · 12 months · <bdi class="bes-amount">4.10%</bdi></span></div>
    <div class="bes-row"><span class="k">Matures</span><span class="v">15 Mar 2027</span></div>
    <div class="bes-row"><span class="k">Early withdrawal</span><span class="v" style="color:var(--bes-status-warning)">base rate 0.5% applies</span></div>
    <div class="bes-row"><span class="k">At maturity</span><span class="v">Pay out to ••4521 (default — you choose, we notify at T-7 days)</span></div>
  </div>
</div>
"""),
("Performance chart", """
<div class="bes-chart" style="max-width:520px" data-bes-chart='{"type":"line","data":[{"label":"Mar","value":44100},{"label":"Apr","value":43200},{"label":"May","value":45900},{"label":"Jun","value":46400},{"label":"Jul","value":47700},{"label":"Aug","value":48320}],"opts":{"label":"Portfolio value over six months","colLabel":"Month","colValue":"AED"}}'></div>
"""),
]

SECTIONS["identity-security"] = [
("National identity sign-in & verified field", """
<div class="demo-stack" style="max-width:420px">
  <button class="bes-btn bes-btn--primary bes-btn--lg" style="background:#111;color:#fff">Continue with UAE PASS</button>
  <div class="bes-field bes-field--verified" style="margin-bottom:0">
    <label class="bes-label" for="ds-eid">Emirates ID number</label>
    <input class="bes-input bes-input--ltr" id="ds-eid" value="784-1990-1234567-1" readonly>
    <div class="bes-verified-note">✓ Verified from UAE PASS · Name changed? Update your Emirates ID first, then re-verify.</div>
  </div>
</div>
"""),
("Document capture states", """
<div class="demo-stack" style="max-width:460px">
  <div class="bes-file"><span class="n">emirates-id-front.jpg</span><span class="meta"><span class="bes-badge bes-badge--pending">Verifying</span></span></div>
  <div class="bes-file"><span class="n">emirates-id-back.jpg</span><span class="meta"><span class="bes-badge bes-badge--success">Verified</span></span></div>
  <div class="bes-file"><span class="n">salary-certificate.pdf</span><span class="meta"><span class="bes-badge bes-badge--error">Glare over the ID number — try tilting away from light</span></span></div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:0">After 3 quality failures the flow changes strategy (upload from files, alternative document, human review) — never an identical-retry loop.</p>
</div>
"""),
("Push approval — same context on the second device", """
<div class="bes-card" style="max-width:380px">
  <div style="font-size:13px;color:var(--bes-text-secondary);margin-bottom:6px">Approval request · iPhone 15 Pro</div>
  <b>Confirm transfer of <bdi class="bes-amount">AED 10,036.75</bdi> to Priya Kumar?</b>
  <div class="demo-row" style="margin-top:12px">
    <button class="bes-btn bes-btn--primary bes-btn--sm" style="flex:1">Approve</button>
    <button class="bes-btn bes-btn--secondary bes-btn--sm" style="flex:1">Deny</button>
  </div>
  <p style="font-size:12.5px;color:var(--bes-text-secondary);margin:10px 0 0">The amount + payee shown here is the anti-tamper anchor. Deny asks "Was this you?" → secure-account path.</p>
</div>
"""),
("Security checkup", """
<div class="bes-card" style="max-width:420px">
  <div class="bes-rows">
    <div class="bes-row"><span class="k">✓ Passkey active</span><span class="v" style="color:var(--bes-status-success)">Done</span></div>
    <div class="bes-row"><span class="k">✓ Devices reviewed</span><span class="v" style="color:var(--bes-status-success)">2 trusted</span></div>
    <div class="bes-row"><span class="k">○ Payee list review</span><span class="v"><a href="#">Review 12 payees</a></span></div>
    <div class="bes-row"><span class="k">○ Alerts</span><span class="v"><a href="#">Turn on sign-in alerts</a></span></div>
  </div>
  <div class="bes-alert bes-alert--info" style="margin-top:10px"><div><b>This month's tip:</b> banks never ask you to move money to a "safe account". Anyone who does is a scammer.</div></div>
</div>
"""),
]

SECTIONS["consent-privacy"] = [
("Consent dashboard card — expiry visible, revoke one tap", """
<div class="bes-card" style="max-width:440px;display:flex;justify-content:space-between;gap:12px;align-items:center">
  <div>
    <b>ABC Finance</b> <span style="font-size:12px;color:var(--bes-status-success);font-weight:600">✓ verified</span><br>
    <span style="font-size:13px;color:var(--bes-text-secondary)">Accounts, balance, 12-month history · granted 12 Mar</span><br>
    <span class="bes-badge bes-badge--warning" style="margin-top:4px">Expires in 12 days</span>
  </div>
  <div style="display:flex;flex-direction:column;gap:6px">
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Details</button>
    <button class="bes-btn bes-btn--destructive bes-btn--sm">Stop sharing</button>
  </div>
</div>
"""),
("Revocation — honest about what it does and doesn't do", """
<div class="bes-card" style="max-width:440px">
  <b>Stop sharing with ABC Finance?</b>
  <p style="font-size:14px;color:var(--bes-text-secondary);margin:6px 0 12px">They lose access immediately. Data they already hold isn't deleted — contact them for deletion. No retention questions, no guilt trips.</p>
  <div class="demo-row">
    <button class="bes-btn bes-btn--destructive-solid bes-btn--sm">Stop sharing</button>
    <button class="bes-btn bes-btn--secondary bes-btn--sm">Keep sharing</button>
  </div>
</div>
"""),
("Connected institution — freshness always labeled", """
<div class="bes-card" style="max-width:440px;display:flex;justify-content:space-between;gap:12px;align-items:center">
  <div>
    <b>Emirates NBD</b> · 2 accounts linked<br>
    <span style="font-size:13px;color:var(--bes-text-secondary)">Updated today 14:32</span>
  </div>
  <span class="bes-badge bes-badge--warning">Reconnect needed</span>
</div>
<p style="font-size:13px;color:var(--bes-text-secondary);margin:10px 0 0">External balances render visually distinct from actionable home balances — stale numbers never read as spendable.</p>
"""),
("Marketing preferences — service messages can't be silenced", """
<div class="demo-stack" style="max-width:420px">
  <label class="bes-switch"><input type="checkbox"><span class="track" aria-hidden="true"></span><span>Offers &amp; product news <span class="state">Off</span></span></label>
  <label class="bes-switch"><input type="checkbox" checked><span class="track" aria-hidden="true"></span><span>Monthly insights <span class="state">On</span></span></label>
  <div class="bes-alert bes-alert--info"><div>You'll always receive security and transaction messages — they keep your account safe and can't be turned off.</div></div>
</div>
"""),
]

SECTIONS["data-viz"] = [
("Bar chart & budget progress", """
<div class="demo-stack" style="max-width:520px">
  <div class="bes-chart" data-bes-chart='{"type":"bar","data":[{"label":"Apr","value":18500},{"label":"May","value":18500},{"label":"Jun","value":21300},{"label":"Jul","value":18500},{"label":"Aug","value":18500}],"opts":{"label":"Income by month in dirhams","colLabel":"Month","colValue":"AED"}}'></div>
  <div class="bes-limit">
    <div style="font-size:13.5px;font-weight:600;margin-bottom:6px">Dining budget — August</div>
    <div class="bes-progress bes-progress--warn"><div class="fill" style="inline-size:84%"></div></div>
    <div class="figures"><span class="used"><bdi class="bes-amount">AED 1,240.00</bdi> spent</span><span><bdi class="bes-amount">AED 240.00</bdi> left</span></div>
  </div>
</div>
"""),
]
