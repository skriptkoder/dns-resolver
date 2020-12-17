""""
A program that search and store store domain name  dns
Domain Name, A Records, MX Records, MX, CNAME, TXT
"""

import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import dns.resolver
import whois
import socket
from tkinter import filedialog


def add_spacer():
    displayResult.insert(END, '----------------------------------------\n')


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


def get_whois(p_domain_name):
    print('Retrieve WHOIS')
    whois_info = whois.whois(p_domain_name)
    displayResult.insert(END, 'Registrar: ')
    displayResult.insert(END, whois_info.registrar)
    displayResult.insert(END, '\n')
    displayResult.insert(END, 'Expiration Date: ')
    displayResult.insert(END, whois_info.expiration_date)
    displayResult.insert(END, '\n')
    add_spacer()


def get_hostname(p_domain_name):
    try:
        a_record = dns.resolver.resolve(p_domain_name, 'A')
    except dns.resolver.NoAnswer:
        print('No A record')

    if not a_record == '':
        # retrieve hostname by ip
        for a_data in a_record:
            str_a_record = str(a_data)
            hostname = socket.gethostbyaddr(str_a_record)
            displayResult.insert(END, 'Hostname: ')
            displayResult.insert(END, hostname[0])
            displayResult.insert(END, '\n')
    else:
        displayResult.insert(END, 'No A record for the Hostname: ')
        displayResult.insert(END, '\n')
    add_spacer()


def loop_record(p_domain_name, p_record_type):
    _record = ''
    try:
        _record = dns.resolver.resolve(p_domain_name, p_record_type)
    except dns.resolver.NoAnswer:
        print('No', p_record_type, 'record')

    if _record:
        for data_record in _record:
            displayResult.insert(END, p_record_type)
            displayResult.insert(END, ': ')
            displayResult.insert(END, data_record)
            displayResult.insert(END, '\n')
    else:
        displayResult.insert(END, 'No', p_record_type, 'record')
        displayResult.insert(END, '\n')
    add_spacer()


def search_command():

    # clear results field
    displayResult.delete(1.0, END)

    domain_name = domainName_text.get()
    if not domain_name:
        displayResult.insert(END, 'Please enter a domain name')
        # displayResult.insert(END, '\n')
    elif not is_registered(domain_name):
        displayResult.insert(END, 'This domain is not registered')
    else:
        print('Domain Name: ', domain_name)
        # print('WHOIS: ', rdo_selected.get())
        if rdo_selected.get() == 1:
            get_whois(domain_name)
        else:
            print('Do not Query WHOIS')

        if rdo_selected_host.get() == 1:
            get_hostname(domain_name)
        else:
            print('Do not Query hostname')

        # print('Query Type', cb_queryType.get())
        record_type = cb_queryType.get()
        if not record_type == 'Any':
            print('Query Specific type', record_type)
            loop_record(domain_name, record_type)
        else:
            print('Query all record type')
            # displayResult.insert(END, 'Any')
            all_record_type = ['NS', 'A', 'CNAME', 'MX', 'TXT']
            for record_type in  all_record_type:
                loop_record(domain_name, record_type)


def reset_command():
    displayResult.delete(1.0, END)
    domainName_entry.delete(0, 'end')
    cb_queryType.current(0)
    rdo_yes.select()


def close_command():
    window.destroy()


def print_command():
    f = filedialog.asksaveasfile(mode='w', initialfile='DNS-' + domainName_text.get() + '.txt',
                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")), defaultextension=".txt")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(displayResult.get(1.0, END))  # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close()  # `()` was missing.


window = tk.Tk()
window.wm_title("DNS Resolver Tool")

frame_domain_name = tk.Frame()
frame_domain_name.pack(pady=5)

frame_ctrl_top = tk.Frame(relief=tk.RAISED, pady=5)
frame_ctrl_top.pack()

frame_display = tk.Frame()
frame_display.pack()

frame_ctrl_bottom = tk.Frame()
frame_ctrl_bottom.pack(pady=10)

# window.geometry("880x500")
window.wm_title("DNS Resolver Tool")

# Labels
lbl_domain_name = tk.Label(master=frame_domain_name, text="Domain Name ", width=13)
lbl_domain_name.pack(side=tk.LEFT)

# Domain name entry field
domainName_text = StringVar()
domainName_entry = tk.Entry(master=frame_domain_name, width=76, textvariable=domainName_text)
domainName_entry.pack(side=tk.LEFT)
domainName_entry.focus()

lbl_whois = tk.Label(master=frame_ctrl_top, text="WHOIS: ")
lbl_whois.pack(side=tk.LEFT)

rdo_selected = IntVar()
rdo_yes = tk.Radiobutton(master=frame_ctrl_top, text='yes', value=1, variable=rdo_selected)
rdo_yes.select()
rdo_yes.pack(side=tk.LEFT)
rdo_no = tk.Radiobutton(master=frame_ctrl_top, text='no', value=2, variable=rdo_selected)
rdo_no.pack(side=tk.LEFT)

lbl_hostname = tk.Label(master=frame_ctrl_top, text="Hostname: ")
lbl_hostname.pack(side=tk.LEFT)
rdo_selected_host = IntVar()
rdo_host_yes = tk.Radiobutton(master=frame_ctrl_top, text='yes', value=1, variable=rdo_selected_host)
rdo_host_yes.select()
rdo_host_yes.pack(side=tk.LEFT)
rdo_host_no = tk.Radiobutton(master=frame_ctrl_top, text='no', value=2, variable=rdo_selected_host)
rdo_host_no.pack(side=tk.LEFT)


lbl_query = tk.Label(master=frame_ctrl_top, text="Query Type:", width=13)
lbl_query.pack(side=tk.LEFT)
# combobox for Record Type
cb_queryType = Combobox(master=frame_ctrl_top, text='Query Type', width=10)
cb_queryType['values'] = ('Any', 'A', 'CNAME', 'MX', 'NS', 'TXT')
cb_queryType.current(0)
cb_queryType.pack(side=tk.LEFT, padx=2)

# Buttons
btn_search = Button(master=frame_ctrl_top, text="Search", width=6, command=search_command)
btn_search.pack(side=tk.LEFT, padx=2)
btn_reset = Button(master=frame_ctrl_top, text="Reset", width=6, command=reset_command)
btn_reset.pack(side=tk.LEFT, padx=2)
btn_close = Button(master=frame_ctrl_top, text="Close", width=6, command=close_command)
btn_close.pack(side=tk.LEFT, padx=2)

# Labels
lbl_result = tk.Label(master=frame_display, text="Result ", width=13)
lbl_result.pack(side=tk.LEFT)

displayResult = tk.scrolledtext.ScrolledText(master=frame_display, height=15, width=60)
displayResult.pack(side=tk.LEFT)

btn_print_to_file = Button(master=frame_ctrl_bottom, text="Print Result to File", width=15, command=print_command)
btn_print_to_file.pack(side=tk.RIGHT)


# Run program
window.mainloop()
