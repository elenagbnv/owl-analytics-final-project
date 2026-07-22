<!-- how your API downloader works
how you limited concurrent API requests
why the log file needed protection from simultaneous writes
what Dara did to the data and how you cleaned it
why pandas was used only on a small sample
why Zehra asked you to use Spark for the full analytics
what your final analytics showed -->

# How you limited concurrent API requests.
## my initial considerations:
My initial code was using sleep(60) as full 60 seconds waiting time.
I then subtracted the elapsed time of each request from 60 seconds to record the ‘actual’ time per request.
The problem with the initial implementation was that the result of subtraction was always positive and so it does not reflect on actual rate-limit.
Another way of doing it that I considered was to record (timestamp) and compare end of waiting time (either actual or 60 seconds wait) of current request to the ‘start time of the next request’: if ‘start time of the next request’ is equal to or less than the end of waiting time of current request we can print zero and 1 otherwise.

The solution I implemented in the end was to record time of when the entry to semaphore critical section/ serial section got acquired ‘acquire wait’.

---

# Why the log file needed protection from simultaneous writes.
The lock/ protection was needed to ensure that only one thread writes into the log file at a time.