# pyfchat
School work assignment: Create a pyhton chat using both Server / Client TCP and peer-to-peer UDP

### Install

```
git clone --depth 1 https://github.com/azerupi/pyfchat.git
cd pyfchat
pip install -r requirements.txt
```

Make sure to use **Python 3**

### Run

To run the server: `python pyfchat.py server` (to quit, `ctrl-c`)

To run the client: `python pyfchat.py`

### Client mode

A couple of commands are available in client mode, they have to be prefixed with a `:` (e.g. type `:help` for help)

Multiple users can connect to you and send you messages, but you can only send to one user at a time. To connect to a user type `:connect <username>` all the following lines you type, that are not commands, will be send to that user.

