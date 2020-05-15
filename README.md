# Purpose

I've used Celery for many projects over the last 10 years or so and while it's always gotten the job done, there's a lot that could be better.

## Problems with Celery

1. Large, slow-moving, old codebase. Type hints aren't used in the codebase and aren't supported in user-defined tasks.
1. Broker integrations use low common denominator features which increases complexity significantly (delayed jobs).
1. Using a separate datastore means it's hard to atomically commit a change to your primary store _and_ schedule a job to be run (e.g., submit an order and send an email confirmation).
1. The Celery task API is large and hard to use. There are many features that I've never used and don't intend to use (e.g., http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#canvas-designing-work-flows).

# Goals

* Django model-backed queue
  - Postgres as first but MySQL should end up "just working"
* Small, simple background tasks.
* Scheduled tasks via a scheduling process.
  - Best effort locking to avoid two processes running at the same time or use the database to dedupe scheduled tasks.
* Store results (failure and success) for some period of time.
* Type hints

# Features

* Database-backed: yes, databases can do this now
* Type hints
  - These should just work
* Small: small amount of code, small set of features, small API
  - Crons need to be simple, hard to screw up, and part of the task definition.
  -
* Serialize with Pickle: yes, there's a lot of bad that can happen with Pickle but that's a human problem with human solutions
* Error at boot for misconfiguration
  - I want to specify the names of the queues in the configuration and I want an error to be raised if a tsak is created with a queue not in that list.


# Example

```python

```


# Links

https://blog.ganssle.io/articles/2018/03/pytz-fastest-footgun.html
