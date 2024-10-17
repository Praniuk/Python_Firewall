# Python_Firewall
This is a simple firewall script in python, with DDos prevention, and logging function. It works by incorporating the pyDivert library, which binds to WinDivert, allowing user-mode applications to capture and modify network traffic. To test this script, I used a socket connection, through which i was sending packets from client device to the server device, that was also running the firewall itself.

To truly see how this script works, I first had to disable both the default Windows firewall, and the routers default DDos protection in the router admin panel. If these were on, they would block the flood packets as DDos attempt before my script had a chance to do it.

![Zrzut ekranu 2024-10-15 183541](https://github.com/user-attachments/assets/b48eda86-0e3b-4bfc-a388-94fcac3a8d4b)

I've also had to whitelist my router's LAN and DHCP module's adresses, so the packets they send do not get interpreted as DDos attempts.

Next, i set up both the server socket, and the firewall script on one of my devices:

![Zrzut ekranu 2024-10-15 181922](https://github.com/user-attachments/assets/4e06a99e-8424-4210-8995-b07df842fe25)

![image](https://github.com/user-attachments/assets/bc0e23b0-4003-4704-9c03-4f6e57559566)

Then i started sending packets from a client socket to the server socket, and since my other device's IP was not blacklisted, they were going through:

![462559614_868397345272116_4888062491183108245_n](https://github.com/user-attachments/assets/76387f86-1a73-4a55-8ae6-63798bae48fd)

![Zrzut ekranu 2024-10-15 181954](https://github.com/user-attachments/assets/2efbfec3-5f79-44a4-80ef-0bb56b227408)

But once i've put client's IP in the blacklist table, the firewall script started capturing and dropping these packets:

![Zrzut ekranu 2024-10-15 181539](https://github.com/user-attachments/assets/dbc4197b-ea93-467c-a2b4-13328c43de7a)

Now to test DDos detection, I've removed the IP from blacklist, but instead of one packet, sent a flood of packets at once. I've had to modify the flood script to disable the Nagle’s Algorithm in my TCP client socket. Without it, the client would be pooling multiple little packets together, and would send them as 1 or 2 big packets. This wouldn't allow us to thest our DDos detection, since right now it's based purely on packet rate, and not their size.
With this change, the firewall script was reacting to the flood packets as intedned:

![Zrzut ekranu 2024-10-15 181706](https://github.com/user-attachments/assets/fe374b88-f06f-404b-9c32-92c5e972781a)

It blocked the IP temporarily, and after set time unblocked it again:

![Zrzut ekranu 2024-10-15 181754](https://github.com/user-attachments/assets/2aeb8b77-a95a-48d5-b4d0-c37462099171)

Finally, everything gets logged into a log file:

![Zrzut ekranu 2024-10-15 182025](https://github.com/user-attachments/assets/37131ca4-2119-4d39-be52-6d3864ee0d84)




