# Example - Objection Handling

> Worked example - illustrative, not a live record. Method from [methodology.md](../methodology.md#6-handle-objections);
> the reasoning behind it is in [psychology.md](../psychology.md).

The loop: **acknowledge → understand → respond → confirm.** Objections are requests for information or
signals of an unresolved fear - never rejection, and never something to argue with.

---

### "It's too expensive."

Usually means *"I'm not convinced of the value."*

> **Acknowledge:** "That's fair - it's a real investment."
> **Understand:** "Compared to what, specifically? And what's the current cost of the problem?"
> **Respond:** Re-anchor on the cost of inaction they already told you - "You said postmortems take 4 hours
> per incident, and you have ~8 a month. That's ~$120k a year in engineering time. This is $9.6k."
> **Confirm:** "Does that change how the number looks?"

**Never:** discount reflexively. That teaches them the price was never real. Trade, don't cave.

---

### "We'll build it ourselves."

Usually means *"I don't see why this is hard."*

> **Acknowledge:** "You could - your team is strong."
> **Understand:** "What would you deprioritise to build and then maintain it?"
> **Respond:** Be honest about where building makes sense. Then name the ongoing cost: not the first
> version, but the evaluation, drift monitoring, and maintenance forever.
> **Confirm:** "Is that trade worth it against your reliability OKR?"

---

### "Now isn't the right time."

Usually means *"This isn't a priority"* or *"There's a blocker you haven't found."*

> **Acknowledge:** "Understood."
> **Understand:** "Is it timing, budget, or priority? What would have to be true for this to matter next quarter?"
> **Respond:** If it's genuinely not a priority, **qualify out honestly** and stay in touch. If there's a
> hidden blocker (a competing project, a missing approver), surface and address it.
> **Confirm:** "Should we revisit after your Q3 planning, or is this a no?"

**Note:** a clean "no" is more valuable than a slow "maybe." Chasing an unqualified deal costs a real one.

---

### "Can you commit to shipping feature X?"

> **Never promise unbuilt features.** Say what's true: "It's not committed. Here's the workaround today,
> and I'll log the need with [product](../../post-launch/feature-requests.md)." Overselling wins a deal and
> creates a churn - the [standards](../standards.md) are explicit about this.
