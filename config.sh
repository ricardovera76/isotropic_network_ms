# Installing necessary packages
sudo apt install libtcmalloc-minimal4
sudo dpkg -i ./packages/netifyd_4.4.5-1_amd64.deb
sudo dpkg -i ./packages/netify-plugin-stats_1.0.17-1_amd64.deb
sudo rm /etc/netifyd.conf
sudo touch /etc/netifyd.conf
sudo echo "[plugin_stats]
np-stats = /usr/lib/x86_64-linux-gnu/libnetify-plugin-stats.so.0.0.0

[netifyd]
enable_sink = no

[socket]
listen_path[0] = /var/run/netifyd/netifyd.sock

[protocols]
all=include" >> /etc/netifyd.conf
sudo touch /var/run/netifyd/netifyd.sock
sudo systemctl restart netifyd.service
sudo nc -U /var/run/netifyd/netifyd.sock