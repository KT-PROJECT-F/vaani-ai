# Business rules

To be finalized in week 1. Change only through a PR reviewed by the mentor.

## Supported cities

Hyderabad, Vijayawada, Guntur, Visakhapatnam, Tirupati

## Supported services

plumber, electrician, water_tanker, ac_repair, carpenter, house_cleaning, pest_control, appliance_repair, ro_service, painter

## Time windows (all times IST)

| Word | Window |
|---|---|
| morning | 08:00 to 12:00 |
| afternoon | 12:00 to 16:00 |
| evening | 16:00 to 20:00 |
| urgent / now / jaldi / ventane | within 2 hours |

## Urgency levels

| Level | Meaning |
|---|---|
| emergency | Safety risk (gas, sparks, shock, flooding). Show safety steps first. |
| today | User wants it today |
| flexible | Any time in the next few days |

## Slots

- Slot length: 2 hours
- Bookings allowed: 08:00 to 20:00, today plus 7 days

## Booking states

```
pending -> confirmed -> completed
pending -> cancelled
confirmed -> rescheduled -> confirmed
confirmed -> cancelled
any -> failed (system error)
```

## Cancel and reschedule

- Free cancel or reschedule up to 1 hour before the slot.

## Provider side

There is no provider app. The matched provider accepts every booking automatically.

## Clarifying questions

- Ask one question at a time.
- After 3 unanswered or unclear answers, create a manual ticket for the admin.
