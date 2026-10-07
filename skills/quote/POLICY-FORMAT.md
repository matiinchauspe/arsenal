# POLICY.md Format

`POLICY.md` lives at the quote home root and holds the user's pricing policy: the same for every client, written by the user. Every value used to price an engagement comes from here.

## Template

```md
# Pricing policy

Updated: {YYYY-MM-DD}

## Rate

- Hourly rate: {amount} {quote currency}
- Charged in: {currency}, converted at {which rate, from where, on which day}

## Pricing rule

- {How a phase price comes from its hours, and how it is rounded}

## Payment terms

- {When each part is paid}

## Warranty

- {What gets fixed free, and on what condition}

## Retainer

- {What the monthly retainer covers, and how hours beyond it are billed}

## Lever

- {What gives when the price is too heavy for the client}

## Capacity

- Hours per week for one client's work: {hours}

## Identities

### {Identity name}
- Contact: {email, phone, site}
- Logo: {absolute path to an image file, or "none"}
- Accent color: {hex}
```

## The interview

Run it when `POLICY.md` is missing. Ask one section at a time, in template order, offering the suggestion below for the user to confirm or change. Write down only what the user confirms.

| Section | Suggestion |
| --- | --- |
| Rate | US$ 25 per hour |
| Charged in | Pesos (ARS) at the MEP dollar rate of the payment day |
| Pricing rule | Hours at the midpoint of the range, priced and rounded up to the next 50 in the quote currency |
| Payment terms | 50% when each phase starts, 50% when it is delivered |
| Warranty | Defects in work the user delivered earlier are fixed free |
| Retainer | Infrastructure at cost plus 2 hours of support a month; hours beyond that at the hourly rate |
| Lever | Cut scope, never the rate |
| Capacity | No suggestion: ask |
| Identities | Leave empty; the first one is added at Checkpoint 2 |

Done when every section except Identities holds a value the user confirmed, and `POLICY.md` is written with today's date.

