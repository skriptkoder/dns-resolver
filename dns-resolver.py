""""
A program that search and store store domain name  dns
Domain Name, A Records, MX Records, MX, CNAME, TXT
"""

from tkinter import *
from tkinter import scrolledtext
import dns.resolver
import whois
import socket


def is_registered(domain_name):
    """
    A function that returns a boolean indicating
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


def loop_record(p_domain_name, p_record_type, p_msg,  p_error_msg):
    _record = ''
    try:
        _record = dns.resolver.resolve(p_domain_name, p_record_type)
    except dns.resolver.NoAnswer:
        print(p_error_msg)
    if _record:
        for data_record in _record:
            displayDNS.insert(END, p_msg)
            displayDNS.insert(END, data_record)
            displayDNS.insert(END, '\n')
        displayDNS.insert(END, '----------------------------------------\n')
    else:
        displayDNS.insert(END, p_error_msg)
        displayDNS.insert(END, '\n')
    displayDNS.insert(END, '----------------------------------------\n')


def search_all_dns():

    # clear all fields
    displayRegistrar.delete(1.0, END)
    displayHost.delete(1.0, END)
    displayDNS.delete(1.0, END)
    # todo: remove http https : ;; and trailing slash
    # todo: is domain lock

    displayRegistrar.configure(state='normal')
    displayHost.configure(state='normal')
    displayDNS.configure(state='normal')

    domain_name = domainName_text.get()
    if not domain_name:
        displayRegistrar.insert(END, 'Please enter a domain name')
        # displayRegistrar.insert(END, '\n')
    elif not is_registered(domain_name):
        displayRegistrar.insert(END, 'This domain is not registered')

    else:
        whois_info = whois.whois(domain_name)
        displayRegistrar.insert(END, 'Registrar: ')
        displayRegistrar.insert(END, whois_info.registrar)
        displayRegistrar.insert(END, '\n')
        displayRegistrar.insert(END, 'Expiration Date: ')
        displayRegistrar.insert(END, whois_info.expiration_date)

        # get the a record
        try:
            a_record = dns.resolver.resolve(domainName_text.get(), 'A')
        except dns.resolver.NoAnswer:
            print('No A record')
        # prepend www to the domain name
        try:
            www_domain_name = 'www.' + domain_name
        except dns.resolver.NoAnswer:
            print('No WWW record')

        # retrieve hostname by ip
        for a_data in a_record:
            str_a_record = str(a_data)
            hostname = socket.gethostbyaddr(str_a_record)
            displayHost.insert(END, 'Hostname: ')
            displayHost.insert(END, hostname[0])
            displayHost.insert(END, '\n')
        displayDNS.insert(END, '----------------------------------------\n')

        # execute DNS query for most used type
        loop_record(domain_name, 'NS', 'NS: ', 'No NS record')
        loop_record(domain_name, 'A', 'A: ', 'No A record')
        loop_record(domain_name, 'MX', 'MX: ', 'No MX record')
        loop_record(domain_name, 'TXT', 'TXT: ', 'No TXT record')
        loop_record(domain_name, 'CNAME', 'CNAME: ', 'No CNAME record')
        loop_record(www_domain_name, 'CNAME', 'CNAME for www: ', 'No CNAME record for www')


# Empty all fields
def reset_command():
    displayRegistrar.delete(1.0, END)
    displayHost.delete(1.0, END)
    displayDNS.delete(1.0, END)
    domainName_entry.delete(0, 'end')


# Event to raise when hit Enter
def callback(event):
    search_all_dns()


# Close button event for the main window
def close_command():
    window.destroy()


# Window and event settings
window = Tk()
window.geometry("880x500")
window.wm_title("DNS Resolver Tool")
window.bind('<Return>', callback)

# Labels
l1 = Label(window, text="Domain Name ")
l1.grid(row=0, column=0)
l2 = Label(window, text="Registrar ")
l2.grid(row=1, column=0)
l3 = Label(window, text="Hosting ")
l3.grid(row=2, column=0)
l4 = Label(window, text="DNS Records")
l4.grid(row=3, column=0)

# Domain name entry field
domainName_text = StringVar()
domainName_entry = Entry(window, width=75, textvariable=domainName_text, )
domainName_entry.grid(row=0, column=1, columnspan=2)
domainName_entry.focus()

# Registrar Display Section
displayRegistrar = Text(window, height=2, width=60)
displayRegistrar.grid(row=1, column=1, pady=10)

# Host Display Section
displayHost = Text(window, height=1, width=60)
displayHost.grid(row=2, column=1, pady=10)

# DNS Display Section
displayDNS = scrolledtext.ScrolledText(window, height=18, width=58)
displayDNS.grid(row=3, column=1)

# Buttons
b1 = Button(window, text="Reset", width=8, command=reset_command)
b1.grid(row=0, column=3, padx=10, pady=10)
b2 = Button(window, text="Close", width=8, command=close_command)
b2.grid(row=0, column=4, pady=10)

# Run program
window.mainloop()
