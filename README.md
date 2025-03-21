# **sswitch**  

*A simple command-line tool to update SSH host IP addresses in your `~/.ssh/config` file.*  
## **🚀 Features**  
✅ Quickly update the IP address of a host in your SSH config  
✅ Easy to install and use as a CLI tool (`sswitch`)  
✅ Supports a customizable SSH config location via `~/.sswitch_config`  

---

## **📌 Installation**  
### **Using `pip` (Recommended)**
```sh
pip install sswitch
```

### **From Source**
```sh
git clone https://github.com/yourusername/sswitch.git
cd sswitch
pip install --editable .
```

---

## **🛠 Usage**  
### **Basic Command**
```sh
sswitch update <HOSTNAME> <NEW_IP>
```
For example:  
```sh
sswitch update myserver 192.168.1.100
```
This will find `myserver` in `~/.ssh/config` and update its `HostName`.

You can also list the current hostnames and IPs as:
```sh
sswitch list
```
You can also add a new hostname as:
```sh
sswitch add new_hostname
```
By default the address of the new host is 1.1.1.1
Use sswitch uodate `new_hostname new_ip` to change it.

---

## **⚙ Custom SSH Config Path**  
By default, `sswitch` edits `~/.ssh/config`.  
To use a **custom SSH config file**, create `~/.sswitch_config`:
```
[settings]
ssh_config = /custom/path/to/ssh_config
```

---

## **📝 Example `.ssh/config` Before & After**  

### **Before**
```ini
Host myserver
    HostName 203.0.113.10
    User myuser
```

### **After Running `sswitch myserver 192.168.1.100`**
```ini
Host myserver
    HostName 192.168.1.100
    User myuser
```

---

## **🔧 Uninstall**
To remove `sswitch`, simply run:
```sh
pip uninstall sswitch
```

---

## **📜 License**  
This project is licensed under the **MIT License**.  
