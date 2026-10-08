# proposal.html Format

`proposal.html` is the one document the client sees. It is written for the person who decides and pays: their words, their problem, what they get, what it costs and when. Everything about how the price was reached stays in `quote.md`.

## Sections

1. **Summary.** Today in two or three sentences, what the work changes, the core modules as a short list, and the monthly running cost, next to the alternative's when it has a price.
2. **Before anything else (Phase 0).** Each fix as problem → risk to the client → fix, in plain words. Warranty items say they are fixed at no charge. Left out when there is nothing to fix first.
3. **What gets built.** Phase by phase, each module with its tag and legend (✅ you asked · 💡 we propose · ⏸ later), then the Later modules, then what is not recommended and why.
4. **Running costs.** The external costs, each with why that plan, and the alternative's price for comparison. Left out when the work has no running costs.
5. **Investment and timeline.** A fixed price and an estimated delivery time per phase, the total, the payment terms, and the monthly retainer with what it covers and when it starts. When `quote.md` has a break-even, the running-cost comparison goes here.
6. **Assumptions and questions.** Every open question from `estimate.md`, each with the assumption this proposal makes until the client answers.
7. **Sources.** Every external cost, exchange rate and fact about the alternative, with its link and consultation date.

Close with the signer's identity: name, contact and logo. Technical detail (schemas, libraries, architecture) appears only where the client needs it to decide, explained in their terms.

## What crosses from quote.md

The proposal carries each phase's **price** and **delivery time**, the payment terms, the retainer's amount and what it covers, the exchange rule the client pays by, and the break-even comparison. The rate, the pricing rule, the exceptions, the warranty's own cost, the lever, the selling points and the history stay internal.

**Hours** appear only when the engagement's `show_hours` is `true`: then each phase shows its priced hours and the retainer its support hours. Otherwise the retainer's support is described by what it covers, and work beyond it as quoted before it starts, since any hour count beside a price reveals the rate.

## HTML rules

- **One self-contained file.** Paste the contents of [proposal.css](./proposal.css) into a `<style>` element, then the identity on top: set `--accent` to its accent color, and embed its logo as a base64 `data:` URI (leave the logo out when the path is "none" or unreadable). Draw every diagram as inline SVG. The file loads nothing from the network, so it opens offline and travels by WhatsApp or email.
- **Prints to A4.** Use the stylesheet's classes; a section or diagram never splits across pages (`.keep`).
- **Diagrams only where they help the client decide:**
  - a timeline of the phases, sized by delivery time, when there is more than one phase;
  - the running cost a month once the work is delivered against the alternative's, as horizontal bars with each value beside its bar, when `quote.md` has a break-even; the break-even month goes in the caption, since a cumulative curve beside the timeline reads as a delivery date;
  - how the delivered work will run (a flow, its states, who does what), only when the client needs it to understand what they are buying. Draw it with the `diagram` skill, stamped Proposed, and inline the SVG it renders.

## Checks

- `rg -n 'src="http|href="http[^"]*\.css|@import|<script' proposal.html` finds nothing; links to sources are the only remote URLs.
- The rate does not appear anywhere in the file, and hours appear only when `show_hours` is `true`.
- Every open question in `estimate.md` appears in Assumptions and questions.
- Every external cost, exchange rate and alternative price in the file appears in Sources with its date.
- The signer's name and contact appear in the closing block.
