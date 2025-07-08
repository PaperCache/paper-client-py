# paper-client-py

The Python [PaperCache](https://papercache.io) client. The client supports all commands described in the wire protocol on the homepage.

## Example
```python
from paper_client.client import PaperClient

client = PaperClient("paper://127.0.0.1:3145")

client.set("hello", "world")
got = client.get("hello")
```
