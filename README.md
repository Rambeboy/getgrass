## GRAS NODE BOT

![grass](assets/img1.jpg)

## Create Accounts

- Create Account : [Grass](https://app.getgrass.io/register/?referralCode=_D-RVWUQOUA6vDI)
- Enter Email and Password
- Verifikasi Email dan Submit SOL Address
- Done

### SETUP & CONFIGURE BOT

```
sudo apt install python3 python3-pip
```

## Installation

1. Clone project repository
```
git clone https://github.com/Rambeboy/getgrass.git && cd getgrass
```

2. Install dependencies
```
pip install -r requirements.txt
```

### Edit `users.txt`

```
nano users.txt
```

**Change with your User ID**

Example:

```bash
i1234xxxxxxxxxxxxxx
```

### Edit `proxies.txt`

```
nano proxies.txt
```

**Change with your proxies**

Example:

```
http://username:password@hostname:port
socks5://username:password@hostname:port
```

### HOW TO GET YOUR USERID

login to [Grass](https://app.getgrass.io)

press f12 go to console, then type ```allow pasting```

then insert this code
```bash
localStorage.getItem('userId')
```


## Run Bot

```
python main.py
```

or

```
python3 main.py
```
