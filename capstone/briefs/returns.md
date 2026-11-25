# Returns: what is driving our returns?

One of the three case-study briefs. Read the [case study README](../README.md) first.

## The request

An online shop sells clothes, shoes, bags, homeware and beauty products across the United Kingdom, through its website, its app and a marketplace. The head of e-commerce sends you this message on Monday morning:

> "Returns are eating our margin. The finance team says refunds went up this autumn and nobody can tell me why. Is it the product, the delivery, the customers, the discounts? I have a meeting with the buying team and the logistics manager in two weeks. Tell me what is going on and what I should ask them to change."

- **Who asked:** the head of e-commerce.
- **The decision:** what to ask the buying team (products and suppliers) and the logistics manager (delivery) to change, in a meeting in two weeks.
- **What they did not say:** what "returns" means (orders, lines, units or money?), which period, or compared with what. Pinning that down is your first job (task 4, `## Question`).

## The data

The shop's data is **made by a kit script**, so it is safe to publish and every student gets a different shop.
The customers, products and suppliers are invented. The data is shaped like a real shop's export, problems included.

Run this in your `casestudy/` folder in Git Bash (one second, no internet):

```bash
uv run ~/da-ess-kit/capstone/data/make_returns.py --student <your-github-username>
```

It writes four files into `data/` and prints their row counts (about 260 products, 19,000 orders, 32,000 order lines and 5,000 returns, different for each student):

| File | One row is | Columns |
|---|---|---|
| `products.csv` | a product | `product_id`, `product_name`, `category`, `supplier`, `list_price` |
| `orders.csv` | an order | `order_id`, `order_date`, `customer_id`, `channel` (web, app, marketplace), `region`, `promo_code` (empty when none), `delivery_days` (days from order to delivery) |
| `order_lines.csv` | one product on an order | `order_id`, `line_no`, `product_id`, `quantity`, `unit_price` (after any discount) |
| `returns.csv` | a return of one order line | `return_id`, `order_id`, `line_no`, `return_date`, `quantity`, `reason`, `refund` |

- **Period:** orders from 1 January 2025 to 30 June 2026; returns up to 30 days later.
- **Money** is in pounds sterling (GBP).
- A return joins its order line on `order_id` and `line_no`.
- **The same `--student` always gives the same files**, on any computer. Your mentor can make your files again to check your numbers.

### Licence and credit

The script is part of the course kit, under the MIT licence. The data it makes is invented and belongs to no one: you may publish it, your charts and your findings freely.
Write this line in your README and report:

```text
Data: invented shop data made with the Anaxion AI course kit (capstone/data/make_returns.py, --student <your-github-username>).
```

Say clearly in your report that the shop is invented. A reader must never think it is a real company.

## What to watch for

This export was made by a busy team, as real exports are. Vet it before you trust it (task 5), and write every problem you find, with its count, in `DATA.md`. Look at least at:

- rows that break a rule that must hold (dates in the wrong order, a refund bigger than the money paid, more units returned than sold);
- the same return recorded twice;
- reasons that are empty or written in different ways;
- whether every month looks complete.

## What a strong answer shows

- **A rate, not a count.** More orders bring more returns. The main number is a return rate with a clear numerator and denominator (lines, units or money), stated in `## Main number`, and the reader can see the counts behind each rate.
- **A fair comparison.** When the overall rate moves, the answer separates a change in *what* was sold (the mix of categories) from a change in *how often* things came back within each category.
- **Drivers the meeting can act on**, each with its size: which categories, products or suppliers, which delivery times, which channels or promotions, and how much money each one costs in refunds. Two or three findings, ranked, beat ten.
- **The reasons used with care.** A reason code is what a customer ticked. It supports a finding; it does not prove it alone.
- **Problems in the data, found and handled.** Every rule you used to drop or fix rows is written down, and the reconciliation shows raw rows = clean rows + dropped rows.
- **Three tests of how it could be wrong** (task 8), at least one of them on the data itself.
- **One page of dashboard** whose title states the finding, and a recommendation for each person in the meeting: one thing for the buying team, one for the logistics manager.
